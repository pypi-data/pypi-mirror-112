/******/ (function(modules) { // webpackBootstrap
/******/ 	// The module cache
/******/ 	var installedModules = {};
/******/
/******/ 	// The require function
/******/ 	function __webpack_require__(moduleId) {
/******/
/******/ 		// Check if module is in cache
/******/ 		if(installedModules[moduleId]) {
/******/ 			return installedModules[moduleId].exports;
/******/ 		}
/******/ 		// Create a new module (and put it into the cache)
/******/ 		var module = installedModules[moduleId] = {
/******/ 			i: moduleId,
/******/ 			l: false,
/******/ 			exports: {}
/******/ 		};
/******/
/******/ 		// Execute the module function
/******/ 		modules[moduleId].call(module.exports, module, module.exports, __webpack_require__);
/******/
/******/ 		// Flag the module as loaded
/******/ 		module.l = true;
/******/
/******/ 		// Return the exports of the module
/******/ 		return module.exports;
/******/ 	}
/******/
/******/
/******/ 	// expose the modules object (__webpack_modules__)
/******/ 	__webpack_require__.m = modules;
/******/
/******/ 	// expose the module cache
/******/ 	__webpack_require__.c = installedModules;
/******/
/******/ 	// define getter function for harmony exports
/******/ 	__webpack_require__.d = function(exports, name, getter) {
/******/ 		if(!__webpack_require__.o(exports, name)) {
/******/ 			Object.defineProperty(exports, name, { enumerable: true, get: getter });
/******/ 		}
/******/ 	};
/******/
/******/ 	// define __esModule on exports
/******/ 	__webpack_require__.r = function(exports) {
/******/ 		if(typeof Symbol !== 'undefined' && Symbol.toStringTag) {
/******/ 			Object.defineProperty(exports, Symbol.toStringTag, { value: 'Module' });
/******/ 		}
/******/ 		Object.defineProperty(exports, '__esModule', { value: true });
/******/ 	};
/******/
/******/ 	// create a fake namespace object
/******/ 	// mode & 1: value is a module id, require it
/******/ 	// mode & 2: merge all properties of value into the ns
/******/ 	// mode & 4: return value when already ns object
/******/ 	// mode & 8|1: behave like require
/******/ 	__webpack_require__.t = function(value, mode) {
/******/ 		if(mode & 1) value = __webpack_require__(value);
/******/ 		if(mode & 8) return value;
/******/ 		if((mode & 4) && typeof value === 'object' && value && value.__esModule) return value;
/******/ 		var ns = Object.create(null);
/******/ 		__webpack_require__.r(ns);
/******/ 		Object.defineProperty(ns, 'default', { enumerable: true, value: value });
/******/ 		if(mode & 2 && typeof value != 'string') for(var key in value) __webpack_require__.d(ns, key, function(key) { return value[key]; }.bind(null, key));
/******/ 		return ns;
/******/ 	};
/******/
/******/ 	// getDefaultExport function for compatibility with non-harmony modules
/******/ 	__webpack_require__.n = function(module) {
/******/ 		var getter = module && module.__esModule ?
/******/ 			function getDefault() { return module['default']; } :
/******/ 			function getModuleExports() { return module; };
/******/ 		__webpack_require__.d(getter, 'a', getter);
/******/ 		return getter;
/******/ 	};
/******/
/******/ 	// Object.prototype.hasOwnProperty.call
/******/ 	__webpack_require__.o = function(object, property) { return Object.prototype.hasOwnProperty.call(object, property); };
/******/
/******/ 	// __webpack_public_path__
/******/ 	__webpack_require__.p = "";
/******/
/******/
/******/ 	// Load entry module and return exports
/******/ 	return __webpack_require__(__webpack_require__.s = "./src/js/myams-core.js");
/******/ })
/************************************************************************/
/******/ ({

/***/ "./src/js/ext-base.js":
/*!****************************!*\
  !*** ./src/js/ext-base.js ***!
  \****************************/
/*! exports provided: init, getModules, initPage, initContent, clearContent, getObject, getFunctionByName, executeFunctionByName, getSource, getScript, getCSS, getQueryVar, generateId, generateUUID, switchIcon, default */
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, "init", function() { return init; });
/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, "getModules", function() { return getModules; });
/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, "initPage", function() { return initPage; });
/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, "initContent", function() { return initContent; });
/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, "clearContent", function() { return clearContent; });
/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, "getObject", function() { return getObject; });
/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, "getFunctionByName", function() { return getFunctionByName; });
/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, "executeFunctionByName", function() { return executeFunctionByName; });
/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, "getSource", function() { return getSource; });
/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, "getScript", function() { return getScript; });
/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, "getCSS", function() { return getCSS; });
/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, "getQueryVar", function() { return getQueryVar; });
/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, "generateId", function() { return generateId; });
/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, "generateUUID", function() { return generateUUID; });
/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, "switchIcon", function() { return switchIcon; });
/* harmony import */ var _ext_registry__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! ./ext-registry */ "./src/js/ext-registry.js");
function _toConsumableArray(arr) { return _arrayWithoutHoles(arr) || _iterableToArray(arr) || _unsupportedIterableToArray(arr) || _nonIterableSpread(); }

function _nonIterableSpread() { throw new TypeError("Invalid attempt to spread non-iterable instance.\nIn order to be iterable, non-array objects must have a [Symbol.iterator]() method."); }

function _iterableToArray(iter) { if (typeof Symbol !== "undefined" && Symbol.iterator in Object(iter)) return Array.from(iter); }

function _arrayWithoutHoles(arr) { if (Array.isArray(arr)) return _arrayLikeToArray(arr); }

function _slicedToArray(arr, i) { return _arrayWithHoles(arr) || _iterableToArrayLimit(arr, i) || _unsupportedIterableToArray(arr, i) || _nonIterableRest(); }

function _nonIterableRest() { throw new TypeError("Invalid attempt to destructure non-iterable instance.\nIn order to be iterable, non-array objects must have a [Symbol.iterator]() method."); }

function _iterableToArrayLimit(arr, i) { if (typeof Symbol === "undefined" || !(Symbol.iterator in Object(arr))) return; var _arr = []; var _n = true; var _d = false; var _e = undefined; try { for (var _i = arr[Symbol.iterator](), _s; !(_n = (_s = _i.next()).done); _n = true) { _arr.push(_s.value); if (i && _arr.length === i) break; } } catch (err) { _d = true; _e = err; } finally { try { if (!_n && _i["return"] != null) _i["return"](); } finally { if (_d) throw _e; } } return _arr; }

