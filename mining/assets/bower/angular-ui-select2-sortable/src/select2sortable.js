/**
 * Enhanced Select2 Dropmenus
 *
 * @AJAX Mode - When in this mode, your value will be an object (or array of objects) of the data used by Select2
 *     This change is so that you do not have to do an additional query yourself on top of Select2's own query
 * @params [options] {object} The configuration options passed to $.fn.select2(). Refer to the documentation
 */
angular.module('ui.select2.sortable', []).directive('uiSelect2Sortable', ['$timeout', '$filter', function ($timeout, $filter) {
    return {
        require: 'ngModel',
        restrict: 'A',
        transclude: true,
        scope: {
            ngModel: '=',
            allowClear: '=?',
            simpleQuery: '=?',
            simpleData: '=?',
            query: '=?',
            toId: '=?',
            toText: '=?',
            sortResults: '=?',
            minimumInputLength: '=?',
            onSelect: '=?'
        },
        link: function (scope, element, attrs, ngModel) {
            //create a function to find an id into object
            if (!scope.toId) {
                scope.toId = function (item) {
                    if (item._id) {
                        return item._id;
                    }
                    if (item.id) {
                        return item.id;
                    }
                    if (item.uri) {
                        return item.uri;
                    }
                    if (item.href) {
                        return item.href;
                    }
                    if (item.resource) {
                        return item.resource;
                    }
                    return item;
                };
            }

            //create a function to find display value into object
            if (!scope.toText) {
                scope.toText = function (item) {
                    if (item.text) {
                        return item.text;
                    }
                    if (item.name) {
                        return item.name;
                    }
                    if (item.label) {
                        return item.label;
                    }
                    return item;
                };
            }

            //create a function to find display value into object
            //this js function is slower than the underscoreJS function below.
            //I recommand you to override this function by the underscoreJS one

//            $scope.sortResults = function (results, container, query) {
//                return _.sortBy(results, function(item) {
//                    return item.text;
//                });
//            };

            if (!scope.sortResults) {
                scope.sortResults = function (results, container, query) {
                    // use the built in javascript sort function
                    return results.sort(function (a, b) {
                        if (a.text > b.text) {
                            return 1;
                        } else if (a.text < b.text) {
                            return -1;
                        } else {
                            return 0;
                        }
                    });
                };
            }

            //prepare options for the select2 element
            scope.opts = {
                multiple: angular.isDefined(attrs.multiple) || false,
                sortable: angular.isDefined(attrs.sortable) || false,
                minimumInputLength: scope.minimumInputLength || 0,
                query: scope.query,
                sortResults: scope.sortResults,
                allowClear: scope.allowClear || false
            };

            // Convert from Select2 view-model to Angular view-model.
            scope.convertToAngularModel = function (select2_data) {
                var model;
                if (angular.isArray(select2_data)) {
                    model = [];
                    angular.forEach(select2_data, function (value) {
                        model.push(value._data);
                    });
                } else {
                    if (select2_data && select2_data._data) {
                        model = select2_data._data;
                    } else {
                        model = select2_data;
                    }
                }
                return model;
            };

            // Convert from Angular view-model to Select2 view-model.
            scope.convertToSelect2Model = function (angular_data) {
                if (angular.isArray(angular_data)) {
                    var model = [];
                    angular.forEach(
                        angular_data,
                        function (value) {
                            model.push({
                                id: scope.toId(value),
                                text: scope.toText(value),
                                _data: value
                            });
                        });
                    return model;
                } else if (angular.isObject(angular_data)) {
                    return {
                        id: scope.toId(angular_data),
                        text: scope.toText(angular_data),
                        _data: angular_data
                    };
                } else if (angular.isString(angular_data)) {
                    return {
                        id: angular_data,
                        text: angular_data,
                        _data: angular_data
                    };
                }

                return angular_data;
            };

            //allow user to create a simple query
            //just use simpleQuery : function(term, callback) { callback(array_of_dummy_objects; }
            if (scope.simpleQuery) {
                scope.opts.query = function (query) {
                    scope.simpleQuery(query.term, function (values) {
                        query.callback({ results: scope.convertToSelect2Model(values) });
                    });
                };
            } else if (scope.simpleData) {
                //Use this if you want to filter on the text field without ajax query
                //Just use data : [Object object] and the toText function
                scope.opts.query = function (query) {
                    query.callback({
                        results: $filter('filter')(scope.convertToSelect2Model(scope.simpleData), {text: query.term}, 'text')
                    });
                };
            }

            // call select2 function to set data and all properties
            scope.render = function () {
                if (scope.opts.multiple) {
                    element.select2('data', scope.convertToSelect2Model(ngModel.$viewValue));
                } else {
                    if (angular.isObject(ngModel.$viewValue)) {
                        element.select2('data', scope.convertToSelect2Model(ngModel.$viewValue));
                    } else if (!ngModel.$viewValue) {
                        element.select2('data', null);
                    } else {
                        element.select2('data', scope.convertToSelect2Model(ngModel.$viewValue));
                    }
                }
                if (scope.opts.sortable) {
                    element.select2("container").find("ul.select2-choices").sortable({
                        containment: 'parent',
                        start: function () {
                            element.select2("onSortStart");
                        },
                        update: function () {
                            element.select2("onSortEnd");
                            element.trigger('change');
                        }
                    });
                }
            };

            // Set the view and model value and update the angular template manually for the ajax/multiple select2.
            element.bind("change", function (event) {
                if (scope.$$phase) {
                    return;
                }
                var e = event;
                scope.$apply(function () {
                    var values = element.select2('data');
                    if (e && e.removed && values) {
                        for (var i = 0; i < values.length; i++) {
                            if (values[i] === e.removed) {
                                values.splice(i, 1);
                            }
                        }
                    }
                    if (values && (angular.isArray(values) || values._data)) {
                        values = scope.convertToAngularModel(values);
                    }
                    ngModel.$setViewValue(values);
                });
            });

            // Watch the model for programmatic changes
            scope.$watch(function () {
                return ngModel.$viewValue;
            }, function (current, old) {
                if (current === old) {
                    return;
                }
                scope.render();
            }, true);

            element.bind("$destroy", function () {
                element.select2("destroy");
            });

            //watch disabled attrs to send event to select2
            attrs.$observe('disabled', function (value) {
                element.select2('enable', !value);
            });

            // add an onSelect element which retreive model object into e.added or e.removed
            if (scope.onSelect) {
                element.on("change", function (e) {
                    if (e.added) {
                        e.added = scope.convertToAngularModel(e.added);
                    }
                    if (e.removed) {
                        e.removed = scope.convertToAngularModel(e.removed);
                    }
                    scope.onSelect(e);
                });
            }

            // Initialize the plugin late so that the injected DOM does not disrupt the template compiler
            $timeout(function () {
                element.select2(scope.opts);
                scope.render();
            });
        }
    };
}]);