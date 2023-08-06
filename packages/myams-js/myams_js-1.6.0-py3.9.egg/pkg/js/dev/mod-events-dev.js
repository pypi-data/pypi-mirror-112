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
    global.modEvents = mod.exports;
  }
})(typeof globalThis !== "undefined" ? globalThis : typeof self !== "undefined" ? self : this, function (_exports) {
  "use strict";

  Object.defineProperty(_exports, "__esModule", {
    value: true
  });
  _exports.events = void 0;

  function _createForOfIteratorHelper(o, allowArrayLike) { var it; if (typeof Symbol === "undefined" || o[Symbol.iterator] == null) { if (Array.isArray(o) || (it = _unsupportedIterableToArray(o)) || allowArrayLike && o && typeof o.length === "number") { if (it) o = it; var i = 0; var F = function F() {}; return { s: F, n: function n() { if (i >= o.length) return { done: true }; return { done: false, value: o[i++] }; }, e: function e(_e2) { throw _e2; }, f: F }; } throw new TypeError("Invalid attempt to iterate non-iterable instance.\nIn order to be iterable, non-array objects must have a [Symbol.iterator]() method."); } var normalCompletion = true, didErr = false, err; return { s: function s() { it = o[Symbol.iterator](); }, n: function n() { var step = it.next(); normalCompletion = step.done; return step; }, e: function e(_e3) { didErr = true; err = _e3; }, f: function f() { try { if (!normalCompletion && it.return != null) it.return(); } finally { if (didErr) throw err; } } }; }

  function _slicedToArray(arr, i) { return _arrayWithHoles(arr) || _iterableToArrayLimit(arr, i) || _unsupportedIterableToArray(arr, i) || _nonIterableRest(); }

  function _nonIterableRest() { throw new TypeError("Invalid attempt to destructure non-iterable instance.\nIn order to be iterable, non-array objects must have a [Symbol.iterator]() method."); }

  function _unsupportedIterableToArray(o, minLen) { if (!o) return; if (typeof o === "string") return _arrayLikeToArray(o, minLen); var n = Object.prototype.toString.call(o).slice(8, -1); if (n === "Object" && o.constructor) n = o.constructor.name; if (n === "Map" || n === "Set") return Array.from(o); if (n === "Arguments" || /^(?:Ui|I)nt(?:8|16|32)(?:Clamped)?Array$/.test(n)) return _arrayLikeToArray(o, minLen); }

  function _arrayLikeToArray(arr, len) { if (len == null || len > arr.length) len = arr.length; for (var i = 0, arr2 = new Array(len); i < len; i++) { arr2[i] = arr[i]; } return arr2; }

  function _iterableToArrayLimit(arr, i) { if (typeof Symbol === "undefined" || !(Symbol.iterator in Object(arr))) return; var _arr = []; var _n = true; var _d = false; var _e = undefined; try { for (var _i = arr[Symbol.iterator](), _s; !(_n = (_s = _i.next()).done); _n = true) { _arr.push(_s.value); if (i && _arr.length === i) break; } } catch (err) { _d = true; _e = err; } finally { try { if (!_n && _i["return"] != null) _i["return"](); } finally { if (_d) throw _e; } } return _arr; }

  function _arrayWithHoles(arr) { if (Array.isArray(arr)) return arr; }

  /* global MyAMS */

  /**
   * MyAMS events management
   */
  var $ = MyAMS.$;
  var _initialized = false;
  var events = {
    init: function init() {
      if (_initialized) {
        return;
      }

      _initialized = true; // Initialize custom click handlers

      $(document).on('click', '[data-ams-click-handler]', MyAMS.events.clickHandler); // Initialize custom change handlers

      $(document).on('change', '[data-ams-change-handler]', MyAMS.events.changeHandler); // Initialize custom event on click

      $(document).on('click', '[data-ams-click-event]', MyAMS.events.triggerEvent);
    },
    initElement: function initElement(element) {
      $('[data-ams-events-handlers]', element).each(function (idx, elt) {
        var context = $(elt),
            handlers = context.data('ams-events-handlers');

        if (handlers) {
          var _loop = function _loop() {
            var _Object$entries$_i = _slicedToArray(_Object$entries[_i], 2),
                event = _Object$entries$_i[0],
                handler = _Object$entries$_i[1];

            context.on(event, function (event) {
              for (var _len = arguments.length, options = new Array(_len > 1 ? _len - 1 : 0), _key = 1; _key < _len; _key++) {
                options[_key - 1] = arguments[_key];
              }

              if (options.length > 0) {
                var _MyAMS$core;

                (_MyAMS$core = MyAMS.core).executeFunctionByName.apply(_MyAMS$core, [handler, document, event].concat(options));
              } else {
                MyAMS.core.executeFunctionByName(handler, document, event, context.data('ams-events-options') || {});
              }
            });
          };

          for (var _i = 0, _Object$entries = Object.entries(handlers); _i < _Object$entries.length; _i++) {
            _loop();
          }
        }
      });
    },

    /**
     * Get events handlers on given element for a specific event
     *
     * @param element: the checked element
     * @param event: event for which handlers lookup is made
     * @returns: an array of elements for which the event handler is defined
     */
    getHandlers: function getHandlers(element, event) {
      var result = [],
          handlers = element.data('ams-events-handlers');

      if (handlers && handlers[event]) {
        result.push(element);
      }

      $('[data-ams-events-handlers]', element).each(function (idx, elt) {
        var context = $(elt),
            handlers = context.data('ams-events-handlers');

        if (handlers && handlers[event]) {
          result.push(context);
        }
      });
      return result;
    },

    /**
     * Generic click event handler
     */
    clickHandler: function clickHandler(event) {
      var source = $(event.currentTarget),
          handlers = source.data('ams-disabled-handlers');

      if (handlers === true || handlers === 'click' || handlers === 'all') {
        return;
      }

      var data = source.data();

      if (data.amsClickHandler) {
        if (data.amsPreventDefault !== false && data.amsClickPreventDefault !== false) {
          event.preventDefault();
        }

        if (data.amsStopPropagation !== false && data.amsClickStopPropagation !== false) {
          event.stopPropagation();
        }

        var _iterator = _createForOfIteratorHelper(data.amsClickHandler.split(/[\s,;]+/)),
            _step;

        try {
          for (_iterator.s(); !(_step = _iterator.n()).done;) {
            var handler = _step.value;
            var callback = MyAMS.core.getFunctionByName(handler);

            if (callback !== undefined) {
              callback.call(document, event, data.amsClickHandlerOptions);
            }
          }
        } catch (err) {
          _iterator.e(err);
        } finally {
          _iterator.f();
        }
      }
    },

    /**
     * Generic change event handler
     */
    changeHandler: function changeHandler(event) {
      var source = $(event.currentTarget); // Disable change handlers for readonly inputs
      // These change handlers are activated by IE!!!

      if (source.prop('readonly')) {
        return;
      }

      var handlers = source.data('ams-disabled-handlers');

      if (handlers === true || handlers === 'change' || handlers === 'all') {
        return;
      }

      var data = source.data();

      if (data.amsChangeHandler) {
        if (data.amsKeepDefault !== false && data.amsChangeKeepDefault !== false) {
          event.preventDefault();
        }

        if (data.amsStopPropagation !== false && data.amsChangeStopPropagation !== false) {
          event.stopPropagation();
        }

        var _iterator2 = _createForOfIteratorHelper(data.amsChangeHandler.split(/[\s,;]+/)),
            _step2;

        try {
          for (_iterator2.s(); !(_step2 = _iterator2.n()).done;) {
            var handler = _step2.value;
            var callback = MyAMS.core.getFunctionByName(handler);

            if (callback !== undefined) {
              callback.call(document, event, data.amsChangeHandlerOptions);
            }
          }
        } catch (err) {
          _iterator2.e(err);
        } finally {
          _iterator2.f();
        }
      }
    },

    /**
     * Genenric click event trigger
     */
    triggerEvent: function triggerEvent(event) {
      var source = $(event.currentTarget);
      $(event.target).trigger(source.data('ams-click-event'), source.data('ams-click-event-options'));
    }
  };
  /**
   * Global module initialization
   */

  _exports.events = events;

  if (MyAMS.env.bundle) {
    MyAMS.config.modules.push('events');
  } else {
    MyAMS.events = events;
    console.debug("MyAMS: events module loaded...");
  }
});
//# sourceMappingURL=mod-events-dev.js.map