function _arrayWithHoles(arr) { if (Array.isArray(arr)) return arr; }

function _createForOfIteratorHelper(o, allowArrayLike) { var it; if (typeof Symbol === "undefined" || o[Symbol.iterator] == null) { if (Array.isArray(o) || (it = _unsupportedIterableToArray(o)) || allowArrayLike && o && typeof o.length === "number") { if (it) o = it; var i = 0; var F = function F() {}; return { s: F, n: function n() { if (i >= o.length) return { done: true }; return { done: false, value: o[i++] }; }, e: function e(_e2) { throw _e2; }, f: F }; } throw new TypeError("Invalid attempt to iterate non-iterable instance.\nIn order to be iterable, non-array objects must have a [Symbol.iterator]() method."); } var normalCompletion = true, didErr = false, err; return { s: function s() { it = o[Symbol.iterator](); }, n: function n() { var step = it.next(); normalCompletion = step.done; return step; }, e: function e(_e3) { didErr = true; err = _e3; }, f: function f() { try { if (!normalCompletion && it.return != null) it.return(); } finally { if (didErr) throw err; } } }; }

function _unsupportedIterableToArray(o, minLen) { if (!o) return; if (typeof o === "string") return _arrayLikeToArray(o, minLen); var n = Object.prototype.toString.call(o).slice(8, -1); if (n === "Object" && o.constructor) n = o.constructor.name; if (n === "Map" || n === "Set") return Array.from(o); if (n === "Arguments" || /^(?:Ui|I)nt(?:8|16|32)(?:Clamped)?Array$/.test(n)) return _arrayLikeToArray(o, minLen); }

function _arrayLikeToArray(arr, len) { if (len == null || len > arr.length) len = arr.length; for (var i = 0, arr2 = new Array(len); i < len; i++) { arr2[i] = arr[i]; } return arr2; }

/* global $, FontAwesome */

/**
 * MyAMS base features
 */
if (!window.jQuery) {
  window.$ = window.jQuery = __webpack_require__(/*! jquery */ "jquery");
}


/**
 * Init JQuery extensions
 */

function init($) {
  /**
   * String prototype extensions
   */
  $.extend(String.prototype, {
    /**
     * Replace dashed names with camelCase variation
     */
    camelCase: function camelCase() {
      if (!this) {
        return this;
      }

      return this.replace(/-(.)/g, function (dash, rest) {
        return rest.toUpperCase();
      });
    },

    /**
     * Replace camelCase string with dashed name
     */
    deCase: function deCase() {
      if (!this) {
        return this;
      }

      return this.replace(/[A-Z]/g, function (cap) {
        return "-".concat(cap.toLowerCase());
      });
    },

    /**
     * Convert first letter only to lowercase
     */
    initLowerCase: function initLowerCase() {
      if (!this) {
        return this;
      }

      return this.charAt(0).toLowerCase() + this.slice(1);
    },

    /**
     * Convert URL params to object
     */
    unserialize: function unserialize() {
      if (!this) {
        return this;
      }

      var str = decodeURIComponent(this),
          chunks = str.split('&'),
          obj = {};

      var _iterator = _createForOfIteratorHelper(chunks),
          _step;

      try {
        for (_iterator.s(); !(_step = _iterator.n()).done;) {
          var chunk = _step.value;

          var _chunk$split = chunk.split('=', 2),
              _chunk$split2 = _slicedToArray(_chunk$split, 2),
              key = _chunk$split2[0],
              val = _chunk$split2[1];

          obj[key] = val;
        }
      } catch (err) {
        _iterator.e(err);
      } finally {
        _iterator.f();
      }

      return obj;
    }
  });
  /**
   * Global JQuery object extensions
   */

  $.extend($, {
    /**
     * Extend source object with given extensions, but only for properties matching
     * given prefix.
     *
     * @param source: source object, which will be updated in-place
     * @param prefix: property names prefix selector
     * @param getter: optional getter used to extract final value
     * @param extensions: list of extensions object
     * @returns {*}: modified source object
     */
    extendPrefix: function extendPrefix(source, prefix, getter) {
      for (var _len = arguments.length, extensions = new Array(_len > 3 ? _len - 3 : 0), _key = 3; _key < _len; _key++) {
        extensions[_key - 3] = arguments[_key];
      }

      for (var _i2 = 0, _extensions = extensions; _i2 < _extensions.length; _i2++) {
        var extension = _extensions[_i2];

        for (var _i3 = 0, _Object$entries = Object.entries(extension); _i3 < _Object$entries.length; _i3++) {
          var _Object$entries$_i = _slicedToArray(_Object$entries[_i3], 2),
              key = _Object$entries$_i[0],
              value = _Object$entries$_i[1];

          if (key.startsWith(prefix)) {
            source[key.substring(prefix.length).initLowerCase()] = getter === null ? value : getter(value);
          }
        }
      }

      return source;
    },

    /**
     * Extend source with given extensions, but only for existing attributes
     *
     * @param source: source object, which will be updated in-place
     * @param getter: optional getter used to extract final value
     * @param extensions: list of extensions object
     * @returns {*}: modified source object
     */
    extendOnly: function extendOnly(source, getter) {
      for (var _len2 = arguments.length, extensions = new Array(_len2 > 2 ? _len2 - 2 : 0), _key2 = 2; _key2 < _len2; _key2++) {
        extensions[_key2 - 2] = arguments[_key2];
      }

      for (var _i4 = 0, _extensions2 = extensions; _i4 < _extensions2.length; _i4++) {
        var extension = _extensions2[_i4];

        for (var _i5 = 0, _Object$entries2 = Object.entries(extension); _i5 < _Object$entries2.length; _i5++) {
          var _Object$entries2$_i = _slicedToArray(_Object$entries2[_i5], 2),
              key = _Object$entries2$_i[0],
              value = _Object$entries2$_i[1];

          if (Object.prototype.hasOwnProperty.call(source, key)) {
            source[key] = getter === null ? value : getter(value);
          }
        }
      }

      return source;
    }
  });
  /**
   * New JQuery functions
   */

  $.fn.extend({
    /**
     * Check if current object is empty or not
     */
    exists: function exists() {
      return $(this).length > 0;
    },

    /**
     * Get object if it supports given CSS class,
     * otherwise look for parents
     */
    objectOrParentWithClass: function objectOrParentWithClass(klass) {
      if (this.hasClass(klass)) {
        return this;
      }

      return this.parents(".".concat(klass));
    },

    /**
     * Build an array of attributes of the given selection
     */
    listattr: function listattr(attr) {
      var result = [];
      this.each(function (index, element) {
        result.push($(element).attr(attr));
      });
      return result;
    },

    /**
     * CSS style function - get or set object style attribute
     * Code from Aram Kocharyan on stackoverflow.com
     */
    style: function style(styleName, value, priority) {
      var result = this;
      this.each(function (idx, node) {
        // Ensure we have a DOM node
        if (typeof node === 'undefined') {
          return false;
        } // CSSStyleDeclaration


        var style = node.style; // Getter/Setter

        if (typeof styleName !== 'undefined') {
          if (typeof value !== 'undefined') {
            // Set style property
            priority = typeof priority !== 'undefined' ? priority : '';
            style.setProperty(styleName, value, priority);
          } else {
            // Get style property
            result = style.getPropertyValue(styleName);
            return false;
          }
        } else {
          // Get CSSStyleDeclaration
          result = style;
          return false;
        }
      });
      return result;
    },

    /**
     * Remove CSS classes starting with a given prefix
     */
    removeClassPrefix: function removeClassPrefix(prefix) {
      this.each(function (i, it) {
        var classes = it.className.split(/\s+/).map(function (item) {
          return item.startsWith(prefix) ? "" : item;
        });
        it.className = $.trim(classes.join(" "));
      });
      return this;
    }
  });
  $(document).ready(function () {
    var html = $('html');
    html.removeClass('no-js').addClass('js');
    MyAMS.core.executeFunctionByName(html.data('ams-init-page') || MyAMS.config.initPage);
  });
}
/**
 * Get list of modules names required by given element
 *
 * @param element: parent element
 * @returns {*[]}
 */

