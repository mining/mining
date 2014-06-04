'use strict';
var report = angular.module('miningApp.report', [])
  .run(['$rootScope', function($rootScope){
    $rootScope.operators = [
      {key: 'gte', value: 'Greater than or equal to'},
      {key: 'lte', value: 'Less than or equal to'},
      {key: 'is', value: 'Equal to'},
      {key: 'in', value: 'In a given list'},
      {key: 'between', value: 'Range'},
      {key: 'like', value: 'Like'},
      {key: 'regex', value: 'Regex'}
    ];
    $rootScope.types = [
      {key: 'date', value: 'Date'},
      {key: 'datetime', value: 'DateTime'},
      {key: 'int', value: 'Integer'},
      {key: 'str', value: 'String'}
    ];
  }]);
