#!/usr/bin/env python
# -*- coding: utf-8 -*-
from pandas import DataFrame
from sqlalchemy import create_engine


e = create_engine('mysql://root:123mudar@192.168.12.4/upessencia_dev1')
connection = e.connect()

sql = """SELECT 
cliente.id_cliente,
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
print df
df.head()
means = df.mean()
means.plot(kind='barh')
