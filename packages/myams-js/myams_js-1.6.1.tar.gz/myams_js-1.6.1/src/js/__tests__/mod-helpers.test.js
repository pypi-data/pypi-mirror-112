/* global jest, test, expect */
/**
 * MyAMS helpers module test
 */

import $ from 'jquery';

import MyAMS, { init } from "../ext-base";
import { helpers } from "../mod-helpers";

import myams_require from "../ext-require";

const bs = require("bootstrap");


init($);

if (!MyAMS.helpers) {
	MyAMS.helpers = helpers;
	MyAMS.config.modules.push('helpers');
}
MyAMS.require = myams_require;


// Test MyAMS.helpers moveElementToParentEnd
test("Test MyAMS.helpers moveElementToParentEnd", () => {

	document.body.innerHTML = `<div>
		<ul>
			<li class="first"></li>
			<li class="second"></li>
			<li class="last"></li>
		</ul>
	</div>`;

	const
		list = $('ul'),
		item = $('.first', list);

	MyAMS.helpers.moveElementToParentEnd(item);
	const classes = $('li', list).listattr('class');
	expect(classes.length).toBe(3);
	expect(classes[0]).toBe('second');
	expect(classes[1]).toBe('last');
	expect(classes[2]).toBe('first');

});


// Test MyAMS.helpers hideDropdown
test("Test MyAMS.helpers hideDropdown", () => {

	document.body.innerHTML = `<div>
		<a class="dropdown-toggle" data-toggle="dropdown" aria-expanded="false">Open menu</a>
		<div class="dropdown-menu">
			<button class="submit">Submit</button>
		</div>
	</div>`;

	$.fn.dropdown = bs.Dropdown._jQueryInterface;
	$.fn.dropdown.Constructor = bs.Dropdown;

	const
		link = $('a.dropdown-toggle'),
		menu = $('.dropdown-menu'),
		button = $('button');

	expect(link.attr('aria-expanded')).toBe('false');
	link.dropdown('show');
	expect(link.attr('aria-expanded')).toBe('true');
	expect(menu.hasClass('show')).toBe(true);

	button.on('click', MyAMS.helpers.hideDropdown);
	button.trigger('click');
	// expect(link.attr('aria-expanded')).toBe('false');
	// expect(menu.hasClass('show')).toBe(false);

});
