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

.. code-block:: bash

	pip install -r requirements_dev.txt


Requirements
------------

* MongoDB (Admin)
* Redis (Queue and DataWarehouse)
* Bower (Install frontend libs, nodejs depends)


Install
-------

.. code-block:: bash

    pip install -r requirements.txt
    pip install numexpr==2.3
    cp mining.sample.ini mining.ini
    bower install


Run
---

.. code-block:: bash

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
