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
    global.modSkin = mod.exports;
  }
})(typeof globalThis !== "undefined" ? globalThis : typeof self !== "undefined" ? self : this, function (_exports) {
  "use strict";

  Object.defineProperty(_exports, "__esModule", {
    value: true
  });
  _exports.skin = void 0;

  var _this = void 0;

  function _slicedToArray(arr, i) { return _arrayWithHoles(arr) || _iterableToArrayLimit(arr, i) || _unsupportedIterableToArray(arr, i) || _nonIterableRest(); }

  function _nonIterableRest() { throw new TypeError("Invalid attempt to destructure non-iterable instance.\nIn order to be iterable, non-array objects must have a [Symbol.iterator]() method."); }

  function _unsupportedIterableToArray(o, minLen) { if (!o) return; if (typeof o === "string") return _arrayLikeToArray(o, minLen); var n = Object.prototype.toString.call(o).slice(8, -1); if (n === "Object" && o.constructor) n = o.constructor.name; if (n === "Map" || n === "Set") return Array.from(o); if (n === "Arguments" || /^(?:Ui|I)nt(?:8|16|32)(?:Clamped)?Array$/.test(n)) return _arrayLikeToArray(o, minLen); }

  function _arrayLikeToArray(arr, len) { if (len == null || len > arr.length) len = arr.length; for (var i = 0, arr2 = new Array(len); i < len; i++) { arr2[i] = arr[i]; } return arr2; }

  function _iterableToArrayLimit(arr, i) { if (typeof Symbol === "undefined" || !(Symbol.iterator in Object(arr))) return; var _arr = []; var _n = true; var _d = false; var _e = undefined; try { for (var _i = arr[Symbol.iterator](), _s; !(_n = (_s = _i.next()).done); _n = true) { _arr.push(_s.value); if (i && _arr.length === i) break; } } catch (err) { _d = true; _e = err; } finally { try { if (!_n && _i["return"] != null) _i["return"](); } finally { if (_d) throw _e; } } return _arr; }

  function _arrayWithHoles(arr) { if (Array.isArray(arr)) return arr; }

  /* global MyAMS */

  /**
   * MyAMS generic skin features
   */
  var $ = MyAMS.$;
  var _initialized = false;
  var skin = {
    /**
     * Main *skin* module initialization
     */
    init: function init() {
      if (_initialized) {
        return;
      }

      _initialized = true; // handle tooltips

      if (MyAMS.config.enableTooltips) {
        MyAMS.dom.root.tooltip({
          selector: '.hint',
          html: MyAMS.config.enableHtmlTooltips
        });
      }

      $('.hint').mousedown(function (evt) {
        $(evt.currentTarget).tooltip('hide');
      });
      $(document).on('clear.ams.content', function () {
        $('.tooltip').remove();
      }); // check URL when hash is changed

      skin.checkURL();
      $(window).on('hashchange', skin.checkURL);
    },

    /**
     * Specific content initialization
     *
     * @param element: the element to initialize
     */
    initElement: function initElement(element) {
      if (!MyAMS.config.enableTooltips) {
        $('.hint', element).tooltip({
          html: MyAMS.config.enableHtmlTooltips
        });
      }
    },

    /**
     * URL checking function.
     *
     * This function is an event handler for window's "hashchange" event, which is
     * triggered when the window location hash is modified; this can notably occur when a
     * navigation menu, for example, is clicked.
     */
    checkURL: function checkURL() {
      return new Promise(function (resolve, reject) {
        var nav = MyAMS.dom.nav;
        var hash = location.hash,
            url = hash.replace(/^#/, ''),
            tag = null;
        var tagPosition = url.indexOf('!');

        if (tagPosition > 0) {
          hash = hash.substring(0, tagPosition + 1);
          tag = url.substring(tagPosition + 1);
          url = url.substring(0, tagPosition);
        }

        var menu;

        if (url) {
          // new hash
          var container = $('#content');

          if (!container.exists()) {
            container = MyAMS.dom.root;
          }

          menu = $("a[href=\"".concat(hash, "\"]"), nav); // load specified URL into '#content'

          MyAMS.skin.loadURL(url, container).then(function () {
            var prefix = $('html head title').data('ams-title-prefix'),
                fullPrefix = prefix ? "".concat(prefix, " > ") : '';
            document.title = "".concat(fullPrefix).concat($('[data-ams-page-title]:first', container).data('ams-page-title') || menu.attr('title') || menu.text().trim() || document.title);

            if (tag) {
              var anchor = $("#".concat(tag));

              if (anchor.exists()) {
                MyAMS.require('ajax').then(function () {
                  MyAMS.ajax.check($.fn.scrollTo, "".concat(MyAMS.env.baseURL, "../ext/jquery-scrollto").concat(MyAMS.env.extext, ".js")).then(function () {
                    $('#main').scrollTo(anchor, {
                      offset: -15
                    });
                  });
                });
              }
            } // try to activate matching navigation menu


            if (menu.exists()) {
              MyAMS.require('nav').then(function () {
                MyAMS.nav.setActiveMenu(menu);
                MyAMS.nav.drawBreadcrumbs();
              }).then(resolve);
            } else {
              resolve();
            }
          }, reject);
        } else {
          // empty hash! We try to check if a specific menu was activated with a custom
          // data attribute, otherwise we go to the first navigation menu!
          var activeUrl = $('[data-ams-active-menu]').data('ams-active-menu');

          if (activeUrl) {
            menu = $("a[href=\"".concat(activeUrl, "\"]"), nav);
          } else {
            menu = $('>ul >li >a[href!="#"]', nav).first();
          }

          if (menu.exists()) {
            MyAMS.require('nav').then(function () {
              MyAMS.nav.setActiveMenu(menu);

              if (activeUrl) {
                MyAMS.nav.drawBreadcrumbs();
              } else {
                // we use location.replace to avoid storing intermediate URL
                // into browser's history
                window.location.replace(window.location.href + menu.attr('href'));
              }
            }).then(resolve, reject);
          } else {
            resolve();
          }
        }
      });
    },

    /**
     * Load specific URL into given container target.
     *
     * The function returns a Promise which is resolved when the remote content is actually
     * loaded and initialized
     *
     * @param url: remote content URL
     * @param target: jQuery selector or target container
     * @param options: additional options to AJAX call
     * @returns {Promise<string>}
     */
    loadURL: function loadURL(url, target) {
      var options = arguments.length > 2 && arguments[2] !== undefined ? arguments[2] : {};
      return new Promise(function (resolve, reject) {
        if (url.startsWith('#')) {
          url = url.substr(1);
        }

        target = $(target);
        MyAMS.core.executeFunctionByName(MyAMS.config.clearContent, document, target).then(function (status) {
          if (!status) {
            // applied veto!
            return;
          }

          var defaults = {
            type: 'GET',
            url: url,
            dataType: 'html',
            cache: false,
            beforeSend: function beforeSend() {
              target.html("<h1 class=\"loading\"><i class=\"fa fa-cog fa-spin\"></i> ".concat(MyAMS.i18n.LOADING, "</h1>"));

              if (options && options.preLoadCallback) {
                MyAMS.core.executeFunctionByName(options.preLoadCallback, _this, options.preLoadCallbackOptions);
              }

              if (target.attr('id') === 'content') {
                MyAMS.require('nav').then(function () {
                  var prefix = $('html head title').data('ams-title-prefix'),
                      fullPrefix = prefix ? "".concat(prefix, " > ") : '';
                  document.title = "".concat(fullPrefix).concat($('.breadcrumb li:last-child').text());
                  MyAMS.dom.root.animate({
                    scrollTop: 0
                  }, 'fast');
                });
              }
            }
          };
          var settings = $.extend({}, defaults, options),
              veto = {
            veto: false
          };
          target.trigger('before-load.ams.content', [settings, veto]);

          if (veto.veto) {
            return;
          }

          $.ajax(settings).then(function (result, status, xhr) {
            if ($.isArray(result)) {
              var _result = result;

              var _result2 = _slicedToArray(_result, 3);

              result = _result2[0];
              status = _result2[1];
              xhr = _result2[2];
            }

            MyAMS.require('ajax').then(function () {
              var response = MyAMS.ajax.getResponse(xhr);

              if (response) {
                var dataType = response.contentType,
                    _result3 = response.data;
                $('.loading', target).remove();

                switch (dataType) {
                  case 'json':
                    MyAMS.ajax.handleJSON(_result3, target);
                    resolve(_result3, status, xhr);
                    break;

                  case 'script':
                  case 'xml':
                    resolve(_result3, status, xhr);
                    break;

                  case 'html':
                  case 'text':
                  default:
                    target.parents('.hidden').removeClass('hidden');
                    MyAMS.core.executeFunctionByName(target.data('ams-clear-content') || MyAMS.config.clearContent, document, target).then(function () {
                      target.css({
                        opacity: '0.0'
                      }).html(_result3).removeClass('hidden').delay(30).animate({
                        opacity: '1.0'
                      }, 300);
                      MyAMS.core.executeFunctionByName(target.data('ams-init-content') || MyAMS.config.initContent, window, target).then(function () {
                        MyAMS.form && MyAMS.form.setFocus(target);
                        target.trigger('after-load.ams.content');
                        resolve(_result3, status, xhr);
                      });
                    }, reject);
                }

                MyAMS.stats && MyAMS.stats.logPageview();
              }
            });
          }, function (xhr, status, error) {
            target.html("<h3 class=\"error\"><i class=\"fa fa-exclamation-triangle text-danger\"></i> \n\t\t\t\t\t\t\t\t".concat(MyAMS.i18n.ERROR, " ").concat(error, "</h3>").concat(xhr.responseText));
            reject(error);
          });
        });
      });
    }
  };
  /**
   * Global module initialization
   */

  _exports.skin = skin;

  if (window.MyAMS) {
    if (MyAMS.env.bundle) {
      MyAMS.config.modules.push('skin');
    } else {
      MyAMS.skin = skin;
      console.debug("MyAMS: skin module loaded...");
    }
  }
});
//# sourceMappingURL=mod-skin-dev.js.map
