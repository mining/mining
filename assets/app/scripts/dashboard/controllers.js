'use strict';
dashboard
  .controller('HomeCtrl',
  ['$scope', function($scope) {
  }])
  .controller('DashboardDetailCtrl', ['$rootScope', '$scope', '$routeParams', 'AlertService', 'Dashboard', 'current_dashboard',
  function($rootScope, $scope, $routeParams, AlertService, Dashboard, current_dashboard){
    $scope.filters={};
    $rootScope.selected_dashboard = current_dashboard[0];
    $($rootScope.selected_dashboard.elements).each(function(ind, val){
      $scope.filters[val.slug] = [];
    });
  }])
;