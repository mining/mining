'use strict';
admin
  .factory('Connection', ['$resource',
    function($resource){
      var Connection = $resource('/api/connection/:slug', {'slug':'@slug'},{
        update:{method:'PUT', params: {'slug':'@slug'}}
      });
      return Connection;
    }
  ])
  .factory('Element', ['$resource',
    function($resource){
      return $resource('/api/element/:slug', {'slug':'@slug'}, {
        update: {method:'PUT', params: {'slug': '@slug'}},
        loadData: {method:'GET', params: {'slug': '@slug', 'page': '@page'}}
      });
    }
  ])
  .factory('Cube', ['$resource',
    function($resource){
      return $resource('/api/cube/:slug', {'slug':'@slug'}, {
        update:{method:'PUT', params: {'slug':'@slug'}},
        testquery: {method:'POST', url:"/api/cubequery.json"}
      });
    }
  ])
  .factory('Dashboard', ['$resource',
    function($resource){
      return $resource('/api/dashboard/:slug', {}, {
        update: { method: 'PUT', params: {'slug': '@slug'}},
        getFull: { method: 'GET', params: {'full': true}},
        getFullList: { method: 'GET', params: {'slug': '@slug', 'full': true}, isArray:true}
      });
    }
  ])
  .factory('User', ['$resource',
    function($resource){
      return $resource('/api/user/:username', {}, {
        update : { method: 'PUT', params: {'username': '@username'}}
      });
    }
  ])
;