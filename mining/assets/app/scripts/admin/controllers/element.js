'use strict';
admin.controller('ElementCtrl', ['$scope', 'Cube', 'Element', 'AlertService', '$http', '$rootScope',
    function ($scope, Cube, Element, AlertService, $http, $rootScope) {
      $rootScope.inSettings = true;
      $scope.types = [
        {'slug': "grid", "name": "Grid"},
        {'slug': "chart_line", "name": "Chart line"},
        {'slug': "chart_bar", "name": "Chart bar"},
        {'slug': "chart_pie", "name": "Chart pie"}
      ];
      $scope.widget_types = [
        {'value': "date", "label": "Date Picker"},
        {'value': "datetime", "label": "Date Time (less) Picker"},
        {'value': "text", "label": "Text Input"},
        {'value': "int", "label": "Integer Input"},
        {'value': "distinct", "label": "Distincts"}
      ];
      $scope.cubes = Cube.query();
      $scope.elements = Element.query();
      $scope.element = new Element();
      $scope.fields = [];
      $scope.selectElement = function (e) {
        $scope.element = e;
        if (!$scope.element.alias)
          $scope.element.alias = {};
        if ($scope.element.scheduler_type == 'day') {
          $scope.show_h = true;
          $scope.show_m = true;
          $scope.hour = parseInt($scope.element.scheduler_interval.split(':')[0]);
          $scope.min = parseInt($scope.element.scheduler_interval.split(':')[1]);
        } else if ($scope.element.scheduler_type == 'minutes') {
          $scope.min = parseInt($scope.element.scheduler_interval);
          $scope.show_h = false;
          $scope.show_m = true;
        } else if ($scope.element.scheduler_type == 'hour') {
          $scope.hour = parseInt($scope.element.scheduler_interval);
          $scope.show_h = true;
          $scope.show_m = false;
        } else {
          $scope.show_h = false;
          $scope.show_m = false;
        }
        $scope.loadFields();
      };
      $scope.deleteElement = function (element) {
        Element.delete({}, {'slug': element.slug});
        $scope.elements.splice($scope.elements.indexOf(element), 1);
      };
      $scope.scheduler_types = [
        {key: 'minutes', val: 'minutes'}
//        {key: 'hour', val: 'hour'},
//        {key: 'day', val: 'day'}
      ];
      $scope.show_h = false;
      $scope.show_m = false;
      $scope.hour = 0;
      $scope.min = 0;
      $scope.changeSchedulerType = function () {
        if ($scope.element.scheduler_type == 'day') {
          $scope.show_h = true;
          $scope.show_m = true;
        } else if ($scope.element.scheduler_type == 'minutes') {
          $scope.show_h = false;
          $scope.show_m = true;
        } else if ($scope.element.scheduler_type == 'hour') {
          $scope.show_h = true;
          $scope.show_m = false;
        } else {
          $scope.show_h = false;
          $scope.show_m = false;
        }
      };
      $scope.save = function (element) {
        $scope.element.scheduler_status = false;
        if ($scope.element.scheduler_type) {
          $scope.element.scheduler_status = true;
          if ($scope.element.scheduler_type == 'day') {
            $scope.element.scheduler_interval = mining.utils.padLeft(parseInt($scope.hour), 2) + ':' + mining.utils.padLeft(parseInt($scope.min), 2);
          } else if ($scope.element.scheduler_type == 'minutes') {
            $scope.element.scheduler_interval = parseInt($scope.min);
          } else if ($scope.element.scheduler_type == 'hour') {
            $scope.element.scheduler_interval = parseInt($scope.hour);
          }
        } else {
          $scope.element.scheduler_status = false;
        }
        if ($scope.element.slug) {
          Element.update({'slug': $scope.element.slug}, $scope.element);
        } else {
          $scope.element.$save().then(function (response) {
            AlertService.add('success', 'Save ok');
            $scope.elements.push(response);
          });
        }
        $scope.element = new Element();
        $scope.element.alias = {};
        $scope.show_h = false;
        $scope.show_m = false;
        $scope.hour = 0;
        $scope.min = 0;
      };
      $scope.addOrder = function () {
        if (!$scope.element.orderby) {
          $scope.element.orderby = [];
          $scope.element.orderby__order = [];
        }
        if ($scope.element.orderby.length < $scope.fields.length) {
          $scope.element.orderby.push('');
          $scope.element.orderby__order.push('');
        }
      };
      $scope.removeOrder = function (ind) {
        $scope.element.orderby.splice(ind, 1);
        $scope.element.orderby__order.splice(ind, 1);
      };
      $scope.addWidget = function () {
        if (!$scope.element.widgets) {
          $scope.element.widgets = [];
        }
        if ($scope.element.widgets.length < $scope.fields.length) {
          $scope.element.widgets.push({'type': '', 'field': '', 'label': ''});
        }
      };
      $scope.removeWidget = function (ind) {
        $scope.element.widgets.splice(ind, 1);
      };

      $scope.checkShowFields = function (field) {
        var checked = false;
        $($scope.element.show_fields).each(function (ind, _field) {
          if (field == _field)
            checked = true;
        });
        return checked;
      };

      $scope.selectShowFields = function (field) {
        if (!$scope.element.show_fields)
          $scope.element.show_fields = [];
        if ($scope.element.show_fields.indexOf(field) >= 0) {
          if ($scope.element.show_fields.length > 1) {
            $scope.element.show_fields.splice($scope.element.show_fields.indexOf(field), 1);
          } else
            AlertService.add('error', 'Select at least one field');
        } else if ($scope.element.show_fields.length < $scope.fields.length) {
          $scope.element.show_fields.push(field);
        }
      };

      $scope.addAlias = function () {
        if (!$scope.element.alias) {
          $scope.element.alias = [];
        }
        if ($scope.element.alias.length < $scope.fields.length) {
          $scope.element.alias.push({'field': '', 'alias': ''});
        }
      };
      $scope.removeAlias = function (ind) {
        $scope.element.alias.splice(ind, 1);
      };
      $scope.loadFields = function (clean) {
        if ($scope.element.cube) {
          $http.get('/api/element/cube/' + $scope.element.cube)
            .success(function (retorno) {
              $scope.fields = retorno.columns;
              if (!$scope.element.slug) {
                $scope.element.show_fields = angular.copy(retorno.columns);
                $scope.element.alias = {};
                $(retorno.columns).each(function(ind, field){
                  $scope.element.alias[field] = undefined;
                });
              }
              else {
                if (!$scope.element.show_fields ||
                  $scope.element.show_fields.length == 0 ||
                  Object.keys($scope.element).length > 0) {
                  $scope.element.show_fields = angular.copy(retorno.columns);
                  $scope.element.alias = {};
                  $(retorno.columns).each(function(ind, field){
                    $scope.element.alias[field] = undefined;
                  });
                }
              }
              if (clean) {
                $scope.element.show_fields = angular.copy(retorno.columns);
                $scope.element.alias = {};
                $(retorno.columns).each(function(ind, field){
                  $scope.element.alias[field] = undefined;
                });
              }
            })
            .error(function (retorno) {
              AlertService.add('error', 'Error!');
            });
        }
      };
      $scope.newForm = function () {
        $scope.element = new Element();
        $scope.element.alias = {};
        $scope.show_h = false;
        $scope.show_m = false;
        $scope.hour = 0;
        $scope.min = 0;
      };
    }]
);