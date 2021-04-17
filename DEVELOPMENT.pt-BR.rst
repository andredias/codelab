Desenvolvimento
===============

O repositório do :code:`Code Lab` é formado por três subprojetos:

1. Frontend
2. Backend
3. Codebox



Frontend
========

.. csv-table::
    :header-rows: 1

    Dependência, Versão
    :code:`Node.js`, 14
    :code:`npm`, 7.9


Para instalar os pacotes, use::

    $ npm install

Para iniciar o servidor do projeto, execute::

    $ npm run serve

Em seguida, abra o navegador no endereço :code:`http://localhost:8080`.


Backend
=======

.. csv-table::
    :header-rows: 1

    Dependência, Versão
    :code:`Python`, 3.9
    :code:`Poetry`, 1.1.2
    :code:`Docker`, 20.10.6


Para instalar os pacotes, use::

    $ poetry install

Ative o ambiente virtual::

    $ poetry shell

Para executar o projeto,
primeiro é necessário ter o Redis rodando::

    $ docker run -d -p 6379:6379 --rm --name redis redis:alpine

E agora, execute o projeto::

    $ make run


.. tip::

    Veja o arquivo `Makefile <backend/Makefile>`_ .


Codebox
=======

O :code:`Codebox` não é um projeto autônomo.
O :code:`Code Lab` inicia um novo container do :code:`Codebox`
cada vez que precisa executar o código de um projeto.


Para instalar os pacotes, use::

    $ poetry install

Ative o ambiente virtual::

    $ poetry shell

Para testá-lo, execute::

    $ make test_in_container

.. tip::

    Veja o arquivo `Makefile <backend/Makefile>`_ .
