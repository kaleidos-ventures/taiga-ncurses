taiga-ncurses
=================

.. image:: http://kaleidos.net/static/img/badge.png
    :target: http://kaleidos.net/community/greenmine/
.. image:: https://api.travis-ci.org/kaleidos/taiga-ncurses.png?branch=master
    :target: https://travis-ci.org/kaleidos/taiga-ncurses
.. image:: https://coveralls.io/repos/kaleidos/taiga-ncurses/badge.png?branch=master
    :target: https://coveralls.io/r/kaleidos/taiga-ncurses?branch=master
.. image:: https://d2weczhvl823v0.cloudfront.net/kaleidos/taiga-ncurses/trend.png
    :alt: Bitdeli badge
    :target: https://bitdeli.com/free

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
