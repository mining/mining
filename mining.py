#!/usr/bin/env python
# -*- coding: utf-8 -*-
from pandas import DataFrame
from sqlalchemy import create_engine
import matplotlib.pyplot as plt

import tornado.ioloop
import tornado.web
import tornado.gen

from StringIO import StringIO


#e = create_engine('mysql://root:123mudar@192.168.12.4/upessencia_dev1')
e = create_engine('mysql://root@127.0.0.1/lerolero')
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

sql2 = "SELECT id, date FROM lerolero"

resoverall = connection.execute(sql2)

df = DataFrame(resoverall.fetchall())
df.columns = resoverall.keys()
#self.write(df.to_json())
df.head()


class MainHandler(tornado.web.RequestHandler):
    @tornado.web.asynchronous
    def get(self):
        self.render('index.html', df=df.to_html())
        self.finish()


class PlotHandler(tornado.web.RequestHandler):
    def get(self):
        self.set_header("Content-Type", 'image/png"')
        means = df.mean()

        plt.figure()
        means.plot(kind='barh')
        plt.legend(loc='best')
        img = StringIO()
        plt.savefig(img)
        img.seek(0)

        self.finish(img.read())


application = tornado.web.Application([
    (r"/", MainHandler),
    (r"/plot.png", PlotHandler),
])


if __name__ == "__main__":
    application.listen(8888)
    tornado.ioloop.IOLoop.instance().start()
