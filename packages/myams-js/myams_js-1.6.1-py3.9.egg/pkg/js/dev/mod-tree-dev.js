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
    global.modTree = mod.exports;
  }
})(typeof globalThis !== "undefined" ? globalThis : typeof self !== "undefined" ? self : this, function (_exports) {
  "use strict";

  Object.defineProperty(_exports, "__esModule", {
    value: true
  });
  _exports.tree = void 0;

  /* global MyAMS */

  /**
   * MyAMS tree management
   */
  var $ = MyAMS.$;
  var tree = {};
  /**
   * Global module initialization
   */

  _exports.tree = tree;

  if (window.MyAMS) {
    if (MyAMS.env.bundle) {
      MyAMS.config.modules.push('tree');
    } else {
      MyAMS.tree = tree;
      console.debug("MyAMS: tree module loaded...");
    }
  }
});
//# sourceMappingURL=mod-tree-dev.js.map
