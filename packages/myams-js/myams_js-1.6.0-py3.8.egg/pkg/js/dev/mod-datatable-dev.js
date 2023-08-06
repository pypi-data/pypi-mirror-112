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
    global.modDatatable = mod.exports;
  }
})(typeof globalThis !== "undefined" ? globalThis : typeof self !== "undefined" ? self : this, function (_exports) {
  "use strict";

  Object.defineProperty(_exports, "__esModule", {
    value: true
  });
  _exports.datatable = void 0;

  /* global MyAMS */

  /**
   * MyAMS datatables management
   */
  var $ = MyAMS.$;
  var datatable = {};
  /**
   * Global module initialization
   */

  _exports.datatable = datatable;

  if (window.MyAMS) {
    if (MyAMS.env.bundle) {
      MyAMS.config.modules.push('datatable');
    } else {
      MyAMS.datatable = datatable;
      console.debug("MyAMS: datatable module loaded...");
    }
  }
});
//# sourceMappingURL=mod-datatable-dev.js.map
