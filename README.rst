greenmine-ncurses
=================

.. image:: http://kaleidos.net/static/img/badge.png
    :target: http://kaleidos.net/community/greenmine/
.. image:: https://api.travis-ci.org/kaleidos/greenmine-ncurses.png?branch=master
    :target: https://travis-ci.org/kaleidos/greenmine-ncurses
.. image:: https://coveralls.io/repos/kaleidos/greenmine-ncurses/badge.png?branch=master
    :target: https://coveralls.io/r/kaleidos/greenmine-ncurses?branch=master
.. image:: https://d2weczhvl823v0.cloudfront.net/kaleidos/greenmine-ncurses/trend.png
    :alt: Bitdeli badge
    :target: https://bitdeli.com/free

A NCurses client for GreenMine.

Setup development environment
-----------------------------

Just execute these commands in your virtualenv(wrapper):

.. code-block::

    $ pip install -r dev-requirements.txt
    $ python setup.py develop
    $ gmncurses   # to run the app
    $ py.test     # to run the tests
    

Obviously you need the `greenmine backend`_ and, if you consider yourself a loser,
you can use the `greenmine web client`_, sometimes. ;-)

Note: greenmine-ncurses only runs with python 3.3+.

.. _greenmine backend: https://github.com/kaleidos/greenmine-back
.. _greenmine web client: https://github.com/kaleidos/greenmine-front
