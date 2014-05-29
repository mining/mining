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
      .when('/admin/dashboard-group', {
        templateUrl: 'assets/app/views/dashboard_group.html',
        controller: 'DashboardGroupCtrl'
      })
      .when('/admin/user', {
        templateUrl: 'assets/app/views/user.html',
        controller: 'UserCtrl'
      })
      .when('/admin/late-scheduler', {
        templateUrl: 'assets/app/views/late_scheduler.html',
        controller: 'LateSchedulerCtrl'
      })
      .otherwise({
        redirectTo: '/'
      });
  }])
    .run(['$rootScope', 'Dashboard', 'Cube', '$interval',
    function($rootScope, Dashboard, Cube, $interval){
      $rootScope.late_cubes = Cube.getLate();
      $rootScope.$on("UPDATE_LATE_CUBES", function(event, message){
        $rootScope.late_cubes = message;
      });
      $interval(function(){
        $rootScope.$emit("UPDATE_LATE_CUBES", Cube.getLate());
      }, 10000);
      $rootScope.dashboard = Dashboard.query();
    }])
;