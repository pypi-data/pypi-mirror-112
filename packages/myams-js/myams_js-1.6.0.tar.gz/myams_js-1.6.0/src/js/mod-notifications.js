/* global MyAMS */
/**
 * MyAMS notifications handlers
 */

const $ = MyAMS.$;

if (!$.templates) {
	const jsrender = require('jsrender');
	$.templates = jsrender.templates;
}


/**
 * Notifications list template string
 */

const ITEM_TEMPLATE_STRING = `
	<li class="p-1">
		<a class="d-flex flex-row"{{if url}} href="{{:url}}"{{/if}}>
			{{if source.avatar}}
			<img class="avatar mx-1 mt-1" src="{{:source.avatar}}" />
			{{else}}
			<i class="avatar fa fa-fw fa-2x fa-user mx-1 mt-1"></i>
			{{/if}}
			<div class="flex-grow-1 ml-2">
				<small class="timestamp float-right text-muted">
					{{*: new Date(data.timestamp).toLocaleString()}}
				</small>
				<strong class="title d-block">
					{{:source.title}}
				</strong>
				<p class="text-muted mb-2">{{:message}}</p>
			</div>
		</a>
	</li>`;

const ITEM_TEMPLATE = $.templates({
	markup: ITEM_TEMPLATE_STRING,
	allowCode: true
});


const LIST_TEMPLATE_STRING = `
	<ul class="list-style-none flex-grow-1 overflow-auto m-0 p-0">
		{{for notifications tmpl=~itemTemplate /}}
	</ul>
	{{if !~options.hideTimestamp}}
	<div class="timestamp border-top pt-1">
		<span>{{*: MyAMS.i18n.LAST_UPDATE }}{{: ~timestamp.toLocaleString() }}</span>
		<i class="fa fa-fw fa-sync float-right"
		   data-ams-click-handler="MyAMS.notifications.getNotifications"
		   data-ams-click-handler-options='{"localTimestamp": "{{: ~useLocalTime }}"}'></i>
	</div>
	{{/if}}`;

const LIST_TEMPLATE = $.templates({
	markup: LIST_TEMPLATE_STRING,
	allowCode: true
});


class NotificationsList {

	/**
	 * List constructor
	 *
	 * @param values: notifications data (may be loaded from JSON)
	 * @param options: list rendering options
	 */
	constructor(values, options={}) {
		this.values = values;
		this.options = options;
	}

	/**
	 * Render list into given parent
	 *
	 * @param parent: JQUery parent object into which the list must be rendered
	 */
	render(parent) {
		$(parent).html(LIST_TEMPLATE.render(this.values, {
			itemTemplate: ITEM_TEMPLATE,
			timestamp: this.options.localTimestamp ?
				new Date() : new Date(this.values.timestamp),
			useLocalTime: this.options.localTimestamp ? 'true' : 'false',
			options: this.options
		}));
	}
}


export const notifications = {

	/**
	 * Load user notifications
	 *
	 * @param evt: source event
	 * @param options: notifications options (which can also be extracted from event data)
	 */
	getNotifications: (evt, options) => {
		const
			data = $.extend({}, options, evt.data),
			target = $(evt.target),
			current = $(evt.currentTarget),
			remote = current.data('ams-notifications-source') ||
				current.parents('[data-ams-notifications-source]').data('ams-notifications-source');
		return new Promise((resolve, reject) => {
			MyAMS.require('ajax').then(() => {
				MyAMS.ajax.get(remote, current.data('ams-notifications-params') || '',
					current.data('ams-notifications-options') || {}).then((result) => {
					const
						tab = $(target.data('ams-notifications-target') ||
						target.parents('[data-ams-notifications-target]').data('ams-notifications-target') ||
						current.attr('href'));
					new NotificationsList(result, data).render(tab);
					resolve();
				}, reject);
			}, reject);
		});
	}
}


/**
 * Global module initialization
 */
if (MyAMS.env.bundle) {
	MyAMS.config.modules.push('notifications');
} else {
	MyAMS.notifications = notifications;
	console.debug("MyAMS: notifications module loaded...");
}