function getModules(element) {
  var modules = [];
  var mods = element.data('ams-modules');

  if (typeof mods === 'string') {
    modules = modules.concat(mods.trim().split(/[\s,;]+/));
  } else if (mods) {
    for (var _i6 = 0, _Object$entries3 = Object.entries(mods); _i6 < _Object$entries3.length; _i6++) {
      var _Object$entries3$_i = _slicedToArray(_Object$entries3[_i6], 2),
          name = _Object$entries3$_i[0],
          path = _Object$entries3$_i[1];

      var entry = {};
      entry[name] = path;
      modules.push(entry);
    }
  }

  $('[data-ams-modules]', element).each(function (idx, elt) {
    var mods = $(elt).data('ams-modules');

    if (typeof mods === 'string') {
      modules = modules.concat(mods.trim().split(/[\s,;]+/));
    } else if (mods) {
      for (var _i7 = 0, _Object$entries4 = Object.entries(mods); _i7 < _Object$entries4.length; _i7++) {
        var _Object$entries4$_i = _slicedToArray(_Object$entries4[_i7], 2),
            _name = _Object$entries4$_i[0],
            _path = _Object$entries4$_i[1];

        var _entry = {};
        _entry[_name] = _path;
        modules.push(_entry);
      }
    }
  });
  return _toConsumableArray(new Set(modules));
}
/**
 * Main page initialization
 */

function initPage() {
  return MyAMS.require('i18n').then(function () {
    MyAMS.dom = getDOM();
    var modules = getModules(MyAMS.dom.root);

    MyAMS.require.apply(MyAMS, _toConsumableArray(modules)).then(function () {
      var _iterator2 = _createForOfIteratorHelper(MyAMS.config.modules),
          _step2;

      try {
        for (_iterator2.s(); !(_step2 = _iterator2.n()).done;) {
          var moduleName = _step2.value;
          executeFunctionByName("MyAMS.".concat(moduleName, ".init"));
        }
      } catch (err) {
        _iterator2.e(err);
      } finally {
        _iterator2.f();
      }

      MyAMS.core.executeFunctionByName(MyAMS.dom.page.data('ams-init-content') || MyAMS.config.initContent);
    });
  });
}
/**
 * Main content initialization; this function will initialize all plug-ins, callbacks and
 * events listeners in the selected element
 *
 * @param element: source element to initialize
 */

function initContent() {
  var element = arguments.length > 0 && arguments[0] !== undefined ? arguments[0] : null;

  if (element === null) {
    element = $('body');
  }

  element = $(element);

  function initElementModules() {
    var _iterator3 = _createForOfIteratorHelper(MyAMS.config.modules),
        _step3;

    try {
      for (_iterator3.s(); !(_step3 = _iterator3.n()).done;) {
        var moduleName = _step3.value;
        executeFunctionByName("MyAMS.".concat(moduleName, ".initElement"), document, element);
      }
    } catch (err) {
      _iterator3.e(err);
    } finally {
      _iterator3.f();
    }
  }

  return new Promise(function (resolve, reject) {
    var modules = getModules(element);
    return MyAMS.require.apply(MyAMS, _toConsumableArray(modules)).then(function () {
      element.trigger('before-init.ams.content');

      if (MyAMS.config.useRegistry && !element.data('ams-disable-registry')) {
        MyAMS.registry.initElement(element).then(function () {
          initElementModules();
        }).then(function () {
          MyAMS.registry.run(element);
          element.trigger('after-init.ams.content');
        }).then(resolve);
      } else {
        initElementModules();
        resolve();
      }
    }, function () {
      reject("Missing MyAMS modules!");
    });
  });
}
/**
 * Container clearing function.
 *
 * This function is called before replacing an element contents with new DOM elements;
 * an 'ams.container.before-cleaning' event is triggered, with arguments which are the
 * container and a "veto" object containing a single boolean "veto" property; if any
 * handler attached to this event set the "veto" property to *true*,
 *
 * The function returns a Promise which is resolved with the opposite value of the "veto"
 * property.
 *
 * @param element: the parent element which may be cleaned
 * @returns {Promise<boolean>}
 */

function clearContent(element) {
  if (typeof element === 'string') {
    element = $(element);
  }

  return new Promise(function (resolve, reject) {
    var veto = {
      veto: false
    };
    $(document).trigger('clear.ams.content', [veto, element]);

    if (!veto.veto) {
      MyAMS.require('events').then(function () {
        $(MyAMS.events.getHandlers(element, 'clear.ams.content')).each(function (idx, elt) {
          $(elt).trigger('clear.ams.content', [veto]);

          if (veto.veto) {
            return false;
          }
        });

        if (!veto.veto) {
          $(MyAMS.events.getHandlers(element, 'cleared.ams.content')).each(function (idx, elt) {
            $(elt).trigger('cleared.ams.content');
          });
          $(document).trigger('cleared.ams.content', [element]);
        }

        resolve(!veto.veto);
      }, function () {
        reject("Missing MyAMS.events module!");
      });
    } else {
      resolve(!veto.veto);
    }
  });
}
/**
 * Get an object given by name
 *
 * @param objectName: dotted name of the object
 * @param context: source context, or window if undefined
 * @returns {Object|undefined}
 */

