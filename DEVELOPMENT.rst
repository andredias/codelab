Development
===========

The :code:`Code Lab` repository contains three subprojects:

1. Frontend
2. Backend
3. Codebox


Frontend
========

.. csv-table::
    :header-rows: 1

    Dependency, Version
    :code:`Node.js`, 14
    :code:`npm`, 7.9


To install the packages, use::

    $ npm install

To serve the project, execute::

    $ npm run serve

Open the browser at :code:`http://localhost:8080`.


Backend
=======

.. csv-table::
    :header-rows: 1

    Dependency, Version
    :code:`Python`, 3.9
    :code:`Poetry`, 1.1.2
    :code:`Docker`, 20.10.6


To install the packages, use::

    $ poetry install

Then, activate the virtual environment::

    $ poetry shell

To run the project,
first it is necessary to have Redis running::

    $ docker run -d -p 6379:6379 --rm --name redis redis:alpine

And then, execute::

    $ make run


.. tip::

    See the `Makefile <backend/Makefile>`_ for other tasks.


Codebox
=======

Codebox is not standalone.
Code Lab initiates a new Codebox container each time it needs to run a project.


To install the packages, use::

    $ poetry install

Then, activate the virtual environment::

    $ poetry shell

To test it, execute::

    $ make test_in_container
