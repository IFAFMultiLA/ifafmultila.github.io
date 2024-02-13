.. _devguide:

Extending the MultiLA software platform
=======================================

This part of the documentation represents the development guide for all components of the MultiLA software platform. The chapter starts with an overview of the components and how they communicate with each other. Then, development and deployment of the different components is discussed.

Overview of the software components
-----------------------------------

The following image show an overview of the MultiLA platform components:

.. image:: img/sw-arch.png
    :width: 100%

- the web API is central and provides a common platform for setting up client applications, configuring and sharing them, and tracking user data and feedback
- all data – user generated or operational – is stored in the database

  - only the web API service has direct access to the database – client applications cannot access the database directly

- for *learnr* and Shiny based client applications, there is a package *learnrextra* that provides all necessary (JavaScript) code to interact with the web API and to make client applications *configurable*

  - this allows to quickly create several client applications that share the same code for interfacing with the web API and that can be configured in some details (e.g. including/excluding certain sections, aesthetic changes, etc.)

- the R Shiny server doesn't communicate with the MultiLA web API, only the JavaScript code on the client side implements the communication
- in general, any (web) application can use the MultiLA web API, which means for example R Shiny applications or Jupyter Notebook applications
- it is possible to connect external services for authentication (e.g. Moodle)

Code repositories overview
^^^^^^^^^^^^^^^^^^^^^^^^^^

