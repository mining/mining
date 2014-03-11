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
    }])
  .controller('CubeCtrl', ['$scope', 'Cube', 'Connection', 'AlertService',
    function($scope, Cube, Connection, AlertService){
      $scope.connections = Connection.query();
      $scope.cubes = Cube.query();
      $scope.cube = new Cube();
      $scope.selectCube = function(c){
        $scope.cube = c;
      };
      $scope.deleteCube = function(cube){
        Cube.delete(cube);
        $scope.cubes.splice($scope.cubes.indexOf(cube),1);
      };
      $scope.save = function(){
        if($scope.cube.slug){
          Cube.update({'slug':$scope.cube.slug},$scope.cube);
        }else{
          $scope.cube.$save().then(function(response) {
            AlertService.add('success', 'Save ok');
            $scope.cubes.push(response);
          });
        }
        $scope.cube = new Cube();
      };
      $scope.testquery = function(){
        Cube.testquery($scope.cube, function(response){
          if(response.status == 'success'){
            AlertService.add('success', 'Query is Ok!');
          }else{
            AlertService.add('error', 'Query is not Ok!');
          }
        });
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
        $scope.element = new Cube();
      };
      $scope.loadFields = function(){
        $http.get('/admin/api/element/cube/'+$scope.element.cube)
          .success(function(retorno){
            if(retorno.status=='success'){
              $scope.fields = retorno.columns;
            }else{
              AlertService.add('error', 'Error!');
            }
          })
          .error(function(retorno){
            AlertService.add('error', 'Error!');
          })
      }
    }])
  .controller('ElementCube', function($scope, $http, $timeout) {
    $scope.categorie = '';

    var loadFields = function(){
      $http({method: 'GET',
        url: "/admin/api/element/cube/" + angular.element(document.querySelector('#cube')).val()}).
        success(function(data) {
          $scope._fields = data.columns;

          if($scope.categorie != ""){
            $timeout(function(){
              $scope.$apply(function(){
                $scope.fields = $scope.categorie;
              });
            });
          }
        });
    };

    var showCategories = function(){
      if (angular.element(document.querySelector('#type')).val() != "grid") {
        loadFields();
        $scope.chart = true;
      } else {
        $scope.chart = false;
      }
    };

    angular.element(document.querySelector('#type')).bind('change', function(){
      showCategories();
    });

    angular.element(document.querySelector('#cube')).bind('change', function(){
      $scope.loading = true;
      loadFields();
      $scope.loading = false;
    });

    showCategories();
  });

