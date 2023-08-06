(function (global, factory) {
  if (typeof define === "function" && define.amd) {
    define(["exports"], factory);
  } else if (typeof exports !== "undefined") {
    factory(exports);
  } else {
    var mod = {
      exports: {}
    };
    factory(mod.exports);
    global.modNotifications = mod.exports;
  }
})(typeof globalThis !== "undefined" ? globalThis : typeof self !== "undefined" ? self : this, function (_exports) {
  "use strict";

  Object.defineProperty(_exports, "__esModule", {
    value: true
  });
  _exports.notifications = void 0;

  function _classCallCheck(instance, Constructor) { if (!(instance instanceof Constructor)) { throw new TypeError("Cannot call a class as a function"); } }

  function _defineProperties(target, props) { for (var i = 0; i < props.length; i++) { var descriptor = props[i]; descriptor.enumerable = descriptor.enumerable || false; descriptor.configurable = true; if ("value" in descriptor) descriptor.writable = true; Object.defineProperty(target, descriptor.key, descriptor); } }

  function _createClass(Constructor, protoProps, staticProps) { if (protoProps) _defineProperties(Constructor.prototype, protoProps); if (staticProps) _defineProperties(Constructor, staticProps); return Constructor; }

  /* global MyAMS */

  /**
   * MyAMS notifications handlers
   */
  var $ = MyAMS.$;

  if (!$.templates) {
    var jsrender = require('jsrender');

    $.templates = jsrender.templates;
  }
  /**
   * Notifications list template string
   */


  var ITEM_TEMPLATE_STRING = "\n\t<li class=\"p-1\">\n\t\t<a class=\"d-flex flex-row\"{{if url}} href=\"{{:url}}\"{{/if}}>\n\t\t\t{{if source.avatar}}\n\t\t\t<img class=\"avatar mx-1 mt-1\" src=\"{{:source.avatar}}\" />\n\t\t\t{{else}}\n\t\t\t<i class=\"avatar fa fa-fw fa-2x fa-user mx-1 mt-1\"></i>\n\t\t\t{{/if}}\n\t\t\t<div class=\"flex-grow-1 ml-2\">\n\t\t\t\t<small class=\"timestamp float-right text-muted\">\n\t\t\t\t\t{{*: new Date(data.timestamp).toLocaleString()}}\n\t\t\t\t</small>\n\t\t\t\t<strong class=\"title d-block\">\n\t\t\t\t\t{{:source.title}}\n\t\t\t\t</strong>\n\t\t\t\t<p class=\"text-muted mb-2\">{{:message}}</p>\n\t\t\t</div>\n\t\t</a>\n\t</li>";
  var ITEM_TEMPLATE = $.templates({
    markup: ITEM_TEMPLATE_STRING,
    allowCode: true
  });
  var LIST_TEMPLATE_STRING = "\n\t<ul class=\"list-style-none flex-grow-1 overflow-auto m-0 p-0\">\n\t\t{{for notifications tmpl=~itemTemplate /}}\n\t</ul>\n\t{{if !~options.hideTimestamp}}\n\t<div class=\"timestamp border-top pt-1\">\n\t\t<span>{{*: MyAMS.i18n.LAST_UPDATE }}{{: ~timestamp.toLocaleString() }}</span>\n\t\t<i class=\"fa fa-fw fa-sync float-right\"\n\t\t   data-ams-click-handler=\"MyAMS.notifications.getNotifications\"\n\t\t   data-ams-click-handler-options='{\"localTimestamp\": \"{{: ~useLocalTime }}\"}'></i>\n\t</div>\n\t{{/if}}";
  var LIST_TEMPLATE = $.templates({
    markup: LIST_TEMPLATE_STRING,
    allowCode: true
  });

  var NotificationsList = /*#__PURE__*/function () {
    /**
     * List constructor
     *
     * @param values: notifications data (may be loaded from JSON)
     * @param options: list rendering options
     */
    function NotificationsList(values) {
      var options = arguments.length > 1 && arguments[1] !== undefined ? arguments[1] : {};

      _classCallCheck(this, NotificationsList);

      this.values = values;
      this.options = options;
    }
    /**
     * Render list into given parent
     *
     * @param parent: JQUery parent object into which the list must be rendered
     */


    _createClass(NotificationsList, [{
      key: "render",
      value: function render(parent) {
        $(parent).html(LIST_TEMPLATE.render(this.values, {
          itemTemplate: ITEM_TEMPLATE,
          timestamp: this.options.localTimestamp ? new Date() : new Date(this.values.timestamp),
          useLocalTime: this.options.localTimestamp ? 'true' : 'false',
          options: this.options
        }));
      }
    }]);

    return NotificationsList;
  }();

  var notifications = {
    /**
     * Load user notifications
     *
     * @param evt: source event
     * @param options: notifications options (which can also be extracted from event data)
     */
    getNotifications: function getNotifications(evt, options) {
      var data = $.extend({}, options, evt.data),
          target = $(evt.target),
          current = $(evt.currentTarget),
          remote = current.data('ams-notifications-source') || current.parents('[data-ams-notifications-source]').data('ams-notifications-source');
      return new Promise(function (resolve, reject) {
        MyAMS.require('ajax').then(function () {
          MyAMS.ajax.get(remote, current.data('ams-notifications-params') || '', current.data('ams-notifications-options') || {}).then(function (result) {
            var tab = $(target.data('ams-notifications-target') || target.parents('[data-ams-notifications-target]').data('ams-notifications-target') || current.attr('href'));
            new NotificationsList(result, data).render(tab);
            resolve();
          }, reject);
        }, reject);
      });
    }
  };
  /**
   * Global module initialization
   */

  _exports.notifications = notifications;

  if (MyAMS.env.bundle) {
    MyAMS.config.modules.push('notifications');
  } else {
    MyAMS.notifications = notifications;
    console.debug("MyAMS: notifications module loaded...");
  }
});
//# sourceMappingURL=mod-notifications-dev.js.map
