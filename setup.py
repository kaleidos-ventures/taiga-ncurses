# -*- coding: utf-8 -*-

"""
A text interface to Taiga.
"""

from gmncurses import __name__, __description__, __version__

from setuptools import setup, find_packages

REQUIREMENTS = [
    "requests==2.0.1",
    "urwid==1.1.1",
    "x256==0.0.3",
]


NAME = __name__
DESCRIPTION = __description__
VERSION = "{0}.{1}".format(*__version__)

setup(name=NAME,
      version=VERSION,
      description=DESCRIPTION,
      packages=find_packages(),
      entry_points={
          "console_scripts": ["gmncurses = gmncurses.cli:main"]
      },
      classifiers=[
          "Development Status :: 3 - Alpha",
          "Environment :: Console :: Curses",
          "Intended Audience :: End Users/Desktop",
          "Operating System :: POSIX :: Linux",
          "Operating System :: MacOS",
          "Programming Language :: Python :: 3.3",
      ],
      install_requires=REQUIREMENTS,)
