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

- create interactive learning applications via RMarkdown notation or as standard Shiny applications using the R package `learnrextra_` (an extension to the popular `learnr`_ R package)
- highly granular, configurable and anonymous tracking of user interactions with the learning applications: mouse movements, clicks, exercise submissions, etc.
- support for A/B-testing experiments and integrated surveys
- configurable learning applications: write base applications once, create variants via configurations
- dynamic summaries for learning applications
- web-based administration interface for publishing learning applications, setting up variants and experiments and downloading collected data
- data preparation and analysis scripts to get started with learning analytics for the collected data
- own your data – self-hosted open-source solution to run in a Docker environment and an R shiny server

Live examples and screenshots
-----------------------------

An example learning application is available at `rshiny.f4.htw-berlin.de/BayesTheorem/ <https://rshiny.f4.htw-berlin.de/BayesTheorem/>`_. There is no demo of the administration interface publicly available. However, screenshots of the administration interface are among the following images:

.. container:: gallery

    .. figure:: img/screenshots/example_app_bayes_02_thumb.png
        :width: 330px
        :target: _static/example_app_bayes_02.png

        A learning application about Bayes' Theorem featuring interactive graphics and the dynamic summary panel on the right side.

    .. figure:: img/screenshots/admin_01_thumb.png
        :width: 330px
        :target: _static/admin_01.png

        The overview of registered applications in the administration interface.

    .. figure:: img/screenshots/admin_05_thumb.png
        :width: 330px
        :target: _static/admin_05.png

        The overview of tracking sessions in the administration interface.

    .. figure:: img/screenshots/trackingdata_02_thumb.png
        :width: 330px
        :target: _static/trackingdata_02.png

        Visualized mouse movements from a tracking session.

Besides the learning application about Bayes' theorem, we also published learning applications about discrete and continuous probability distributions. These are however only available in German.

.. container:: gallery

    .. figure:: img/screenshots/discrete_prob_distrib_app_thumb.png
        :width: 330px
        :target: https://rshiny.f4.htw-berlin.de/WVDiskret/

        Learning application about discrete probability distributions.

    .. figure:: img/screenshots/cont_prob_distrib_app_thumb.png
        :width: 330px
        :target: https://rshiny.f4.htw-berlin.de/WVStetig/

        Learning application about continuous probability distributions.

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
