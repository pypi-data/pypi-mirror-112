/* global MyAMS */
/**
 * MyAMS tree management
 */

const $ = MyAMS.$;


export const tree = {

};


/**
 * Global module initialization
 */
if (window.MyAMS) {
	if (MyAMS.env.bundle) {
		MyAMS.config.modules.push('tree');
	} else {
		MyAMS.tree = tree;
		console.debug("MyAMS: tree module loaded...");
	}
}
