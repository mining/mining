Open Mining
===========

.. image:: https://circleci.com/gh/mining/mining/tree/master.svg?style=svg
    :target: https://circleci.com/gh/mining/mining/tree/master
    :alt: Build Status - Circle CI

.. image:: https://coveralls.io/repos/github/mining/mining/badge.svg?branch=master
    :target: https://coveralls.io/github/mining/mining?branch=master

.. image:: https://landscape.io/github/mining/mining/master/landscape.svg?style=flat
   :target: https://landscape.io/github/mining/mining/master
   :alt: Code Health


.. image:: https://raw.githubusercontent.com/mining/frontend/master/assets/image/openmining.io.png
    :alt: OpenMining

Business Intelligence (BI) Application Server written in Python


Requirements
------------

* Python 2.7 (Backend)
* Lua 5.2 or LuaJIT 5.1 (OML backend)
* MongoDB (Admin)
* Redis (Queue and DataWarehouse)
* Bower (Install frontend libs, NodeJS depends)


Install dependencies
-------

.. code:: bash
    
    $ sudo apt-get install mongodb-10gen redis-server nodejs nodejs-dev npm
    $ npm install bower


If you use Mac OSX you can install all dependencies using `HomeBrew <http://brew.sh/>`_.


Install Open Mining
-------

**Clone the repository**

.. code:: bash

    $ git clone git@github.com:mining/mining.git

**Install python and bower dependencies using make command**

.. code:: bash

    $ make build

**FAQ**

**If mongodb or redis-server problems**

Install mongodb and redis-server, make sure it running


**Supported databases**

For example, to connect to a PostgreSQL database make sure you install a driver like **psycopg2**. OpenMining supports all databases that the underlying ORM SQLAlchemy supports.

See the `SQLAlchemy documentation <http://docs.sqlalchemy.org/en/rel_0_9/core/engines.html>`_ for more info about drivers and connection strings.


Run
---

.. code:: bash

    python manage.py runserver
    python manage.py celery
    python manage.py scheduler


Running Demo
------------

Make sure runserver still running when run 'build_demo' command.

.. code:: bash

    python manage.py runserver
    python manage.py build_demo


And now you can login with: username 'admin' and password 'admin'.

Screenshots
-----------

**Dashboard OpenMining**

.. image:: https://raw.github.com/mining/mining/master/docs/docs/img/dashboard-openmining_new.png
    :alt: Dashboard OpenMining

**Dashboard Charts OpenMining**

.. image:: https://raw.github.com/mining/mining/master/docs/docs/img/charts-openmining_new.png
    :alt: Dashboard Charts OpenMining

**Dashboard Charts OpenMining**

.. image:: https://raw.github.com/mining/mining/master/docs/docs/img/charts2-openmining_new.png
    :alt: Dashboard Charts OpenMining

**Dashboard Widgets OpenMining**

.. image:: https://raw.github.com/mining/mining/master/docs/docs/img/widgets-openmining_new.png
    :alt: Dashboard Widgets OpenMining


**Late Scheduler and running Cubes OpenMining**

.. image:: https://raw.github.com/mining/mining/master/docs/docs/img/late-scheduler-openmining_new.png
    :alt: Late Scheduler and running Cubes OpenMining


Contribute
----------

Join us on IRC at **#openmining** on freenode (`web access <http://webchat.freenode.net/?channels=openmining>`_).


Credits
-------

Authors: `Avelino <https://github.com/avelino/>`_ and `UP! Essência <http://www.upessencia.com.br/>`_

Many thanks to all the contributors!


License
-------

Licensed under the MIT license (see the (`LICENSE file <https://github.com/mining/mining/blob/master/LICENSE>`_).
