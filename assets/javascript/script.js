angular.module('OpenMining', ["highcharts-ng"])
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
})


.controller('Chart',
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



        $scope.chartConfig = {
          options: {
            chart: {
              type: 'line',
              zoomType: 'x'
            }
          },
          series: [
            {
              name: "Testando meta dados 1",
              data: [10002, 15987, 12987, 82222, 77622, 16236, 17833, 19787, 15223, 10123]
            },
            {   
              name: "Testando meta dados 2",
              data: [11762, 212319, 231231, 52760, 212330, 10000, 123220]
            }
          ],
          title: {
            text: 'Hello'
          },
          credits: {
            enabled: false
          },
          xAxis: {currentMin: 0, currentMax: 10, minRange: 1},
          loading: false
        }




    };
});
