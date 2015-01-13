Open Mining
===========

.. image:: https://raw.githubusercontent.com/mining/frontend/master/assets/image/openmining.io.png
    :alt: OpenMining

.. image:: https://travis-ci.org/avelino/mining.png?branch=master
    :target: https://travis-ci.org/avelino/mining
    :alt: Build Status - Travis CI

Business Intelligence (BI) Application Server written in Python 


Contribute
----------

Join us on IRC at **#openmining** on freenode (`web access <http://webchat.freenode.net/?channels=openmining>`_).


Requirements
------------

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

**Clone the repository and install it**

.. code:: bash

    $ git clone git@github.com:avelino/mining.git
    $ cd mining
    $ git submodule update
    $ python setup.py install

**Run pip install on project requirements**

.. code:: bash

    $ pip install -r requirements.txt

**Install numexpr**

.. code:: bash

    $ pip install numexpr==2.3

**Copy the sample ini file to mining.ini**

.. code:: bash

    $ cp mining/mining.sample.ini mining/mining.ini

**Install javascript assets using Bower**

.. code:: bash

    $ mining/frontend
    $ bower install

**FAQ**

**If mongodb or redis-server problems**

Install mongodb and redis-server, make sure it running

**If "python manage.py runserver" returns "ConfigParser.NoSectionError: No section: 'mongodb'"**

copy mining/mining.sample.ini to mining/mining.ini


Run
---

.. code:: bash

    python manage.py runserver
    python mining/bin/scheduler.py
    rqworker


Running Demo
------------

.. code:: bash

    python mining/bin/demo/build_admin.py


And now you can login with: username 'admin' and password 'admin'.

Screenshot
----------

**Dashboard OpenMining**

.. image:: https://raw.github.com/avelino/mining/master/docs/docs/img/dashboard-openmining_new.png
    :alt: Dashboard OpenMining

**Dashboard Charts OpenMining**

.. image:: https://raw.github.com/avelino/mining/master/docs/docs/img/charts-openmining_new.png
    :alt: Dashboard Charts OpenMining

**Dashboard Charts OpenMining**

.. image:: https://raw.github.com/avelino/mining/master/docs/docs/img/charts2-openmining_new.png
    :alt: Dashboard Charts OpenMining

**Dashboard Widgets OpenMining**

.. image:: https://raw.github.com/avelino/mining/master/docs/docs/img/widgets-openmining_new.png
    :alt: Dashboard Widgets OpenMining


**Late Scheduler and running Cubes OpenMining**

.. image:: https://raw.github.com/avelino/mining/master/docs/docs/img/late-scheduler-openmining_new.png
    :alt: Late Scheduler and running Cubes OpenMining


Sponsor
-------

* `UP! Essência <http://www.upessencia.com.br/>`_
* `Lemes Consultoria <http://www.lemeconsultoria.com.br/>`_
