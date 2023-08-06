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
    global.modModal = mod.exports;
  }
})(typeof globalThis !== "undefined" ? globalThis : typeof self !== "undefined" ? self : this, function (_exports) {
  "use strict";

  Object.defineProperty(_exports, "__esModule", {
    value: true
  });
  _exports.modalToggleEventHandler = modalToggleEventHandler;
  _exports.modalShownEventHandler = modalShownEventHandler;
  _exports.dynamicModalShownEventHandler = dynamicModalShownEventHandler;
  _exports.modalDismissEventHandler = modalDismissEventHandler;
  _exports.modalHiddenEventHandler = modalHiddenEventHandler;
  _exports.dynamicModalHiddenEventHandler = dynamicModalHiddenEventHandler;
  _exports.modal = void 0;

  /* global MyAMS */

  /**
   * MyAMS modal dialogs support
   */
  var $ = MyAMS.$;
  var _initialized = false;
  /*
   * Standard data-toggle="modal" handler
   */

  function modalToggleEventHandler(evt) {
    return new Promise(function (resolve, reject) {
      var source = $(evt.currentTarget),
          handlers = source.data('ams-disabled-handlers');

      if (source.attr('disabled') || source.hasClass('disabled') || handlers === true || handlers === 'click' || handlers === 'all') {
        resolve(false);
        return;
      }

      if (source.data('ams-context-menu') === true) {
        resolve(false);
        return;
      }

      if (source.data('ams-stop-propagation') === true) {
        evt.stopPropagation();
      }

      evt.preventDefault();
      source.tooltip('hide');
      MyAMS.modal.open(source).then(function () {
        resolve(true);
      }, reject);
    });
  }
  /**
   * Standard modal shown event handler
   * This handler is used to allow modals stacking
   */


  function modalShownEventHandler(evt) {
    var zIndexModal = 1100; // Enable modals stacking

    var dialog = $(evt.target),
        visibleModalsCount = $('.modal:visible').length,
        zIndex = zIndexModal + 100 * visibleModalsCount;
    dialog.css('z-index', zIndex);
    setTimeout(function () {
      $('.modal-backdrop').not('.modal-stack').first().css('z-index', zIndex - 10).addClass('modal-stack');
    }, 0); // Check form contents before closing modals

    $(dialog).off('click', '[data-dismiss="modal"]').on('click', '[data-dismiss="modal"]', function (evt) {
      var handler = $(evt.currentTarget).data('ams-dismiss-handler') || modalDismissEventHandler;
      return MyAMS.core.executeFunctionByName(handler, document, evt);
    });
  }
  /**
   * Dynamic modal 'shown' callback
   * This callback is used to initialize modal's viewport size
   *
   * @param evt: source event
   */


  function dynamicModalShownEventHandler(evt) {
    var dialog = $(evt.target);
    return MyAMS.core.executeFunctionByName(dialog.data('ams-init-content') || MyAMS.config.initContent, document, dialog);
  }
  /**
   * Modal dismiss handler
   */


  function modalDismissEventHandler(evt) {
    return new Promise(function (resolve, reject) {
      var source = $(evt.currentTarget),
          dialog = source.parents('.modal').first();
      dialog.data('modal-result', $(evt.currentTarget).data('modal-dismiss-value'));

      if (MyAMS.form) {
        MyAMS.form.confirmChangedForm(dialog).then(function (status) {
          if (status === 'success') {
            dialog.modal('hide');
          }
        }).then(resolve, reject);
      } else {
        dialog.modal('hide');
        resolve();
      }
    });
  }
  /**
   * Standard modal hidden event handler
   *
   * If several visible modals are still, a "modal-open" class is added to body to ensure
   * modals are still visible.
   */


  function modalHiddenEventHandler() {
    if ($('.modal:visible').length > 0) {
      $.fn.modal.Constructor.prototype._checkScrollbar();

      $.fn.modal.Constructor.prototype._setScrollbar();

      $('body').addClass('modal-open');
    }
  }
  /**
   * Dynamic modal 'hidden' callback
   * This callback is used to clear and remove dynamic modals
   *
   * @param evt: source event
   */


  function dynamicModalHiddenEventHandler(evt) {
    var dialog = $(evt.target);
    MyAMS.core.executeFunctionByName(dialog.data('ams-clear-content') || MyAMS.config.clearContent, document, dialog).then(function () {
      if (dialog.data('dynamic') === true) {
        dialog.remove();
      }
    });
  }
  /**
   * Main modal module definition
   */


  var modal = {
    init: function init() {
      if (_initialized) {
        return;
      }

      _initialized = true;

      if (MyAMS.config.ajaxNav) {
        // Initialize modal dialogs links
        // Standard Bootstrap handlers are removed!!
        $(document).off('click', '[data-toggle="modal"]').on('click', '[data-toggle="modal"]', function (evt) {
          var handler = $(evt.currentTarget).data('ams-modal-handler') || modalToggleEventHandler;
          MyAMS.core.executeFunctionByName(handler, document, evt);
        });
      } // Handle modal shown event to allow modals stacking


      $(document).on('shown.bs.modal', '.modal', function (evt) {
        var handler = $(evt.currentTarget).data('ams-shown-handler') || modalShownEventHandler;
        MyAMS.core.executeFunctionByName(handler, document, evt);
      }); // Handle modal hidden event to check remaining modals

      $(document).on('hidden.bs.modal', '.modal', function (evt) {
        var handler = $(evt.currentTarget).data('ams-hidden-handler') || modalHiddenEventHandler;
        MyAMS.core.executeFunctionByName(handler, document, evt);
      });
    },
    open: function open(source, options) {
      return new Promise(function (resolve, reject) {
        var sourceData = {},
            url = source;

        if (typeof source !== 'string') {
          sourceData = source.data();
          url = source.attr('href') || sourceData.amsUrl;
        }

        var urlGetter = MyAMS.core.getFunctionByName(url);

        if (typeof urlGetter === 'function') {
          url = urlGetter(source);
        }

        if (!url) {
          reject("No provided URL!");
        }

        if (url.startsWith('#')) {
          // Open inner modal
          $(url).modal('show');
          resolve();
        } else {
          $.ajax({
            type: 'get',
            url: url,
            cache: sourceData.amsAllowCache === undefined ? false : sourceData.amsAllowCache,
            data: options
          }).then(function (data, status, request) {
            var modal = null;

            MyAMS.require('ajax').then(function () {
              var response = MyAMS.ajax.getResponse(request),
                  dataType = response.contentType,
                  result = response.data;
              var content, dialog, dialogData, dialogOptions, settings;

              switch (dataType) {
                case 'json':
                  MyAMS.ajax.handleJSON(result, $($(source).data('ams-json-target') || '#content'));
                  break;

                case 'script':
                case 'xml':
                  break;

                case 'html':
                case 'text':
                default:
                  content = $(result), dialog = $('.modal-dialog', content.wrap('<div></div>').parent()), dialogData = dialog.data() || {}, dialogOptions = {
                    backdrop: dialogData.backdrop === undefined ? 'static' : dialogData.backdrop
                  };
                  settings = $.extend({}, dialogOptions, dialogData.amsOptions);
                  settings = MyAMS.core.executeFunctionByName(dialogData.amsInit, dialog, settings) || settings;
                  modal = $('<div>').addClass('modal fade').data('dynamic', true).append(content).on('show.bs.modal', dynamicModalShownEventHandler).on('hidden.bs.modal', dynamicModalHiddenEventHandler).modal(settings);

                  if (MyAMS.stats && !(sourceData.amsLogEvent === false || dialogData.amsLogEvent === false)) {
                    MyAMS.stats.logPageview(url);
                  }

              }
            }).then(function () {
              resolve(modal);
            });
          });
        }
      });
    },

    /**
     * Close modal associated with given element
     *
     * @param element: the element contained into closed modal
     */
    close: function close(element) {
      if (typeof element === 'string') {
        element = $(element);
      } else if (typeof element === 'undefined') {
        element = $('.modal-dialog:last');
      }

      var dialog = element.objectOrParentWithClass('modal');

      if (dialog.length > 0) {
        dialog.modal('hide');
      }
    }
  };
  /**
   * Global module initialization
   */

  _exports.modal = modal;

  if (MyAMS.env.bundle) {
    MyAMS.config.modules.push('modal');
  } else {
    MyAMS.modal = modal;
    console.debug("MyAMS: modal module loaded...");
  }
});
//# sourceMappingURL=mod-modal-dev.js.map
