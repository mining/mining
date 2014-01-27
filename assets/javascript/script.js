angular.module('OpenMining', [])
.value('API_URL', '/process.json?')

.controller('Process',
  function($scope, $http, $location, API_URL) {
    for (var key in $location.search()){
      API_URL += key + "=" + $location.search()[key] + "&";
    }
    console.log(API_URL)
    $scope.loading = true;
    $http({method: 'POST', url: API_URL}).
      success(function(data, status, headers, config) {
        console.log(data)
        $scope.process = data.json;
        $scope.columns = data.columns;
        $scope.predicate = "-id_cliente";
        $scope.loading = false;
      });
});
