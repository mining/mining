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

    var logsOutUserOn401 = ['$q', function ($q) {
      var success = function (response) {
        return response;
      };

      var error = function (response) {
        if (response.status === 401) {
          //redirect them back to login page
          window.location.href="/login";

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
  .run(['$rootScope', '$location', 'AuthenticationService',
    function ($rootScope, $location, AuthenticationService) {
    'use strict';
    $rootScope.AuthService = AuthenticationService;

    $rootScope.$on('$routeChangeStart', function (ev, to, toParams, from, fromParams) {
      // if route requires auth and user is not logged in
      if(AuthenticationService.isLoggedIn()){
        if($location.path().split('/')[1] == 'dashboard'){
          if (!AuthenticationService.hasPermission(to.params.slug, 'dashboard')) {
            $rootScope.$broadcast('alert',{'msg':'Oops, You not have permission!', 'type': 'info', 'hold': true});
            $location.path('/');
          }
        }
      }else{
        ev.preventDefault();
        window.location.href='/login';
      }
    });
  }])
  .controller('LoginCtrl', ['$scope', 'AuthenticationService', '$location', 'SessionService',
    function ($scope, AuthenticationService, $location, SessionService) {
      'use strict';
      var obj_user = {
        "username": "yuripiratello",
        "rule": "root",
        "permissions": {
          "dashboard-bar": ["tipo-bonus-bar"],
          "dashboard-2-graficos": ["tipo-bonus-bar"]
        }
      };
      $scope.loginUser = function () {
        // this should be replaced with a call to your API for user verification (or you could also do it in the service)
        AuthenticationService.login(obj_user)
          .then(function(response){
            SessionService.currentUser = response;
            $location.path('/');
          }, function(response){
            console.log('Login error');
          })
          .finally(function(){
            console.log('Login finally');
          });
      };

      $scope.loginAdmin = function () {
        // this should be replaced with a call to your API for user verification (or you could also do it in the service)
        AuthenticationService.login(obj_user)
          .then(function(response){
            SessionService.currentUser = response;
            $location.path('/');
          }, function(response){
            console.log('Login error');
          })
          .finally(function(){
            console.log('Login finally');
          });
      };
    }
  ])
;