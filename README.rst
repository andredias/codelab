Overview
========

The `Code Lab`_ project allows you to program directly from the browser,
without any other external dependency.
It is interesting for cases where you want to do a quick experiment
but there is no computer with the language installed and configured nearby.

This project was originally made as a proof of concept
and also to help my students to use different programming languages
without needing to install anything on their machines.


Running Code Lab
================

Dependencies:

.. csv-table::
    :header-rows: 1

    Dependency, Version
    :code:`Node.js`, 14
    :code:`npm`, 7.9
    :code:`Python`, 3.9
    :code:`Docker`, 20.10.6
    :code:`docker-compose`, 1.27.4
    :code:`GNU Make`, 4.2.1


To run the project in :code:`development` mode, execute::

    $ make run

Then, you should access you browser at :code:`https://127.0.0.1`.


Development
===========

To use the project directly from the its development environment,
see `DEVELOPMENT.rst <DEVELOPMENT.rst>`_.


How It Works?
=============

Running code from an unknown source poses security risks
because malicious code can try to take control of the system,
access restricted areas and data or misuse available resources
(memory, processes, disk, etc.).
The way to mitigate those risks is to run the code in a *sandbox*,
which is a type of virtualization of a restricted and controlled environment [1]_.

In the `Code Lab`_,
the *sandbox* is based on a container Docker called Codebox_,
which contains all the languages, libraries and tools offered by :code:`Code Lab`,
but that runs with limitations on user permissions, time, memory and network access restriction.
Even if there is a security breach,
its effects will be contained and then eliminated when the container is destroyed.

Communication is done through :code:`Codebox`'s standard input (:code:`stdin`) and standard output (:code:`stdout`).
The project files, input data and the commands to be executed are sent to :code:`stdin`.
The output (:code:`stdout`) and errors (:code:`stderr`) of the commands
are grouped and returned from :code:`Codebox`'s :code:`stdout`.


.. image:: frontend/src/assets/images/codebox-operation.png


The models used to exchange information are specified in the file :code:`backend/app/models.py`.


Architecture
============

Codebox_ is the most important part, but it doesn't work alone:
It all starts with the web application, which follows the SPA_ standard (Single Page Application)
and is built with Vue.js_.
The backend is hosted in a droplet of :code:`DigitalOcean`.
The application is served through a reverse proxy by Caddy_
and a Hypercorn_ server, which uses the `ASGI (Asynchronous Server Gateway Interface)`_ standard,
and serves the application built with FastAPI_.

The execution of the projects is not immediate.
First, a check is made in the cache (Redis_)
and only if it is not there, the project is executed in :code:`Codebox`.


.. image:: frontend/src/assets/images/codelab_codebox_v2.png


.. note ::

    If you notice, you will see files like :code:`.hgignore` and :code:`.hgtags` in the repository.
    This means that I use Mercurial_ as a version control for my personal projects
    despite hosting them on :code:`GitHub`.


References
===========

.. [1] Sandbox (computer security): https://en.wikipedia.org/wiki/Sandbox_(computer_security)


.. _ASGI (Asynchronous Server Gateway Interface): https://asgi.readthedocs.io/en/latest/introduction.html
.. _Caddy: https://caddyserver.com/
.. _Code Lab: https://codelab.pronus.io
.. _Codebox: https://github.com/andredias/Codebox
.. _FastAPI: https://fastapi.tiangolo.com/
.. _Flexbox: https://css-tricks.com/snippets/css/a-guide-to-flexbox/
.. _Grid Layout: https://css-tricks.com/snippets/css/complete-guide-grid/
.. _Hypercorn: https://pgjones.gitlab.io/hypercorn/
.. _Mercurial: https://www.mercurial-scm.org/
.. _React: https://reactjs.org/
.. _Redis: https://redis.io/
.. _SPA: https://en.wikipedia.org/wiki/Single-page_application
.. _Vue.js: https://v3.vuejs.org/
