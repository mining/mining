'use strict';
/**
 * Created by yuri on 12/03/14.
 * Description: Directives for Dashboard
 */

dashboard
  .directive('chart', [function() {

    var getTemplate = function(contentType) {
      var template = '';
      switch(contentType) {
        case 'grid':
            template = imageTemplate;
            break;
        case 'line':
            template = videoTemplate;
            break;
        case 'bar':
            template = noteTemplate;
            break;
      }
      return template;
    };

    var linker = function($scope, element, attrs) {
        var dashboard_element = attrs.element;
        var API_URL = "ws://"+ location.host +"/process/" + dashboard_element.slug + ".ws?";
        for (var key in $scope.$parent.filters[dashboard_element]){
          API_URL += key + "=" + $scope.$parent.filters[dashboard_element.slug][key] + "&";
        }
        if(dashboard_element.type == 'grid'){

        }else if(dashboard_element.type=='chart line'){
          var sock = new WebSocket(API_URL);
          sock.onmessage = function (e) {
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
            }
          };

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
  }])
;