'use strict';
var dashboard = angular.module('miningApp.dashboard', [])
  .config(['$routeProvider', function ($routeProvider) {
    $routeProvider
      .when('/dashboard/:slug', {
        templateUrl: 'assets/app/views/dashboard_detail.html',
        controller: 'DashboardDetailCtrl',
        resolve: {
          'current_dashboard': ['Dashboard', '$route', '$http',
            function(Dashboard, $route, $http){
              if($route.current.params.slug){
                return $http.get('/api/dashboard/'+$route.current.params.slug+'?full=' + true);
                // return Dashboard.getFull({'slug':$route.current.params.slug});
              }else{
                AlertService.add('error', 'Error!');
                return '';
              }
            }
          ]
        }
      })
      .otherwise({
        redirectTo: '/'
      });
  }])
  .run(['$rootScope', 'Dashboard', function($rootScope, Dashboard){
    $rootScope.selected_dashboard = {'name':'xxxxxxxxxx'};
    $rootScope.dashboards = Dashboard.query();
  }])
;