'use strict';
admin.controller('CubeCtrl', ['$scope', 'Cube', 'Connection', 'AlertService', '$timeout', '$rootScope', '$http',
    function ($scope, Cube, Connection, AlertService, $timeout, $rootScope, $http) {
      $rootScope.inSettings = true;
      $scope.editorOptions = {
        lineWrapping: true,
        lineNumbers: true,
        readOnly: false,
        mode: 'text/x-sql',
        onLoad: function (editor) { // FIX TEMP ISSUE: https://github.com/angular-ui/ui-codemirror/issues/35
          editor.on('blur', function () {
            $timeout(function () {
              $scope.cube.sql = editor.getValue();
            });
          })
        }
      };
      $scope.cube_valid = false;
      $scope.connections = Connection.query();
      $scope.cubes = Cube.query();
      $scope.cube = new Cube();
      $scope.scheduler_types = [
        {key: 'minutes', val: 'minutes'}
//        {key: 'hour', val: 'hour'},
//        {key: 'day', val: 'day'}
      ];
      $scope.templates = {
        'relational': 'assets/app/views/cube_relational.html',
        'cube_join': 'assets/app/views/cube_join.html'
      };
      $scope.loadCubeFields = function (ind) {
        if ($scope.cube.relationship[ind].cube) {
          $http.get('/api/element/cube/' + $scope.cube.relationship[ind].cube)
            .success(function (retorno) {
              $scope.cube.relationship[ind].fields = retorno.columns;
            })
            .error(function (retorno) {
              AlertService.add('error', 'Error!');
            });
        }
      };
      $scope.addRelationship = function () {
        if (!$scope.cube.relationship) {
          $scope.cube.relationship = [];
        }
        if ($scope.cube.relationship.length < $scope.cubes.length) {
          $scope.cube.relationship.push({
            'cube': '',
            'field': ''
          });
        }
      };
      $scope.removeRelationship = function (ind) {
        $scope.cube.relationship.splice(ind, 1);
      };
      $scope.show_h = false;
      $scope.show_m = false;
      $scope.hour = 0;
      $scope.min = 0;
      $scope.changeSchedulerType = function () {
        if ($scope.cube.scheduler_type == 'day') {
          $scope.show_h = true;
          $scope.show_m = true;
        } else if ($scope.cube.scheduler_type == 'minutes') {
          $scope.show_h = false;
          $scope.show_m = true;
        } else if ($scope.cube.scheduler_type == 'hour') {
          $scope.show_h = true;
          $scope.show_m = false;
        } else {
          $scope.show_h = false;
          $scope.show_m = false;
        }
      };
      $scope.selectCube = function (c) {
        $scope.cube = c;
        if ($scope.cube.scheduler_type == 'day') {
          $scope.show_h = true;
          $scope.show_m = true;
          $scope.hour = parseInt($scope.cube.scheduler_interval.split(':')[0]);
          $scope.min = parseInt($scope.cube.scheduler_interval.split(':')[1]);
        } else if ($scope.cube.scheduler_type == 'minutes') {
          $scope.min = parseInt($scope.cube.scheduler_interval);
          $scope.show_h = false;
          $scope.show_m = true;
        } else if ($scope.cube.scheduler_type == 'hour') {
          $scope.hour = parseInt($scope.cube.scheduler_interval);
          $scope.show_h = true;
          $scope.show_m = false;
        } else {
          $scope.show_h = false;
          $scope.show_m = false;
        }
        if (c.type == 'cube_join') {
          $($scope.cube.relationship).each(function (ind, rel) {
            $scope.loadCubeFields(ind);
          });
        }
      };
      $scope.deleteCube = function (cube) {
        Cube.delete({}, {'slug': cube.slug});
        $scope.cubes.splice($scope.cubes.indexOf(cube), 1);
      };
      $scope.save = function () {
        $scope.cube.scheduler_status = false;
        if ($scope.cube.scheduler_type) {
          $scope.cube.scheduler_status = true;
          if ($scope.cube.scheduler_type == 'day') {
            $scope.cube.scheduler_interval = mining.utils.padLeft(parseInt($scope.hour), 2) + ':' + mining.utils.padLeft(parseInt($scope.min), 2);
          } else if ($scope.cube.scheduler_type == 'minutes') {
            $scope.cube.scheduler_interval = parseInt($scope.min);
          } else if ($scope.cube.scheduler_type == 'hour') {
            $scope.cube.scheduler_interval = parseInt($scope.hour);
          }
        } else {
          $scope.cube.scheduler_status = false;
        }
        if ($scope.cube.type == 'cube_join') {
          $($scope.cube.relationship).each(function (ind, rel) {
            delete $scope.cube.relationship[ind].fields;
          });
        }
        if ($scope.cube.slug) {
          $scope.cube.status = false;
          Cube.update({'slug': $scope.cube.slug}, $scope.cube);
        } else {
          $scope.cube.$save().then(function (response) {
            AlertService.add('success', 'Save ok');
            $scope.cubes.push(response);
          });
        }
        $scope.cube = new Cube();
        $scope.show_h = false;
        $scope.show_m = false;
        $scope.hour = 0;
        $scope.min = 0;
      };
      $scope.testquery = function () {
        Cube.testquery($scope.cube, function (response) {
          if (response.status == 'success') {
            $scope.cube_valid = true;
            AlertService.add('success', 'Query is Ok!');
          } else {
            AlertService.add('error', 'Query is not Ok!');
          }
        });
      };
      $scope.newForm = function () {
        $scope.cube = new Cube();
        $scope.show_h = false;
        $scope.show_m = false;
        $scope.hour = 0;
        $scope.min = 0;
      };
    }]
);