'use strict';
auth
  .factory('AuthenticationService', ['$http', 'SessionService', '$q', '$timeout', '$rootScope',
    function ($http, SessionService, $q, $timeout, $rootScope) {
      'use strict';

      return {

        login: function (user) {
          // this method could be used to call the API and set the user instead of taking it in the function params
          var deferred = $q.defer();
          // TODO: make url to login
          $timeout(function(){
            deferred.resolve(user);
          }, 200);
          return deferred.promise;
        },

        logout: function(){
          $http.get('/api/user/logout')
            .success(function(response){
              window.location.href='/';
            })
            .error(function(response){
              window.location.href='/';
            });
        },

        isLoggedIn: function () {
          return SessionService.currentUser !== null;
        },

        getUser: function () {
          return SessionService.currentUser;
        },

        refreshUser: function(){
          var deferred = $q.defer();
          // TODO: make url get
          $timeout(function(){
            var yuri = {
              "username": "yuripiratello",
              "rule": "root",
              "permissions": {
                "dashboard-bar": ["tipo-bonus-bar"], "dashboard-2-graficos": ["tipo-bonus-bar"]
              }
            };
            deferred.resolve(yuri);
          }, 2000);
          return deferred.promise;
        },

        setUser: function(data){
          SessionService.currentUser = data;
        },

        hasPermission: function(permission, type, dashboard){
          if (SessionService.currentUser.rule == 'root' || SessionService.currentUser.rule == 'admin')
            return true;
          var perm = false;
          if (type == 'dashboard'){
            if(SessionService.currentUser.permissions.hasOwnProperty(permission))
              perm = true;
            if(SessionService.currentUser.is_admin_group)
              $(SessionService.currentUser.is_admin_group).each(function(key, dg){
                if(dg.permissions.hasOwnProperty(permission))
                  perm = true;
              });
            return perm;
          }else if(type == 'element' && dashboard)
            if(SessionService.currentUser.permissions[dashboard] &&
              SessionService.currentUser.permissions[dashboard].indexOf(permission) >= 0)
              perm = true;
            if(SessionService.currentUser.is_admin_group)
              $(SessionService.currentUser.is_admin_group).each(function(key, dg){
                if(dg.permissions.hasOwnProperty(dashboard) && dg.permissions[dashboard].indexOf(permission) >= 0)
                  perm = true;
              });
          return perm;
        },

        userIsAdminGroup : function(){
          if(SessionService.currentUser.rule == 'root')
            return true;
          return SessionService.currentUser.is_admin_group;
        }
      };
    }
  ])
  .factory('SessionService', function () {

    'use strict';

    return {
      currentUser: null
    };
  })
  .factory('PermissionsGroup', ['$resource',
    function($resource){
      return $resource('/api/permissions_group/:slug', {}, {
        update : { method: 'PUT', params: {'slug': '@slug'}}
      });
    }
  ])
;
