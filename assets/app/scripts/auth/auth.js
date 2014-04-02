'use strict';
var auth = angular.module('miningApp.auth', [])
  .config(['$routeProvider', function ($routeProvider) {
    $routeProvider
      .when('/login', {
        templateUrl: 'assets/app/views/login.html',
        controller: 'LoginCtrl'
      })
      .when('/admin', {
        templateUrl: 'assets/app/views/admin.html',
        controller: 'AdminCtrl'
      })
      .when('/error', {
        templateUrl: 'assets/app/views/error.html',
        controller: 'LoginCtrl'
      })
      .otherwise({
        redirectTo: '/'
      });
  }])
  .config(['$httpProvider', function ($httpProvider) {
    'use strict';

    var logsOutUserOn401 = ['$q', '$location', function ($q, $location) {
      var success = function (response) {
        return response;
      };

      var error = function (response) {
        if (response.status === 401) {
          //redirect them back to login page
          $location.path('/login');

          return $q.reject(response);
        } else {
          return $q.reject(response);
        }
      };

      return function (promise) {
        return promise.then(success, error);
      };
    }];

    $httpProvider.responseInterceptors.push(logsOutUserOn401);
  }])
  .run(['$rootScope', '$location', 'AuthenticationService', 'SessionService',
    function ($rootScope, $location, AuthenticationService, SessionService) {
    'use strict';
    var yuri = {"username": "yuripiratello", "rule": "root", "permissions": {"dashboard-bar": ["tipo-bonus-bar"], "dashboard-2-graficos": ["tipo-bonus-bar"]}};
    AuthenticationService.login(yuri);

    $rootScope.$on('$routeChangeStart', function (ev, to, toParams, from, fromParams) {
      // if route requires auth and user is not logged in
      if (!AuthenticationService.hasPermission(to.params.slug, 'dashboard'))
        $location.path('/');
//      if (!routeClean($location.url()) && !AuthenticationService.isLoggedIn()) {
//        // redirect back to login
//        ev.preventDefault();
//        $location.path('/login');
//      }
//      else if (routeAdmin($location.url()) && !RoleService.validateRoleAdmin(SessionService.currentUser)) {
//        // redirect back to login
//        ev.preventDefault();
//        $location.path('/error');
//      }
    });
  }])
;