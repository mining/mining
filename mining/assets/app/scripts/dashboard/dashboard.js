'use strict';
var dashboard = angular.module('miningApp.dashboard', [])
  .constant('PROTOCOL', window.protocol)
  .filter('replaceUnderToSpace', function() {
    return function(input) {
      input = input || '';
      return input.replace(/_/g, ' ');
    };
  })
  .filter('getLabel',[
    function(){
      return function(field, element){
        var label = field;
        if(element.alias)
          if(element.alias.hasOwnProperty(field))
            if (element.alias[field] != '')
              label = element.alias[field];
        return label;
      };
    }])
  .filter('formatDataTable',[
    function(){
      return function(value){
        if (!isNaN(value)) {
          if(typeof value == 'string')
            value = parseFloat(value);
          if(value.toString().split('.').length > 1)
            return mining.utils.formatNumber(value, 2, 3, '.', ',');
          else
            return mining.utils.formatNumber(value, 0, 3, '.', ',');
        }
        return value;
      };
    }])
  .filter('dashboardGroupFilter', function() {
    return function(dashboards, group) {
      var new_dashboards = [];
      $(dashboards).each(function(key, dashboard){
        $(mining.utils.getNestedProp(group, 'dashboards', [])).each(function(key, dash){
          if(mining.utils.getNestedProp(dashboard, 'slug', undefined) == dash.id)
            new_dashboards.push(dashboard);
        })
      });
      return new_dashboards;
    };
  })
  .filter('elementFields', function() {
    return function(columns, element) {
      if(!element.show_fields)
        return columns;
      if(element.show_fields.length < 1)
        return columns;
      var new_columns = [];
      $(columns).each(function(key, column){
        if(element.show_fields.indexOf(column) >= 0)
          new_columns.push(column);
      });
      return new_columns;
    };
  })
  .directive('changeMenu', ['$window', '$rootScope', '$timeout' ,function ($window, $rootScope, $timeout) {
    return {
      link: function (scope, elem, attr){
        angular.element(elem).click(function(ev){
          $timeout(function(){
            scope.$apply(function(){
              $rootScope.$emit('WINDOW_RESIZE');
            });
          });
        });
      }
    }
  }])
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
  .run(['$rootScope', 'Dashboard', 'AlertService', 'DashboardGroup',
    function($rootScope, Dashboard, AlertService, DashboardGroup){
      $rootScope.dashboardGroups = DashboardGroup.query();
      $rootScope.setOpenMenu = function(menu, subMenu){
        if(menu == $rootScope.menuOpen && !subMenu)
          menu = '';
        $rootScope.menuOpen = menu;
        if (!subMenu || subMenu == $rootScope.subMenuOpen)
          subMenu = '';
        $rootScope.subMenuOpen = subMenu;
      };
      $rootScope.$watch('dashboardFilter.$', function(newVal, oldVal){
        if(newVal && newVal != "")
          $rootScope.menuOpen = 'dashboard';
      });
      $rootScope.groupUndefined = function(dashboard) {
        var ret = true;
        $($rootScope.dashboardGroups).each(function(key_group, group){
          $(group.dashboards).each(function(key_dash, dash){
            if(dash.id == dashboard.slug)
              ret = false;
          });
        });
        return ret;
      };
      $rootScope.dashboards = Dashboard.query();
      $rootScope.$on('$routeChangeStart', function (ev, to, toParams, from, fromParams) {
        AlertService.clearTemporarios();
      });
    }
  ])
;
