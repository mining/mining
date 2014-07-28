'use strict';
dashboard
  .controller('HomeCtrl',
    ['$scope', function ($scope) {
    }])
  .controller('DashboardDetailCtrl',
    ['$scope', '$routeParams', 'AlertService', 'current_dashboard', 'Element', '$anchorScroll', '$timeout', '$http',
      'AuthenticationService', '$rootScope', 'Filter', '$interval',
      function ($scope, $routeParams, AlertService, current_dashboard, Element, $anchorScroll, $timeout, $http, AuthenticationService, $rootScope, Filter, $interval) {
        $rootScope.inDashboard = true;

        $scope.filter_name = undefined;

        $scope.gotoBottom = function (hash) {
          $location.hash(hash);
          $anchorScroll();
        };

        $scope.isNumber = function(n){
            return !isNaN(n);
        };

        function loadGrid(el) {
          el.from = (el.current_page-1)*50+1;
          el.process = [];
          el.loading = true;
          var prot = 'ws';
          if (window.protocol == 'https')
            prot = 'wss';
          var API_URL = prot + "://" + location.host + "/stream/data/" + el.slug + "?";
          for (var key in el.filters) {
            API_URL += key + "=" + el.filters[key] + "&";
          }
          API_URL += 'page=' + el.current_page + "&";
          if (el.orderby)
            API_URL += 'orderby=' + el.orderby + "&orderby__order=" + el.orderby__order;
          var sock = new WebSocket(API_URL);
          sock.onmessage = function (e) {
            var data = JSON.parse(e.data.replace(/NaN/g, 'null'));
            if (data.type == 'columns') {
              el.columns = data.data;
            } else if (data.type == 'max_page') {
              el.total_rows = data.data;
              el.total_pages = Math.ceil(data.data / 50);
            } else if (data.type == 'last_update') {
              el.cube.lastupdate = moment(data.data).format('YYYY-MM-DDTHH:mm:ss');
            } else if (data.type == 'data') {
              el.process.push(data.data);
            } else if (data.type == 'close') {
              sock.close();
              el.to = el.from + 49;
              if (el.process.length < 50)
                el.to = el.process.length;
              el.loading = false;
              $timeout(function () {
                $scope.$apply();
              });
            }
          };
        }

        $scope.getRefreshElementDetail = function(el){
          if($scope.selected_dashboard.scheduler_type && $scope.selected_dashboard.refresh_elements){
            return $scope.selected_dashboard.scheduler_interval + ' ' + $scope.selected_dashboard.scheduler_type;
          }else if(el.scheduler_type){
            return el.scheduler_interval + ' ' + el.scheduler_type;
          }
        };

        $scope.getPages = function (el) {
          el.pages = [];
          for (var x = el.current_page - 3; x <= el.current_page + 3; x++) {
            if (x > 0 && x <= el.total_pages)
              el.pages.push(x);
          }
          return el.pages;
        };

        $scope.selectPage = function (el, p) {
          if (p != el.current_page) {
            el.current_page = p;
            loadGrid(el);
          }
        };

        $scope.addFilter = function (el) {
          var chave = 'filter__' + el.filter_field + "__" + el.filter_operator + '__' + el.filter_type;
          if (el.filter_format)
            chave = chave + '__' + el.filter_format;
          var ind = $scope.selected_dashboard.element.indexOf(el);
          $scope.selected_dashboard.element[ind].filters[chave] = el.filter_value;
        };
        $scope.removeFilter = function (el, index) {
          delete el.filters[index];
        };
        $scope.applyFilters = function (el) {
          el.current_page = 1;
          el.total_pages = undefined;
          el.pages = [];
          if (el.type == 'grid') {
            loadGrid(el);
          } else if (el.type == 'chart_bar') {
            loadBar(el);
          } else if (el.type == 'chart_line') {
            loadLine(el);
          }
        };

        $scope.startSaveSettings = function (ele) {
          if (!ele.saveSettings)
            ele.saveSettings = true;
        };

        $scope.saveFilters = function (el) {
          var tmp_filters = angular.copy(el.filters);
          tmp_filters['element'] = el.slug;
          tmp_filters['name'] = el.filter_name;
          var newFilter = new Filter();
          angular.extend(newFilter, tmp_filters);
          if (el._filter.name == el.filter_name) {
            newFilter['slug'] = el._filter['slug'];
            newFilter.$update()
              .then(function (response) {
                $(el.saved_filters).each(function (ind, filt) {
                  if (filt.slug == el._filter.slug)
                    el.saved_filters[ind] = response;
                });
                el.saveSettings = false;
                el.filter_name = '';
                el.filter_operator = '';
                el.filter_field = '';
                el.filter_type = '';
                el.filter_format = '';
                el.filter_value = '';
                el._filter = response;
                el.filter_message = {'status': 'success', 'msg': 'Success!'};
              });
          } else {
            newFilter.$save()
              .then(function (response) {
                el.saved_filters.push(response);
                el.saveSettings = false;
                el.filter_name = '';
                el.filter_operator = '';
                el.filter_field = '';
                el.filter_type = '';
                el.filter_format = '';
                el.filter_value = '';
                el.filter_message = {'status': 'success', 'msg': 'Success!'};
              });
          }
        };

        $scope.export = function (el, type, link) {
          var url = link + '.' + type + '?';
          for (var key in el.filters) {
            url += key + "=" + el.filters[key] + "&";
          }
          window.open(url);
        };
        $scope.removeOrder = function (el, field) {
          el.current_page = 1;
          el.total_pages = undefined;
          el.pages = [];
          var ind = el.orderby.indexOf(field);
          el.orderby__order.splice(ind, 1);
          el.orderby.splice(ind, 1);
          if (el.type == 'grid') {
            loadGrid(el);
          } else if (el.type == 'chart_bar') {
            loadBar(el);
          } else if (el.type == 'chart_line') {
            loadLine(el);
          }
        };
        $scope.removeOrder = function (el, field) {
          el.current_page = 1;
          el.total_pages = undefined;
          el.pages = [];
          el.orderby.splice(el.orderby.indexOf(field), 1);
          el.orderby__order.splice(el.orderby.indexOf(field), 1);
          if (el.type == 'grid') {
            loadGrid(el);
          } else if (el.type == 'chart_bar') {
            loadBar(el);
          } else if (el.type == 'chart_line') {
            loadLine(el);
          }
        };
        $scope.applyOrder = function (el, field, asc) {
          el.current_page = 1;
          el.total_pages = undefined;
          el.pages = [];
          if (!el.orderby)
            el.orderby = [];
          if (!el.orderby__order)
            el.orderby__order = [];
          if (el.orderby.indexOf(field) < '0') {
//            Advanced Order TODO: Flow to advanced order
//            el.orderby.push(field);
            el.orderby = [field];
          }
//          Advanced Order TODO: Flow to advanced order
//          el.orderby__order[el.orderby.indexOf(field)] = '0';
//          if (asc == '0')
//            el.orderby__order[el.orderby.indexOf(field)] = '1';
          el.orderby__order = ['0'];
          if (asc == '0')
            el.orderby__order = ['1'];

          if (el.type == 'grid') {
            loadGrid(el);
          } else if (el.type == 'chart_bar') {
            loadBar(el);
          } else if (el.type == 'chart_line') {
            loadLine(el);
          }
        };

        $scope.selectDateFilter = function(widget, field){
          if(field == 'until'){
            if(!widget.value.from || widget.value.from == ''){
              widget.value.from = widget.value.until;
            }
          }else if(field == 'from'){
            if(!widget.value.until || widget.value.until == ''){
              widget.value.until = widget.value.from;
            }
          }
        };

        $scope.selectFilter = function (el) {
          el.filters = {};
          el.filter_name = '';
          if (el.selected_filter != "") {
            var tmp_filters = angular.copy(el.saved_filters[el.selected_filter]);
            delete(tmp_filters['element']);
            delete(tmp_filters['slug']);
            delete(tmp_filters['name']);
            el._filter = angular.copy(el.saved_filters[el.selected_filter]);
            el.filters = tmp_filters;
            el.filter_name = el.saved_filters[el.selected_filter].name;
          }
          $scope.applyFilters(el);
        };
        $scope.applyFastFilters = function (el) {
          $(el.widgets).each(function (key, widget) {
            if (widget.value != '' && 
                widget.value != undefined &&
                widget.value || (
                    mining.utils.getNestedProp(widget, 'value.from', '') != '' && 
                    mining.utils.getNestedProp(widget, 'value.until', '') != '')
                ){
              if (widget.type == 'datetime' || widget.type == 'date') {
                var chave = "filter__" + widget.field + "__between__"+ widget.type +"__:Y-:m-:d",
                  ind = $scope.selected_dashboard.element.indexOf(el);
                $scope.selected_dashboard.element[ind].filters[chave] =
                  moment(widget.value.from).format("YYYY-MM-DD") + ':' + moment(widget.value.until).format("YYYY-MM-DD");
              }else if(widget.type == 'distinct' || widget.type == 'text'){
                var chave = "filter__" + widget.field + "__is__str",
                  ind = $scope.selected_dashboard.element.indexOf(el);
                $scope.selected_dashboard.element[ind].filters[chave] = widget.value;
              }else if(widget.type == 'int'){
                var chave = "filter__" + widget.field + "__is__int",
                  ind = $scope.selected_dashboard.element.indexOf(el);
                $scope.selected_dashboard.element[ind].filters[chave] = widget.value;
              }
            }
          });
          $scope.applyFilters(el);
        };

        $scope.clearFastFilters = function(el){
          $(el.widgets).each(function (key, widget) {
            if (widget.type == 'date' || widget.type == 'datetime') {
              widget.value= {
                'from':'',
                'until': ''
              };
            }else if(widget.type == 'distinct' || widget.type == 'text' || widget.type == 'int'){
              widget.value = '';
            }
          });
          el.filters = {};
          $scope.applyFilters(el);
        };

        $scope.selected_dashboard = current_dashboard.data;

        function refreshDashboard() {
          $($scope.selected_dashboard.element).each(function (ind, val) {
            if (AuthenticationService.hasPermission(val.slug, 'element', $scope.selected_dashboard.slug)) {
              val.last_refresh = moment().format('YYYY-MM-DDTHH:mm:ss');
              if (val.type == 'grid') {
                loadGrid(val);
              }else if(val.type == 'chart_bar'){
                loadBar(val);
              }
              else if(val.type == 'chart_line'){
                loadLine(val);
              }
              if(val.scheduler_status == true && (!$scope.selected_dashboard.refresh_elements || $scope.selected_dashboard.scheduler_status != true)){
                if (!val.intervals) {
                  if (val.scheduler_type == 'minutes') {
                    val.intervals = $interval(function () {
                      val.last_refresh = moment().format('YYYY-MM-DDTHH:mm:ss');
                      if (val.type == 'grid') {
                        loadGrid(val);
                      }else if(val.type == 'chart_bar'){
                        loadBar(val);
                      }
                      else if(val.type == 'chart_line'){
                        loadLine(val);
                      }
                    }, parseInt(val.scheduler_interval) * 60000);
                  }
                }
              }
            }
          });
        }

        $($scope.selected_dashboard.element).each(function (ind, val) {
          if (AuthenticationService.hasPermission(val.slug, 'element', $scope.selected_dashboard.slug)) {
            angular.extend($scope.selected_dashboard.element[ind], {
              isCollapsed: false,
              filterIsCollapsed: true,
              current_page: 1,
              total_pages: 0,
              total_rows: 0,
              filter_name: '',
              filter_operator: '',
              filter_field: '',
              filter_type: '',
              filter_format: '',
              filter_value: '',
              filters: {},
              saveSettings: false,
              columns: [],
              process: [],
              loading: true,
              last_refresh: undefined
            });
            // Element.loadData({'slug': val.slug, 'page': val.current_page, 'filters': val.filters});
            if (val.type == 'grid') {
              val.last_refresh = moment().format('YYYY-MM-DDTHH:mm:ss');
            } else if ($scope.selected_dashboard.element[ind].type == 'chart_bar') {
              $scope.selected_dashboard.element[ind].xkey = [$scope.selected_dashboard.element[ind].field_x];
              $scope.selected_dashboard.element[ind].ykeys = [$scope.selected_dashboard.element[ind].field_y];
              $scope.selected_dashboard.element[ind].labels = [$scope.selected_dashboard.element[ind].field_y];
            } else if ($scope.selected_dashboard.element[ind].type == 'chart_line') {
              $scope.selected_dashboard.element[ind].xkey = [$scope.selected_dashboard.element[ind].field_x];
              $scope.selected_dashboard.element[ind].labels = [$scope.selected_dashboard.element[ind].field_y];
            }
            $(val.widgets).each(function(key, widget){
              if(widget.type == 'distinct'){
                widget.disabled = true;
                loadDistinct($scope.selected_dashboard.element[ind], key);
              }else{
                widget.disabled = false;
              }
            });
          }
        });

        if ($scope.selected_dashboard.scheduler_type && $scope.selected_dashboard.refresh_elements) {
          if ($scope.selected_dashboard.scheduler_type == 'minutes') {
            $scope.selected_dashboard.last_refresh = moment().format('YYYY-MM-DDTHH:mm:ss');
            refreshDashboard();
            $scope.selected_dashboard.intervals = $interval(function () {
              $scope.selected_dashboard.last_refresh = moment().format('YYYY-MM-DDTHH:mm:ss');
              refreshDashboard();
            }, parseInt($scope.selected_dashboard.scheduler_interval) * 60000);
          }
        } else {
          refreshDashboard();
        }

        $scope.$on('$destroy', function () {
          $($scope.selected_dashboard.element).each(function (ind, val) {
            if (val.intervals)
              $interval.cancel(val.intervals);
          });
          if ($scope.selected_dashboard.intervals)
             $interval.cancel($scope.selected_dashboard.intervals);
        });

        $rootScope.$on('WINDOW_RESIZE', function (x, y) {
          $($scope.selected_dashboard.element).each(function (ind, val) {
            if (val.graph)
              val.graph.redraw();
          });
        });

        function loadDistinct(el, widget_index){
          el.widgets[widget_index].distinct_values = [];
          var prot = 'ws';
          if (window.protocol == 'https')
            prot = 'wss';
          var API_URL = prot + "://" + location.host + "/stream/data/" + el.slug + "?";
          API_URL += 'fields=' + el.widgets[widget_index].field + '&';
          API_URL += 'limit=' + false + '&';
          API_URL += 'groupby=' + el.widgets[widget_index].field;
          var sock_2 = new WebSocket(API_URL);
          sock_2.onmessage = function (e) {
            var data = JSON.parse(e.data.replace(/NaN/g, 'null'));
            if (data.type == 'data') {
              el.widgets[widget_index].distinct_values = $.map(data.data,
                function(value, index) {
                  return [value];
                }
              );
            } else if (data.type == 'close') {
              sock_2.close();
              $timeout(function () {
                $scope.$apply(function () {
                  el.widgets[widget_index].disabled = false;
                });
              });
            }
          };
        }

        function loadBar(el) {
          el.process = [];
          el.loading = true;
          var element = 'bar-chart-' + el.slug;
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
                  el.graph = Morris.Bar({
                    element: element,
                    data: el.process,
                    xkey: el.xkey,
                    ykeys: el.ykeys,
                    labels: el.labels,
                    resize: true,
                    redraw: true
                  });
                });
              });
            }
          };
        }

        function loadLine(el) {
          el.process = [];
          el.labels = [];
          el.ykeys = [];
          el.loading = true;
          var count = 0;
          var element = 'chart-line-' + el.slug;
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
              count = count + 1;
              if (el.labels.indexOf(data.data[el.field_serie]) < 0)
                el.labels.push(data.data[el.field_serie]);
              if (el.ykeys.indexOf(data.data[el.field_serie]) < 0)
                el.ykeys.push(data.data[el.field_serie]);
              var have = false;
              var key = -1;
              $(el.process).each(function (i_key, val) {
                if (val[el.field_x] == data.data[el.field_x]) {
                  have = true;
                  key = i_key;
                }
              });
              if (!have) {
                data.data[data.data[el.field_serie]] = data.data[el.field_y];
                el.process.push(data.data);
              } else {
                el.process[key][data.data[el.field_serie]] = data.data[el.field_y];
              }
            } else if (data.type == 'close') {
              sock.close();
              el.loading = false;
              $timeout(function () {
                $scope.$apply(function () {
                  el.graph = Morris.Line({
                    element: element,
                    data: el.process,
                    xkey: el.xkey,
                    ykeys: el.ykeys,
                    labels: el.labels,
                    resize: true,
                    redraw: true
                  });
                });
              });
            }
          };
        }
      }
    ])
;