function getObject(objectName, context) {
  if (!objectName) {
    return undefined;
  }

  if (typeof objectName !== 'string') {
    return objectName;
  }

  var namespaces = objectName.split('.');
  context = context === undefined || context === null ? window : context;

  var _iterator4 = _createForOfIteratorHelper(namespaces),
      _step4;

  try {
    for (_iterator4.s(); !(_step4 = _iterator4.n()).done;) {
      var name = _step4.value;

      try {
        context = context[name];
      } catch (exc) {
        return undefined;
      }
    }
  } catch (err) {
    _iterator4.e(err);
  } finally {
    _iterator4.f();
  }

  return context;
}
/**
 * Get function object from name
 *
 * @param functionName: dotted name of the function
 * @param context: source context; window if undefined
 * @returns {function|undefined}
 */

function getFunctionByName(functionName, context) {
  if (functionName === null || typeof functionName === 'undefined') {
    return undefined;
  } else if (typeof functionName === 'function') {
    return functionName;
  } else if (typeof functionName !== 'string') {
    return undefined;
  }

  var namespaces = functionName.split("."),
      func = namespaces.pop();
  context = context === undefined || context === null ? window : context;

  var _iterator5 = _createForOfIteratorHelper(namespaces),
      _step5;

  try {
    for (_iterator5.s(); !(_step5 = _iterator5.n()).done;) {
      var name = _step5.value;

      try {
        context = context[name];
      } catch (e) {
        return undefined;
      }
    }
  } catch (err) {
    _iterator5.e(err);
  } finally {
    _iterator5.f();
  }

  try {
    return context[func];
  } catch (e) {
    return undefined;
  }
}
/**
 * Execute a function, given by it's name
 *
 * @param functionName: dotted name of the function
 * @param context: parent context, or window if undefined
 * @param args...: optional function arguments
 * @returns {*}: result of the called function
 */

function executeFunctionByName(functionName, context
/*, args */
) {
  var func = getFunctionByName(functionName, window);

  if (typeof func === 'function') {
    var args = Array.prototype.slice.call(arguments, 2);
    return func.apply(context, args);
  }
}
/**
 * Get target URL matching given source
 *
 * Given URL can include variable names (with their namespace), given between braces,
 * as in {MyAMS.env.baseURL}
 */

function getSource(url) {
  return url.replace(/{[^{}]*}/g, function (match) {
    return getObject(match.substr(1, match.length - 2));
  });
}
/**
 * Dynamic script loader function
 *
 * @param url: script URL
 * @param options: a set of options to be added to AJAX call
 */

function getScript(url) {
  var options = arguments.length > 1 && arguments[1] !== undefined ? arguments[1] : {};
  return new Promise(function (resolve, reject) {
    var defaults = {
      dataType: 'script',
      url: getSource(url),
      cache: MyAMS.env.devmode,
      async: true
    };
    var settings = $.extend({}, defaults, options);
    $.ajax(settings).then(function () {
      resolve(url);
    }, function (xhr, status, error) {
      reject(error);
    });
  });
}
/**
 * Get CSS matching given URL
 *
 * @param url: CSS source URL
 * @param name: name of the given CSS
 */

function getCSS(url, name) {
  return new Promise(function (resolve
  /*, reject */
  ) {
    var head = $('HEAD');
    var style = $("style[data-ams-id=\"".concat(name, "\"]"), head);

    if (style.length === 0) {
      style = $('<style>').attr('data-ams-id', name).text("@import \"".concat(getSource(url), "\";")).appendTo(head);
      var styleInterval = setInterval(function () {
        try {
          // eslint-disable-next-line no-unused-vars
          var _check = style[0].sheet.cssRules; // Is only populated when file is loaded

          clearInterval(styleInterval);
          resolve(true);
        } catch (e) {// CSS is not loaded yet, just wait...
        }
      }, 10);
    } else {
      resolve(false);
    }
  });
}
/**
 * Extract parameter value from given query string
 *
 * @param src: source URL
 * @param varName: variable name
 * @returns {boolean|*}
 */

function getQueryVar(src, varName) {
  // Check src
  if (typeof src !== 'string' || src.indexOf('?') < 0) {
    return undefined;
  }

  if (!src.endsWith('&')) {
    src += '&';
  } // Dynamic replacement RegExp


  var regex = new RegExp(".*?[&\\?]".concat(varName, "=(.*?)&.*")); // Apply RegExp to the query string

  var val = src.replace(regex, "$1"); // If the string is the same, we didn't find a match - return null

  return val === src ? null : val;
}
/**
 * Generate a random ID
 */

function generateId() {
  function s4() {
    return Math.floor((1 + Math.random()) * 0x10000).toString(16).substring(1);
  }

  return s4() + s4() + s4() + s4();
}
/**
 * Generate a random unique UUID
 */

function generateUUID() {
  var d = new Date().getTime();
  return 'xxxxxxxx-xxxx-4xxx-yxxx-xxxxxxxxxxxx'.replace(/[xy]/g, function (c) {
    var r = (d + Math.random() * 16) % 16 | 0;
    d = Math.floor(d / 16);
    return (c === 'x' ? r : r & 0x3 | 0x8).toString(16);
  });
}
/**
 * Switch a FontAwesome icon.
 * Use FontAwesome API to get image as SVG, if FontAwesome is loaded from Javascript and is using
 * SVG auto-replace, otherwise just switch CSS class.
 *
 * @param element: source element
 * @param fromClass: initial CSS class (without "fa-" prefix)
 * @param toClass: new CSS class (without "fa-" prefix)
 */

function switchIcon(element, fromClass, toClass) {
  if (typeof element === 'string') {
    element = $(element);
  }

  if (MyAMS.config.useSVGIcons) {
    var iconDef = FontAwesome.findIconDefinition({
      iconName: toClass
    });
    element.html(FontAwesome.icon(iconDef).html);
  } else {
    element.removeClass("fa-".concat(fromClass)).addClass("fa-".concat(toClass));
  }
}
/**
 * MyAMS base functions
 *
 * @type {{devmode: boolean, baseURL: string, devext: string}}
 */

