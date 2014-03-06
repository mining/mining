'use strict';
dashboard
  .controller('HomeCtrl',
  ['$scope', function($scope) {

  }])
  .controller('LoadDashboard',
  ['$scope','$http', function($scope, $http) {
    $http.get("/api/dashboard/").success(function(data){
      $scope.dashboard_list = data;
    })
  }])
;