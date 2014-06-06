'use strict';
admin.controller('TasksControllers', ['$scope', 'Cube', '$rootScope', 'AlertService', '$interval',
    function ($scope, Cube, $rootScope, AlertService, $interval) {
      $scope.tasks = [];
      $scope.loading = true;
      $scope.tasks = Cube.checkTasks();
      $scope.loading = false;
      $scope.show_tasks = false;

      $interval(function () {
        $scope.loading = true;
        $scope.tasks = Cube.checkTasks();
        $scope.loading = false;
      }, 30000);

      $scope.forceRefresh = function () {
        $scope.loading = true;
        $scope.tasks = Cube.checkTasks();
        $scope.loading = false;
      }
    }]
);