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
      .otherwise({
        redirectTo: '/'
      });
  }])
;