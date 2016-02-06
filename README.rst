Open Mining
===========

.. image:: https://raw.githubusercontent.com/mining/frontend/master/assets/image/openmining.io.png
    :alt: OpenMining

.. image:: https://travis-ci.org/avelino/mining.png?branch=master
    :target: https://travis-ci.org/avelino/mining
    :alt: Build Status - Travis CI

.. image:: https://coveralls.io/repos/avelino/mining/badge.svg?branch=master&service=github
    :target: https://coveralls.io/github/avelino/mining?branch=master

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

**Clone the repository and install submodule**

.. code:: bash

    $ git clone git@github.com:avelino/mining.git
    $ cd mining
    $ git submodule init
    $ git submodule update

**Run pip install on project requirements**

.. code:: bash

    $ pip install -r requirements.txt

**Copy the sample ini file to mining.ini**

.. code:: bash

    $ cp mining/mining.sample.ini mining/mining.ini

**Install it**

.. code:: bash

    $ python setup.py install

**Install numexpr**

.. code:: bash

    $ pip install numexpr==2.3

**Install javascript assets using Bower**

.. code:: bash

    $ cd mining/frontend
    $ bower install

**FAQ**

**If mongodb or redis-server problems**

Install mongodb and redis-server, make sure it running

**If "python setup.py install" returns "error: can't copy 'mining/mining.ini': doesn't exist or not a regular file"**

copy mining/mining.sample.ini to mining/mining.ini


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


Credits
-------

Authors: Thiago Avelino and `UP! Essência <http://www.upessencia.com.br/>`_

Many thanks to all the contributors!


License
-------

Licensed under the MIT license (see MIT-LICENSE file)
