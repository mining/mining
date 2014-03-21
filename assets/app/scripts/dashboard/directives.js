'use strict';
/**
 * Created by yuri on 12/03/14.
 * Description: Directives for Dashboard
 */

 dashboard
 .directive('chart', ['$compile', 
  function($compile) {
    var gridTemplate = '<pre>[[ columns | json ]]</pre>';
    var x='<table class="process table table-bordered table-hover"><tr><th ng-repeat="c in columns"><a ng-click="predicate = \'[[c]]\'; reverse=!reverse">[[c]]</a></th></tr><tr ng-repeat="p in process | orderBy:predicate:reverse"><td ng-repeat="c in columns">[[ p[c] ]]</td></tr></table><ul class="pagination"><li ng-class="{\'disabled\':current_page==1}"><a ng-click="selectPage(\'[[d[\'cube\']]]\',1)">First</a></li><li ng-repeat="(key,p) in getPages()" ng-class="{\'active\':p==current_page}"><a ng-click="selectPage(\'[[d[\'cube\']]]\', p)">[[ p ]]</a></li><li ng-class="{\'disabled\':current_page==total_pages}"><a ng-click="selectPage(\'[[d[\'cube\']]]\', total_pages)">Last</a></li></ul>';
    var getTemplate = function(contentType) {
      var template = '';
      switch(contentType) {
        case 'grid':
        template = gridTemplate;
        break;
        case 'line':
        template = '';
        break;
        case 'bar':
        template = '';
        break;
      }
      return template;
    };

    var linker = function($scope, element, attrs) {
      var dashboard_element = JSON.parse(attrs.element);
      var API_URL = "ws://"+ location.host +"/stream/data/" + dashboard_element.slug + "?";
      for (var key in $scope.$parent.filters[dashboard_element]){
        API_URL += key + "=" + $scope.$parent.filters[dashboard_element.slug][key] + "&";
      }
      $scope.total_pages = 0;
      $scope.process = [];
      $scope.current_page = 0;
      $scope.columns = [];

      var sock = new WebSocket(API_URL);
      sock.onmessage = function (e) {
        var data = JSON.parse(e.data.replace(/NaN/g,'null'));
        if(dashboard_element.type == 'grid'){
          API_URL += 'page=' + $scope.current_page + "&";
          if (data.type == 'columns') {
            $scope.columns = data.data;
          }else if (data.type == 'max_page') {
            $scope.total_pages = Math.ceil(data.data/50);
          }else if (data.type == 'data') {
            $scope.process.push(data.data);
          }else if (data.type == 'close') {
            console.log('fechou');
            sock.close();
            element.html(getTemplate('grid')).show();
            $compile(element.contents())($scope);
            console.log('compilou');
          }
        }else if(dashboard_element.type=='chart line'){
          var data = JSON.parse(e.data);
          console.log(data);
          if (data.type == 'columns') {
            $scope.columns = data.data;
          }else if (data.type == 'data') {
            $scope.process.push(data.data);
          }else if (data.type == 'categories') {
            $scope.chartConfig[slug].xAxis.categories = data.data;
          }else if (data.type == 'close') {
            sock.close();
            Morris.Line({
              element: element,
              data: [
              { y: '2006', b: 90 },
              { y: '2007', b: 65 },
              { y: '2008', a: 50,  b: 40 },
              { y: '2009', a: 75,  b: 65 },
              { y: '2010', a: 50,  b: 90 },
              { y: '2011', a: 75},
              { y: '2012', a: 100}
              ],
              xkey: 'y',
              ykeys: ['a', 'b'],
              labels: ['Series A', 'Series B']
            });
          }
        }
      };
    };

    return {
      // required to make it work as an element
      restrict: "E",
      rep1ace: true,
      link: linker,
      scope: {
        'fil': '@filters'
      }
    };
  }]
  )
.directive('barchart', function() {

  return {
    restrict: 'E',
    template: '<div></div>',
    replace: true,
    scope: true,
    link: function($scope, element, attrs) {
      var index= attrs.index;
      var el = $scope.selected_dashboard.element[index],
      xkey = el.xkey,
      ykeys= el.ykeys,
      labels= el.labels,
      data = el.process;
      console.log(data);

      var setData = function(){
        console.log('entrou data', data);
        console.log('inside setData function');
        Morris.Bar({
          element: element,
          data: data,
          xkey: xkey,
          ykeys: ykeys,
          labels: labels
        });
      };
      // The idea here is that when data variable changes, 
      // the setData() is called. But it is not happening.
      attrs.$observe('data',setData);
      // $scope.$watch('selected_dashboard.element.'+index+'.process', setData);
    }

  };

});
;