'use strict';

var miningApp = angular.module('miningApp', [
    'ngCookies',
    'ngResource',
    'ngSanitize',
    'ngRoute',
    'highcharts-ng',
    'miningApp.auth',
    'miningApp.dashboard',
    'miningApp.report',
    'miningApp.admin',
    'ui.bootstrap',
    'ui.codemirror',
    'ui.select2',
    'ui.select2.sortable'
  ])
  .factory('AlertService', ['$rootScope', '$timeout',
    function ($rootScope, $timeout) {
      var alertService = {};

      // create an array of alerts available globally
      $rootScope.alerts = [];

      alertService.add = function (al) {
        $rootScope.alerts.push(al);
        if (al['hold']) {
          var messageStack = $rootScope.alerts;
          $timeout(function () {
            var msgIndex = $.inArray(al, messageStack);

            if (msgIndex !== -1)
              messageStack.splice(msgIndex, 1);
          }, 5000);
        }
      };

      $rootScope.$on('alert', alertService.add);

      alertService.getAll = function () {
        return $rootScope.alerts;
      };

      alertService.closeAlert = function (index) {
        $rootScope.alerts.splice(index, 1);
      };

      alertService.clearTemporarios = function () {
        for (var a = $rootScope.alerts.length; a <= $rootScope.alerts.length && a >= 0; a--) {
          if ($rootScope.alerts[a] !== undefined) {
            if (!$rootScope.alerts[a].hold) {
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
  .factory('ServiceUtils', ['$q', '$http', function($q, $http) {

    return {
      'unenvelope': function(method, url, data, httpErrorMessage){
        var deferred = $q.defer(),
          promise = $http({
              method: method,
              url: url,
              params: data
          });

        promise.then(
          function(response) {
            if (response.data.status == 'success')
              deferred.resolve(response.data.data);
            else
              deferred.reject(response.data.errors);
          },
          function() {
            deferred.reject(httpErrorMessage);
          }
        );
        return deferred.promise;
      }
    }
  }])
  .filter('timeAgo',[
    function(){
      return function(input){
        return moment(input, 'YYYY-MM-DD HH:mm:ss').fromNow();
      };
    }])
  .config(['$routeProvider', '$interpolateProvider',
    function ($routeProvider, $interpolateProvider) {
      $routeProvider
        .when('/', {
          templateUrl: 'assets/app/views/home.html',
          controller: 'HomeCtrl'
        })
        .otherwise({
          redirectTo: '/'
        });
      $interpolateProvider.startSymbol('[[');
      $interpolateProvider.endSymbol(']]');
    }])
  .run(['$rootScope', 'AlertService', '$locale', '$timeout',
    function ($rootScope, AlertService, $locale, $timeout) {
      $rootScope.closeAlert = AlertService.closeAlert;
      $locale.id = 'pt-br';
      $rootScope.abreMenu = function(){
        $timeout(function(){
          $rootScope.$emit('WINDOW_RESIZE');
        }, 1000);
      };

      $rootScope.$on('$routeChangeStart', function (ev, to, toParams, from, fromParams) {
        $rootScope.inSettings = false;
        $rootScope.inDashboard = false;
      });
    }])
  .controller('HomeCtrl', function () {});
var mining = {};
mining['utils'] = {
  padLeft: function (nr, n, str) {
    return Array(n - String(nr).length + 1).join(str || '0') + nr;
  },
  getNestedProp: function (obj, propString, fallback) {
    if (!propString) return obj;
    var prop, props = propString.split('.');

    for (var i = 0, iLen = props.length - 1; i <= iLen; i++) {
      prop = props[i];

      if (typeof obj == 'object' && obj !== null && prop in obj) {
        obj = obj[prop];
      }
      else
        return fallback;
    }

    return obj;
  },
  deepExtend: function(destination, source) {
    for (var property in source) {
      if (source[property] && source[property].constructor &&
       source[property].constructor === Object) {
        destination[property] = destination[property] || {};
        mining.utils.deepExtend(destination[property], source[property]);
      } else {
        destination[property] = source[property];
      }
    }
    return destination;
  },
  isNumber: function(obj) { return !isNaN(parseFloat(obj)) }
};