- Web API and database: `<https://github.com/IFAFMultiLA/webapi>`_
- *learnrextra* R package: `<https://github.com/IFAFMultiLA/learnrextra>`_
- learning applications (using *learnrextra*):

  - TestgenauigkeitBayes (Bayes' Theorem applied to medical testing): `<https://github.com/IFAFMultiLA/TestgenauigkeitBayes>`_
  - Wahrscheinlichkeitsverteilungen (probability distributions): `<https://github.com/IFAFMultiLA/Wahrscheinlichkeitsverteilungen>`_
  - basic learnrextra test application in RMarkdown/learnr  `<https://github.com/IFAFMultiLA/learnrextra_testapp>`_
  - basic learnrextra test application in Shiny `<https://github.com/IFAFMultiLA/learnrextra_testapp_shiny>`_
  - basic learnr test application with Python `<https://github.com/IFAFMultiLA/learnr_py>`_

- scripts for preparing and analysing collected tracking data: `<https://github.com/IFAFMultiLA/TrackingDataScripts>`_
- this documentation: `<https://github.com/IFAFMultiLA/ifafmultila.github.io>`_

Client-server communication
---------------------------

The client-server communication happens on the basis of a RESTful web API implemented in the `WebAPI repository`_ and the main implementation is in ``api/views.py``. The API exposes an OpenAPI schema under the URL ``http[s]://<HOST>/openapi`` when ``settings.DEBUG`` is ``True``.


Client-server communication flowchart
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

- an application session may either require a login or not – this can be configured in the administration backend for  each application session as "authentication mode"
- all API endpoints except for ``session/`` and ``session_login/`` require an HTTP authorization token, a.k.a "user token", even when no login is required
- this makes sure that each request to the API is linked to a user – either to a registered user (when a login is required) or to an anonymous user that is only identified with a unique code (when no login is required)

Without login ("anonymous"):

- doesn't require an account
- user authentication is based on a user token that is generated on first visit and then stored to cookies for re-use

.. image:: img/client-server-noauth.png
    :width: 100%

With login:

- requires that the user has registered an account with email and password

.. image:: img/client-server-login.png
    :width: 100%

Application configuration
^^^^^^^^^^^^^^^^^^^^^^^^^

- to each application, a configuration can be passed when starting the application session
- the API sends the configuration as JSON object after the initial session request (anonymous session) or after log in (session that requires login) – this is displayed as ``app_config`` key in the above figures
- on the client side, the *learnrextra* R package handles reading the configuration and setting up the application accordingly
- the application configuration JSON object has the following format and options::

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


Development of MultiLA platform components
------------------------------------------

This section shows how to set up your local development environment for working on the MultiLA platform components.

General requirements and setup
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

The development setup has been tested on Ubuntu Linux but should work on other Unix based platforms (like MacOS) without problems. Windows may require more effort, but should also work. It's necessary to have recent versions of `pandoc <https://pandoc.org/>`_ and `Docker <https://www.docker.com/>`_ (for the WebAPI) installed on your system and it's recommended to have installed ``make``.

It's recommended to put all components of the MultiLA platform in one folder on your machine. We will refer to this folder as ``multila/``. The recommended structure of this directory is as follows::

    apps/                   – contains all learning applications
    learnrextra/            – R package from https://github.com/IFAFMultiLA/learnrextra
    TrackingDataScripts/    – tracking data preparation & analysis from https://github.com/IFAFMultiLA/TrackingDataScripts
    webapi/                 – MultiLA Web API from https://github.com/IFAFMultiLA/webapi

You should clone the git repositories that you need into the respective folders. The following section describe how to get the respective components working on your machine so that they interact with each other just as on a server.

WebAPI set up
^^^^^^^^^^^^^

After cloning the repository, it's recommended to create a Makefile that contains shortcuts for important terminal commands that allow you to manage and deploy the project. You can use the following template for the Makefile:

.. code-block:: makefile

    COMPFILE := docker/compose_dev.yml
    COMP := compose -f $(COMPFILE)
    EXEC := $(COMP) exec web
    EXECDB := $(COMP) exec db
    SERVER := <SERVER FOR DEPLOYMENT>
    APPDIR := <DIRECTORY ON SERVER FOR DEPLOYMENT>
    SERVER_APP := $(SERVER):$(APPDIR)
    RSYNC_COMMON := -rcv --exclude-from=.rsyncexclude
    NOW := date -Is | sed "s/://g" | cut -d+ -f 1

    up:
        docker $(COMP) up

    down:
        docker $(COMP) down

    build:
        docker $(COMP) build

    create:
        docker $(COMP) create

    enter:
        docker $(EXEC) /bin/bash || echo "web container is not running"

    superuser:
        docker $(EXEC) python manage.py createsuperuser || python src/manage.py createsuperuser

    djangoshell:
        docker $(EXEC) python manage.py shell || python src/manage.py shell

    migrations:
        docker $(EXEC) python manage.py makemigrations || python src/manage.py makemigrations

    migrate:
        docker $(EXEC) python manage.py migrate || python src/manage.py migrate

    dump:
        docker $(EXEC) python manage.py dumpdata -o /fixtures/dump-`$(NOW)`.json.gz || python src/manage.py dumpdata -o data/fixtures/dump-`$(NOW)`.json.gz

    dbbackup:
        docker $(EXECDB) /bin/bash -c 'pg_dump -U admin -F c multila > /data_backup/local_dev_multila-`$(NOW)`.pgdump'

    collectstatic:
        docker $(EXEC) python manage.py collectstatic || python src/manage.py collectstatic

    test:
        docker $(EXEC) python manage.py test api || python src/manage.py test api

    sync:
        rsync $(RSYNC_COMMON) . $(SERVER_APP) && ssh $(SERVER) "mv $(APPDIR)/Makefile_server $(APPDIR)/Makefile"

    testsync:
        rsync $(RSYNC_COMMON) -n . $(SERVER_APP)

    adminer_tunnel:
        ssh -N -L 8081:localhost:8081 $(SERVER)

    server_restart_web:
        ssh $(SERVER) 'cd $(APPDIR) && make restart_web'

You should also create a second Makefile, named ``Makefile_server``, that will be copied to the server on deployment and contains management commands to be run on the server:

.. code-block:: makefile

    COMPFILE := docker/compose_prod.yml
    COMP := compose -f $(COMPFILE)
    EXEC := $(COMP) exec web
    EXECDB := $(COMP) exec db
    NOW := date -Is | sed "s/://g" | cut -d+ -f 1

    up:
        docker $(COMP) up -d

    logs:
        docker $(COMP) logs -f

    down:
        docker $(COMP) down

    restart_web:
        docker $(COMP) restart web

    build:
        docker $(COMP) build

    create:
        docker $(COMP) create

    enter:
        docker $(EXEC) /bin/bash

    migrate:
        docker $(EXEC) python manage.py migrate

    check:
        docker $(EXEC) python manage.py check --deploy

    test:
        docker $(EXEC) python manage.py test api

    superuser:
        docker $(EXEC) python manage.py createsuperuser

    copy_static:
        cp -r static_files/* /var/www/api_static_files/

    dbbackup:
        docker $(EXECDB) /bin/bash -c 'pg_dump -U admin -F c multila > /data_backup/multila-`$(NOW)`.pgdump'


There are two ways to set up a local development environment: either by using a Python virtual environment *(venv)*
on the local machine to run the Python interpreter or by using a Python interpreter inside a Docker container. The
latter is currently harder to set up in conjunction with an IDE.

Option 1: Using a venv on the local machine
"""""""""""""""""""""""""""""""""""""""""""

- create a Python 3.11 virtual environment and activate it (e.g. via ``python3 -m venv venv`` in the project root
  directory and then activating it via ``source venv/bin/activate``)
- install the required packages via pip: ``pip install -r requirements.txt``
- create a project in your IDE, set up the Python interpreter as the one you just created in the virtual environment
- copy ``docker/compose_dev_db_only.yml`` to ``docker/compose_dev.yml``
- start the docker services for the first time via ``make up`` or via your IDE's docker interface

  - **note:** the first start of the "web" service may fail, since the database is initialized in parallel and may not
    be ready yet when "web" is started – simply starting the services as second time should solve the problem

- optional: create a launch configuration for Django in your IDE
- start the web application using the launch configuration in your IDE or use ``python src/manage.py runserver``

Option 2: Using a Python interpreter inside a docker container
""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""

- copy ``docker/compose_dev_full.yml`` to ``docker/compose_dev.yml``
- create a project in your IDE, set up a connection to Docker and set up to use the Python interpreter inside the
  ``multila-web`` service

  - for set up with PyCharm Professional, `see here <https://www.jetbrains.com/help/pycharm/using-docker-compose-as-a-remote-interpreter.html>`_

- start all services for a first time

  - **note:** the first start of the "web" service may fail, since the database is initialized in parallel and may not
    be ready yet when "web" is started – simply starting the services as second time should solve the problem

- alternatively, to manually control the docker services outside your IDE, use the commands specified in the Makefile:

  - ``make create`` to create the containers
  - ``make up`` to launch all services

Common set up steps for both options
""""""""""""""""""""""""""""""""""""

- when all services were started successfully, run ``make migrate`` to run the initial database migrations
- run ``make superuser`` to create a backend admin user
- the web application is then available under ``http://localhost:8000``
- a simple database administration web interface is then available under ``http://localhost:8080/admin``
- to check if everything works, you should run ``make test``

learnextra R package setup
^^^^^^^^^^^^^^^^^^^^^^^^^^

The `learnrextra`_ R package is a central part of the MultiLA software platform. It's an extension to the `learnr`_ to create learning applications that allow to anonymously track usage data and collect this data via the web API. It furthermore provides some extra features to learnr such as an optional summary panel and the ability to create several variants of a single base learning application via configurations.

Installation
""""""""""""

- install `renv`_ if you haven't yet
- then install all R dependencies via ``renv::restore()``
- also install `NodeJS <https://nodejs.org/>`_ and the `Node package manager (npm) <https://www.npmjs.com/>`_
- then run ``npm install`` to install all JavaScript dependencies
- run ``npm run build`` to check if building the JavaScript sources works

Project structure
"""""""""""""""""

Folder ``inst/rmarkdown/templates/tutorial``:

- template for creating new learning applications
- sub-folder ``resources`` contains main JavaScript code, additional CSS and HTML

Folder ``learnrextra-js``:

- contains JavaScript code for additional custom packages that need to be built locally (see section below)
- sub-folder ``format`` contains JavaScript code for the ``tutorial`` object
- sub-folder ``musjs`` contains JavaScript code for a modified variant of the `musjs project <https://github.com/ineventapp/musjs>`_

Folder ``R``:

- contains R code for the few functions that this packages exposes

Building custom JavaScript packages
"""""""""""""""""""""""""""""""""""

npm run build


Building the documentation
""""""""""""""""""""""""""

devtools::document()


