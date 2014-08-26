Open Mining
===========

.. image:: https://raw.github.com/avelino/mining/master/mining/assets/image/openmining.io.png
    :alt: OpenMining

.. image:: https://travis-ci.org/avelino/mining.png?branch=master
    :target: https://travis-ci.org/avelino/mining
    :alt: Build Status - Travis CI

Business Intelligence (BI) Application Server written in Python 


Contribute
----------

Join us on IRC at **#openmining** on freenode (`web access <http://webchat.freenode.net/?channels=openmining>`_).

.. code:: bash

	pip install -r requirements_dev.txt


Requirements
------------

* MongoDB (Admin)
* Redis (Queue and DataWarehouse)
* Bower (Install frontend libs, nodejs depends)


Install
-------

**Make a new project directory to host the mining repository**

.. code:: bash

    $ mkdir openmining

**Change into new directory**

.. code:: bash

    $ cd openmining

**Create a new virtual environment**

.. code:: bash

    $ virtualenv env

**Clone the repository into the current directory**

.. code:: bash

    $ git clone <repo>

**Change directory into new repo**

.. code:: bash

    $ cd mining

**Run pip on project requirements**

.. code:: bash

    $ pip install -r requirements.txt

**Should end successfully with**

*Successfully installed numpy pandas ipython SQLAlchemy bottle bottle-mongo bottle-websocket bottle-auth bottle-beaker beaker pymongo python-dateutil nose redis rq openpyxl xlwt gevent schedule requests pytz gevent-websocket webob six greenlet*

**Install numexpr**

.. code:: bash

    $ pip install numexpr==2.3

**Copy the sample ini file to mining.ini**

.. code:: bash

    $ cp mining/mining.sample.ini ../env/local/lib/python2.7/site-packages/mining-0.2.0-py2.7.egg/mining/mining.ini

**Install JS**

.. code:: bash

    $ bower install

**FAQ**

**If mongodb or redis-server problems**

Install mongodb and redis-server, make sure running

**If <<python manage.py runserver>> returns "ConfigParser.NoSectionError: No section: 'mongodb'"**

copy mining.sample.ini to openmining/env/local/lib/python2.7/site-packages/mining-0.2.0-py2.7.egg/mining/mining.ini


Run
---

.. code:: bash

    python manage.py runserver
    python bin/scheduler.py
    rqworker


Screenshot
----------

.. image:: https://raw.github.com/avelino/mining/master/docs/docs/img/dashboard-openmining.png
    :alt: Dashboard OpenMining

.. image:: https://raw.github.com/avelino/mining/master/docs/docs/img/dashboard-filter-openmining.png
    :alt: Dashboard filter OpenMining

.. image:: https://raw.github.com/avelino/mining/master/docs/docs/img/dashboard-apply-filter-openmining.png
    :alt: Dashboard apply filter OpenMining


Sponsor
-------

* `UP! Essência <http://www.upessencia.com.br/>`_
* `Lemes Consultoria <http://www.lemeconsultoria.com.br/>`_
