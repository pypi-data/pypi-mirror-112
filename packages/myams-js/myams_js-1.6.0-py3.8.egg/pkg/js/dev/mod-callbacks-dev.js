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
    global.modCallbacks = mod.exports;
  }
})(typeof globalThis !== "undefined" ? globalThis : typeof self !== "undefined" ? self : this, function (_exports) {
  "use strict";

  Object.defineProperty(_exports, "__esModule", {
    value: true
  });
  _exports.callbacks = void 0;

  function _createForOfIteratorHelper(o, allowArrayLike) { var it; if (typeof Symbol === "undefined" || o[Symbol.iterator] == null) { if (Array.isArray(o) || (it = _unsupportedIterableToArray(o)) || allowArrayLike && o && typeof o.length === "number") { if (it) o = it; var i = 0; var F = function F() {}; return { s: F, n: function n() { if (i >= o.length) return { done: true }; return { done: false, value: o[i++] }; }, e: function e(_e) { throw _e; }, f: F }; } throw new TypeError("Invalid attempt to iterate non-iterable instance.\nIn order to be iterable, non-array objects must have a [Symbol.iterator]() method."); } var normalCompletion = true, didErr = false, err; return { s: function s() { it = o[Symbol.iterator](); }, n: function n() { var step = it.next(); normalCompletion = step.done; return step; }, e: function e(_e2) { didErr = true; err = _e2; }, f: function f() { try { if (!normalCompletion && it.return != null) it.return(); } finally { if (didErr) throw err; } } }; }

  function _unsupportedIterableToArray(o, minLen) { if (!o) return; if (typeof o === "string") return _arrayLikeToArray(o, minLen); var n = Object.prototype.toString.call(o).slice(8, -1); if (n === "Object" && o.constructor) n = o.constructor.name; if (n === "Map" || n === "Set") return Array.from(o); if (n === "Arguments" || /^(?:Ui|I)nt(?:8|16|32)(?:Clamped)?Array$/.test(n)) return _arrayLikeToArray(o, minLen); }

  function _arrayLikeToArray(arr, len) { if (len == null || len > arr.length) len = arr.length; for (var i = 0, arr2 = new Array(len); i < len; i++) { arr2[i] = arr[i]; } return arr2; }

  /* global MyAMS */

  /**
   * MyAMS callbacks management
   */
  var $ = MyAMS.$;
  var _initialized = false;
  var callbacks = {
    init: function init() {
      if (_initialized) {
        return;
      }

      _initialized = true;
    },
    initElement: function initElement(element) {
      return new Promise(function (resolve, reject) {
        var deferred = [];
        $('[data-ams-callback]', element).each(function (idx, elt) {
          var data = $(elt).data();
          var callbacks = data.amsCallback;

          if (typeof callbacks === 'string') {
            try {
              callbacks = JSON.parse(data.amsCallback);
            } catch (e) {
              callbacks = data.amsCallback.split(/[\s,;]+/);
            }
          }

          if (!$.isArray(callbacks)) {
            callbacks = [callbacks];
          }

          var _iterator = _createForOfIteratorHelper(callbacks),
              _step;

          try {
            var _loop = function _loop() {
              var callback = _step.value;
              var callname = void 0,
                  callable = void 0,
                  source = void 0,
                  options = void 0;

              if (typeof callback === 'string') {
                callname = callback;
                callable = MyAMS.core.getFunctionByName(callname);
                source = data.amsCallbackOptions;
                options = data.amsCallbackOptions;

                if (typeof options === 'string') {
                  options = options.unserialize();
                }
              } else {
                // JSON object
                callname = callback.callback;
                callable = MyAMS.core.getFunctionByName(callname);
                source = callback.source;
                options = callback.options;
              }

              if (typeof callable === 'undefined') {
                if (source) {
                  deferred.push(MyAMS.core.getScript(source).then(function () {
                    callable = MyAMS.core.getFunctionByName(callname);

                    if (typeof callable === 'undefined') {
                      console.warn("Missing callback ".concat(callname, "!"));
                    } else {
                      callable.call(document, elt, options);
                    }
                  }));
                } else {
                  console.warn("Missing source for undefined callback ".concat(callback, "!"));
                }
              } else {
                deferred.push(Promise.resolve(callable.call(document, elt, options)));
              }
            };

            for (_iterator.s(); !(_step = _iterator.n()).done;) {
              _loop();
            }
          } catch (err) {
            _iterator.e(err);
          } finally {
            _iterator.f();
          }
        });
        $.when.apply($, deferred).then(resolve, reject);
      });
    }
  };
  /**
   * Global module initialization
   */

  _exports.callbacks = callbacks;

  if (window.MyAMS) {
    if (MyAMS.env.bundle) {
      MyAMS.config.modules.push('callbacks');
    } else {
      MyAMS.callbacks = callbacks;
      console.debug("MyAMS: callbacks module loaded...");
    }
  }
});
//# sourceMappingURL=mod-callbacks-dev.js.map
