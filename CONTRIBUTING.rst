========================
Contributing to Code Lab
========================

Thank you for investing your time in contributing to our project!
You can help in different ways: testing, reporting issues, proposing changes, implementing changes.
Let's start by making Code Lab run in your machine.

Code Lab consists of three parts: frontend, backend, and the sandbox (provided by Codebox_).
Frontend and backend are located in this repository
while Codebox is held in a separate one as an independent project.
So, as long as you use Codebox as is and don't modify it,
you don't need to fork or clone the project.


Project Setup
=============

The first step is to clone the project:

.. code:: console

    $ git clone https://github.com/andredias/codelab.git


The second step is to install the version control hooks:

.. code:: console

    $ make install_hooks

This step is optional, but it is recommended to install the hooks
before you start working on the project.
The hooks will run some checks before you commit or push your changes.


The whole project has the following basic dependencies:

.. csv-table::
    :header-rows: 1

    Dependency, Version
    :code:`Node.js`, 18.4.0
    :code:`npm`, 8.13.2
    :code:`Python`, 3.10.4
    :code:`poetry`, 1.1.11
    :code:`Docker`, 23.01.1
    :code:`GNU Make`, 4.3

With everything installed, you might be able to run the project using:

.. code:: console

    $ make run

This command will take care of everything necessary to spin up the application.
It must be accessible at :code:`https://localhost`.

.. important::

    As the access is made via HTTPS in a local environment,
    you need to ignore the browser warning about the certificate and go ahead.


In order to run the application in development mode,
you should run the frontend and backend separately.
In different terminals, run:

.. code:: console

    $ cd frontend
    $ npm run dev

.. code:: console

    $ make dev

Then, visit ``http://localhost:3000`` and test the application.


Backend
-------

To work with the backend, you need to install the dependencies:

.. code:: console

    $ cd backend
    $ poetry install

The ``backend`` directory contains its own ``Makefile`` with some tasks such as
``lint``, ``test`` and ``format``.
You should have the virtual environment activated before running the commands:

.. code:: console

    $ poetry shell
    $ make lint


.. _reporting an issue:

Reporting an Issue
==================

Proposals, enhancements, bugs or tasks should be directly reported on the `issue tracker`_.

When creating a bug issue, provide the following information at least:

#. Steps to reproduce the problem
#. The resulting output
#. The expected output



Contacting the Author
=====================

``Code Lab`` is written and maintained by André Felipe Dias.
You can reach me at Twitter_ or by email (andre.dias@pronus.io).

.. _Codebox project: https://github.com/andredias/codebox
.. _Codebox: https://github.com/andredias/Codebox
.. _issue tracker: https://github.com/andredias/codelab/issues
.. _Mercurial: https://www.mercurial-scm.org/
.. _Poetry: https://python-poetry.org/
.. _Twitter: https://twitter.com/andref_dias
