'use strict';
auth
  .directive('hasPermission', ['AuthenticationService',
    function (AuthenticationService) {
      return {
        link: function (scope, element, attrs) {
          if (!_.isString(attrs.hasPermission))
            throw "hasPermission value must be a string";

          var value = attrs.hasPermission.trim();
          var notPermissionFlag = value[0] === '!';
          if (notPermissionFlag) {
            value = value.slice(1).trim();
          }

          function toggleVisibilityBasedOnPermission() {
            var hasPermission = AuthenticationService.hasPermission(value);

            if (hasPermission && !notPermissionFlag || !hasPermission && notPermissionFlag)
              element.show();
            else
              element.hide();
          }

          toggleVisibilityBasedOnPermission();
          scope.$on('permissionsChanged', toggleVisibilityBasedOnPermission);
        }
      };
    }
  ]);