function getEnv($) {
  var script = $('script[src*="/myams.js"], script[src*="/myams-dev.js"], ' + 'script[src*="/myams-core.js"], script[src*="/myams-core-dev.js"], ' + 'script[src*="/myams-mini.js"], script[src*="/myams-mini-dev.js"]'),
      src = script.attr('src'),
      devmode = src ? src.indexOf('-dev.js') >= 0 : true; // testing mode

  return {
    bundle: src ? src.indexOf('-core') < 0 : true,
    // testing mode
    devmode: devmode,
    devext: devmode ? '-dev' : '',
    extext: devmode ? '' : '.min',
    baseURL: src ? src.substring(0, src.lastIndexOf('/') + 1) : '/'
  };
}
/**
 * Get base DOM elements
 */


function getDOM() {
  return {
    page: $('html'),
    root: $('body'),
    nav: $('nav'),
    main: $('#main'),
    leftPanel: $('#left-panel'),
    shortcuts: $('#shortcuts')
  };
}
/**
 * MyAMS default configuration
 *
 * @type {Object}:
 *      modules: array of loaded extension modules
 * 		ajaxNav: true if AJAX navigation is enabled
 * 	    enableFastclick: true is "smart-click" extension is to be activated on mobile devices
 * 		menuSpeed: menu speed, in miliseconds
 * 	    initPage: dotted name of MyAMS global init function
 * 	    initContent: dotted name of MyAMS content init function
 * 	    alertContainerCLass: class of MyAMS alerts container
 * 		safeMethods: HTTP methods which can be used without CSRF cookie verification
 * 		csrfCookieName: CSRF cookie name
 * 		csrfHeaderName: CSRF header name
 *      enableTooltips: global tooltips enable flag
 *      enableHtmlTooltips: allow HTML code in tooltips
 * 		warnOnFormChange: flag to specify if form changes should be warned
 * 		formChangeCallback: global form change callback
 * 		isMobile: boolean, true if device is detected as mobile
 * 	    device: string: 'mobile' or 'desktop'
 */


var isMobile = /iphone|ipad|ipod|android|blackberry|mini|windows\sce|palm/i.test(navigator.userAgent.toLowerCase()),
    config = {
  modules: [],
  ajaxNav: true,
  enableFastclick: true,
  useSVGIcons: window.FontAwesome !== undefined && FontAwesome.config.autoReplaceSvg === 'nest',
  menuSpeed: 235,
  initPage: 'MyAMS.core.initPage',
  initContent: 'MyAMS.core.initContent',
  clearContent: 'MyAMS.core.clearContent',
  useRegistry: true,
  alertsContainerClass: 'toast-wrapper',
  safeMethods: ['GET', 'HEAD', 'OPTIONS', 'TRACE'],
  csrfCookieName: 'csrf_token',
  csrfHeaderName: 'X-CSRF-Token',
  enableTooltips: true,
  enableHtmlTooltips: true,
  warnOnFormChange: true,
  formChangeCallback: null,
  isMobile: isMobile,
  device: isMobile ? 'mobile' : 'desktop'
},
    core = {
  getObject: getObject,
  getFunctionByName: getFunctionByName,
  executeFunctionByName: executeFunctionByName,
  getSource: getSource,
  getScript: getScript,
  getCSS: getCSS,
  getQueryVar: getQueryVar,
  generateId: generateId,
  generateUUID: generateUUID,
  switchIcon: switchIcon,
  initPage: initPage,
  initContent: initContent,
  clearContent: clearContent
};
var MyAMS = {
  $: $,
  env: getEnv($),
  config: config,
  core: core,
  registry: _ext_registry__WEBPACK_IMPORTED_MODULE_0__["registry"]
};
window.MyAMS = MyAMS;
/* harmony default export */ __webpack_exports__["default"] = (MyAMS);

/***/ }),

/***/ "./src/js/ext-registry.js":
/*!********************************!*\
  !*** ./src/js/ext-registry.js ***!
  \********************************/
/*! exports provided: registry */
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, "registry", function() { return registry; });
function _slicedToArray(arr, i) { return _arrayWithHoles(arr) || _iterableToArrayLimit(arr, i) || _unsupportedIterableToArray(arr, i) || _nonIterableRest(); }

function _nonIterableRest() { throw new TypeError("Invalid attempt to destructure non-iterable instance.\nIn order to be iterable, non-array objects must have a [Symbol.iterator]() method."); }

function _iterableToArrayLimit(arr, i) { if (typeof Symbol === "undefined" || !(Symbol.iterator in Object(arr))) return; var _arr = []; var _n = true; var _d = false; var _e = undefined; try { for (var _i = arr[Symbol.iterator](), _s; !(_n = (_s = _i.next()).done); _n = true) { _arr.push(_s.value); if (i && _arr.length === i) break; } } catch (err) { _d = true; _e = err; } finally { try { if (!_n && _i["return"] != null) _i["return"](); } finally { if (_d) throw _e; } } return _arr; }

function _arrayWithHoles(arr) { if (Array.isArray(arr)) return arr; }

function _typeof(obj) { "@babel/helpers - typeof"; if (typeof Symbol === "function" && typeof Symbol.iterator === "symbol") { _typeof = function _typeof(obj) { return typeof obj; }; } else { _typeof = function _typeof(obj) { return obj && typeof Symbol === "function" && obj.constructor === Symbol && obj !== Symbol.prototype ? "symbol" : typeof obj; }; } return _typeof(obj); }

function _createForOfIteratorHelper(o, allowArrayLike) { var it; if (typeof Symbol === "undefined" || o[Symbol.iterator] == null) { if (Array.isArray(o) || (it = _unsupportedIterableToArray(o)) || allowArrayLike && o && typeof o.length === "number") { if (it) o = it; var i = 0; var F = function F() {}; return { s: F, n: function n() { if (i >= o.length) return { done: true }; return { done: false, value: o[i++] }; }, e: function e(_e2) { throw _e2; }, f: F }; } throw new TypeError("Invalid attempt to iterate non-iterable instance.\nIn order to be iterable, non-array objects must have a [Symbol.iterator]() method."); } var normalCompletion = true, didErr = false, err; return { s: function s() { it = o[Symbol.iterator](); }, n: function n() { var step = it.next(); normalCompletion = step.done; return step; }, e: function e(_e3) { didErr = true; err = _e3; }, f: function f() { try { if (!normalCompletion && it.return != null) it.return(); } finally { if (didErr) throw err; } } }; }

