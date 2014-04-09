'use strict';
dashboard
  .factory('Filter',['$resource',
    function($resource){
      return $resource('/api/filter/:slug', {'slug':'@slug'}, {
        update:{method:'PUT', params: {'slug':'@slug'}}
      });
    }
  ])
;