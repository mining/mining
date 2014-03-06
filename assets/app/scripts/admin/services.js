'use strict';
admin
  .factory('Connection', ['$resource',
    function($resource){
      return $resource('/api/connection/:slug', {'slug':''}, {});
    }])
  .factory('Element', ['$resource',
    function($resource){
      return $resource('/api/element/:slug', {'slug':''}, {});
    }])
  .factory('Cube', ['$resource',
    function($resource){
      return $resource('/api/cube/:slug', {'slug':''}, {});
    }])
  .factory('Dashboard', ['$resource',
    function($resource){
      return $resource('/api/dashboard/:slug', {'slug':''}, {});
    }])
;