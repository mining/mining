'use strict';
var auth = angular.module('miningApp.auth', [])
  .config(['$routeProvider', function ($routeProvider) {
    $routeProvider
      .when('/new_user', {
        templateUrl: 'assets/app/views/new_user.html',
        controller: 'NewUserCtrl'
      })
      .when('/admin', {
        templateUrl: 'assets/app/views/admin.html',
        controller: 'AdminCtrl'
      })
      .when('/admin/permissions-group', {
        templateUrl: 'assets/app/views/permissions_group.html',
        controller: 'PermissionsGroupCtrl'
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
  .run(['$rootScope', '$location', 'AuthenticationService', 'getCurrentUser', 'AlertService', 'newUser',
    function ($rootScope, $location, AuthenticationService, getCurrentUser, AlertService, newUser) {
    'use strict';
    $rootScope.AuthService = AuthenticationService;
    if(newUser)
      $rootScope.new_user = true;
    AuthenticationService.setUser(getCurrentUser);
    $location.url($location.path());


    $rootScope.$on('$routeChangeStart', function (ev, to, toParams, from, fromParams) {
      // if route requires auth and user is not logged in
      if(AuthenticationService.isLoggedIn()){
        if($rootScope.new_user && $location.path() != '/new_user'){
          $location.path('/new_user');
        }else{
          if($location.path().split('/')[1] == 'dashboard'){
            if (!AuthenticationService.hasPermission(to.params.slug, 'dashboard')) {
              AlertService.add({'msg':'Oops, You not have permission!', 'type': 'warning', 'hold': true});
              $location.path('/');
            }
          }else if($location.path().split('/')[1] == 'admin'){
            if(AuthenticationService.getUser().rule =='user' && !AuthenticationService.userIsAdminGroup()){
              AlertService.add({'msg':'Oops, You not have permission!', 'type': 'warning', 'hold': true});
              $location.path('/');
            }
          }
        }
      }else{
        ev.preventDefault();
        window.location.href='/';
      }
    });
  }])
  .controller('NewUserCtrl', ['$scope', 'AuthenticationService', '$location', 'User', 'AlertService', '$rootScope',
    function ($scope, AuthenticationService, $location, User, AlertService, $rootScope) {
      'use strict';
      $scope.user = AuthenticationService.getUser();
      $scope.saveNewUser = function(){
        var tmp_user = new User();
        angular.extend(tmp_user,$scope.user);
        tmp_user.permissions = [];
        tmp_user.rule = 'user';
        tmp_user.$save()
          .then(function(response) {
            AlertService.add({type:'success', msg:'Save ok', hold:true});
            $rootScope.new_user = false;
            $location.path('/');
          });
      };
//      SessionService.currentUser = response;
    }
  ])
;