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
    global.modHelpers = mod.exports;
  }
})(typeof globalThis !== "undefined" ? globalThis : typeof self !== "undefined" ? self : this, function (_exports) {
  "use strict";

  Object.defineProperty(_exports, "__esModule", {
    value: true
  });
  _exports.helpers = void 0;

  /* global MyAMS */

  /**
   * MyAMS generic helpers
   */
  var $ = MyAMS.$;
  var helpers = {
    /**
     * Click handler used to clear input
     */
    clearValue: function clearValue(evt) {
      var target = $(evt.currentTarget).data('target');

      if (target) {
        $(target).val(null);
      }
    },

    /**
     * Click handler used to clear datetime input
     */
    clearDatetimeValue: function clearDatetimeValue(evt) {
      var target = $(evt.currentTarget).data('target'),
          picker = $(target).data('datetimepicker');

      if (picker) {
        picker.date(null);
      }
    },

    /**
     * Refresh a DOM element with content provided in
     * the <code>options</code> object.
     *
     * @param form: optional parent element
     * @param options: element properties:
     *   - object_id: ID of the refreshed element
     *   - content: new element content
     */
    refreshElement: function refreshElement(form, options) {
      return new Promise(function (resolve, reject) {
        var element = $("[id=\"".concat(options.object_id, "\"]"));
        MyAMS.core.executeFunctionByName(MyAMS.config.clearContent, document, element).then(function () {
          element.replaceWith($(options.content));
          element = $("[id=\"".concat(options.object_id, "\"]"));
          MyAMS.core.executeFunctionByName(MyAMS.config.initContent, document, element).then(function () {
            resolve(element);
          }, reject);
        }, reject);
      });
    },

    /**
     * Refresh a form widget with content provided in
     * the <code>options</code> object
     *
     * @param form: optional parent form
     * @param options: updated widget properties:
     *   - widget_id: ID of the refreshed widget
     *   - content: new element content
     */
    refreshWidget: function refreshWidget(form, options) {
      return new Promise(function (resolve, reject) {
        var widget = $("[id=\"".concat(options.widget_id, "\"]")),
            group = widget.parents('.widget-group');
        MyAMS.core.executeFunctionByName(MyAMS.config.clearContent, document, group).then(function () {
          group.replaceWith($(options.content));
          widget = $("[id=\"".concat(options.widget_id, "\"]"));
          group = widget.parents('.widget-group');
          MyAMS.core.executeFunctionByName(MyAMS.config.initContent, document, group).then(function () {
            resolve(widget);
          }, reject);
        }, reject);
      });
    },

    /**
     * Add new row to table
     *
     * @param form: optional parent form
     * @param options: added row properties:
     *  - content: new row content
     */
    addTableRow: function addTableRow(form, options) {
      return new Promise(function (resolve, reject) {
        var selector = "table[id=\"".concat(options.table_id, "\"]"),
            table = $(selector),
            dtTable = table.DataTable();
        var newRow;

        if (options.data) {
          dtTable.rows.add(options.data).draw();
          newRow = $("tr[id=\"".concat(options.row_id, "\"]"), table);
          resolve(newRow);
        } else {
          newRow = $(options.content);
          dtTable.rows.add(newRow).draw();
          MyAMS.core.executeFunctionByName(MyAMS.config.initContent, document, newRow).then(function () {
            resolve(newRow);
          }, reject);
        }
      });
    },

    /**
     * Refresh a table row with content provided in
     * the <code>options</code> object
     *
     * @param form: optional parent form
     * @param options: updated row properties:
     *   - row_id: ID of the refreshed row
     *   - content: new row content
     */
    refreshTableRow: function refreshTableRow(form, options) {
      return new Promise(function (resolve, reject) {
        var selector = "tr[id=\"".concat(options.row_id, "\"]"),
            row = $(selector),
            table = row.parents('table').first(),
            dtTable = table.DataTable();

        if (options.data) {
          dtTable.row(selector).data(options.data);
          resolve(row);
        } else {
          var newRow = $(options.content);
          row.replaceWith(newRow);
          MyAMS.core.executeFunctionByName(MyAMS.config.initContent, document, newRow).then(function () {
            resolve(newRow);
          }, reject);
        }
      });
    },

    /**
     * Refresh a single image with content provided in
     * the <code>options</code> object.
     *
     * @param form: optional parent element
     * @param options: image properties:
     *   - image_id: ID of the refreshed image
     *   - src: new image source URL
     */
    refreshImage: function refreshImage(form, options) {
      var image = $("[id=\"".concat(options.image_id, "\"]"));
      image.attr('src', options.src);
    },

    /**
     * Move given element to the end of it's parent
     *
     * @param element: the element to be moved
     * @returns {*}
     */
    moveElementToParentEnd: function moveElementToParentEnd(element) {
      var parent = element.parent();
      return element.detach().appendTo(parent);
    },

    /**
     * Toggle dropdown associated with given event target
     *
     * @param evt: source event
     */
    hideDropdown: function hideDropdown(evt) {
      $(evt.target).closest('.dropdown-menu').dropdown('hide');
    }
  };
  /**
   * Global module initialization
   */

  _exports.helpers = helpers;

  if (window.MyAMS) {
    if (MyAMS.env.bundle) {
      MyAMS.config.modules.push('helpers');
    } else {
      MyAMS.helpers = helpers;
      console.debug("MyAMS: helpers module loaded...");
    }
  }
});
//# sourceMappingURL=mod-helpers-dev.js.map
