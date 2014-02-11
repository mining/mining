"use strict";
angular.module('OpenMining', ["highcharts-ng"])
  .factory('LineChart', function($http){
    var return_val = {
      'getConfig':function(URL){
        return $http.post(URL)
      }
    };
    return return_val;
  })
  .controller('Process',
  function($scope, $http, $location) {
    $scope.loading = true;
    $scope.init = function(slug) {
      var API_URL = "/process/" + slug + ".json?";
      for (var key in $location.search()){
        API_URL += key + "=" + $location.search()[key] + "&";
      }

      $http({method: 'POST', url: API_URL}).
        success(function(data, status, headers, config) {
          $scope.process = data.json;
          $scope.columns = data.columns;
          $scope.loading = false;
        });
    };
  })
  .controller('Chart',
  function($scope, $http, $location, LineChart) {
    $scope.loading = true;
    $scope.columns = [];
    $scope.chartConfig = {};
    $scope.filters = {};
    $scope.operators =[
      { key:'gte'     ,value : 'gte'},
      { key:'lte'     ,value: 'lte'},
      { key:'is'      ,value: 'is'},
      { key:'in'      ,value: 'in'},
      { key:'between' ,value: 'between'}
    ];
    $scope.types=[
      { key:'date'     ,value : 'Date'},
      { key:'int'     ,value: 'Integer'},
      { key:'str'      ,value: 'String'}
    ];
    $scope.addFilter = function(){
      $scope.filters['filter__'+$scope.filter_field+"__"+$scope.filter_operator.key+'__'+$scope.filter_type.key] = $scope.filter_value;
    };
    function makeChart(API_URL, slug, categorie, type, title){
      LineChart.getConfig(API_URL)
        .success(function(data, status, headers, config) {
          $scope.columns = data.columns;
          var series = {};
          var loopseries = {}
          for (var j in data.json) {
            for (var c in data.json[j]) {
              if (typeof loopseries[c] == 'undefined'){
                loopseries[c] = {};
                loopseries[c].data = [];
              }
              loopseries[c].name = c;
              loopseries[c].data.push(data.json[j][c]);
            }
          }
          series[slug] = []
          for (var ls in loopseries){
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
    }

    $scope.applyFilters = function(slug, categorie, type, title){
      var API_URL = "/process/" + slug + ".json?";
      for (var key in $scope.filters){
        API_URL += key + "=" + $scope.filters[key] + "&";
      }
      makeChart(API_URL, slug, categorie, type, title);
    };
    $scope.init = function(slug, categorie, type, title) {
      var API_URL = "/process/" + slug + ".json?";
      for (var key in $location.search()){
        API_URL += key + "=" + $location.search()[key] + "&";
      }
      makeChart(API_URL, slug, categorie, type, title);
    };
  });
