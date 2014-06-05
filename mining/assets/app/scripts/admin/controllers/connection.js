'use strict';
admin.controller('ConnectionCtrl', ['$scope', 'Connection', 'AlertService', '$rootScope',
  function ($scope, Connection, AlertService, $rootScope) {
    $rootScope.inSettings = true;
    $scope.connections = Connection.query();
    $scope.connection = new Connection();
    $scope.selectConnection = function (c) {
      $scope.connection = c;
    };
    $scope.deleteConnection = function (connection) {
      Connection.delete({}, {'slug': connection.slug});
      $scope.connections.splice($scope.connections.indexOf(connection), 1);
    };
    $scope.save = function () {
      if ($scope.connection.slug) {
        Connection.update({'slug': $scope.connection.slug}, $scope.connection);
      } else {
        $scope.connection.$save().then(function (response) {
          AlertService.add('success', 'Save ok');
          $scope.connections.push(response);
        });
      }
      $scope.connection = new Connection();
    };
    $scope.newForm = function () {
      $scope.connection = new Connection();
    };
  }
]);