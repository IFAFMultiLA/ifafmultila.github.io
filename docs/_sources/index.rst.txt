.. webapi documentation master file

MultiLA software platform
=========================

Welcome to the documentation for the *MultiLA* software platform. This platform allows you to create web-based, interactive learning applications and track the user interactions with them for learning analytics.

This software platform was developed as part of the `IFAF MultiLA project`_ at the `HTW Berlin`_ and `HWR Berlin`_.

.. container:: images

    .. image:: img/ifaf_logo.jpg
        :width: 200px
        :target: `IFAF Berlin`_

    .. image:: img/htw_logo.jpg
        :width: 200px
        :target: `HTW Berlin`_

    .. image:: img/hwr_logo.png
        :width: 200px
        :target: `HWR Berlin`_


Main features
-------------

- create interactive learning applications via RMarkdown notation using an extension to the popular `learnr`_ R package
- highly granular, configurable and anonymous tracking of user interactions with the learning applications: mouse movements, clicks, exercise submissions, etc.
- user device category (desktop, tablet, smartphone) detection
- support for A/B-testing experiments
- configurable learning applications: write base applications once, create variants via configurations
- dynamic summaries for learning applications
- web-based administration interface for publishing learning applications, setting up variants and experiments and downloading collected data
- data preparation and analysis scripts to get started with learning analytics for the collected data
- self-hosted solution to run in a Docker environment and an R shiny server

Structure of the documentation
------------------------------

This documentation is divided into several chapters for different target audiences.

- :doc:`learning_apps` (authoring tool guide)
- :doc:`serversetup` (server administration guide)
- :doc:`trackingdata` (learning analytics guide)
- :doc:`devguide` (developer guide)

Table of contents
-----------------

.. toctree::

    learning_apps
    serversetup
    trackingdata
    devguide
    codebook_raw_data
    codebook_prepared_data


Based on open-source projects
-----------------------------

.. container:: images

    .. image:: img/learnr.png
        :width: 100px
        :target: `learnr`_

    .. image:: img/shiny.png
        :width: 100px
        :target: `Shiny`_

    .. image:: img/django.resized.png
        :width: 100px
        :target: `Django`_
