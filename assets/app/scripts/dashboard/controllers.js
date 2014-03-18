'use strict';
dashboard
.controller('HomeCtrl',
  ['$scope', function($scope) {
  }])
.controller('DashboardDetailCtrl', 
  ['$scope', '$routeParams', 'AlertService', 'current_dashboard', 'Element', '$anchorScroll',
  function($scope, $routeParams, AlertService, current_dashboard, Element, $anchorScroll){

    $scope.gotoBottom = function (hash){
      $location.hash(hash);
      $anchorScroll();
    }

    function loadGrid(el){
      var API_URL = "ws://"+ location.host +"/process/" + el.slug + ".ws?";
      for (var key in el.filters){
        API_URL += key + "=" + el.filters[key] + "&";
      }
      API_URL += 'page=' + el.current_page + "&";

      var sock = new WebSocket(API_URL);
      sock.onmessage = function (e) {
        var data = JSON.parse(e.data.replace(/NaN/g,'null'));
        console.log(data);
        if (data.type == 'columns') {
          e.columns = data.data;
        }else if (data.type == 'max_page') {
          e.total_pages = Math.ceil(data.data/50);
        }else if (data.type == 'data') {
          e.process.push(data.data);
        }else if (data.type == 'close') {
          sock.close();
        }
        $timeout(function(){
          $scope.$apply();
        });
      };
    }

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