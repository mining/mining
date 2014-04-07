'use strict';
dashboard
.controller('HomeCtrl',
  ['$scope', function($scope) {
  }])
.controller('DashboardDetailCtrl', 
  ['$scope', '$routeParams', 'AlertService', 'current_dashboard', 'Element', '$anchorScroll', '$timeout', '$http',
    'AuthenticationService', '$rootScope',
  function($scope, $routeParams, AlertService, current_dashboard, Element, $anchorScroll, $timeout, $http,
    AuthenticationService, $rootScope){
    $rootScope.inDashboard = true;

    $scope.gotoBottom = function (hash){
      $location.hash(hash);
      $anchorScroll();
    };

    function loadGrid(el){
      el.process = [];
      var API_URL = "ws://"+ location.host +"/stream/data/" + el.slug + "?";
      for (var key in el.filters){
        API_URL += key + "=" + el.filters[key] + "&";
      }
      API_URL += 'page=' + el.current_page + "&";
      var sock = new WebSocket(API_URL);
      sock.onmessage = function (e) {
        var data = JSON.parse(e.data.replace(/NaN/g,'null'));
        if (data.type == 'columns') {
          el.columns = data.data;
        }else if (data.type == 'max_page') {
          el.total_pages = Math.ceil(data.data/50);
        }else if (data.type == 'data') {
          el.process.push(data.data);
        }else if (data.type == 'close') {
          sock.close();
          $timeout(function(){
            $scope.$apply();
          });
        }
      };
    }

    $scope.getPages = function(el){
      el.pages = [];
      for(var x = el.current_page-3; x<=el.current_page+3; x++){
        if(x>0 && x<=el.total_pages)
          el.pages.push(x);
      }
      return el.pages;
    };

    $scope.selectPage = function(el, p){
      if(p!=el.current_page){
        el.current_page = p;
        loadGrid(el);
      }
    };

    // $scope.$watch('selected_dashboard.element.filter_format', function(newVal, oldVal, scope){
    //   if(getNestedProp(newVal, 'key', '') == 'date'){
    //     debugger;
    //     $scope.filter_format = ":Y-:m-:d";
    //   }else{
    //     $scope.filter_format = "";
    //   }
    // });

    $scope.addFilter = function(el){
      var chave = 'filter__'+el.filter_field+"__"+el.filter_operator.key+'__'+el.filter_type.key;
      if (el.filter_format)
        chave = chave + '__'+el.filter_format;
      var ind = $scope.selected_dashboard.element.indexOf(el);
      $scope.selected_dashboard.element[ind].filters[chave] = el.filter_value;
    };
    $scope.removeFilter = function(el, index){
      delete el.filters[index];
    };
    $scope.applyFilters = function(el){
      el.current_page = 1;
      el.total_pages = undefined;
      el.pages = [];
      if(el.type == 'grid'){
        loadGrid(el);
      }else if(el.type == 'chart_bar'){
        loadBar(el);
      }else if(el.type == 'chart_line'){
        loadLine(el);
      }
    };

    $scope.export = function(el, type, link){
      var url = link+'.'+type+'?';
      for (var key in el.filters){
        url += key + "=" + el.filters[key] + "&";
      }
      window.open(url);
    };

    $scope.selected_dashboard = current_dashboard.data;
    
    $($scope.selected_dashboard.element).each(function(ind, val){
      if(AuthenticationService.hasPermission(val.slug, 'element', $scope.selected_dashboard.slug)){
        angular.extend($scope.selected_dashboard.element[ind], {
          isCollapsed: false,
          filterIsCollapsed: true,
          current_page : 1,
          total_pages : 0,
          filter_operator : '',
          filter_field : '',
          filter_type : '',
          filter_format : '',
          filter_value : '',
          filters : {},
          columns : [],
          process : []
        });
        // Element.loadData({'slug': val.slug, 'page': val.current_page, 'filters': val.filters});
        if($scope.selected_dashboard.element[ind].type == 'grid')
          loadGrid(val);
        else if($scope.selected_dashboard.element[ind].type == 'chart_bar'){
          $scope.selected_dashboard.element[ind].xkey = [$scope.selected_dashboard.element[ind].field_x];
          $scope.selected_dashboard.element[ind].ykeys = [$scope.selected_dashboard.element[ind].field_y];
          $scope.selected_dashboard.element[ind].labels = [$scope.selected_dashboard.element[ind].field_y];
          loadBar(val);
        }else if($scope.selected_dashboard.element[ind].type == 'chart_line'){
          $scope.selected_dashboard.element[ind].xkey = [$scope.selected_dashboard.element[ind].field_x];
          $scope.selected_dashboard.element[ind].labels = [$scope.selected_dashboard.element[ind].field_y];
          loadLine(val);
        }
      }
    });

    function loadBar(el){
      el.process = [];
      var element = 'bar-chart-'+el.slug;
      if(angular.element('#'+element))
        angular.element('#'+element).html('');
      var API_URL = "ws://"+ location.host +"/stream/data/" + el.slug + "?";
      for (var key in el.filters){
        API_URL += key + "=" + el.filters[key] + "&";
      }
      API_URL += 'page=' + el.current_page + "&";
      var sock = new WebSocket(API_URL);
      sock.onmessage = function (e) {
        var data = JSON.parse(e.data.replace(/NaN/g,'null'));
        if (data.type == 'columns') {
          el.columns = data.data;
        }else if (data.type == 'max_page') {
          el.total_pages = Math.ceil(data.data/50);
        }else if (data.type == 'data') {
          el.process.push(data.data);
        }else if (data.type == 'close') {
          sock.close();
          $timeout(function(){
            $scope.$apply(function(){
              Morris.Bar({
                element: element,
                data: el.process,
                xkey: el.xkey,
                ykeys: el.ykeys,
                labels: el.labels
              });
            });
          });
        }
      };
    }
    function loadLine(el){
      el.process = [];
      el.labels = [];
      el.ykeys = [];
      var count = 0;
      var element = 'chart-line-'+el.slug;
      if(angular.element('#'+element))
        angular.element('#'+element).html('');
      var API_URL = "ws://"+ location.host +"/stream/data/" + el.slug + "?";
      for (var key in el.filters){
        API_URL += key + "=" + el.filters[key] + "&";
      }
      API_URL += 'page=' + el.current_page + "&";
      var sock = new WebSocket(API_URL);
      sock.onmessage = function (e) {
        var data = JSON.parse(e.data.replace(/NaN/g,'null'));
        if (data.type == 'columns') {
          el.columns = data.data;
        }else if (data.type == 'max_page') {
          el.total_pages = Math.ceil(data.data/50);
        }else if (data.type == 'data') {
          count=count+1;
          if(el.labels.indexOf(data.data[el.field_serie]) < 0)
              el.labels.push(data.data[el.field_serie]);
          if(el.ykeys.indexOf(data.data[el.field_serie]) < 0)
            el.ykeys.push(data.data[el.field_serie]);
          var have = false;
          var key = -1;
          $(el.process).each(function(i_key, val){
            if(val[el.field_x] == data.data[el.field_x]){
              have = true;
              key = i_key;
            }
          });
          if (!have){
            data.data[data.data[el.field_serie]] = data.data[el.field_y];
            el.process.push(data.data);
          }else{
            el.process[key][data.data[el.field_serie]] = data.data[el.field_y];
          }
        }else if (data.type == 'close') {
          sock.close();
          console.log(count);
          $timeout(function(){
            $scope.$apply(function(){
              Morris.Line({
                element: element,
                data: el.process,
                xkey: el.xkey,
                ykeys: el.ykeys,
                labels: el.labels
              });
            });
          });
        }
      };
    }
  }
])
;