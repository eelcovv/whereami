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

Varying output format
---------------------

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

Note that you can copy-paste the sexagesimal representation  *52° 22′ 26.4″ N, 4° 53′ 22.9″ E* into
google maps in order to show your location on the map.

Distance from your location
---------------------------

This utility can be used to determine the distance of your server to your current location.
For instances, if your are located in Amsterdam, NL and your are logged in onto the google server,
you can do::

    whereami  --my_location Amsterdam,NL

Now, next to the location of your sever, also the distance to your location is given::

    Server 8.8.8.8 @ Mountain View/United States (US) has coordinates (37° 24′ 20.2″ N, 122° 4′ 39.0″ W)
    Distance from Amsterdam,NL (52° 22′ 21.9″ N, 4° 53′ 37.0″ E):  8816km.

You can also specify the server location in your are not logged into it like::

    whereami --ip 8.8.8.8 --my_location Amsterdam,NL

Note the your location does not need to be a server, but can be any address recognised by google.
In case you specify another server and don't specify your location, by
default your location is set to the location of your current server. The distance is calculated
based on this location.





.. _pyscaffold-notes:

Note
====

This project has been set up using PyScaffold 4.2.1. For details and usage
information on PyScaffold see https://pyscaffold.org/.
