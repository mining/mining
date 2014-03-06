"use strict";

var getNestedProp = function (obj, propString, fallback) {

  if (!propString) return obj;
  var prop, props = propString.split('.');

  for (var i = 0, iLen = props.length - 1; i <= iLen; i++) {
    prop = props[i];

    if (typeof obj == 'object' && obj !== null && prop in obj) {
      obj = obj[prop];
    }
    else
      return fallback;
  }

  return obj;
};

angular.module('OpenMining', ["highcharts-ng"])

  .run(function($rootScope){
    $rootScope.operators = [
      {key: 'gte', value: 'gte'},
      {key: 'lte', value: 'lte'},
      {key: 'is', value: 'is'},
      {key: 'in', value: 'in'},
      {key: 'between', value: 'between'}
    ];
    $rootScope.types = [
      {key: 'date', value: 'Date'},
      {key: 'int', value: 'Integer'},
      {key: 'str', value: 'String'}
    ];

  })

  .factory('LineChart', function($http){
    return {
      'getConfig':function(URL){
        return $http.post(URL)
      }
    };
  })

  .controller('Process',
  function($scope, $http, $location, $timeout) {
    $scope.loading = true;
    $scope.filters = {};
    $scope.current_page = 1;
    $scope.total_pages = undefined;
    $scope.pages = [];

    $scope.getPages = function(){
      $scope.pages = [];
      for(var x = $scope.current_page-3; x<=$scope.current_page+3; x++){
        if(x>0 && x<=$scope.total_pages)
          $scope.pages.push(x);
      }
      return $scope.pages;
    };

    $scope.selectPage = function(slug, p){
      if(p!=$scope.current_page){
        $scope.current_page = p;
        $scope.gridload(slug);
      }
    };

    $scope.$watch('filter_type', function(newVal){
      if(getNestedProp(newVal, 'key', '') == 'date')
        $scope.filter_format = ":Y-:m-:d";
      else
        $scope.filter_format = "";
    });

    $scope.addFilter = function(){
      var chave = 'filter__'+$scope.filter_field+"__"+$scope.filter_operator.key+'__'+$scope.filter_type.key;
      if ($scope.filter_format)
        chave = chave + '__'+$scope.filter_format;
      $scope.filters[chave] = $scope.filter_value;
    };
    $scope.removeFilter = function(index){
      delete $scope.filters[index];
    };

    $scope.export = function(type, link){
      var url = link+'.'+type+'?';
      for (var key in $scope.filters){
        url += key + "=" + $scope.filters[key] + "&";
      }
      window.open(url);
    };

    $scope.gridload = function(slug) {
      $scope.process = [];

      var API_URL = "ws://"+ location.host +"/process/" + slug + ".ws?";
      for (var key in $scope.filters){
        API_URL += key + "=" + $scope.filters[key] + "&";
      }
      API_URL += 'page=' + $scope.current_page + "&";

      var sock = new WebSocket(API_URL);
      sock.onmessage = function (e) {
        var data = JSON.parse(e.data.replace(/NaN/g,'null'));

        if (data.type == 'columns') {
          $scope.columns = data.data;
        }else if (data.type == 'max_page') {
          $scope.total_pages = Math.ceil(data.data/50);
        }else if (data.type == 'data') {
          $scope.process.push(data.data);
        }else if (data.type == 'close') {
          sock.close();
        }

        $timeout(function(){
          $scope.$apply();
        });

        $scope.loading = false;
      };
    };

    $scope.applyFilters = function(slug){
      $scope.current_page = 1;
      $scope.total_pages = undefined;
      $scope.pages = [];
      $scope.gridload(slug);
    };
    $scope.init = function(slug) {
      $scope.gridload(slug);
    };
  })

  .controller('Chart',
  function($scope, $http, $location, LineChart, $timeout) {
    $scope.loading = true;
    $scope.chartConfig = [];
    $scope.columns = [];
    $scope.process = [];
    $scope.filters = {};

    $scope.$watch('filter_type', function(newVal){
      if(getNestedProp(newVal, 'key', '') == 'date')
        $scope.filter_format = ":Y-:m-:d";
      else
        $scope.filter_format = "";
    });
    $scope.addFilter = function(){
      var chave = 'filter__'+$scope.filter_field+"__"+$scope.filter_operator.key+'__'+$scope.filter_type.key;
      if ($scope.filter_format)
        chave = chave + '__'+$scope.filter_format;
      $scope.filters[chave] = $scope.filter_value;
    };
    $scope.removeFilter = function(index){
      delete $scope.filters[index];
    };

    $scope.chartload = function(slug, categorie, type, title){

      var API_URL = "ws://"+ location.host +"/process/" + slug + ".ws?";
      for (var key in $scope.filters){
        API_URL += key + "=" + $scope.filters[key] + "&";
      }
      $scope.columns = [];
      $scope.process = [];
      $scope.chartConfig[slug] = {
        options: {
          chart: {
            type: type
          }
        },
        series: [],
        title: {
          text: title
        },
        xAxis: {
          currentMin: 0,
          categories: []
        }
      };

      var sock = new WebSocket(API_URL);
      sock.onmessage = function (e) {
        var data = JSON.parse(e.data);

        if (data.type == 'columns') {
          $scope.columns = data.data;
        }else if (data.type == 'data') {
          $scope.process.push(data.data);
        }else if (data.type == 'categories') {
          $scope.chartConfig[slug].xAxis.categories = data.data;
        }else if (data.type == 'close') {
          sock.close();
        }

        var loopseries = {};
        for (var j in $scope.process) {
          for (var c in $scope.process[j]) {
            if (typeof loopseries[c] == 'undefined'){
              loopseries[c] = {};
              loopseries[c].data = [];
            }
            loopseries[c].name = c;
            loopseries[c].data.push($scope.process[j][c]);
          }
        }

        $scope.chartConfig[slug].series = [];
        for (var ls in loopseries){
          if (ls != categorie) {
            $scope.chartConfig[slug].series.push(loopseries[ls]);
          }
        }

        $timeout(function(){
          $scope.$apply();
        });
        $scope.loading = false;
      };
    };

    $scope.applyFilters = function(slug, categorie, type, title){
      $scope.chartload(slug, categorie, type, title);
    };
    $scope.init = function(slug, categorie, type, title) {
      $scope.chartload(slug, categorie, type, title);
    };
  })

  .controller('LoadDashboard',
  function($scope, $http) {
    $http.get("/api/dashboard.json").success(function(data){
      $scope.dashboard_list = data;
    })
  })

  .controller('Ctrl',
  function($scope) {
    $scope.loading = true;
  })

  .controller('CubeQuery', function($scope, $http, $timeout) {
    $scope.testquery = function(){
      $scope.loadcubequery = false;
      $scope.ajaxload = true;
      $scope.force_save=true;
      var sql = angular.element('#sql').val();
      var connection = angular.element('#connection').val();

      $http.post("/api/cubequery.json", {'sql': sql, 'connection': connection})
        .success(function(a){
          if(a.msg != "Error!"){
            $scope.loadcubequery = true;
          }else{
            $scope.loadcubequery = false;
          };
          $scope.status = a.msg;
          $scope.ajaxload = false;
        })
    };
  })

  .controller('ElementCube', function($scope, $http, $timeout) {
    $scope.categorie = '';

    var loadFields = function(){
      $http({method: 'GET',
        url: "/admin/api/element/cube/" + angular.element(document.querySelector('#cube')).val()}).
        success(function(data) {
          $scope._fields = data.columns;

          if($scope.categorie != ""){
            $timeout(function(){
              $scope.$apply(function(){
                $scope.fields = $scope.categorie;
              });
            });
          }
        });
    };

    var showCategories = function(){
      if (angular.element(document.querySelector('#type')).val() != "grid") {
        loadFields();
        $scope.chart = true;
      } else {
        $scope.chart = false;
      }
    };

    angular.element(document.querySelector('#type')).bind('change', function(){
      showCategories();
    });

    angular.element(document.querySelector('#cube')).bind('change', function(){
      $scope.loading = true;
      loadFields();
      $scope.loading = false;
    });

    showCategories();
  });
