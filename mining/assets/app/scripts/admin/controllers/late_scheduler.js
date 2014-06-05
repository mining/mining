'use strict';
admin.controller('LateSchedulerCtrl', ['$scope', 'Cube', '$rootScope',
    function ($scope, Cube, $rootScope) {
      $scope.cubes = Cube.getLate();
      $scope.loading = false;

      $scope.refreshNow = function () {
        $scope.loading = true;
        $scope.cubes = Cube.getLate();
        $scope.$emit('UPDATE_LATE_CUBES', $scope.cubes);
        $scope.loading = false;
      };

      $rootScope.$on("UPDATE_LATE_CUBES", function (event, cubes) {
        $scope.cubes = cubes;
      });

      $scope.forceRefresh = function (cb) {
        $scope.loading = true;
        Cube.get({'slug': cb.slug}, function (cube) {
          cube.status = false;
          Cube.update({'slug': cube.slug}, cube);
          $scope.cubes = Cube.getLate();
          $scope.$emit('UPDATE_LATE_CUBES', $scope.cubes);
          $scope.loading = false;
        });
      }
    }]
);