function _unsupportedIterableToArray(o, minLen) { if (!o) return; if (typeof o === "string") return _arrayLikeToArray(o, minLen); var n = Object.prototype.toString.call(o).slice(8, -1); if (n === "Object" && o.constructor) n = o.constructor.name; if (n === "Map" || n === "Set") return Array.from(o); if (n === "Arguments" || /^(?:Ui|I)nt(?:8|16|32)(?:Clamped)?Array$/.test(n)) return _arrayLikeToArray(o, minLen); }

function _arrayLikeToArray(arr, len) { if (len == null || len > arr.length) len = arr.length; for (var i = 0, arr2 = new Array(len); i < len; i++) { arr2[i] = arr[i]; } return arr2; }

function _classCallCheck(instance, Constructor) { if (!(instance instanceof Constructor)) { throw new TypeError("Cannot call a class as a function"); } }

function _defineProperties(target, props) { for (var i = 0; i < props.length; i++) { var descriptor = props[i]; descriptor.enumerable = descriptor.enumerable || false; descriptor.configurable = true; if ("value" in descriptor) descriptor.writable = true; Object.defineProperty(target, descriptor.key, descriptor); } }

function _createClass(Constructor, protoProps, staticProps) { if (protoProps) _defineProperties(Constructor.prototype, protoProps); if (staticProps) _defineProperties(Constructor, staticProps); return Constructor; }

/* global $, MyAMS */

/**
 * MyAMS dynamic plug-ins loading management
 */

/**
 * Plug-ins loading order
 *  - initialize registry
 *  - initialize DOM data attributes
 *  - register all plug-ins from given DOM element
 *  - load all plug-ins from given DOM element
 *  - get list of disabled plug-ins into given DOM element
 *  - call callbacks for all enabled plug-ins
 *  - call callbacks for enabled "async" plug-ins
 */

/**
 * Base plug-in class
 */
var Plugin = /*#__PURE__*/function () {
  function Plugin(name) {
    var props = arguments.length > 1 && arguments[1] !== undefined ? arguments[1] : {};
    var loaded = arguments.length > 2 && arguments[2] !== undefined ? arguments[2] : false;

    _classCallCheck(this, Plugin);

    // plug-in name
    this.name = name; // plug-in source URL

    this.src = props.src; // plug-in associated CSS

    this.css = props.css; // plug-in callbacks

    this.callbacks = [];

    if (props.callback) {
      this.callbacks.push({
        callback: props.callback,
        context: props.context || 'body'
      });
    } // async plug-ins are loaded simultaneously; sync ones are loaded and called after...


    this.async = props.async === undefined ? true : props.async; // loaded flag

    this.loaded = loaded;
  }
  /**
   * Load plug-in from remote script
   *
   * @returns {Promise<void>|*}
   */


  _createClass(Plugin, [{
    key: "load",
    value: function load() {
      var _this = this;

      return new Promise(function (resolve, reject) {
        if (!_this.loaded) {
          var deferred = [];

          if (_this.src) {
            deferred.push(MyAMS.core.getScript(_this.src));
          }

          if (_this.css) {
            deferred.push(MyAMS.core.getCSS(_this.css, "".concat(_this.name, "_css")));
          }

          $.when.apply($, deferred).then(function () {
            _this.loaded = true;
            resolve();
          }, reject);
        } else {
          resolve();
        }
      });
    }
    /**
     * Run plug-in
     *
     * @param element: plug-in execution context
     */

  }, {
    key: "run",
    value: function run(element) {
      var results = [];

      var _iterator = _createForOfIteratorHelper(this.callbacks),
          _step;

      try {
        for (_iterator.s(); !(_step = _iterator.n()).done;) {
          var callback = _step.value;

          if (typeof callback.callback === 'string') {
            console.debug("Resolving callback ".concat(callback.callback));
            callback.callback = MyAMS.core.getFunctionByName(callback.callback) || callback.callback;
          }

          results.push(callback.callback(element, callback.context));
        }
      } catch (err) {
        _iterator.e(err);
      } finally {
        _iterator.f();
      }

      return Promise.all(results);
    }
  }]);

  return Plugin;
}();
/**
 * Plug-ins registry class
 */


