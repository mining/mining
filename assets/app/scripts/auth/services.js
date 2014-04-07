'use strict';
auth
  .factory('AuthenticationService', ['$http', 'SessionService', '$q', '$timeout',
    function ($http, SessionService, $q, $timeout) {
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

        hasPermission: function(permission, type, dashboard){
          if (type == 'dashboard')
            return SessionService.currentUser.permissions.hasOwnProperty(permission);
          else if(type == 'element' && dashboard)
            return SessionService.currentUser.permissions[dashboard].indexOf(permission) >= 0;
          return false;
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
;