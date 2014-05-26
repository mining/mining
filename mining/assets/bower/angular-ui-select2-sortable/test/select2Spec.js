// a helper directive for injecting formatters and parsers
angular.module('ui.select2.sortable').directive('injectTransformers', [ function () {
    return {
        restrict: 'A',
        require: 'ngModel',
        priority: -1,
        link: function (scope, element, attr, ngModel) {
            var local = scope.$eval(attr.injectTransformers);

            if (!angular.isObject(local) || !angular.isFunction(local.fromModel) || !angular.isFunction(local.fromElement)) {
                throw "The injectTransformers directive must be bound to an object with two functions (`fromModel` and `fromElement`)";
            }

            ngModel.$parsers.push(local.fromElement);
            ngModel.$formatters.push(local.fromModel);
        }
    };
}]);

/*global describe, beforeEach, module, inject, it, spyOn, expect, $ */
describe('uiSelect2Sortable', function () {
    'use strict';

    var scope, $compile, options, $timeout;
    beforeEach(module('ui.select2.sortable'));
    beforeEach(inject(function (_$rootScope_, _$compile_, _$window_, _$timeout_) {
        scope = _$rootScope_.$new();
        $compile = _$compile_;
        $timeout = _$timeout_;
        scope.simpleQuery = function(term, callback) {
            callback([
                {href:'http://www.github.com', text : 'test', data : 42},
                {href:'http://www.google.com', text : 'google', data : 420},
                {href:'http://angularjs.org', text : 'Angular !!', data : 24}
            ]);
        };

        scope.stringQuery = function(term, callback) {
            callback(['test', 't1', 't2']);
        };
    }));

    /**
     * Compile a template synchronously
     * @param  {String} template The string to compile
     * @return {Object}          A reference to the compiled template
     */
    function compile(template) {
        var element = $compile(template)(scope);
        scope.$apply();
        $timeout.flush();
        return element;
    }

    describe('with an <input> element', function () {
        describe('compiling this directive', function () {
            it('should throw an error if we have no model defined', function () {
                expect(function () {
                    compile('<input ui-select2-sortable/>');
                }).toThrow();
            });
            it('should not create a select2 element if we have no simple-query defined', function () {
                expect(function () {
                    compile('<input ui-select2-sortable ng-model="foo"/>');
                }).toThrow();
            });
            it('should create proper DOM structure', function () {
                var element = compile('<input type="hidden" ui-select2-sortable ng-model="foo" simple-query="simpleQuery"/>');
                expect(element.siblings().is('div.select2-container')).toBe(true);
            });
        });
        describe('when model is changed programmatically', function () {
            describe('for single-select', function () {
                it('should call select2(data, ...) for objects', function () {
                    var element = compile('<input ng-model="foo" ui-select2-sortable simple-query="simpleQuery">');
                    spyOn($.fn, 'select2');
                    scope.$apply('foo={ id: 1, text: "first" }');
                    expect(element.select2).toHaveBeenCalledWith('data', { id: 1, text: "first", _data : { id: 1, text: "first" } });
                });
                it('should call select2(data, ...) for strings', function () {
                    var element = compile('<input ng-model="foo" ui-select2-sortable simple-query="simpleQuery">');
                    spyOn($.fn, 'select2');
                    scope.$apply('foo="first"');
                    expect(element.select2).toHaveBeenCalledWith('data', { id : 'first', text : 'first', _data : 'first' });
                });
            });
            describe('for multi-sortable-select', function () {
                it('should call select2(data, ...) for arrays', function () {
                    var element = compile('<input ng-model="foo" multiple ui-select2-sortable simple-query="simpleQuery">');
                    spyOn($.fn, 'select2');
                    scope.$apply('foo=[{ id: 1, text: "first" },{ id: 2, text: "second" }]');
                    expect(element.select2).toHaveBeenCalledWith('data', [
                        { id: 1, text: "first", _data : { id: 1, text: "first" } },
                        { id: 2, text: "second", _data : { id: 2, text: "second" } }
                    ]);
                });
                it('should call select2(data, []) for falsey values', function () {
                    var element = compile('<input ng-model="foo" multiple ui-select2-sortable simple-query="simpleQuery">');
                    spyOn($.fn, 'select2');
                    scope.$apply('foo=[]');
                    expect(element.select2).toHaveBeenCalledWith('data', []);
                });
                it('should call select2(data, ...) for strings', function () {
                    var element = compile('<input ng-model="foo" multiple ui-select2-sortable simple-query="stringQuery">');
                    spyOn($.fn, 'select2');
                    scope.$apply('foo="first,second"');
                    expect(element.select2).toHaveBeenCalledWith('data', { id : 'first,second', text : 'first,second', _data : 'first,second' });
                });
            });
        });

        it('updated the view when model changes with complex object', function () {
            scope.foo = [
                {'href': '0', 'name': '0'}
            ];
            var element = compile('<input ng-model="foo" multiple ui-select2-sortable simple-query="stringQuery">');
            scope.$digest();

            scope.foo.push({'href': 'ref', 'name': 'myName'});
            scope.$digest();

            expect(element.select2('data')).toEqual(
                [
                    { id : '0', text : '0', _data : { href : '0', name : '0' } },
                    { id : 'ref', text : 'myName', _data : { href : 'ref', name : 'myName' } }
                ]);
        });
    });
});