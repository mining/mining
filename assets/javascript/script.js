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
    $scope.init = function(slug, categorie, type, title) {
      API_URL = "/process/" + slug + ".json?";
      for (var key in $location.search()){
        API_URL += key + "=" + $location.search()[key] + "&";
      };

      $http({method: 'POST', url: API_URL}).
        success(function(data, status, headers, config) {
          $scope.loading = false;

          var series = {};
          var loopseries = {}
          for (j in data.json) {
            for (c in data.json[j]) {
              if (typeof loopseries[c] == 'undefined'){
                loopseries[c] = {};
                loopseries[c].data = [];
              }
              loopseries[c].name = c;
              loopseries[c].data.push(data.json[j][c]);
            }
          }
          series[slug] = []
          for (ls in loopseries){
            if (ls != categorie) {
              series[slug].push(loopseries[ls]);
            }
          }

          $scope.chartConfig = {
            options: {
              chart: {
                type: type
              }
            },
            series: series[slug],
            title: {
              text: title
            },
            xAxis: {
              categories: loopseries[categorie].data
            }
          };
        });
    };
});
