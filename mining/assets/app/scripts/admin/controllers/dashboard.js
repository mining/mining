'use strict';
admin.controller('DashboardCtrl', ['$scope', 'Dashboard', 'Element', 'AlertService', '$rootScope', '$filter',
    function ($scope, Dashboard, Element, AlertService, $rootScope, $filter) {
      $rootScope.inSettings = true;
      $rootScope.dashboards = Dashboard.query();
      $scope.elements = Element.query();
      $scope.dashboard = new Dashboard();

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
        if ($scope.dashboard.scheduler_type == 'day') {
          $scope.show_h = true;
          $scope.show_m = true;
        } else if ($scope.dashboard.scheduler_type == 'minutes') {
          $scope.show_h = false;
          $scope.show_m = true;
        } else if ($scope.dashboard.scheduler_type == 'hour') {
          $scope.show_h = true;
          $scope.show_m = false;
        } else {
          $scope.show_h = false;
          $scope.show_m = false;
        }
      };

      $scope.selectDashboard = function (d) {
        $scope.dashboard = d;
        if ($scope.dashboard.scheduler_type == 'day') {
          $scope.show_h = true;
          $scope.show_m = true;
          $scope.hour = parseInt($scope.dashboard.scheduler_interval.split(':')[0]);
          $scope.min = parseInt($scope.dashboard.scheduler_interval.split(':')[1]);
        } else if ($scope.dashboard.scheduler_type == 'minutes') {
          $scope.min = parseInt($scope.dashboard.scheduler_interval);
          $scope.show_h = false;
          $scope.show_m = true;
        } else if ($scope.dashboard.scheduler_type == 'hour') {
          $scope.hour = parseInt($scope.dashboard.scheduler_interval);
          $scope.show_h = true;
          $scope.show_m = false;
        } else {
          $scope.show_h = false;
          $scope.show_m = false;
        }
      };
      $scope.deleteDashboard = function (dashboard) {
        Dashboard.delete({}, {'slug': dashboard.slug});
        $rootScope.dashboards.splice($rootScope.dashboards.indexOf(dashboard), 1);
      };
      $scope.queryElements = function (term, result) {
        var ls = [];
        $($scope.elements).each(function (key, val) {
          ls.push({
            id: val.slug,
            label: val.name
          });
        });
        result($filter('filter')(ls, term));
      };
      $scope.save = function (dashboard) {
        $scope.dashboard.scheduler_status = false;
        if ($scope.dashboard.scheduler_type) {
          $scope.dashboard.scheduler_status = true;
          if ($scope.dashboard.scheduler_type == 'day') {
            $scope.dashboard.scheduler_interval = mining.utils.padLeft(parseInt($scope.hour), 2) + ':' + mining.utils.padLeft(parseInt($scope.min), 2);
          } else if ($scope.dashboard.scheduler_type == 'minutes') {
            $scope.dashboard.scheduler_interval = parseInt($scope.min);
          } else if ($scope.dashboard.scheduler_type == 'hour') {
            $scope.dashboard.scheduler_interval = parseInt($scope.hour);
          }
        } else {
          $scope.dashboard.scheduler_status = false;
        }
        if ($scope.dashboard.slug) {
          $scope.dashboard.status = false;
          Dashboard.update({'slug': $scope.dashboard.slug}, $scope.dashboard);
        } else {
          $scope.dashboard.$save().then(function (response) {
            AlertService.add('success', 'Save ok');
            $rootScope.dashboards.push(response);
          });
        }
        $scope.dashboard = new Dashboard();
        $scope.show_h = false;
        $scope.show_m = false;
        $scope.hour = 0;
        $scope.min = 0;
      };
      $scope.newForm = function () {
        $scope.dashboard = new Dashboard();
      };
    }]
);