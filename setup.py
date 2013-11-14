# -*- coding: utf-8 -*-

"""
gmncurses
~~~~~~

A text interface to GreenMine.
"""

from setuptools import setup, find_packages

REQUIREMENTS = [
    "requests==2.0.1",
    "urwid==1.1.1",
]


NAME = "gmncurses"
DESCRIPTION = "A text interface to GreenMine."
VERSION = "0.0.0"

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
