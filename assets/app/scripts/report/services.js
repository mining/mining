'use strict';
report
  .factory('LineChart', function($http){
    return {
      'getConfig':function(URL){
        return $http.post(URL)
      }
    };
  })