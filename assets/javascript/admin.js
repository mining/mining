angular.module('MiningAdmin', [])

.controller('Ctrl',
  function($scope, $http) {
    $scope.loading = true;
})

.controller('ElementCube', function($scope, $http) {

  angular.element(document.querySelector('#type')).bind('change', function(){
    if (angular.element(document.querySelector('#type')).val() != "grid") {
      $scope.chart = true;
    } else {
      $scope.chart = false;
    }
    $scope.$apply();
  });

  angular.element(document.querySelector('#cube')).bind('change', function(){
    $scope.loading = true;
    $http({method: 'GET',
      url: "/admin/api/element/cube/" + angular.element(document.querySelector('#cube')).val()}).
      success(function(data, status, headers, config) {
        $scope._fields = data.columns;
        $scope.loading = false;
      });
    $scope.$apply();
  });
});
