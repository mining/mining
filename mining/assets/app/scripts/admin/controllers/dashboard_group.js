'use strict';
admin.controller('DashboardGroupCtrl', ['$scope', 'DashboardGroup', 'AlertService', '$rootScope', '$filter',
    function ($scope, DashboardGroup, AlertService, $rootScope, $filter) {
      $rootScope.inSettings = true;
      $rootScope.dashboardGroups = DashboardGroup.query();
      $scope.dashboardGroup = new DashboardGroup();
      $scope.selectDashboardGroup = function (dg) {
        $scope.dashboardGroup = dg;
      };
      $scope.deleteDashboardGroup = function (dg) {
        DashboardGroup.delete({}, {'slug': dg.slug});
        $rootScope.dashboardGroups.splice($rootScope.dashboardGroups.indexOf(dg), 1);
      };
      $scope.queryDashboards = function (term, result) {
        var ls = [];
        $($rootScope.dashboard).each(function (key, val) {
          ls.push({
            id: val.slug,
            label: val.name
          });
        });
        result($filter('filter')(ls, term));
      };
      $scope.save = function (dg) {
        if ($scope.dashboardGroup.slug) {
          DashboardGroup.update({'slug': $scope.dashboardGroup.slug}, $scope.dashboardGroup);
        } else {
          $scope.dashboardGroup.$save().then(function (response) {
            AlertService.add('success', 'Save ok');
            $rootScope.dashboardGroups.push(response);
          });
        }
        $scope.dashboard = new DashboardGroup();
      };
      $scope.newForm = function () {
        $scope.dashboard = new DashboardGroup();
      };
    }]
);