Development
===========

The :code:`Code Lab` repository contains two subprojects:

1. Frontend
2. Backend


Frontend
========

.. csv-table::
    :header-rows: 1

    Dependency, Version
    :code:`Node.js`, 18.4.0
    :code:`npm`, 8.13.2


To install the packages, use:

.. code:: console

    $ cd frontend
    $ npm install

To serve the project, execute:

.. code:: console

    $ npm run dev

In order to run the backend in development mode, run::

.. code:: console

    $ make dev

Open the browser at :code:`http://localhost:3000` to test the frontend.


.. tip::

    ``npm run dev`` serves the frontend in an alternative way
    than the one provided by ``make dev``.


Backend
=======

.. csv-table::
    :header-rows: 1

    Dependency, Version
    :code:`Python`, 3.10
    :code:`Poetry`, 1.1.2
    :code:`Docker`, 20.10.6


To install the packages, use::

    $ poetry install

Then, activate the virtual environment::

    $ poetry shell

And then, execute::

    $ make dev


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

.. tip::

    See the `Makefile <codebox/Makefile>`_ for other tasks.
