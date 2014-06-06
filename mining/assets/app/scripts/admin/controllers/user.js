'use strict';
admin.controller('UserCtrl', ['$scope', 'User', 'AlertService', 'Dashboard', 'AuthenticationService', '$rootScope',
    function ($scope, User, AlertService, Dashboard, AuthenticationService, $rootScope) {
      $rootScope.inSettings = true;
      $scope.users = User.query();
      $scope.permissions = Dashboard.getFullList();
      $scope.my_permited_dashboards = Dashboard.getFullList();
      $scope.user = new User();
      $scope.editing = false;
      $scope.change_pass = false;
      $scope.rules = ['user', 'admin', 'root'];
      function clearPermissions() {
        $($scope.permissions).each(function (key, dash) {
          dash.permitted = false;
          $(dash.element).each(function (key, elem) {
            elem.permitted = false;
          });
        });
      }

      $scope.selectUser = function (us) {
        $scope.user = us;
        $scope.editing = true;
        $scope.change_pass = false;
        clearPermissions();
        $($scope.permissions).each(function (key, dash) {
          if ($scope.user.permissions[dash.slug]) {
            dash.permitted = true;
            $(dash.element).each(function (key, elem) {
              if ($scope.user.permissions[dash.slug].indexOf(elem.slug) >= 0)
                elem.permitted = true;
            });
          }
        });
      };
      $scope.selectDashboard = function (da) {
        for (var x = 0; x < da.element.length; x++) {
          da.element[x].permitted = !da.permitted;
        }
      };
      $scope.deleteUser = function (user) {
        User.delete({}, {'username': user.username});
        $scope.users.splice($scope.users.indexOf(user), 1);
        $scope.newForm();
      };
      $scope.changePass = function (user) {
        $scope.user = user;
        $scope.editing = false;
        $scope.change_pass = true;
        clearPermissions();
      };
      $scope.selectElement = function (dashboard) {
        dashboard.permitted = true;
      };
      $scope.save = function () {
        var current_perm = $scope.user.permissions;
        var new_perm = {};
        $($scope.permissions).each(function (key, dash) {
          if (dash.permitted) {
            new_perm[dash.slug] = [];
            $(dash.element).each(function (key, elem) {
              if (elem.permitted)
                new_perm[dash.slug].push(elem.slug);
            });
          }
        });
        if (AuthenticationService.getUser().rule == 'admin') {
          // PERMISSIONS MERGE
          mining.utils.deepExtend(current_perm, new_perm);
          $($scope.my_permited_dashboards).each(function (key, dashboard) {
            if (!(dashboard.slug in Object.keys(new_perm))) {
              if (current_perm[dashboard.slug]) {
                if (current_perm[dashboard.slug].length == dashboard.element.length)
                  delete current_perm[dashboard.slug];
              }
            }
            $(dashboard.element).each(function (key, element) {
              if (!(element.slug in mining.utils.getNestedProp(new_perm, dashboard.slug, []))) {
                if (mining.utils.getNestedProp(current_perm, dashboard.slug, []).indexOf(element.slug) > -1)
                  delete current_perm[dashboard.slug][current_perm[dashboard.slug].indexOf(element.slug)];
              }
            });
          });
          $scope.user.permissions = current_perm;
        } else {
          $scope.user.permissions = new_perm;
        }
        if ($scope.editing) {
          User.update({'username': $scope.user.username}, $scope.user);
          if ($scope.user.username == AuthenticationService.getUser().username) {
            AuthenticationService.setUser($scope.user);
          }
        } else {
          $scope.user.$save().then(function (response) {
            AlertService.add('success', 'Save ok');
            $scope.users.push(response);
          });
        }
        $scope.newForm();
      };
      $scope.newForm = function () {
        $scope.user = new User();
        $scope.editing = false;
        $scope.change_pass = false;
        clearPermissions();
      };
    }
  ]
);