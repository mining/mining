'use strict';
auth
  .controller('PermissionsGroupCtrl', ['$scope', 'User', 'AlertService', 'PermissionsGroup', '$rootScope',
    'Dashboard', '$filter',
    function ($scope, User, AlertService, PermissionsGroup, $rootScope, Dashboard, $filter) {
      $rootScope.inSettings = true;
      $scope.users = User.query();
      $scope.permissionsGroups = new PermissionsGroup.query();
      $scope.permissionsGroup = new PermissionsGroup();
      $scope.permissions = Dashboard.getFullList();
      function clearPermissions() {
        $($scope.permissions).each(function (key, dash) {
          dash.permitted = false;
          $(dash.element).each(function (key, elem) {
            elem.permitted = false;
          });
        });
      }
      $scope.queryAdmins = function (term, result) {
        var ls = [];
        $($scope.users).each(function (key, val) {
          ls.push({
            id: val.username,
            label: val.username
          });
        });
        result($filter('filter')(ls, term));
      };
      $scope.selectPermissionsGroup = function (dg) {
        $scope.permissionsGroup = dg;
        clearPermissions();
        $($scope.permissions).each(function (key, dash) {
          if ($scope.permissionsGroup.permissions[dash.slug]) {
            dash.permitted = true;
            $(dash.element).each(function (key, elem) {
              if ($scope.permissionsGroup.permissions[dash.slug].indexOf(elem.slug) >= 0)
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
      $scope.selectElement = function (dashboard) {
        dashboard.permitted = true;
      };
      $scope.save = function () {
        $scope.permissionsGroup.permissions = {};
        $($scope.permissions).each(function (key, dash) {
          if (dash.permitted) {
            $scope.permissionsGroup.permissions[dash.slug] = [];
            $(dash.element).each(function (key, elem) {
              if (elem.permitted)
                $scope.permissionsGroup.permissions[dash.slug].push(elem.slug);
            });
          }
        });
        if ($scope.permissionsGroup.slug) {
          PermissionsGroup.update({'slug': $scope.permissionsGroup.slug}, $scope.permissionsGroup);
        } else {
          $scope.permissionsGroup.$save().then(function (response) {
            AlertService.add('success', 'Save ok');
            $scope.permissionsGroups.push(response);
          });
        }
        $scope.newForm();
      };
      $scope.newForm = function () {
        $scope.permissionsGroup = new PermissionsGroup();
        clearPermissions();
      };
    }
  ])
;