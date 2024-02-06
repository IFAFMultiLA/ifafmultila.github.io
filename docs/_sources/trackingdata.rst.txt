.. _tracking_data:

Working with tracking data
==========================


Setting up a learning application for tracking
----------------------------------------------

In the chapter ":doc:`serversetup`", you set up a server with the web API that acts as endpoint at ``https://<SERVER>/api/`` for collecting the tracking data that comes from the learning applications. For each application that you deploy, you need to set this endpoint in the frontmatter options of its RMarkdown file under ``apiserver``, e.g.:

.. code-block:: yaml

    # ...
    output:
        learnrextra::tutorial:
            language: en
            apiserver: https://<SERVER>/api/
    # ...

This will make sure that the deployed learning applications know where to send the collected data.

Registering a learning application with the MultiLA administration backend
--------------------------------------------------------------------------

Each learning application for which you want to collect tracking data is required to be registered in the administration interface that is available under ``https://<SERVER>/api/admin/`` after you installed it on a server as explained in chapter ":doc:`serversetup`".

After logging in to the administration interface, go to *API > Applications* and select *Add application*. You will see a form as follows:

.. image:: img/admin-add-app.png
    :align: center

Give the new learning application a name and most importantly, enter the full URL under which it is available, e.g. ``https://<SERVER>/myapp/``.

For each learning application, you can create several *application configuration.* These allow you to create different variants of the same base application. You need to at least create one default configuration, so go to *API > Application configurations > Add*. You will see the following form:

.. image:: img/admin-add-config.png
    :align: center

First, select the application for which you want to create a configuration. Next, create a label and optionally modify the default configuration code. The configuration code is a JSON structure with the following options:

.. code-block::

    {
      "exclude": [<HTML element IDs to exclude>],
      "js": [<additional JavaScript files to load>],
      "css": [<additional CSS files to load>],
      "feedback": <bool>, # enable/disable specific user feedback features
      "summary": <bool>,  # enable/disable displaying summary
      "tracking": {       # enable/disable specific tracking features
        "mouse": <bool>,    # mouse tracking w/ mus.js
        "inputs": <bool>,   # tracking of input changes
        "attribute_changes": <bool>,  # tracking of attribute changes
        "chapters": <bool>  # tracking of switching betw. chapters
      }
    }

After you created one or more application configurations, you finally have to create at least one *application session.* An application session is an instance of your configured learning application for which you collect tracking data. Each application session will receive a unique session ID and therefore a unique URL that you can share. To create an application session, go to *API > Application sessions > Add* and you will be presented the following form:

.. image:: img/admin-add-session.png
    :align: center

Select the application configuration (and hence the target learning application) and specify whether users should need to authenticate via login. Note that the authentication mode is very minimal: it only consists of a user name and password (no user email or other data). It's main purpose is to allow tracking users across different devices and time distinct user sessions. If you don't need that, you should disable user authentication.

.. note:: This hierarchy of *applications → application configurations → application sessions* allows to create several variants of a single learning application (e.g. for A/B testing – see below) and furthermore allows to bind tracking to specific events, e.g. by creating a session for a specific teaching course or workshop. You will then later be able to download and analyse data for these specific application sessions.

After saving, a unique session ID will be created along with a shareable URL that has the format ``https://<SERVER>/myapp/?sess=<UNIQUE_ID>``, as you can also see in the following screenshot:

.. image:: img/admin-add-session.png
    :align: center

The URL is very important: If visiting this URL and consenting to data collection, a *tracking session* will be created for the user and tracking data will be collected as configured in the application configuration while the user interacts with the learning application. This tracking data will be associated with the application session that corresponds to the unique session ID.

Note that it is also possible to set a "default application session." This means that every time someone visits the learning application under its base URL ``https://<SERVER>/myapp/``, the collected data will be automatically associated with the default application session. If no default application session is set, a user will either be forwared to the last application session she or he visited for that application or otherwise tracking will either be disabled. You can set a default application session under *API > Applications.*

(Optional) Creating application sessions gates for A/B tests
------------------------------------------------------------


Monitoring user tracking
------------------------


Downloading and preparing tracking data for analysis
----------------------------------------------------


Descriptive and explorative analysis of tracking data
-----------------------------------------------------

