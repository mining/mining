'use strict';

var miningApp = angular.module('miningApp', [
    'ngCookies',
    'ngResource',
    'ngSanitize',
    'ngRoute',
    'highcharts-ng',
//    'miningApp.auth',
    'miningApp.dashboard',
    'miningApp.report',
    'miningApp.admin',
    'ui.bootstrap',
    'ui.codemirror'
  ])
  .factory('AlertService', ['$rootScope',
    function ($rootScope) {
      var alertService = {};

      // create an array of alerts available globally
      $rootScope.alerts = [];

      alertService.add = function (type, msg, persistente) {
        $rootScope.alerts.push({'type': type, 'msg': msg, 'persistente': persistente || false});
      };

      alertService.getAll = function () {
        return $rootScope.alerts;
      };

      alertService.closeAlert = function (index) {
        $rootScope.alerts.splice(index, 1);
      };

      alertService.clearTemporarios = function () {
        for (var a = $rootScope.alerts.length; a <= $rootScope.alerts.length && a>=0; a--) {
          if ($rootScope.alerts[a] !== undefined) {
            if (!$rootScope.alerts[a].persistente) {
              $rootScope.alerts.splice(a, 1);
            }
          }
        }
      };

      alertService.alertType = function (type) {
        if (type == 'success')
          return 'alert-success';
        else if (type == 'info')
          return 'alert-info';
        else if (type == 'error')
          return 'alert-error';
        else
          return 'alert-warning';
      };

      return alertService;
    }])
  .config(['$routeProvider', '$interpolateProvider',
    function ($routeProvider, $interpolateProvider) {
    $routeProvider
      .when('/', {
        templateUrl: 'views/home.html',
        controller: 'HomeCtrl'
      })
      .otherwise({
        redirectTo: '/'
      });
      $interpolateProvider.startSymbol('[['); 
      $interpolateProvider.endSymbol(']]');
  }])
  .run(['$rootScope', 'AlertService', '$locale',
    function($rootScope, AlertService, $locale){
      $rootScope.closeAlert = AlertService.closeAlert;
      $locale.id = 'pt-br';
    }])
  .controller('HomeCtrl', function(){});
var mining = {};
mining['utils'] = {
  padLeft: function (nr, n, str) {
    return Array(n - String(nr).length + 1).join(str || '0') + nr;
  }
};