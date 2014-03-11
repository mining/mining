'use strict';
var admin = angular.module('miningApp.admin',[])
.config(['$routeProvider', function ($routeProvider) {
    $routeProvider
      .when('/admin/connection', {
        templateUrl: 'views/connection.html',
        controller: 'ConnectionCtrl'
      })
      .when('/admin/cube', {
        templateUrl: 'views/cube.html',
        controller: 'CubeCtrl'
      })
      .when('/admin/element', {
        templateUrl: 'views/element.html',
        controller: 'ElementCtrl'
      })
      .when('/admin/dashboard', {
        templateUrl: 'views/dashboard.html',
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