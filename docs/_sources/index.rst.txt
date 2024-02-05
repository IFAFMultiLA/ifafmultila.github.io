.. webapi documentation master file

MultiLA software plattform
==========================

Welcome to the documentation for the *MultiLA* software platform. This platform allows you to create web-based, interactive learning applications and track the user interactions with them for learning analytics.

This software platform was developed as part of the `IFAF MultiLA project`_ at the `HTW Berlin`_ and `HWR Berlin`_.

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
- self-hosted solution to run in a Docker environment and a R shiny server

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

Indices and tables
------------------

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`

Based on open-source projects
-----------------------------

.. image:: img/learnr.png
    :width: 100px
    :target: `learnr`_

.. image:: img/shiny.png
    :width: 100px
    :target: `Shiny`_

.. image:: img/django.resized.png
    :width: 100px
    :target: `Django`_

.. _IFAF MultiLA project: https://www.htw-berlin.de/forschung/online-forschungskatalog/projekte/projekt/?eid=3251
.. _HTW Berlin: https://www.htw-berlin.de/
.. _HWR Berlin: https://www.hwr-berlin.de/
.. _learnr: https://rstudio.github.io/learnr/
.. _Shiny: https://shiny.posit.co/
.. _Django: https://www.djangoproject.com/
