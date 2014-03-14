'use strict';
var admin = angular.module('miningApp.admin',[])
.config(['$routeProvider', function ($routeProvider) {
    $routeProvider
      .when('/admin/connection', {
        templateUrl: 'assets/app/views/connection.html',
        controller: 'ConnectionCtrl'
      })
      .when('/admin/cube', {
        templateUrl: 'assets/app/views/cube.html',
        controller: 'CubeCtrl'
      })
      .when('/admin/element', {
        templateUrl: 'assets/app/views/element.html',
        controller: 'ElementCtrl'
      })
      .when('/admin/dashboard', {
        templateUrl: 'assets/app/views/dashboard.html',
        controller: 'DashboardCtrl'
      })
      .otherwise({
        redirectTo: '/'
      });
  }])
    .run(['$rootScope', 'Dashboard',
    function($rootScope, Dashboard){
      $rootScope.dashboard = Dashboard.query();
    }])
;