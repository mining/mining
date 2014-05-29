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
  .filter('checkGroupsPermissions',
    ['AuthenticationService',
      function(AuthenticationService){
        return function(group){
          return group.filter(
            function(group, index, array){
              var have = false;
              $(group.dashboards).each(function(key, dashboard){
                if(AuthenticationService.hasPermission(dashboard.id, 'dashboard'))
                  have = true;
              });
              if(have)
                return group;
            }
          );
        }
      }
    ]
  )
;