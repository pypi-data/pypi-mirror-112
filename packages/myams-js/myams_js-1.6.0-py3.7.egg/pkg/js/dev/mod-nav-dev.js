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
    global.modNav = mod.exports;
  }
})(typeof globalThis !== "undefined" ? globalThis : typeof self !== "undefined" ? self : this, function (_exports) {
  "use strict";

  Object.defineProperty(_exports, "__esModule", {
    value: true
  });
  _exports.linkClickHandler = linkClickHandler;
  _exports.nav = _exports.NavigationMenu = void 0;

  function _slicedToArray(arr, i) { return _arrayWithHoles(arr) || _iterableToArrayLimit(arr, i) || _unsupportedIterableToArray(arr, i) || _nonIterableRest(); }

  function _nonIterableRest() { throw new TypeError("Invalid attempt to destructure non-iterable instance.\nIn order to be iterable, non-array objects must have a [Symbol.iterator]() method."); }

  function _iterableToArrayLimit(arr, i) { if (typeof Symbol === "undefined" || !(Symbol.iterator in Object(arr))) return; var _arr = []; var _n = true; var _d = false; var _e = undefined; try { for (var _i = arr[Symbol.iterator](), _s; !(_n = (_s = _i.next()).done); _n = true) { _arr.push(_s.value); if (i && _arr.length === i) break; } } catch (err) { _d = true; _e = err; } finally { try { if (!_n && _i["return"] != null) _i["return"](); } finally { if (_d) throw _e; } } return _arr; }

  function _arrayWithHoles(arr) { if (Array.isArray(arr)) return arr; }

  function _createForOfIteratorHelper(o, allowArrayLike) { var it; if (typeof Symbol === "undefined" || o[Symbol.iterator] == null) { if (Array.isArray(o) || (it = _unsupportedIterableToArray(o)) || allowArrayLike && o && typeof o.length === "number") { if (it) o = it; var i = 0; var F = function F() {}; return { s: F, n: function n() { if (i >= o.length) return { done: true }; return { done: false, value: o[i++] }; }, e: function e(_e2) { throw _e2; }, f: F }; } throw new TypeError("Invalid attempt to iterate non-iterable instance.\nIn order to be iterable, non-array objects must have a [Symbol.iterator]() method."); } var normalCompletion = true, didErr = false, err; return { s: function s() { it = o[Symbol.iterator](); }, n: function n() { var step = it.next(); normalCompletion = step.done; return step; }, e: function e(_e3) { didErr = true; err = _e3; }, f: function f() { try { if (!normalCompletion && it.return != null) it.return(); } finally { if (didErr) throw err; } } }; }

  function _unsupportedIterableToArray(o, minLen) { if (!o) return; if (typeof o === "string") return _arrayLikeToArray(o, minLen); var n = Object.prototype.toString.call(o).slice(8, -1); if (n === "Object" && o.constructor) n = o.constructor.name; if (n === "Map" || n === "Set") return Array.from(o); if (n === "Arguments" || /^(?:Ui|I)nt(?:8|16|32)(?:Clamped)?Array$/.test(n)) return _arrayLikeToArray(o, minLen); }

  function _arrayLikeToArray(arr, len) { if (len == null || len > arr.length) len = arr.length; for (var i = 0, arr2 = new Array(len); i < len; i++) { arr2[i] = arr[i]; } return arr2; }

  function _classCallCheck(instance, Constructor) { if (!(instance instanceof Constructor)) { throw new TypeError("Cannot call a class as a function"); } }

  function _defineProperties(target, props) { for (var i = 0; i < props.length; i++) { var descriptor = props[i]; descriptor.enumerable = descriptor.enumerable || false; descriptor.configurable = true; if ("value" in descriptor) descriptor.writable = true; Object.defineProperty(target, descriptor.key, descriptor); } }

  function _createClass(Constructor, protoProps, staticProps) { if (protoProps) _defineProperties(Constructor.prototype, protoProps); if (staticProps) _defineProperties(Constructor, staticProps); return Constructor; }

  /* global MyAMS, FontAwesome, Hammer */

  /**
   * MyAMS navigation module
   */
  var $ = MyAMS.$;
  /**
   * Dynamic navigation menu class
   */

  var MenuHeader = /*#__PURE__*/function () {
    function MenuHeader(props) {
      _classCallCheck(this, MenuHeader);

      this.props = props;
    }

    _createClass(MenuHeader, [{
      key: "render",
      value: function render() {
        return $('<li class="header"></li>').text(this.props.header || '');
      }
    }]);

    return MenuHeader;
  }();

  var MenuDivider = /*#__PURE__*/function () {
    function MenuDivider() {
      _classCallCheck(this, MenuDivider);
    }

    _createClass(MenuDivider, [{
      key: "render",
      value: function render() {
        return $('<li class="divider"></li>');
      }
    }]);

    return MenuDivider;
  }();

  var Menu = /*#__PURE__*/function () {
    function Menu(items) {
      _classCallCheck(this, Menu);

      this.items = items;
    }

    _createClass(Menu, [{
      key: "render",
      value: function render() {
        var menu = $('<div></div>');

        var _iterator = _createForOfIteratorHelper(this.items),
            _step;

        try {
          for (_iterator.s(); !(_step = _iterator.n()).done;) {
            var item = _step.value;

            if (item.label) {
              var props = $('<li></li>'),
                  link = $('<a></a>').attr('href', item.href || '#').attr('title', item.label);

              for (var _i = 0, _Object$entries = Object.entries(item.attrs || {}); _i < _Object$entries.length; _i++) {
                var _Object$entries$_i = _slicedToArray(_Object$entries[_i], 2),
                    key = _Object$entries$_i[0],
                    val = _Object$entries$_i[1];

                link.attr(key, val);
              }

              if (item.icon) {
                $('<i class="fa-lg fa-fw mr-1"></i>').addClass(item.icon).appendTo(link);
              }

              $('<span class="menu-item-parent"></span>').text(item.label).appendTo(link);

              if (item.badge) {
                $('<span class="badge ml-1 mr-3 float-right"></span>').addClass("bg-".concat(item.badge.status)).text(item.badge.value).appendTo(link);
              }

              link.appendTo(props);

              if (item.items) {
                $('<ul></ul>').append(new Menu(item.items).render()).appendTo(props);
              }

              props.appendTo(menu);
            } else {
              new MenuDivider().render().appendTo(menu);
            }
          }
        } catch (err) {
          _iterator.e(err);
        } finally {
          _iterator.f();
        }

        return menu.children();
      }
    }]);

    return Menu;
  }();

  var NavigationMenu = /*#__PURE__*/function () {
    function NavigationMenu(menus, parent, settings) {
      _classCallCheck(this, NavigationMenu);

      this.menus = menus;
      this.parent = parent;
      this.settings = settings;
    }

    _createClass(NavigationMenu, [{
      key: "getMenus",
      value: function getMenus() {
        var nav = $('<ul></ul>');

        var _iterator2 = _createForOfIteratorHelper(this.menus),
            _step2;

        try {
          for (_iterator2.s(); !(_step2 = _iterator2.n()).done;) {
            var props = _step2.value;

            if (props.header !== undefined) {
              nav.append(new MenuHeader(props).render());
            }

            nav.append(new Menu(props.items).render());
          }
        } catch (err) {
          _iterator2.e(err);
        } finally {
          _iterator2.f();
        }

        return nav;
      }
    }, {
      key: "render",
      value: function render() {
        var menus = this.getMenus();
        this.init(menus);
        this.parent.append(menus);
      }
    }, {
      key: "init",
      value: function init(menus) {
        var settings = this.settings; // add mark to menus with childrens

        menus.find('li').each(function (idx, elt) {
          var menuItem = $(elt);

          if (menuItem.find('ul').length > 0) {
            var firstLink = menuItem.find('a:first'); // add multi-level sign next to link

            var sign = $("<b class=\"collapse-sign\">".concat(settings.closedSign, "</b>"));
            sign.on('click', function (evt) {
              evt.preventDefault();
            });
            firstLink.append(sign); // avoid jumping to top of page when href is a #

            if (firstLink.attr('href') === '#') {
              firstLink.click(function () {
                return false;
              });
            }
          }
        }); // open active level

        menus.find('li.active').each(function (idx, elt) {
          var activeParent = $(elt).parents('ul'),
              activeItem = activeParent.parent('li');
          activeParent.slideDown(settings.speed);
          activeItem.find('b:first').html(settings.openedSign);
          activeItem.addClass('open');
        }); // handle click event

        menus.find("li a").on('click', function (evt) {
          var link = $(evt.currentTarget);

          if (link.hasClass('active')) {
            return;
          }

          link.parents('li').removeClass('active');
          var href = link.attr('href').replace(/^#/, ''),
              parentUL = link.parent().find("ul");

          if (settings.accordion) {
            var parents = link.parent().parents("ul"),
                visibleMenus = menus.find("ul:visible");
            visibleMenus.each(function (visibleIndex, visibleElt) {
              var close = true;
              parents.each(function (parentIndex, parentElt) {
                if (parentElt === visibleElt) {
                  close = false;
                  return false;
                }
              });

              if (close && parentUL !== visibleElt) {
                var visibleItem = $(visibleElt);

                if (href || !visibleItem.hasClass('active')) {
                  visibleItem.slideUp(settings.speed, function () {
                    visibleItem.parent("li").removeClass('open').find("b:first").delay(settings.speed).html(settings.closedSign);
                  });
                }
              }
            });
          }

          var firstUL = link.parent().find("ul:first");

          if (!href && firstUL.is(":visible") && !firstUL.hasClass("active")) {
            firstUL.slideUp(settings.speed, function () {
              link.parent("li").removeClass("open").find("b:first").delay(settings.speed).html(settings.closedSign);
            });
          } else {
            firstUL.slideDown(settings.speed, function () {
              link.parent("li").addClass("open").find("b:first").delay(settings.speed).html(settings.openedSign);
            });
          }
        });
      }
    }]);

    return NavigationMenu;
  }();

  _exports.NavigationMenu = NavigationMenu;
  var _initialized = false,
      _hammer = null;
  /**
   * Main navigation module
   */

  function _openPage(href) {
    if (location && href.startsWith('#')) {
      if (href !== location.hash) {
        location.hash = href;
      }
    } else {
      if (location.toString() === href) {
        location.reload();
      } else {
        window.location = href;
      }
    }
  }
  /**
   * Main link click event handler
   *
   * @param evt
   */


  function linkClickHandler(evt) {
    return new Promise(function (resolve, reject) {
      var link = $(evt.currentTarget),
          handlers = link.data('ams-disabled-handlers');

      if (handlers === true || handlers === 'click' || handlers === 'all') {
        return;
      }

      var href = link.attr('href') || link.data('ams-url');

      if (!href || href.startsWith('javascript:') || link.attr('target') || link.data('ams-context-menu') === true) {
        return;
      }

      evt.preventDefault();
      evt.stopPropagation();
      var url, target, params;

      if (href.indexOf('?') >= 0) {
        url = href.split('?');
        target = url[0];
        params = url[1].unserialize();
      } else {
        target = href;
        params = undefined;
      }

      var hrefGetter = MyAMS.core.getFunctionByName(target);

      if (typeof hrefGetter === 'function') {
        href = hrefGetter(link, params);
      }

      if (typeof href === 'function') {
        resolve(href(link, params));
      } else {
        // Standard AJAX or browser URL call
        // Convert %23 characters to #
        href = href.replace(/%23/, '#');

        if (evt.ctrlKey) {
          window.open && window.open(href);
          resolve();
        } else {
          var linkTarget = link.data('ams-target') || link.attr('target');

          if (linkTarget) {
            if (linkTarget === '_blank') {
              window.open && window.open(href);
              resolve();
            } else {
              if (MyAMS.form) {
                MyAMS.form.confirmChangedForm().then(function (result) {
                  if (result !== 'success') {
                    return;
                  }

                  MyAMS.skin && MyAMS.skin.loadURL(href, linkTarget, link.data('ams-link-options'), link.data('ams-link-callback')).then(resolve, reject);
                });
              } else {
                MyAMS.skin && MyAMS.skin.loadURL(href, linkTarget, link.data('ams-link-options'), link.data('ams-link-callback')).then(resolve, reject);
              }
            }
          } else {
            if (MyAMS.form) {
              MyAMS.form.confirmChangedForm().then(function (result) {
                if (result !== 'success') {
                  return;
                }

                _openPage(href);
              }).then(resolve);
            } else {
              _openPage(href);

              resolve();
            }
          }
        }
      }
    });
  }

  var nav = {
    /**
     * initialize navigation through data attributes
     */
    init: function init() {
      if (_initialized) {
        return;
      }

      _initialized = true;
      $.fn.extend({
        navigationMenu: function navigationMenu(options) {
          var _this = this;

          if (this.length === 0) {
            return;
          }

          var data = this.data();
          var defaults = {
            accordion: data.amsMenuAccordion !== false,
            speed: 200
          };

          if (MyAMS.config.useSVGIcons) {
            var downIcon = FontAwesome.findIconDefinition({
              iconName: 'angle-down'
            }),
                upIcon = FontAwesome.findIconDefinition({
              iconName: 'angle-up'
            });
            $.extend(defaults, {
              closedSign: "<em data-fa-i2svg>".concat(FontAwesome.icon(downIcon).html, "</em>"),
              openedSign: "<em data-fa-i2svg>".concat(FontAwesome.icon(upIcon).html, "</em>")
            });
          } else {
            $.extend(defaults, {
              closedSign: '<em class="fa fa-angle-down"></em>',
              openedSign: '<em class="fa fa-angle-up"></em>'
            });
          }

          var settings = $.extend({}, defaults, options);

          if (data.amsMenuConfig) {
            MyAMS.require('ajax', 'skin').then(function () {
              MyAMS.ajax.get(data.amsMenuConfig).then(function (result) {
                var menuFactory = MyAMS.core.getObject(data.amsMenuFactory) || NavigationMenu;
                new menuFactory(result, $(_this), settings).render();
                MyAMS.skin.checkURL();
              });
            });
          } else {
            // static menus
            var menus = $('ul', this);
            new NavigationMenu(null, $(this), settings).init(menus);
          }
        }
      });

      if (MyAMS.config.ajaxNav) {
        // Disable clicks on # hrefs
        $(document).on('click', 'a[href="#"]', function (evt) {
          evt.preventDefault();
        }); // Activate clicks

        $(document).on('click', 'a[href!="#"]:not([data-toggle]), [data-ams-url]:not([data-toggle])', function (evt) {
          // check for specific click handler
          var handler = $(evt).data('ams-click-handler');

          if (handler) {
            return;
          }

          return linkClickHandler(evt);
        }); // Blank target clicks

        $(document).on('click', 'a[target="_blank"]', function (evt) {
          evt.preventDefault();
          var target = $(evt.currentTarget);
          window.open && window.open(target.attr('href'));
          MyAMS.stats && MyAMS.stats.logEvent(target.data('ams-stats-category') || 'Navigation', target.data('ams-stats-action') || 'External', target.data('ams-stats-label') || target.attr('href'));
        }); // Top target clicks

        $(document).on('click', 'a[target="_top"]', function (evt) {
          evt.preventDefault();
          MyAMS.form && MyAMS.form.confirmChangedForm().then(function (result) {
            if (result !== 'success') {
              return;
            }

            window.location = $(evt.currentTarget).attr('href');
          });
        }); // Disable clicks on disabled tabs

        $(document).on("click", '.nav-tabs a[data-toggle=tab]', function (evt) {
          if ($(evt.currentTarget).parent('li').hasClass("disabled")) {
            evt.stopPropagation();
            evt.preventDefault();
            return false;
          }
        }); // Enable tabs dynamic loading

        $(document).on('show.bs.tab', function (evt) {
          var link = $(evt.target);

          if (link.exists() && link.get(0).tagName !== 'A') {
            link = $('a[href]', link);
          }

          var data = link.data();

          if (data && data.amsUrl) {
            if (data.amsTabLoaded) {
              return;
            }

            link.append('<i class="fa fa-spin fa-cog ml-1"></i>');

            MyAMS.require('skin').then(function () {
              MyAMS.skin.loadURL(data.amsUrl, link.attr('href')).then(function () {
                if (data.amsTabLoadOnce) {
                  data.amsTabLoaded = true;
                }

                $('i', link).remove();
              }, function () {
                $('i', link).remove();
              });
            });
          }
        });

        if (!MyAMS.config.isMobile) {
          MyAMS.dom.root.addClass('desktop-detected');
        } else {
          MyAMS.dom.root.addClass('mobile-detected');

          MyAMS.require('ajax').then(function () {
            if (MyAMS.config.enableFastclick) {
              MyAMS.ajax.check($.fn.noClickDelay, "".concat(MyAMS.env.baseURL, "../ext/js-smartclick").concat(MyAMS.env.extext, ".js")).then(function () {
                $('a', MyAMS.dom.nav).noClickDelay();
                $('a', '#hide-menu').noClickDelay();
              });
            }

            if (MyAMS.dom.root.exists()) {
              MyAMS.ajax.check(window.Hammer, "".concat(MyAMS.env.baseURL, "../ext/hammer").concat(MyAMS.env.extext, ".js")).then(function () {
                _hammer = new Hammer.Manager(MyAMS.dom.root.get(0));

                _hammer.add(new Hammer.Pan({
                  direction: Hammer.DIRECTION_HORIZONTAL,
                  threshold: 200
                }));

                _hammer.on('panright', function () {
                  if (!MyAMS.dom.root.hasClass('hidden-menu')) {
                    MyAMS.nav.switchMenu();
                  }
                });

                _hammer.on('panleft', function () {
                  if (MyAMS.dom.root.hasClass('hidden-menu')) {
                    MyAMS.nav.switchMenu();
                  }
                });
              });
            }
          });
        }
      }

      nav.restoreState();
    },
    initElement: function initElement(element) {
      $('nav', element).navigationMenu({
        speed: MyAMS.config.menuSpeed
      });
    },

    /**
     * Display current active menu
     *
    	 * @param menu: current active menu
     */
    setActiveMenu: function setActiveMenu(menu) {
      var nav = MyAMS.dom.nav;
      $('.active', nav).removeClass('active');
      menu.addClass('open').addClass('active');
      menu.parents('li').addClass('open active').children('ul').addClass('active').show();
      menu.parents('li:first').removeClass('open');
      menu.parents('ul').addClass(menu.attr('href').replace(/^#/, '') ? 'active' : '').show();

      if (menu.exists()) {
        var scroll = nav.scrollTop(),
            position = $(menu).parents('li:last').position();

        if (position.top < scroll) {
          nav.scrollTop(position.top);
        } else if (position.top > nav.height() + scroll) {
          nav.scrollTop(position.top);
        }
      }
    },

    /**
     * Internal breadcrumbs drawing function
     *
     * @private
     */
    drawBreadcrumbs: function drawBreadcrumbs() {
      var crumb = $('ol.breadcrumb', '#ribbon');
      $('li', crumb).not('.persistent').remove();

      if (!$('li', crumb).exists()) {
        var template = "<li class=\"breadcrumb-item\">\n\t\t\t\t\t<a class=\"p-r-1\" href=\"".concat($('a[href!="#"]:first', MyAMS.dom.nav).attr('href'), "\">\n\t\t\t\t\t\t").concat(MyAMS.i18n.HOME, "\n\t\t\t\t\t</a>\n\t\t\t\t</li>");
        crumb.append($(template));
      }

      $('li.active >a', MyAMS.dom.nav).each(function (idx, elt) {
        var menu = $(elt),
            text = $.trim(menu.clone().children('.badge').remove().end().text()),
            href = menu.attr('href'),
            item = $('<li class="breadcrumb-item"></li>').append(href.replace(/^#/, '') ? $('<a></a>').html(text).attr('href', href) : text);
        crumb.append(item);
      });
    },

    /**
     * Click handler for navigation menu "minify" button
     *
     * @param evt: original click event
     */
    minifyMenu: function minifyMenu(evt) {
      evt && evt.preventDefault();
      MyAMS.dom.root.toggleClass('minified');

      if (MyAMS.dom.root.hasClass('minified')) {
        MyAMS.core.switchIcon($('i', evt.currentTarget), 'arrow-circle-left', 'arrow-circle-right');
      } else {
        MyAMS.core.switchIcon($('i', evt.currentTarget), 'arrow-circle-right', 'arrow-circle-left');
      }

      if (window.localStorage) {
        if (MyAMS.dom.root.hasClass('minified')) {
          localStorage.setItem('window-state', 'minified');
        } else {
          localStorage.setItem('window-state', '');
        }
      }
    },

    /**
     * Click handler for menu hide button
     *
     * @param evt: original click event
     */
    switchMenu: function switchMenu(evt) {
      evt && evt.preventDefault();
      MyAMS.dom.root.toggleClass('hidden-menu');

      if (window.localStorage) {
        if (MyAMS.dom.root.hasClass('hidden-menu')) {
          localStorage.setItem('window-state', 'hidden-menu');
        } else {
          localStorage.setItem('window-state', '');
        }
      }
    },

    /**
     * Restore window state on application startup
     *
     * Previous window state is stored in local storage.
     */
    restoreState: function restoreState() {
      // restore window state
      if (window.localStorage) {
        var state = localStorage.getItem('window-state');

        if (state === 'minified') {
          MyAMS.nav.minifyMenu({
            currentTarget: $('#minifyme'),
            preventDefault: function preventDefault() {}
          });
        } else {
          MyAMS.dom.root.addClass(state);
        }
      }
    }
  };
  /**
   * Global module initialization
   */

  _exports.nav = nav;

  if (MyAMS.env.bundle) {
    MyAMS.config.modules.push('nav');
  } else {
    MyAMS.nav = nav;
    console.debug("MyAMS: nav module loaded...");
  }
});
//# sourceMappingURL=mod-nav-dev.js.map
