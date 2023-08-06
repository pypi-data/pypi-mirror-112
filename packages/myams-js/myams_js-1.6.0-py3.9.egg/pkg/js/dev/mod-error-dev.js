(function (global, factory) {
  if (typeof define === "function" && define.amd) {
    define(["exports", "jsrender"], factory);
  } else if (typeof exports !== "undefined") {
    factory(exports, require("jsrender"));
  } else {
    var mod = {
      exports: {}
    };
    factory(mod.exports, global.jsrender);
    global.modError = mod.exports;
  }
})(typeof globalThis !== "undefined" ? globalThis : typeof self !== "undefined" ? self : this, function (_exports, _jsrender) {
  "use strict";

  Object.defineProperty(_exports, "__esModule", {
    value: true
  });
  _exports.error = void 0;

  function _createForOfIteratorHelper(o, allowArrayLike) { var it; if (typeof Symbol === "undefined" || o[Symbol.iterator] == null) { if (Array.isArray(o) || (it = _unsupportedIterableToArray(o)) || allowArrayLike && o && typeof o.length === "number") { if (it) o = it; var i = 0; var F = function F() {}; return { s: F, n: function n() { if (i >= o.length) return { done: true }; return { done: false, value: o[i++] }; }, e: function e(_e) { throw _e; }, f: F }; } throw new TypeError("Invalid attempt to iterate non-iterable instance.\nIn order to be iterable, non-array objects must have a [Symbol.iterator]() method."); } var normalCompletion = true, didErr = false, err; return { s: function s() { it = o[Symbol.iterator](); }, n: function n() { var step = it.next(); normalCompletion = step.done; return step; }, e: function e(_e2) { didErr = true; err = _e2; }, f: function f() { try { if (!normalCompletion && it.return != null) it.return(); } finally { if (didErr) throw err; } } }; }

  function _unsupportedIterableToArray(o, minLen) { if (!o) return; if (typeof o === "string") return _arrayLikeToArray(o, minLen); var n = Object.prototype.toString.call(o).slice(8, -1); if (n === "Object" && o.constructor) n = o.constructor.name; if (n === "Map" || n === "Set") return Array.from(o); if (n === "Arguments" || /^(?:Ui|I)nt(?:8|16|32)(?:Clamped)?Array$/.test(n)) return _arrayLikeToArray(o, minLen); }

  function _arrayLikeToArray(arr, len) { if (len == null || len > arr.length) len = arr.length; for (var i = 0, arr2 = new Array(len); i < len; i++) { arr2[i] = arr[i]; } return arr2; }

  var $ = MyAMS.$;
  var ERRORS_TEMPLATE_STRING = "\n\t<div class=\"alert alert-{{:status}}\" role=\"alert\">\n\t\t<button type=\"button\" class=\"close\" data-dismiss=\"alert\" \n\t\t\t\taria-label=\"{{*: MyAMS.i18n.BTN_CLODE }}\">\n\t\t\t<i class=\"fa fa-times\" aria-hidden=\"true\"></i>\t\n\t\t</button>\n\t\t{{if header}}\n\t\t<h5 class=\"alert-heading\">{{:header}}</h5>\n\t\t{{/if}}\n\t\t{{if message}}\n\t\t<p>{{:message}}</p>\n\t\t{{/if}}\n\t\t{{if messages}}\n\t\t<ul>\n\t\t{{for messages}}\n\t\t\t<li>\n\t\t\t\t{{if header}}<strong>{{:header}} :</strong>{{/if}}\n\t\t\t\t{{:message}}\n\t\t\t</li>\n\t\t{{/for}}\n\t\t</ul>\n\t\t{{/if}}\n\t\t{{if widgets}}\n\t\t<ul>\n\t\t{{for widgets}}\n\t\t\t<li>\n\t\t\t\t{{if header}}<strong>{{:header}} :</strong>{{/if}}\n\t\t\t\t{{:message}}\n\t\t\t</li>\n\t\t{{/for}}\n\t\t</ul>\n\t\t{{/if}}\n\t</div>";
  var ERROR_TEMPLATE = $.templates({
    markup: ERRORS_TEMPLATE_STRING,
    allowCode: true
  });
  var error = {
    /**
     * Show errors as alert in given parent
     *
     * @param parent: alert parent element
     * @param errors: errors properties
     */
    showErrors: function showErrors(parent, errors) {
      return new Promise(function (resolve, reject) {
        if (typeof errors === 'string') {
          // simple error message
          MyAMS.require('i18n', 'alert').then(function () {
            MyAMS.alert.alert({
              parent: parent,
              status: 'danger',
              header: MyAMS.i18n.ERROR_OCCURED,
              message: errors
            });
          }).then(resolve, reject);
        } else if ($.isArray(errors)) {
          // array of messages
          MyAMS.require('i18n', 'alert').then(function () {
            MyAMS.alert.alert({
              parent: parent,
              status: 'danger',
              header: MyAMS.i18n.ERRORS_OCCURED,
              message: errors
            });
          }).then(resolve, reject);
        } else {
          // full errors with widgets
          MyAMS.require('i18n', 'ajax', 'alert', 'form').then(function () {
            // clear previous alerts
            MyAMS.form.clearAlerts(parent); // create new alert

            var messages = [];

            var _iterator = _createForOfIteratorHelper(errors.messages || []),
                _step;

            try {
              for (_iterator.s(); !(_step = _iterator.n()).done;) {
                var message = _step.value;

                if (typeof message === 'string') {
                  messages.push({
                    header: null,
                    message: message
                  });
                } else {
                  messages.push(message);
                }
              }
            } catch (err) {
              _iterator.e(err);
            } finally {
              _iterator.f();
            }

            var _iterator2 = _createForOfIteratorHelper(errors.widgets || []),
                _step2;

            try {
              for (_iterator2.s(); !(_step2 = _iterator2.n()).done;) {
                var widget = _step2.value;
                messages.push({
                  header: widget.label,
                  message: widget.message
                });
              }
            } catch (err) {
              _iterator2.e(err);
            } finally {
              _iterator2.f();
            }

            var header = errors.header || (messages.length > 1 ? MyAMS.i18n.ERRORS_OCCURED : MyAMS.i18n.ERROR_OCCURED),
                props = {
              status: 'danger',
              header: header,
              message: errors.error || null,
              messages: messages
            };
            $(ERROR_TEMPLATE.render(props)).prependTo(parent); // update status of invalid widgets

            var _iterator3 = _createForOfIteratorHelper(errors.widgets || []),
                _step3;

            try {
              for (_iterator3.s(); !(_step3 = _iterator3.n()).done;) {
                var _widget = _step3.value;
                var input = void 0;

                if (_widget.id) {
                  input = $("#".concat(_widget.id), parent);
                } else {
                  input = $("[name=\"".concat(_widget.name, "\"]"), parent);
                }

                if (input.exists()) {
                  MyAMS.form.setInvalid(parent, input, _widget.message);
                }
              }
            } catch (err) {
              _iterator3.e(err);
            } finally {
              _iterator3.f();
            }

            MyAMS.ajax.check($.fn.scrollTo, "".concat(MyAMS.env.baseURL, "../ext/jquery-scrollto").concat(MyAMS.env.extext, ".js")).then(function () {
              var scrollBox = parent.parents('.modal-body');

              if (!scrollBox.exists()) {
                scrollBox = $('#main');
              }

              scrollBox.scrollTo(parent, {
                offset: -15
              });
            });
          }).then(resolve, reject);
        }
      });
    },

    /**
     * Display message for standard HTTP error
     *
     * @param error: error object
     */
    showHTTPError: function showHTTPError(error) {
      return new Promise(function (resolve, reject) {
        MyAMS.require('alert').then(function () {
          MyAMS.alert.messageBox({
            status: 'error',
            title: error.title,
            message: error.message,
            hideTimestamp: false,
            timeout: 0
          });
        }).then(resolve, reject);
      });
    }
  };
  /**
   * Global module initialization
   */

  _exports.error = error;

  if (window.MyAMS) {
    if (MyAMS.env.bundle) {
      MyAMS.config.modules.push('error');
    } else {
      MyAMS.error = error;
      console.debug("MyAMS: error module loaded...");
    }
  }
});
//# sourceMappingURL=mod-error-dev.js.map
