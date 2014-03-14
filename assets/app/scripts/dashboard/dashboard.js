'use strict';
var dashboard = angular.module('miningApp.dashboard', [])
  .config(['$routeProvider', function ($routeProvider) {
    $routeProvider
      .when('/dashboard/:slug', {
        templateUrl: 'views/dashboard_detail.html',
        controller: 'DashboardDetailCtrl',
        resolve: {
          'current_dashboard': ['Dashboard', '$route', 
            function(Dashboard, $route){
              if($route.current.params.slug){
                return Dashboard.getFull({'slug':$route.current.params.slug});
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
  .run(['$rootScope', function($rootScope){
    $rootScope.selected_dashboard = {'name':'xxxxxxxxxx'};
  }])
;