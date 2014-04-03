'use strict';
auth
  .factory('AuthenticationService', ['$http', 'SessionService', function ($http, SessionService) {

    'use strict';

    return {

      login: function (user) {
        // this method could be used to call the API and set the user instead of taking it in the function params
        SessionService.currentUser = user;
      },

      isLoggedIn: function () {
        return SessionService.currentUser !== null;
      },
      hasPermission: function(permission, type, dashboard){
        return true;
        if (type == 'dashboard')
          return SessionService.currentUser.permissions.indexOf() >= 0
        else if(type == 'element' && dashboard)
          return SessionService.currentUser.permissions[dashboard].indexOf() >= 0
        return false;
      }
    };
  }])
  .factory('SessionService', function () {

    'use strict';

    return {
      currentUser: null
    };
  })
  .factory('permissions', function ($rootScope) {
    var permissionList;
    return {
      setPermissions: function (permissions) {
        permissionList = permissions;
        $rootScope.$broadcast('permissionsChanged')
      },
      hasPermission: function (permission) {
        permission = permission.trim();
        return _.some(permissionList, function (item) {
          if (_.isString(item.Name))
            return item.Name.trim() === permission
        });
      }
    };
  })
;