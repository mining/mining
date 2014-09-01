'use strict';
/**
 * Created by yuri on 12/03/14.
 * Description: Directives for MorriJs charts
 */

dashboard
  .directive('chartBar', ['$compile', '$timeout',
    function ($compile, $timeout) {
      var controller = function ($scope) {
        function loadBar() {
          $scope.element.directive_status = 'running';
          var el = $scope.element;
          el.process = [];
          el.loading = true;
          var element = 'chart-bar-' + el.slug;
          if (angular.element('#' + element))
            angular.element('#' + element).html('');
          var prot = 'ws';
          if (window.protocol == 'https')
            prot = 'wss';
          var API_URL = prot + "://" + location.host + "/stream/data/" + el.slug + "?";
          for (var key in el.filters) {
            API_URL += key + "=" + el.filters[key] + "&";
          }
          API_URL += 'page=' + el.current_page + "&";
          var sock = new WebSocket(API_URL);
          sock.onmessage = function (e) {
            var data = JSON.parse(e.data.replace(/NaN/g, 'null'));
            if (data.type == 'columns') {
              el.columns = data.data;
            } else if (data.type == 'max_page') {
              el.total_pages = Math.ceil(data.data / 50);
            } else if (data.type == 'last_update') {
              el.cube.lastupdate = moment(data.data).format('YYYY-MM-DDTHH:mm:ss');
            } else if (data.type == 'data') {
              el.process.push(data.data);
            } else if (data.type == 'close') {
              sock.close();
              el.loading = false;
              $timeout(function () {
                $scope.$apply(function () {
                  $scope.element.graph = Morris.Bar({
                    element: element,
                    data: $scope.element.process,
                    xkey: $scope.element.xkey,
                    ykeys: $scope.element.ykeys,
                    labels: $scope.element.labels,
                    resize: true,
                    redraw: true
                  });
                  $scope.element.directive_status = 'done';
                });
              });
            }
          };
        }

        $scope.$on('morris-bar-'+ $scope.element.slug, function() {
            loadBar();
        });
        loadBar();
      };
      return {
        // required to make it work as an element
        restrict: "E",
        rep1ace: true,
        controller: controller,
        scope: {
          element: '=',
          filters: '='
        },
        templateUrl: '/assets/app/scripts/dashboard/directives/templates/bar.html'
      };
    }
  ])
;