'use strict';

var miningApp = angular.module('miningApp', [
    'ngCookies',
    'ngResource',
    'ngSanitize',
    'ngRoute',
    'highcharts-ng',
    'miningApp.dashboard',
    'miningApp.report',
    'miningApp.admin'
  ])
  .config(['$routeProvider', function ($routeProvider) {
    $routeProvider
      .when('/', {
        templateUrl: 'views/home.html',
        controller: 'HomeCtrl'
      })
      .otherwise({
        redirectTo: '/'
      });
  }]);
