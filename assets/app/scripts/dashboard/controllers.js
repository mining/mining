'use strict';
dashboard
.controller('HomeCtrl',
  ['$scope', function($scope) {
  }])
.controller('DashboardDetailCtrl', 
  ['$scope', '$routeParams', 'AlertService', 'current_dashboard', 'Element', '$anchorScroll', '$timeout',
  function($scope, $routeParams, AlertService, current_dashboard, Element, $anchorScroll, $timeout){

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
      console.log(API_URL);
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

    $scope.selected_dashboard = current_dashboard.data;
    $($scope.selected_dashboard.element).each(function(ind, val){
      angular.extend($scope.selected_dashboard.element[ind], {
        current_page : 1,
        total_pages : 0,
        filter_operator : '',
        filter_field : '',
        filter_type : '',
        filter_format : '',
        filter_value : '',
        filters : [],
        columns : [],
        process : [],
      });
      // Element.loadData({'slug': val.slug, 'page': val.current_page, 'filters': val.filters});
      loadGrid(val);
    });
  }
  ])
;