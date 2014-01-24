#!/usr/bin/env python
# -*- coding: utf-8 -*-
import json
import riak
import memcache
from pandas import DataFrame
from sqlalchemy import create_engine


mc = memcache.Client(['127.0.0.1:11211'], debug=0)
mc.delete('testando')

myClient = riak.RiakClient(protocol='http', http_port=8098, host='127.0.0.1')
myBucket = myClient.bucket('openmining')

c = 'mysql://root:123mudar@192.168.12.4/upessencia_dev1'
e = create_engine('mysql://root:123mudar@192.168.12.4/upessencia_dev1')
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
AND pedido.entrega_forma<>'franquia' limit 10000"""

resoverall = connection.execute(sql)

df = DataFrame(resoverall.fetchall())
df.columns = resoverall.keys()
df.head()


def fix_str(name):
    try:
        return unicode(name)
    except UnicodeDecodeError:
        return unicode(name.decode('latin1'))


convert = [{colname: (fix_str(row[i]) if type(row[i]) is str else row[i]) for i, colname in enumerate(df.columns) if colname not in ['pedido_data', 'cliente_data']}
           for row in df.values]

join = json.dumps(convert)
b1 = myBucket.new('testando', data=join)
b1.store()

b2 = myBucket.new('testando-columns', data=json.dumps([c for c in df.columns]))
b2.store()

b3 = myBucket.new('testando-connect', data=c)
b3.store()

b4 = myBucket.new('testando-sql', data=sql)
b4.store()
