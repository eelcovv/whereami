.. These are examples of badges you might want to add to your README:
please update the URLs accordingly

    .. image:: https://api.cirrus-ci.com/github/<USER>/whereami.svg?branch=main
        :alt: Built Status
        :target: https://cirrus-ci.com/github/<USER>/whereami
    .. image:: https://readthedocs.org/projects/whereami/badge/?version=latest
        :alt: ReadTheDocs
        :target: https://whereami.readthedocs.io/en/stable/
    .. image:: https://img.shields.io/coveralls/github/<USER>/whereami/main.svg
        :alt: Coveralls
        :target: https://coveralls.io/r/<USER>/whereami
    .. image:: https://img.shields.io/pypi/v/whereami.svg
        :alt: PyPI-Server
        :target: https://pypi.org/project/whereami/
    .. image:: https://img.shields.io/conda/vn/conda-forge/whereami.svg
        :alt: Conda-Forge
        :target: https://anaconda.org/conda-forge/whereami
    .. image:: https://pepy.tech/badge/whereami/month
        :alt: Monthly Downloads
        :target: https://pepy.tech/project/whereami
    .. image:: https://img.shields.io/twitter/url/http/shields.io.svg?style=social&label=Twitter
        :alt: Twitter
        :target: https://twitter.com/whereami

.. image:: https://img.shields.io/badge/-PyScaffold-005CA0?logo=pyscaffold
    :alt: Project generated with PyScaffold
    :target: https://pyscaffold.org/

|

========
whereami
========


    Get the geolocation of the current server


This package provides a command line utility to get the geolocation of the current server.

Installation
============

To install with conda do::

   conda install whereami

To install with pip do::

   pip install whereami

Requirements
------------

- appdirs
- country_converter
- geocoder
- latloncalc

Usage
=====

You can simply run on the command line::

  whereami

This yields the location of the server you are currently logged into, e.g.::

   >>> Server 37.97.253.1 @ Amsterdam/Netherlands (NL) has coordinates (52° 22′ 26.4″ N, 4° 53′ 22.9″ E)

Other output formats can be picked as well. If you only want the geo coordinates of the location of your server you can do::

   whereami --format sexagesimal

which yields::

   >>> 52° 22′ 26.4″ N, 4° 53′ 22.9″ E

Or if you prefer to have a decimal representation of your server's location you can do::

   whereami --format decimal

resulting in::

   >>> 52.37, 4.89

To get the name of the location in stead of coordinates you can do::

   whereami --format human

which gives::

   >>> Amsterdam/Netherlands (NL)










.. _pyscaffold-notes:

Note
====

This project has been set up using PyScaffold 4.2.1. For details and usage
information on PyScaffold see https://pyscaffold.org/.