var PluginsRegistry = /*#__PURE__*/function () {
  function PluginsRegistry() {
    _classCallCheck(this, PluginsRegistry);

    this.plugins = new Map();
  }
  /**
   * Register new plug-in
   *
   * @param props: plugin function caller, or object containing plug-in properties
   * @param name: plug-in unique name
   */


  _createClass(PluginsRegistry, [{
    key: "register",
    value: function register(props, name) {
      // check arguments
      if (!name && Object.prototype.hasOwnProperty.call(props, 'name')) {
        name = props.name;
      } // check for already registered plug-in


      var plugins = this.plugins;

      if (plugins.has(name)) {
        if (window.console) {
          console.debug && console.debug("Plug-in ".concat(name, " is already registered!"));
        }

        var plugin = plugins.get(name);
        var addContext = true;

        var _iterator2 = _createForOfIteratorHelper(plugin.callbacks),
            _step2;

        try {
          for (_iterator2.s(); !(_step2 = _iterator2.n()).done;) {
            var callback = _step2.value;

            if (callback.callback === props.callback && callback.context === props.context) {
              addContext = false;
              break;
            }
          }
        } catch (err) {
          _iterator2.e(err);
        } finally {
          _iterator2.f();
        }

        if (addContext) {
          plugin.callbacks.push({
            callback: props.callback,
            context: props.context || 'body'
          });
        }

        return plugin;
      } // register new plug-in


      if (typeof props === 'string') {
        // callable name
        props = MyAMS.core.getFunctionByName(props);
      }

      if (typeof props === 'function') {
        // callable object
        plugins.set(name, new Plugin(name, {
          callback: props
        }, true));
      } else if (_typeof(props) === 'object') {
        // plug-in properties object
        plugins.set(name, new Plugin(name, props, !(props.src || props.css)));
      } // check callback


      return plugins.get(name);
    }
    /**
     * Load plug-ins declared into DOM element
     *
     * @param element
     */

  }, {
    key: "load",
    value: function load(element) {
      var _this2 = this;

      // scan element for new plug-ins
      var asyncPlugins = [],
          syncPlugins = [];
      $('[data-ams-plugins]', element).each(function (idx, elt) {
        var source = $(elt),
            names = source.data('ams-plugins');
        var plugin, props;

        if (typeof names === 'string') {
          var _iterator3 = _createForOfIteratorHelper(names.split(/[\s,;]+/)),
              _step3;

          try {
            for (_iterator3.s(); !(_step3 = _iterator3.n()).done;) {
              var name = _step3.value;
              var lowerName = name.toLowerCase();
              props = {
                src: source.data("ams-plugin-".concat(lowerName, "-src")),
                css: source.data("ams-plugin-".concat(lowerName, "-css")),
                callback: source.data("ams-plugin-".concat(lowerName, "-callback")),
                context: source,
                async: source.data("ams-plugin-".concat(lowerName, "-async"))
              };
              plugin = _this2.register(props, name);

              if (!plugin.loaded) {
                if (props.async === false) {
                  syncPlugins.push(plugin.load());
                } else {
                  asyncPlugins.push(plugin.load());
                }
              }
            }
          } catch (err) {
            _iterator3.e(err);
          } finally {
            _iterator3.f();
          }
        } else {
          // JSON plug-in declaration
          var _iterator4 = _createForOfIteratorHelper($.isArray(names) ? names : [names]),
              _step4;

          try {
            for (_iterator4.s(); !(_step4 = _iterator4.n()).done;) {
              props = _step4.value;
              $.extend(props, {
                context: source
              });
              plugin = _this2.register(props);

              if (!plugin.loaded) {
                if (plugin.async === false) {
                  syncPlugins.push(plugin.load());
                } else {
                  asyncPlugins.push(plugin.load());
                }
              }
            }
          } catch (err) {
            _iterator4.e(err);
          } finally {
            _iterator4.f();
          }
        }
      }); // load plug-ins

      var result = $.when.apply($, asyncPlugins); // eslint-disable-next-line no-unused-vars

      for (var _i = 0, _syncPlugins = syncPlugins; _i < _syncPlugins.length; _i++) {
        var plugin = _syncPlugins[_i];
        result = result.done(function () {});
      }

      return result;
    }
    /**
     * Run registered plug-ins on given element
     *
     * @param element: source element
     * @param names: array list of plug-ins to activate, or all registered plug-ins if null
     */

  }, {
    key: "run",
    value: function run(element) {
      var names = arguments.length > 1 && arguments[1] !== undefined ? arguments[1] : null;
      // check for disabled plug-ins
      var disabled = new Set();
      $('[data-ams-plugins-disabled]', element).each(function (idx, elt) {
        var names = $(elt).data('ams-plugins-disabled').split(/[\s,;]+/);

        var _iterator5 = _createForOfIteratorHelper(names),
            _step5;

        try {
          for (_iterator5.s(); !(_step5 = _iterator5.n()).done;) {
            var name = _step5.value;
            disabled.add(name);
          }
        } catch (err) {
          _iterator5.e(err);
        } finally {
          _iterator5.f();
        }
      });
      var plugins = this.plugins;

      if (names) {
        // only run given plug-ins, EVEN DISABLED ONES
        var _iterator6 = _createForOfIteratorHelper(names),
            _step6;

        try {
          for (_iterator6.s(); !(_step6 = _iterator6.n()).done;) {
            var name = _step6.value;

            if (plugins.has(name)) {
              plugins.get(name).run(element);
            }
          }
        } catch (err) {
          _iterator6.e(err);
        } finally {
          _iterator6.f();
        }
      } else {
        // run all plug-ins, except disabled ones
        var _iterator7 = _createForOfIteratorHelper(plugins.entries()),
            _step7;

        try {
          for (_iterator7.s(); !(_step7 = _iterator7.n()).done;) {
            var _step7$value = _slicedToArray(_step7.value, 2),
                _name = _step7$value[0],
                plugin = _step7$value[1];

            if (disabled.has(_name)) {
              continue;
            }

            plugin.run(element);
          }
        } catch (err) {
          _iterator7.e(err);
        } finally {
          _iterator7.f();
        }
      }
    }
  }]);

  return PluginsRegistry;
}();

var plugins = new PluginsRegistry();
var registry = {
  /**
   * Plug-ins registry
   */
  plugins: plugins,

  /**
   * Initialize plug-ins registry from DOM
   *
   * @param element: source element to initialize from
   */
  initElement: function initElement() {
    var element = arguments.length > 0 && arguments[0] !== undefined ? arguments[0] : '#content';
    // populate data attributes
    MyAMS.registry.initData(element); // load plug-ins from given DOM element

    return plugins.load(element);
  },

  /**
   * Register a new plug-in through Javascript instead of HTML data attributes
   *
   * @param plugin: callable object, or object containing plug-in properties
   * @param name: plug-in name, used if @plugin is a function
   * @param callback: callback function which can be called after plug-in registration
   */
  register: function register(plugin, name, callback) {
    return plugins.register(plugin, name, callback);
  },

  /**
   * Data attributes initializer
   *
   * This function converts a single "data-ams-data" attribute into a set of several "data-*"
   * attributes.
   * This can be used into HTML templates engines which don't allow to create dynamic attributes
   * easilly.
   *
   * @param element: parent element
   */
  initData: function initData(element) {
    $('[data-ams-data]', element).each(function (idx, elt) {
      var $elt = $(elt),
          data = $elt.data('ams-data');

      if (data) {
        for (var name in data) {
          if (!Object.prototype.hasOwnProperty.call(data, name)) {
            continue;
          }

          var elementData = data[name];

          if (typeof elementData !== 'string') {
            elementData = JSON.stringify(elementData);
          }

          $elt.attr("data-".concat(name), elementData);
        }
      }

      $elt.removeAttr('data-ams-data');
    });
  },

  /**
   * Run registered plug-ins on given element
   *
   * @param element: DOM element
   * @param names: names of plug-in to run on given element; all if null
   */
  run: function run(element) {
    var names = arguments.length > 1 && arguments[1] !== undefined ? arguments[1] : null;
    return plugins.run(element, names);
  }
};

/***/ }),

/***/ "./src/js/ext-require.js":
/*!*******************************!*\
  !*** ./src/js/ext-require.js ***!
  \*******************************/
/*! exports provided: default */
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, "default", function() { return myams_require; });
function _slicedToArray(arr, i) { return _arrayWithHoles(arr) || _iterableToArrayLimit(arr, i) || _unsupportedIterableToArray(arr, i) || _nonIterableRest(); }

function _nonIterableRest() { throw new TypeError("Invalid attempt to destructure non-iterable instance.\nIn order to be iterable, non-array objects must have a [Symbol.iterator]() method."); }

function _iterableToArrayLimit(arr, i) { if (typeof Symbol === "undefined" || !(Symbol.iterator in Object(arr))) return; var _arr = []; var _n = true; var _d = false; var _e = undefined; try { for (var _i = arr[Symbol.iterator](), _s; !(_n = (_s = _i.next()).done); _n = true) { _arr.push(_s.value); if (i && _arr.length === i) break; } } catch (err) { _d = true; _e = err; } finally { try { if (!_n && _i["return"] != null) _i["return"](); } finally { if (_d) throw _e; } } return _arr; }

