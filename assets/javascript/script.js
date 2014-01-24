angular.module('OpenMining', [])
.value('API_URL', '/process.json?fields=')

.controller('Process',
  function($scope, $http, API_URL) {
    $scope.loading = true;
    $http({method: 'POST', url: API_URL}).
      success(function(data, status, headers, config) {
        $scope.process = data.json;
        $scope.columns = data.columns;
        $scope.predicate = "-id_cliente";
        $scope.loading = false;
      });
});
