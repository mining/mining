'use strict';
admin
  .controller('TasksControllers', ['$scope', 'Cube', '$rootScope', 'AlertService', '$interval',
    function ($scope, Cube, $rootScope, AlertService, $interval) {
      $scope.tasks = [];
      $scope.loading = true;
      $scope.tasks = Cube.checkTasks();
      $scope.loading = false;

      $interval(function () {
        $scope.loading = true;
        $scope.tasks = Cube.checkTasks();
        console.log($scope.tasks);
        $scope.loading = false;
      }, 1000);

      $scope.forceRefresh = function () {
        $scope.loading = true;
        $scope.tasks = Cube.checkTasks();
        $scope.loading = false;
      }
    }
  ])
  .controller('ConnectionCtrl', ['$scope', 'Connection', 'AlertService', '$rootScope',
    function ($scope, Connection, AlertService, $rootScope) {
      $rootScope.inSettings = true;
      $scope.connections = Connection.query();
      $scope.connection = new Connection();
      $scope.selectConnection = function (c) {
        $scope.connection = c;
      };
      $scope.deleteConnection = function (connection) {
        Connection.delete(connection);
        $scope.connections.splice($scope.connections.indexOf(connection), 1);
      };
      $scope.save = function () {
        if ($scope.connection.slug) {
          Connection.update({'slug': $scope.connection.slug}, $scope.connection);
        } else {
          $scope.connection.$save().then(function (response) {
            AlertService.add('success', 'Save ok');
            $scope.connections.push(response);
          });
        }
        $scope.connection = new Connection();
      };
      $scope.newForm = function () {
        $scope.connection = new Connection();
      };
    }])
  .controller('CubeCtrl', ['$scope', 'Cube', 'Connection', 'AlertService', '$timeout', '$rootScope',
    function ($scope, Cube, Connection, AlertService, $timeout, $rootScope) {
      $rootScope.inSettings = true;
      $scope.editorOptions = {
        lineWrapping: true,
        lineNumbers: true,
        readOnly: false,
        mode: 'text/x-sql',
        onLoad: function (editor) { // FIX TEMP ISSUE: https://github.com/angular-ui/ui-codemirror/issues/35
          editor.on('blur', function () {
            $timeout(function () {
              $scope.cube.sql = editor.getValue();
            });
          })
        }
      };
      $scope.cube_valid = false;
      $scope.connections = Connection.query();
      $scope.cubes = Cube.query();
      $scope.cube = new Cube();
      $scope.scheduler_types = [
        {key: 'minutes', val: 'minutes'}
//        {key: 'hour', val: 'hour'},
//        {key: 'day', val: 'day'}
      ];
      $scope.show_h = false;
      $scope.show_m = false;
      $scope.hour = 0;
      $scope.min = 0;
      $scope.changeSchedulerType = function () {
        if ($scope.cube.scheduler_type == 'day') {
          $scope.show_h = true;
          $scope.show_m = true;
        } else if ($scope.cube.scheduler_type == 'minutes') {
          $scope.show_h = false;
          $scope.show_m = true;
        } else if ($scope.cube.scheduler_type == 'hour') {
          $scope.show_h = true;
          $scope.show_m = false;
        } else {
          $scope.show_h = false;
          $scope.show_m = false;
        }
      };
      $scope.selectCube = function (c) {
        $scope.cube = c;
        if ($scope.cube.scheduler_type == 'day') {
          $scope.show_h = true;
          $scope.show_m = true;
          $scope.hour = parseInt($scope.cube.scheduler_interval.split(':')[0]);
          $scope.min = parseInt($scope.cube.scheduler_interval.split(':')[1]);
        } else if ($scope.cube.scheduler_type == 'minutes') {
          $scope.min = parseInt($scope.cube.scheduler_interval);
          $scope.show_h = false;
          $scope.show_m = true;
        } else if ($scope.cube.scheduler_type == 'hour') {
          $scope.hour = parseInt($scope.cube.scheduler_interval);
          $scope.show_h = true;
          $scope.show_m = false;
        } else {
          $scope.show_h = false;
          $scope.show_m = false;
        }
      };
      $scope.deleteCube = function (cube) {
        Cube.delete(cube);
        $scope.cubes.splice($scope.cubes.indexOf(cube), 1);
      };
      $scope.save = function () {
        $scope.cube.scheduler_status = false;
        if ($scope.cube.scheduler_type) {
          $scope.cube.scheduler_status = true;
          if ($scope.cube.scheduler_type == 'day') {
            $scope.cube.scheduler_interval = mining.utils.padLeft(parseInt($scope.hour), 2) + ':' + mining.utils.padLeft(parseInt($scope.min), 2);
          } else if ($scope.cube.scheduler_type == 'minutes') {
            $scope.cube.scheduler_interval = parseInt($scope.min);
          } else if ($scope.cube.scheduler_type == 'hour') {
            $scope.cube.scheduler_interval = parseInt($scope.hour);
          }
        } else {
          $scope.cube.scheduler_status = false;
        }
        if ($scope.cube.slug) {
          $scope.cube.status = false;
          Cube.update({'slug': $scope.cube.slug}, $scope.cube);
        } else {
          $scope.cube.$save().then(function (response) {
            AlertService.add('success', 'Save ok');
            $scope.cubes.push(response);
          });
        }
        $scope.cube = new Cube();
        $scope.show_h = false;
        $scope.show_m = false;
        $scope.hour = 0;
        $scope.min = 0;
      };
      $scope.testquery = function () {
        Cube.testquery($scope.cube, function (response) {
          if (response.status == 'success') {
            $scope.cube_valid = true;
            AlertService.add('success', 'Query is Ok!');
          } else {
            AlertService.add('error', 'Query is not Ok!');
          }
        });
      };
      $scope.newForm = function () {
        $scope.cube = new Cube();
        $scope.show_h = false;
        $scope.show_m = false;
        $scope.hour = 0;
        $scope.min = 0;
      };
    }])
  .controller('ElementCtrl', ['$scope', 'Cube', 'Element', 'AlertService', '$http', '$rootScope',
    function ($scope, Cube, Element, AlertService, $http, $rootScope) {
      $rootScope.inSettings = true;
      $scope.types = [
        {'slug': "grid", "name": "Grid"},
        {'slug': "chart_line", "name": "Chart line"},
        {'slug': "chart_bar", "name": "Chart bar"},
        {'slug': "chart_pie", "name": "Chart pie"}
      ];
      $scope.cubes = Cube.query();
      $scope.elements = Element.query();
      $scope.element = new Element();
      $scope.fields = [];
      $scope.selectElement = function (e) {
        $scope.element = e;
        $scope.loadFields();
      };
      $scope.toId = function (a) {
        return a.label
      };
      $scope.deleteElement = function (element) {
        Element.delete(element);
        $scope.elements.splice($scope.elements.indexOf(element), 1);
      };
      $scope.save = function (element) {
        if ($scope.element.slug) {
          Element.update({'slug': $scope.element.slug}, $scope.element);
        } else {
          $scope.element.$save().then(function (response) {
            AlertService.add('success', 'Save ok');
            $scope.elements.push(response);
          });
        }
        $scope.element = new Element();
      };
      $scope.addOrder = function () {
        if (!$scope.element.orderby) {
          $scope.element.orderby = [];
          $scope.element.orderby__order = [];
        }
        if ($scope.element.orderby.length < $scope.fields.length) {
          $scope.element.orderby.push('');
          $scope.element.orderby__order.push('');
        }
      };
      $scope.removeOrder = function (ind) {
        $scope.element.orderby.splice(ind, 1);
        $scope.element.orderby__order.splice(ind, 1);
      };
      $scope.loadFields = function () {
        if ($scope.element.cube) {
          $http.get('/api/element/cube/' + $scope.element.cube)
            .success(function (retorno) {
              $scope.fields = retorno.columns;
            })
            .error(function (retorno) {
              AlertService.add('error', 'Error!');
            });
        }
      };
      $scope.newForm = function () {
        $scope.element = new Element();
      };
    }])
  .controller('DashboardCtrl', ['$scope', 'Dashboard', 'Element', 'AlertService', '$rootScope', '$filter',
    function ($scope, Dashboard, Element, AlertService, $rootScope, $filter) {
      $rootScope.inSettings = true;
      $rootScope.dashboards = Dashboard.query();
      $scope.elements = Element.query();
      $scope.dashboard = new Dashboard();
      $scope.scheduler_types = [
        {key: 'minutes', val: 'minutes'}
//        {key: 'hour', val: 'hour'},
//        {key: 'day', val: 'day'}
      ];
      $scope.show_h = false;
      $scope.show_m = false;
      $scope.hour = 0;
      $scope.min = 0;
      $scope.changeSchedulerType = function () {
        if ($scope.dashboard.scheduler_type == 'day') {
          $scope.show_h = true;
          $scope.show_m = true;
        } else if ($scope.dashboard.scheduler_type == 'minutes') {
          $scope.show_h = false;
          $scope.show_m = true;
        } else if ($scope.dashboard.scheduler_type == 'hour') {
          $scope.show_h = true;
          $scope.show_m = false;
        } else {
          $scope.show_h = false;
          $scope.show_m = false;
        }
      };
      $scope.selectDashboard = function (d) {
        $scope.dashboard = d;
        if ($scope.dashboard.scheduler_type == 'day') {
          $scope.show_h = true;
          $scope.show_m = true;
          $scope.hour = parseInt($scope.dashboard.scheduler_interval.split(':')[0]);
          $scope.min = parseInt($scope.dashboard.scheduler_interval.split(':')[1]);
        } else if ($scope.dashboard.scheduler_type == 'minutes') {
          $scope.min = parseInt($scope.dashboard.scheduler_interval);
          $scope.show_h = false;
          $scope.show_m = true;
        } else if ($scope.dashboard.scheduler_type == 'hour') {
          $scope.hour = parseInt($scope.dashboard.scheduler_interval);
          $scope.show_h = true;
          $scope.show_m = false;
        } else {
          $scope.show_h = false;
          $scope.show_m = false;
        }
      };
      $scope.deleteDashboard = function (dashboard) {
        Dashboard.delete(dashboard);
        $rootScope.dashboards.splice($rootScope.dashboards.indexOf(dashboard), 1);
      };
      $scope.queryElements = function (term, result) {
        var ls = [];
        $($scope.elements).each(function (key, val) {
          ls.push({
            id: val.slug,
            label: val.name
          });
        });
        result($filter('filter')(ls, term));
      };
      $scope.save = function (dashboard) {
        $scope.dashboard.scheduler_status = false;
        if ($scope.dashboard.scheduler_type) {
          $scope.dashboard.scheduler_status = true;
          if ($scope.dashboard.scheduler_type == 'day') {
            $scope.dashboard.scheduler_interval = mining.utils.padLeft(parseInt($scope.hour), 2) + ':' + mining.utils.padLeft(parseInt($scope.min), 2);
          } else if ($scope.dashboard.scheduler_type == 'minutes') {
            $scope.dashboard.scheduler_interval = parseInt($scope.min);
          } else if ($scope.dashboard.scheduler_type == 'hour') {
            $scope.dashboard.scheduler_interval = parseInt($scope.hour);
          }
        } else {
          $scope.dashboard.scheduler_status = false;
        }
        if ($scope.dashboard.slug) {
          $scope.dashboard.status = false;
          Dashboard.update({'slug': $scope.dashboard.slug}, $scope.dashboard);
        } else {
          $scope.dashboard.$save().then(function (response) {
            AlertService.add('success', 'Save ok');
            $rootScope.dashboards.push(response);
          });
        }
        $scope.dashboard = new Dashboard();
        $scope.show_h = false;
        $scope.show_m = false;
        $scope.hour = 0;
        $scope.min = 0;
      };
      $scope.newForm = function () {
        $scope.dashboard = new Dashboard();
        $scope.show_h = false;
        $scope.show_m = false;
        $scope.hour = 0;
        $scope.min = 0;
      };
    }])
  .controller('UserCtrl', ['$scope', 'User', 'AlertService', 'Dashboard', 'AuthenticationService', '$rootScope',
    function ($scope, User, AlertService, Dashboard, AuthenticationService, $rootScope) {
      $rootScope.inSettings = true;
      $scope.users = User.query();
      $scope.permissions = Dashboard.getFullList();
      $scope.user = new User();
      $scope.editing = false;
      $scope.change_pass = false;
      $scope.rules = ['user', 'admin', 'root'];
      function clearPermissions() {
        $($scope.permissions).each(function (key, dash) {
          dash.permitted = false;
          $(dash.element).each(function (key, elem) {
            elem.permitted = false;
          });
        });
      }

      $scope.selectUser = function (us) {
        $scope.user = us;
        $scope.editing = true;
        $scope.change_pass = false;
        clearPermissions();
        $($scope.permissions).each(function (key, dash) {
          if ($scope.user.permissions[dash.slug]) {
            dash.permitted = true;
            $(dash.element).each(function (key, elem) {
              if ($scope.user.permissions[dash.slug].indexOf(elem.slug) >= 0)
                elem.permitted = true;
            });
          }
        });
      };
      $scope.selectDashboard = function (da) {
        for (var x = 0; x < da.element.length; x++) {
          da.element[x].permitted = !da.permitted;
        }
      };
      $scope.deleteUser = function (user) {
        User.delete(user);
        $scope.users.splice($scope.users.indexOf(user), 1);
        $scope.newForm();
      };
      $scope.changePass = function (user) {
        $scope.user = user;
        $scope.editing = false;
        $scope.change_pass = true;
        clearPermissions();
      };
      $scope.selectElement = function (dashboard) {
        dashboard.permitted = true;
      };
      $scope.save = function () {
        $scope.user.permissions = {};
        $($scope.permissions).each(function (key, dash) {
          if (dash.permitted) {
            $scope.user.permissions[dash.slug] = [];
            $(dash.element).each(function (key, elem) {
              if (elem.permitted)
                $scope.user.permissions[dash.slug].push(elem.slug);
            });
          }
        });
        if ($scope.editing) {
          User.update({'username': $scope.user.username}, $scope.user);
          if ($scope.user.username == AuthenticationService.getUser().username) {
            AuthenticationService.setUser($scope.user);
          }
        } else {
          $scope.user.$save().then(function (response) {
            AlertService.add('success', 'Save ok');
            $scope.users.push(response);
          });
        }
        $scope.newForm();
      };
      $scope.newForm = function () {
        $scope.user = new User();
        $scope.editing = false;
        $scope.change_pass = false;
        clearPermissions();
      };
    }])
;