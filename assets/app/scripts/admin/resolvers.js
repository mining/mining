'use strict';

admin['resolvers'] = {
  'connection': {
    'getConnections': ['Connection',function(Connection){
      return Connection.get();
    }]
  }
};