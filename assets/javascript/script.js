angular.module('OpenMining', [])
.controller('Process',
  function($scope, $http, $location) {
    $scope.loading = true;
    $scope.init = function(slug) {
      API_URL = "/process/" + slug + ".json?";
      for (var key in $location.search()){
        API_URL += key + "=" + $location.search()[key] + "&";
      };

      $http({method: 'POST', url: API_URL}).
        success(function(data, status, headers, config) {
          $scope.process = data.json;
          $scope.columns = data.columns;
          $scope.loading = false;
        });
    };
});
