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
    global.modAlert = mod.exports;
  }
})(typeof globalThis !== "undefined" ? globalThis : typeof self !== "undefined" ? self : this, function (_exports) {
  "use strict";

  Object.defineProperty(_exports, "__esModule", {
    value: true
  });
  _exports.alert = void 0;

  /* global MyAMS */

  /**
   * MyAMS alerts management
   */
  var $ = MyAMS.$;

  if (!$.templates) {
    var jsrender = require('jsrender');

    $.templates = jsrender.templates;
  }
  /**
   * Alert template
   */


  var ALERT_TEMPLATE_STRING = "\n\t<div class=\"alert alert-{{:status}}\" role=\"alert\">\n\t\t<button type=\"button\" class=\"close\" data-dismiss=\"alert\" \n\t\t\t\taria-label=\"{{*: MyAMS.i18n.BTN_CLODE }}\">\n\t\t\t<i class=\"fa fa-times\" aria-hidden=\"true\"></i>\t\n\t\t</button>\n\t\t{{if header}}\n\t\t<h5 class=\"alert-heading\">{{:header}}</h5>\n\t\t{{/if}}\n\t\t{{* if (typeof message === 'string') { }}\n\t\t<ul>\n\t\t\t<li>{{:message}}</li>\n\t\t</ul>\n\t\t{{* } else { }}\n\t\t<ul>\n\t\t{{for message}}\n\t\t\t<li>{{:}}</li>\n\t\t{{/for}}\n\t\t</ul>\n\t\t{{* } }}\n\t</div>";
  var ALERT_TEMPLATE = $.templates({
    markup: ALERT_TEMPLATE_STRING,
    allowCode: true
  });
  /**
   * Standard message template
   */

  var MESSAGE_TEMPLATE_STRING = "\n\t<div role=\"alert\" class=\"toast toast-{{:status}} fade hide\"\n\t\t data-autohide=\"{{*: Boolean(data.timeout !== 0).toString() }}\"\n\t\t data-delay=\"{{: timeout || 5000}}\">\n\t\t<div class=\"toast-header\">\n\t\t{{if icon}}\n\t\t\t<i class=\"fa {{:icon}} mr-2\"></i>\n\t\t{{/if}}\n\t\t\t<strong class=\"mr-auto\">{{:title}}</strong>\n\t\t{{if !hideTimestamp}}\n\t\t\t<small>{{*: new Date().toLocaleTimeString() }}</small>\n\t\t{{/if}}\n\t\t\t<button type=\"button\" class=\"ml-2 mb-1 close\" data-dismiss=\"toast\">\n\t\t\t\t<i class=\"fa fa-times text-white\"></i>\n\t\t\t</button>\n\t\t</div>\n\t\t<div class=\"toast-body\">\n\t\t\t<div>\n\t\t\t{{if content}}\n\t\t\t\t{{:content}}\n\t\t\t{{else}}\n\t\t\t\t<p>{{:message}}</p>\n\t\t\t{{/if}}\n\t\t\t</div>\n\t\t</div>\n\t</div>";
  var MESSAGE_TEMPLATE = $.templates({
    markup: MESSAGE_TEMPLATE_STRING,
    allowCode: true
  });
  /**
   * Small box message template
   */

  var SMALLBOX_TEMPLATE_STRING = "\n\t<div role=\"alert\" class=\"toast toast-{{:status}} fade hide\"\n\t\t data-autohide=\"true\"\n\t\t data-delay=\"{{: timeout || 5000}}\">\n\t\t<div class=\"toast-body\">\n\t\t\t<div>\n\t\t\t{{if content}}\n\t\t\t\t{{:content}}\n\t\t\t{{else}}\n\t\t\t\t<span>\n\t\t\t\t\t{{if icon}}\n\t\t\t\t\t<i class=\"fa {{:icon}} mr-2\"></i>\n\t\t\t\t\t{{/if}}\n\t\t\t\t\t{{:message}}\n\t\t\t\t</span>\n\t\t\t{{/if}}\n\t\t\t</div>\n\t\t</div>\n\t</div>";
  var SMALLBOX_TEMPLATE = $.templates({
    markup: SMALLBOX_TEMPLATE_STRING,
    allowCode: true
  });
  /**
   * Big box message template
   */

  var BIGBOX_TEMPLATE_STRING = "\n\t<div class=\"modal fade\" data-backdrop=\"static\" role=\"dialog\">\n\t\t<div class=\"modal-dialog\">\n\t\t\t<div class=\"modal-content\">\n\t\t\t\t<div class=\"modal-header alert-{{:status}}\">\n\t\t\t\t\t<h5 class=\"modal-title\">\n\t\t\t\t\t{{if icon}}\n\t\t\t\t\t\t<i class=\"fa {{:icon}} mr-2\"></i>\n\t\t\t\t\t{{/if}}\n\t\t\t\t\t{{:title}}\n\t\t\t\t\t</h5>\n\t\t\t\t\t<button type=\"button\" class=\"close\" \n\t\t\t\t\t\t\tdata-dismiss=\"modal\" data-modal-dismiss-value=\"cancel\">\n\t\t\t\t\t\t<i class=\"fa fa-times\"></i>\n\t\t\t\t\t</button>\n\t\t\t\t</div>\n\t\t\t\t<div class=\"modal-body\">\n\t\t\t\t\t<p>{{:message}}</p>\n\t\t\t\t</div>\n\t\t\t\t<div class=\"modal-footer\">\n\t\t\t\t\t<button type=\"button\" class=\"btn btn-primary\" \n\t\t\t\t\t\t\tdata-dismiss=\"modal\" data-modal-dismiss-value=\"success\">\n\t\t\t\t\t\t{{*: data.successLabel || MyAMS.i18n.BTN_OK }}\n\t\t\t\t\t</button>\n\t\t\t\t\t<button type=\"button\" class=\"btn btn-secondary\" \n\t\t\t\t\t\t\tdata-dismiss=\"modal\" data-modal-dismiss-value=\"cancel\">\n\t\t\t\t\t\t{{*: data.cancelLabel || MyAMS.i18n.BTN_CANCEL }}\n\t\t\t\t\t</button>\n\t\t\t\t</div>\n\t\t\t</div>\n\t\t</div>\n\t</div>";
  var BIGBOX_TEMPLATE = $.templates({
    markup: BIGBOX_TEMPLATE_STRING,
    allowCode: true
  });
  /**
   * Main alert object
   */

  var alert = {
    /**
     * Display alert message into current document
     *
     * @param props:
     *  - parent: DOM element which should receive the alert
     *  - status: alert status ('info', 'success', 'warning', 'danger'...)
     *  - header: alert header
     *  - subtitle: message sub-title
     *  - message: main alert message
     */
    alert: function alert() {
      var props = arguments.length > 0 && arguments[0] !== undefined ? arguments[0] : {};
      var status = props.status || 'info';

      if (status === 'error') {
        status = 'danger';
      }

      props.status = status;
      $(".alert-".concat(status), props.parent).not('.persistent').remove();
      $(ALERT_TEMPLATE.render(props)).prependTo(props.parent);

      MyAMS.require('ajax').then(function () {
        MyAMS.ajax.check($.fn.scrollTo, "".concat(MyAMS.env.baseURL, "../ext/jquery-scrollto").concat(MyAMS.env.extext, ".js")).then(function () {
          $('#content').scrollTo(props.parent, {
            offset: -15
          });
        });
      });
    },

    /**
     * Display notification message on bottom right
     *
     * @param props: message properties:
     *  - status: message status: 'info', 'success', 'warning', 'danger'
     *  - title: message title
     *  - icon: message icon
     *  - content: full HTML content
     *  - message: simple string message
     *  - hideTimestamp: boolean value to specify if timestamp must be hidden
     *  - timeout: timeout in ms; default to 5000, set to 0 to disable auto-hide
     */
    messageBox: function messageBox() {
      var props = arguments.length > 0 && arguments[0] !== undefined ? arguments[0] : {};
      var status = props.status || 'info';

      if (status === 'error') {
        status = 'danger';
      }

      props.status = status;
      var wrapper = $(".".concat(MyAMS.config.alertsContainerClass));

      if (wrapper.length === 0) {
        wrapper = $('<div></div>').addClass(MyAMS.config.alertsContainerClass).appendTo(MyAMS.dom.root);
      }

      $(MESSAGE_TEMPLATE.render(props)).appendTo(wrapper).toast('show').on('hidden.bs.toast', function (evt) {
        $(evt.currentTarget).remove();
      });
    },

    /**
     * Display small notification message on top right
     *
     * @param props
     */
    smallBox: function smallBox() {
      var props = arguments.length > 0 && arguments[0] !== undefined ? arguments[0] : {};
      var status = props.status || 'info';

      if (status === 'error') {
        status = 'danger';
      }

      props.status = status;
      var wrapper = $(".".concat(MyAMS.config.alertsContainerClass));

      if (wrapper.length === 0) {
        wrapper = $('<div></div>').addClass(MyAMS.config.alertsContainerClass).appendTo(MyAMS.dom.root);
      }

      $(SMALLBOX_TEMPLATE.render(props)).appendTo(wrapper).toast('show').on('hidden.bs.toast', function (evt) {
        $(evt.currentTarget).remove();
      });
    },

    /**
     * Modal message box
     *
     * @param props
     * @returns {Promise<unknown>}
     */
    bigBox: function bigBox() {
      var props = arguments.length > 0 && arguments[0] !== undefined ? arguments[0] : {};
      return new Promise(function (resolve, reject) {
        var status = props.status || 'info';

        if (status === 'error') {
          status = 'danger';
        }

        props.status = status;

        MyAMS.require('modal').then(function () {
          var alert = $(BIGBOX_TEMPLATE.render(props)).appendTo(MyAMS.dom.root);
          alert.on('shown.bs.modal', function (evt) {
            $('.btn-primary', evt.target).focus();
          });
          alert.on('hidden.bs.modal', function () {
            resolve(alert.data('modal-result'));
            alert.remove();
          });
          alert.modal('show');
        }, function () {
          reject("Missing 'modal' module!");
        });
      });
    }
  };
  /**
   * Global module initialization
   */

  _exports.alert = alert;

  if (window.MyAMS) {
    if (MyAMS.env.bundle) {
      MyAMS.config.modules.push('alert');
    } else {
      MyAMS.alert = alert;
      console.debug("MyAMS: alert module loaded...");
    }
  }
});
//# sourceMappingURL=mod-alert-dev.js.map
