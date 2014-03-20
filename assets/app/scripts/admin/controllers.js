'use strict';
admin
.controller('ConnectionCtrl', ['$scope', 'Connection', 'AlertService',
  function($scope, Connection, AlertService){
    $scope.connections = Connection.query();
    $scope.connection = new Connection();
    $scope.selectConnection = function(c){
      $scope.connection = c;
    };
    $scope.deleteConnection = function(connection){
      Connection.delete(connection);
      $scope.connections.splice($scope.connections.indexOf(connection),1);
    };
    $scope.save = function(){
      if($scope.connection.slug){
        Connection.update({'slug':$scope.connection.slug},$scope.connection);
      }else{
        $scope.connection.$save().then(function(response) {
          AlertService.add('success', 'Save ok');
          $scope.connections.push(response);
        });
      }
      $scope.connection = new Connection();
    };
    $scope.newForm = function(){
      $scope.connection = new Connection();
    };
  }])
.controller('CubeCtrl', ['$scope', 'Cube', 'Connection', 'AlertService',
  function($scope, Cube, Connection, AlertService){
    $scope.editorOptions = {
        lineWrapping : true,
        lineNumbers: true,
        readOnly: false,
        mode: 'text/x-sql'
    };
    $scope.cube_valid = false;
    $scope.connections = Connection.query();
    $scope.cubes = Cube.query();
    $scope.cube = new Cube();
    $scope.scheduler_types = [
    {key:'minute', val: 'minute'},
    {key:'hour', val: 'hour'},
    {key:'day', val: 'day'}
    ];
    $scope.show_h = false;
    $scope.show_m = false;
    $scope.hour = 0;
    $scope.min = 0;
    $scope.changeSchedulerType = function(){
      if($scope.cube.scheduler_type == 'day'){
        $scope.show_h = true;
        $scope.show_m = true;
      }else if($scope.cube.scheduler_type == 'minute'){
        $scope.show_h = false;
        $scope.show_m = true;
      }else if($scope.cube.scheduler_type == 'hour'){
        $scope.show_h = true;
        $scope.show_m = false;
      }else{
        $scope.show_h = false;
        $scope.show_m = false;
      }
    }
    $scope.selectCube = function(c){
      $scope.cube = c;
      if($scope.cube.scheduler_type == 'day'){
        $scope.show_h = true;
        $scope.show_m = true;
        $scope.hour = parseInt($scope.cube.scheduler_interval.split(':')[0]);
        $scope.min = parseInt($scope.cube.scheduler_interval.split(':')[1]);
      }else if($scope.cube.scheduler_type == 'minute'){
        $scope.min = parseInt($scope.cube.scheduler_interval);
        $scope.show_h = false;
        $scope.show_m = true;
      }else if($scope.cube.scheduler_type == 'hour'){
        $scope.hour = parseInt($scope.cube.scheduler_interval);
        $scope.show_h = true;
        $scope.show_m = false;
      }else{
        $scope.show_h = false;
        $scope.show_m = false;
      }
    };
    $scope.deleteCube = function(cube){
      Cube.delete(cube);
      $scope.cubes.splice($scope.cubes.indexOf(cube),1);
    };
    $scope.save = function(){
      if($scope.cube.scheduler_type){
        $scope.cube.scheduler_status = true;
        if($scope.cube.scheduler_type == 'day'){
          $scope.cube.scheduler_interval = mining.utils.padLeft(parseInt($scope.hour),2) +':'+ mining.utils.padLeft(parseInt($scope.min),2);
        }else if($scope.cube.scheduler_type == 'minute'){
          $scope.cube.scheduler_interval = parseInt($scope.min);
        }else if($scope.cube.scheduler_type == 'hour'){
          $scope.cube.scheduler_interval = parseInt($scope.hour);
        }
      }else{
        $scope.cube.scheduler_status = false;
      }
      if($scope.cube.slug){
        Cube.update({'slug':$scope.cube.slug},$scope.cube);
      }else{
        $scope.cube.$save().then(function(response) {
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
    $scope.testquery = function(){
      Cube.testquery($scope.cube, function(response){
        if(response.status == 'success'){
          $scope.cube_valid = true;
          AlertService.add('success', 'Query is Ok!');
        }else{
          AlertService.add('error', 'Query is not Ok!');
        }
      });
    };
    $scope.newForm = function(){
      $scope.cube = new Cube();
      $scope.show_h = false;
      $scope.show_m = false;
      $scope.hour = 0;
      $scope.min = 0;
    };
  }])
.controller('ElementCtrl', ['$scope', 'Cube', 'Element', 'AlertService', '$http',
  function($scope, Cube, Element, AlertService, $http){
    $scope.types = [
    {'slug':"grid","name":"Grid"},
    {'slug':"chart_line", "name":"Chart line"},
    {'slug':"chart_bar","name":"Chart bar"},
    {'slug':"chart_pie","name":"Chart pie"}
    ];
    $scope.cubes = Cube.query();
    $scope.elements = Element.query();
    $scope.element = new Element();
    $scope.fields = [];
    $scope.selectElement = function(e){
      $scope.element = e;
    };
    $scope.deleteElement = function(element){
      Element.delete(element);
      $scope.elements.splice($scope.elements.indexOf(element),1);
    };
    $scope.save = function(element){
      if($scope.element.slug){
        Element.update({'slug':$scope.element.slug},$scope.element);
      }else{
        $scope.element.$save().then(function(response) {
          AlertService.add('success', 'Save ok');
          $scope.elements.push(response);
        });
      }
      $scope.element = new Element();
    };
    $scope.loadFields = function(){
      if($scope.element.type != 'grid'){
        $http.get('/api/element/cube/'+$scope.element.cube)
        .success(function(retorno){
          $scope.fields = retorno.columns;
        })
        .error(function(retorno){
          AlertService.add('error', 'Error!');
        });
      }
    };
    $scope.newForm = function(){
      $scope.element = new Element();
    };
  }])
.controller('DashboardCtrl', ['$scope', 'Dashboard', 'Element', 'AlertService', '$rootScope',
  function($scope, Dashboard, Element, AlertService, $rootScope){
    $rootScope.dashboards = Dashboard.query();
    $scope.elements = Element.query();
    $scope.dashboard = new Dashboard();
    $scope.selectDashboard = function(d){
      $scope.dashboard = d;
    };
    $scope.deleteElement = function(dashboard){
      Dashboard.delete(dashboard);
      $rootScope.dashboards.splice($rootScope.dashboards.indexOf(dashboard),1);
    };
    $scope.save = function(dashboard){
      if($scope.dashboard.slug){
        Dashboard.update({'slug':$scope.dashboard.slug},$scope.dashboard);
      }else{
        $scope.dashboard.$save().then(function(response) {
          AlertService.add('success', 'Save ok');
          $rootScope.dashboards.push(response);
        });
      }
      $scope.dashboard = new Dashboard();
    };
    $scope.newForm = function(){
      $scope.dashboard = new Dashboard();
    };
  }]);