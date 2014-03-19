'use strict';
dashboard
.controller('HomeCtrl',
  ['$scope', function($scope) {
  }])
.controller('DashboardDetailCtrl', 
  ['$scope', '$routeParams', 'AlertService', 'current_dashboard', 'Element', '$anchorScroll', '$timeout', '$http',
  function($scope, $routeParams, AlertService, current_dashboard, Element, $anchorScroll, $timeout, $http){

    $scope.gotoBottom = function (hash){
      $location.hash(hash);
      $anchorScroll();
    }

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
      loadGrid(el);
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
        process : [],
      });
      // Element.loadData({'slug': val.slug, 'page': val.current_page, 'filters': val.filters});
      if($scope.selected_dashboard.element[ind].type == 'grid')
        loadGrid(val);
    });
    // $scope.xkey = 'range';

    // $scope.ykeys = ['total_tasks', 'total_overdue'];

    // $scope.labels = ['Total Tasks', 'Out of Budget Tasks'];

    // $scope.myModel = [
    // { range: 'January', total_tasks: 5, total_overdue: 5 },
    // { range: 'January', total_tasks: 35, total_overdue: 8 },
    // { range: 'January', total_tasks: 20, total_overdue: 1 },
    // { range: 'January', total_tasks: 20, total_overdue: 6 }
    // ];

    // $http({method: 'GET', url: '/api/element/cube/top-bonus'}).
    // success(function(data, status, headers, config) {
    //     // here I would populate myModel with values from above url. 
    //     // But for simplicity, I'm just hardcoding the values(changed slightly) again.
    //     $scope.myModel = [
    //     // changing just one value in first row.
    //     { range: 'January', total_tasks: 25, total_overdue: 5 },
    //     { range: 'January', total_tasks: 35, total_overdue: 8 },
    //     { range: 'January', total_tasks: 20, total_overdue: 1 },
    //     { range: 'January', total_tasks: 20, total_overdue: 6 }
    //     ];
    //     console.log('success ' + $scope.myModel[0].total_tasks);

    //   }).
    // error(function(data, status, headers, config) {
    //   console.log('error');
    // });

    }
])
;