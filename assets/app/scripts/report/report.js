'use strict';
var report = angular.module('miningApp.report', [])
  .run(['$rootScope', function($rootScope){
    $rootScope.operators = [
      {key: 'gte', value: 'gte'},
      {key: 'lte', value: 'lte'},
      {key: 'is', value: 'is'},
      {key: 'in', value: 'in'},
      {key: 'between', value: 'between'}
    ];
    $rootScope.types = [
      {key: 'date', value: 'Date'},
      {key: 'int', value: 'Integer'},
      {key: 'str', value: 'String'}
    ];
  }]);