function _arrayWithHoles(arr) { if (Array.isArray(arr)) return arr; }

function _createForOfIteratorHelper(o, allowArrayLike) { var it; if (typeof Symbol === "undefined" || o[Symbol.iterator] == null) { if (Array.isArray(o) || (it = _unsupportedIterableToArray(o)) || allowArrayLike && o && typeof o.length === "number") { if (it) o = it; var i = 0; var F = function F() {}; return { s: F, n: function n() { if (i >= o.length) return { done: true }; return { done: false, value: o[i++] }; }, e: function e(_e2) { throw _e2; }, f: F }; } throw new TypeError("Invalid attempt to iterate non-iterable instance.\nIn order to be iterable, non-array objects must have a [Symbol.iterator]() method."); } var normalCompletion = true, didErr = false, err; return { s: function s() { it = o[Symbol.iterator](); }, n: function n() { var step = it.next(); normalCompletion = step.done; return step; }, e: function e(_e3) { didErr = true; err = _e3; }, f: function f() { try { if (!normalCompletion && it.return != null) it.return(); } finally { if (didErr) throw err; } } }; }

function _unsupportedIterableToArray(o, minLen) { if (!o) return; if (typeof o === "string") return _arrayLikeToArray(o, minLen); var n = Object.prototype.toString.call(o).slice(8, -1); if (n === "Object" && o.constructor) n = o.constructor.name; if (n === "Map" || n === "Set") return Array.from(o); if (n === "Arguments" || /^(?:Ui|I)nt(?:8|16|32)(?:Clamped)?Array$/.test(n)) return _arrayLikeToArray(o, minLen); }

function _arrayLikeToArray(arr, len) { if (len == null || len > arr.length) len = arr.length; for (var i = 0, arr2 = new Array(len); i < len; i++) { arr2[i] = arr[i]; } return arr2; }

/* global MyAMS */

/**
 * MyAMS dynamic module loader
 */
var $ = MyAMS.$;

function getModule(module) {
  var moduleSrc;

  if (module.startsWith('http://') || module.startsWith('https://')) {
    moduleSrc = module;
  } else if (module.endsWith('.js')) {
    // custom module with relative path
    moduleSrc = module;
  } else {
    // standard MyAMS module
    moduleSrc = "".concat(MyAMS.env.baseURL, "mod-").concat(module).concat(MyAMS.env.devext, ".js");
  }

  return MyAMS.core.getScript(moduleSrc, {
    async: true
  }, console.error);
}
/**
 * Dynamic loading of MyAMS modules
 *
 * @param modules: single module name, or array of modules names
 * @returns Promise
 */


function myams_require() {
  for (var _len = arguments.length, modules = new Array(_len), _key = 0; _key < _len; _key++) {
    modules[_key] = arguments[_key];
  }

  return new Promise(function (resolve, reject) {
    var names = [],
        deferred = [],
        loaded = MyAMS.config.modules;

    var _iterator = _createForOfIteratorHelper(modules),
        _step;

    try {
      for (_iterator.s(); !(_step = _iterator.n()).done;) {
        var module = _step.value;

        if (typeof module === 'string') {
          if (loaded.indexOf(module) < 0) {
            names.push(module);
            deferred.push(getModule(module));
          }
        } else if ($.isArray(module)) {
          // strings array
          var _iterator3 = _createForOfIteratorHelper(module),
              _step3;

          try {
            for (_iterator3.s(); !(_step3 = _iterator3.n()).done;) {
              var name = _step3.value;

              if (loaded.indexOf(name) < 0) {
                names.push(name);
                deferred.push(getModule(name));
              }
            }
          } catch (err) {
            _iterator3.e(err);
          } finally {
            _iterator3.f();
          }
        } else {
          // object
          for (var _i = 0, _Object$entries = Object.entries(module); _i < _Object$entries.length; _i++) {
            var _Object$entries$_i = _slicedToArray(_Object$entries[_i], 2),
                _name = _Object$entries$_i[0],
                src = _Object$entries$_i[1];

            if (loaded.indexOf(_name) < 0) {
              names.push(_name);
              deferred.push(getModule(src));
            }
          }
        }
      }
    } catch (err) {
      _iterator.e(err);
    } finally {
      _iterator.f();
    }

    $.when.apply($, deferred).then(function () {
      var _iterator2 = _createForOfIteratorHelper(names),
          _step2;

      try {
        for (_iterator2.s(); !(_step2 = _iterator2.n()).done;) {
          var moduleName = _step2.value;

          if (loaded.indexOf(moduleName) < 0) {
            loaded.push(moduleName);
            MyAMS.core.executeFunctionByName("MyAMS.".concat(moduleName, ".init"));
          }
        }
      } catch (err) {
        _iterator2.e(err);
      } finally {
        _iterator2.f();
      }

      resolve();
    }, function () {
      reject("Can't load requested modules (".concat(names, ")!"));
    });
  });
}

/***/ }),

/***/ "./src/js/myams-core.js":
/*!******************************!*\
  !*** ./src/js/myams-core.js ***!
  \******************************/
/*! no exports provided */
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony import */ var _ext_base__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! ./ext-base */ "./src/js/ext-base.js");
/* harmony import */ var _ext_require__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! ./ext-require */ "./src/js/ext-require.js");
/**
 * MyAMS core features
 *
 * This script is used to build MyAMS mini-core-package.
 *
 * This package only includes MyAMS core features, but not CSS or external modules
 * which can be loaded using MyAMS.require function.
 */


_ext_base__WEBPACK_IMPORTED_MODULE_0__["default"].$.extend(_ext_base__WEBPACK_IMPORTED_MODULE_0__["default"], {
  require: _ext_require__WEBPACK_IMPORTED_MODULE_1__["default"]
});
var html = _ext_base__WEBPACK_IMPORTED_MODULE_0__["default"].$('html');

if (html.data('ams-init') !== false) {
  Object(_ext_base__WEBPACK_IMPORTED_MODULE_0__["init"])(_ext_base__WEBPACK_IMPORTED_MODULE_0__["default"].$);
}
/** Version: 1.5.1  */

/***/ }),

/***/ "jquery":
/*!*************************!*\
  !*** external "jquery" ***!
  \*************************/
/*! no static exports found */
/***/ (function(module, exports) {

module.exports = jquery;

/***/ })

/******/ });
//# sourceMappingURL=myams-core-dev.js.map