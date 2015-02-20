taiga-ncurses
=================

.. image:: http://kaleidos.net/static/img/badge.png
    :target: http://kaleidos.net/community/greenmine/
.. image:: https://taiga.io/media/support/attachments/article-22/banner-gh.png
    :target: https://taiga.io
.. image:: https://travis-ci.org/taigaio/taiga-ncurses.svg?branch=master
    :target: https://travis-ci.org/taigaio/taiga-ncurses
.. image:: https://coveralls.io/repos/taigaio/taiga-ncurses/badge.svg?branch=master 
    :target: https://coveralls.io/r/taigaio/taiga-ncurses?branch=master



A NCurses client for Taiga.

Project status
--------------

Currently on design phases: This project was a proof of concept to try to create a curses client 
for Taiga in the 6th `PiWeek`_. It isn't finished yet and currently it isn't 
feature complete. You can see some screenshots at https://github.com/taigaio/taiga-ncurses/issues/4#issuecomment-57717386 

Setup development environment
-----------------------------

Just execute these commands in your virtualenv(wrapper):

.. code-block::

    $ pip install -r dev-requirements.txt
    $ python setup.py develop
    $ py.test               # to run the tests
    $ taiga-ncurses         # to run the app


Obviously you need the `taiga backend`_ and, if you don't fancy living in darkness,
you can use the `taiga web client`_, sometimes. :P

Note: taiga-ncurses only runs with python 3.3+.

Community
---------

Taiga has a `mailing list`_. Feel free to join it and ask any questions you may have.

To subscribe for announcements of releases, important changes and so on, please follow 
`@taigaio`_ on Twitter.

.. _taiga backend: https://github.com/kaleidos/taiga-back
.. _taiga web client: https://github.com/kaleidos/taiga-front
.. _mailing list: http://groups.google.com/d/forum/taigaio
.. _@taigaio: https://twitter.com/taigaio
.. _PiWeek: http://piweek.com
