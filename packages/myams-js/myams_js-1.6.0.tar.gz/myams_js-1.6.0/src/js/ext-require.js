/* global MyAMS */
/**
 * MyAMS dynamic module loader
 */

const $ = MyAMS.$;


function getModule(module) {
	let moduleSrc;
	if (module.startsWith('http://') || module.startsWith('https://')) {
		moduleSrc = module;
	} else if (module.endsWith('.js')) {  // custom module with relative path
		moduleSrc = module;
	} else {  // standard MyAMS module
		moduleSrc = `${MyAMS.env.baseURL}mod-${module}${MyAMS.env.devext}.js`;
	}
	return MyAMS.core.getScript(moduleSrc, {async: true}, console.error);
}


/**
 * Dynamic loading of MyAMS modules
 *
 * @param modules: single module name, or array of modules names
 * @returns Promise
 */
export default function myams_require(...modules) {

	return new Promise((resolve, reject) => {

		const
			names = [],
			deferred = [],
			loaded = MyAMS.config.modules;

		for (const module of modules) {
			if (typeof module === 'string') {
				if (loaded.indexOf(module) < 0) {
					names.push(module);
					deferred.push(getModule(module));
				}
			} else if ($.isArray(module)) {  // strings array
				for (const name of module) {
					if (loaded.indexOf(name) < 0) {
						names.push(name);
						deferred.push(getModule(name));
					}
				}
			} else {  // object
				for (const [name, src] of Object.entries(module)) {
					if (loaded.indexOf(name) < 0) {
						names.push(name);
						deferred.push(getModule(src));
					}
				}
			}
		}

		$.when.apply($, deferred)
			.then(() => {
				for (const moduleName of names) {
					if (loaded.indexOf(moduleName) < 0) {
						loaded.push(moduleName);
						MyAMS.core.executeFunctionByName(`MyAMS.${moduleName}.init`);
					}
				}
				resolve();
			}, () => {
				reject(`Can't load requested modules (${names})!`);
			});
	});
}
