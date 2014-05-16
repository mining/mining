'use strict';
auth
  .filter('checkElementPermission',
    ['AuthenticationService',
      function(AuthenticationService){
        return function(elements, dashboard){
          return elements.filter(
            function(element, index, array){
              if(AuthenticationService.hasPermission(element.slug, 'element', dashboard))
                return element;
            }
          );
        }
      }
    ]
  )
  .filter('checkDashboardPermission',
    ['AuthenticationService',
      function(AuthenticationService){
        return function(dashboards){
          return dashboards.filter(
            function(dashboard, index, array){
              if(AuthenticationService.hasPermission(dashboard.slug, 'dashboard'))
                return dashboard;
            }
          );
        }
      }
    ]
  )
  .filter('checkDashboardDirectoryPermission',
    ['AuthenticationService',
      function(AuthenticationService){
        return function(dashboards){
          return dashboards.filter(
            function(dashboard, index, array){
              return dashboard;
//              TODO: Check group permission
//              if(AuthenticationService.hasPermission(dashboard.slug, 'dashboard'))
//                return dashboard;
            }
          );
        }
      }
    ]
  )
;