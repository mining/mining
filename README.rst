openmining.io
=============

.. image:: https://raw.github.com/avelino/mining/master/assets/image/openmining.io.png
    :alt: OpenMining

.. image:: https://travis-ci.org/avelino/mining.png?branch=master
    :target: https://travis-ci.org/avelino/mining
    :alt: Build Status - Travis CI

Business Intelligence (BI) Application Server written in Python 


Requirements
------------

* Riak (Data Warehouse)
* MongoDB (Admin)
* Redis (Queue)
* Memcache


Install
-------

.. code-block:: bash

    pip install -r requirements.txt
    pip install numexpr==2.3
    mv mining.sample.ini mining.ini
    bower install


Run
---

.. code-block:: bash

    python manage.py
    python bin/scheduler.py
    rqworker


Contribute
----------

.. code-block:: bash

	pip install -r requirements_dev.txt


Screenshot
----------

.. image:: https://raw.github.com/avelino/mining/master/docs/static/dashboard-openmining.png
    :alt: Dashboard OpenMining

.. image:: https://raw.github.com/avelino/mining/master/docs/static/dashboard-filter-openmining.png
    :alt: Dashboard filter OpenMining

.. image:: https://raw.github.com/avelino/mining/master/docs/static/dashboard-apply-filter-openmining.png
    :alt: Dashboard apply filter OpenMining


Sponsor
-------

* `UP! Essência <http://www.upessencia.com.br/>`_
