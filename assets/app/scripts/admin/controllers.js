'use strict';
admin
  .controller('ConnectionCtrl', ['$scope', 'Connection', 'getConnections',
    function($scope, Connection, getConnections){
      $scope.connections = [];
      $scope.connection = {
        'slug':'',
        'name': '',
        'connection': ''
      };
      $scope.selectConnection = function(c){

      };
      $scope.deleteConnection = function(c){

      };
    }])
  .controller('CubeQuery', function($scope, $http, $timeout) {
    $scope.testquery = function(){
      $scope.loadcubequery = false;
      $scope.ajaxload = true;
      $scope.force_save=true;
      var sql = angular.element('#sql').val();
      var connection = angular.element('#connection').val();

      $http.post("/api/cubequery.json", {'sql': sql, 'connection': connection})
        .success(function(a){
          if(a.msg != "Error!"){
            $scope.loadcubequery = true;
          }else{
            $scope.loadcubequery = false;
          };
          $scope.status = a.msg;
          $scope.ajaxload = false;
        })
    };
  })
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

