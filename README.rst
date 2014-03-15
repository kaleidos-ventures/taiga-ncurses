taiga-ncurses
=================

.. image:: http://kaleidos.net/static/img/badge.png
    :target: http://kaleidos.net/community/greenmine/
.. image:: https://api.travis-ci.org/taigaio/taiga-ncurses.png?branch=master
    :target: https://travis-ci.org/taigaio/taiga-ncurses
.. image:: https://coveralls.io/repos/taigaio/taiga-ncurses/badge.png?branch=master
    :target: https://coveralls.io/r/taigaio/taiga-ncurses?branch=master


A NCurses client for Taiga.

Setup development environment
-----------------------------

Just execute these commands in your virtualenv(wrapper):

.. code-block::

    $ pip install -r dev-requirements.txt
    $ python setup.py develop
    $ py.test               # to run the tests
    $ taiga-ncurses         # to run the app


Obviously you need the `taiga backend`_ and, if you consider yourself a loser,
you can use the `taiga web client`_, sometimes. ;-)

Note: taiga-ncurses only runs with python 3.3+.

.. _taiga backend: https://github.com/kaleidos/taiga-back
.. _taiga web client: https://github.com/kaleidos/taiga-front
