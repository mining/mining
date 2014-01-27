#!/usr/bin/env python
# -*- coding: utf-8 -*-
import json
import riak
import memcache

from pandas import DataFrame
from sqlalchemy import create_engine

from utils import pandas_to_dict


myClient = riak.RiakClient(protocol='http',
                           http_port=8098,
                           host='127.0.0.1')
radmin = myClient.bucket('openmining-admin')

for cube in radmin.get('cube').data:
    slug = cube['slug']
    sql = cube['sql']
    for c in radmin.get('connection').data:
        if c['slug'] == cube['conection']:
            connection = c['conection']

    print "# CLEAN MEMCACHE: {}".format(slug)
    mc = memcache.Client(['127.0.0.1:11211'], debug=0)
    mc.delete(str(slug))
    mc.delete(str('{}-columns'.format(slug)))

    rmining = myClient.bucket('openmining')

    print "# CONNECT IN RELATION DATA BASE: {}".format(slug)
    e = create_engine(connection)
    connection = e.connect()

    print sql
    resoverall = connection.execute(sql)

    df = DataFrame(resoverall.fetchall())
    df.columns = resoverall.keys()
    df.head()

    convert = pandas_to_dict(df)

    join = json.dumps(convert)
    b1 = rmining.new(slug, data=join)
    b1.store()

    b2 = rmining.new(u'{}-columns'.format(slug), data=json.dumps([c for c in df.columns]))
    b2.store()

    b3 = rmining.new(u'{}-connect'.format(slug), data=c)
    b3.store()

    b4 = rmining.new(u'{}-sql'.format(slug), data=sql)
    b4.store()

exit(0)


mc = memcache.Client(['127.0.0.1:11211'], debug=0)
mc.delete('testando')
mc.delete('testando-columns')

myClient = riak.RiakClient(protocol='http', http_port=8098, host='127.0.0.1')
myBucket = myClient.bucket('openmining')

c = 'mysql://root:123mudar@192.168.12.4/upessencia_dev1'
e = create_engine(c)
connection = e.connect()

sql = """SELECT
cliente.id_cliente,
cliente.nome,
pedido.id_pedido,
pedido.criacao_ts as 'pedido_data',
cliente.criacao_ts as 'cliente_data'
FROM pedido
inner join cliente on cliente.id_cliente = pedido.id_cliente
WHERE pedido.id_pedido_status NOT IN (4,8,9)
AND pedido.entrega_forma<>'franquia' limit 100"""

resoverall = connection.execute(sql)

df = DataFrame(resoverall.fetchall())
df.columns = resoverall.keys()
df.head()

convert = pandas_to_dict(df)

join = json.dumps(convert)
b1 = myBucket.new('testando', data=join)
b1.store()

b2 = myBucket.new('testando-columns', data=json.dumps([c for c in df.columns]))
b2.store()

b3 = myBucket.new('testando-connect', data=c)
b3.store()

b4 = myBucket.new('testando-sql', data=sql)
b4.store()
