.. _serversetup:

Hosting learning applications and the web API
=============================================

This chapter is a guide server setup for the MultiLA software platform either on a server or a local development machine. Note that only Unix-based operating systems (Linux, MacOS) are covered by this guide. The software should run on Windows systems as well but may require different setup steps.

Hosting learning applications
-----------------------------

Server setup
^^^^^^^^^^^^

The server needs to have R installed. It's highly recommended to use `renv`_ during development and also for deployment, so you should install this package also on the server.

For hosting learning applications, you need to install and setup a Shiny server as explained in the `Shiny administrator's guide <https://docs.posit.co/shiny-server/>`_. You must also install a recent version of `pandoc <https://pandoc.org/>`_ on the server (``sudo apt install pandoc`` on Debian or Ubuntu based Linux systems).

It's recommended to implement at least the following security measures on the server:

- Run the Shiny applications via an HTTPS proxy (as explained `this blog post <https://emeraldreverie.org/1/01/01/>`_).
- Restrict R code execution on the server via RApparmor (see `learnr documentation <https://rstudio.github.io/learnr/articles/publishing.html#start-and-cleanup-hooks>`_).

Learning application deployment
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

It's highly recommended to use `renv`_ during deployment.

First, create a snapshot of the necessary packages for your learning app by running ``renv::snapshot()`` locally. Create a folder for your application on the server. Then copy *only* the following files from your local machine to the app folder on the server:

- RMarkdown document (.Rmd) – make sure to set the ``apiserver`` in the frontmatter options to the URL at which the web API will be available, e.g. ``https://<SERVER>/api/``
- ``renv.lock`` with all dependencies necessary to run your learning application
- possible embedded images, CSS, JavaScript, etc. in folder ``images`` or ``www``

On the server, navigate to the app folder and open an R session there (by simply invoking ``R`` in the terminal. There, run the following code to set up renv for the app and install all packages that reported in ``renv.lock``:

.. code-block:: R

    renv::init()
    renv::restore()

Please note that you need to run ``renv::snapshot()`` locally every time you update/install packages and that you also need to copy the updated ``renv.lock`` to the app folder on the server and run ``renv::restore()`` within an R session there.

Check that the application was successfully deployed by visiting the respective URL in your browser (depends on the Shiny server setup). If anything fails, check the Shiny logs (``~/ShinyApps/log``, ``/var/log/shiny-server/access.log``, ``/var/log/shiny-server.log``).

When you publish an update for your learning application, you must also set a new timestamp to a special file named ``restart.txt`` in the learning application project folder on the server via ``touch restart.txt``.

Setting up the web API and the administration interface
-------------------------------------------------------

.. note:: The following instructions all refer to the *webapi* component of the MultiLA software platform, which is a `Django`_ web application running inside a docker container. You must initially clone the current version from its `GitHub repository <https://github.com/IFAFMultiLA/webapi>`_.

Prerequisites
^^^^^^^^^^^^^

- Docker with Docker Compose v2 (recommended: run Docker in *rootless* mode)
- an HTTP server such as Apache or nginx used as proxy
- a valid SSL certificate – **only run this service via HTTPS in production!**

Initial deployment
^^^^^^^^^^^^^^^^^^

1. Create a Docker Compose configuration like the following as ``docker/compose_prod.yml``:

.. code-block:: yaml

    version: '2'

    services:
      # # optional: DB admin web interface accessible on local port 8081
      # adminer:
      #  image: adminer
      #  ports:
      #    - 127.0.0.1:8081:8080
      #  restart: always

      db:
        image: postgres
        volumes:
          - '../data/db:/var/lib/postgresql/data'
          - '../data/backups:/data_backup'
        environment:
          - 'POSTGRES_USER=admin'
          - 'POSTGRES_PASSWORD=<CHANGE_THIS>'
          - 'POSTGRES_DB=multila'
        restart: always

      web:
        build:
          context: ..
          dockerfile: ./docker/Dockerfile_prod
        command: python -m uvicorn --host 0.0.0.0 --port 8000 multila.asgi:application
        volumes:
          - '../src:/code'
          - '../data/export:/data_export'
        ports:
          - "8000:8000"
        environment:
          - 'POSTGRES_USER=admin'
          - 'POSTGRES_PASSWORD=<CHANGE_THIS>'
          - 'POSTGRES_DB=multila'
          - 'DJANGO_SETTINGS_MODULE=multila.settings_prod'
          - 'SECRET_KEY=<CHANGE_THIS>'
        depends_on:
          - db
        restart: always


2. Make sure the correct server and directory is entered in ``Makefile`` under ``SERVER`` and ``APPDIR``. Then run:

    - ``make collectstatic`` to copy all static files to the ``static_files`` directory
    - ``make sync`` to upload all files to the server

3. On the server, do the following:

    - run ``make copy_static`` to copy the static files to the directory ``/var/www/api_static_files/`` (you must have
      the permissions to do so)
    - run ``make build`` to build the web application
    - run ``make create`` to create the docker containers
    - run ``make up`` to launch the containers
    - run ``make migrate`` to initialize the DB
    - run ``make superuser`` to create a backend admin user – **use a secure password**
    - run ``make check`` to check the deployment
    - run ``make test`` to run the tests in the deployment environment
    - you may run ``make logs`` and/or ``curl http://0.0.0.0:8000/`` to check if the web server is running

4. On the server, create an HTTP proxy to forward HTTP requests to the server to the docker container running the web application. For example, a configuration for the Apache webserver that forwards all requests to ``https://<HOST>/api/`` would use the following::

    # setup static files (and prevent them to be passed through the proxy)
    ProxyPass /api_static_files !
    Alias /api_static_files /var/www/api_static_files

    # setup proxy for API
    ProxyPass /api/ http://0.0.0.0:8000/
    ProxyPassReverse /api/ http://0.0.0.0:8000/

All requests to ``https://<SERVER>/api/`` should then be forwarded to the web application.

Check that the deployment of the web API was successful by visiting ``https://<SERVER>/api/admin/`` and entering your backend admin user credentials (from ``make superuser``).

(Optional) Publishing updates
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

In case there are updates to the web API component, you can do the following:

- locally, run ``make testsync`` and ``make sync`` to publish updated files to the server
- on the server, optional run ``make migrate`` to update the database and run ``make restart_web`` to restart the web
  application (there is a shortcut ``make server_restart_web`` that you can run *locally* in order to restart the web
  application on the server)
- if there are changes in the static files, you should run ``make collectstatic`` before ``make sync`` and then run
  ``make copy_static`` on the server
- if there are changes in the dependencies, you need to rebuild the container as decribed above under
  *Initial deployment*, point (3)

(Optional) DB administration interface
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

If you have enabled the ``adminer`` service in the docker compose file above, a small DB administration web interface
is running on port 8081 on the server. For security reasons, it is only accessible from localhost, i.e. you need to set
up an SSH tunnel to make it available remotely from your machine. You can do so on your machine by running::

    ssh -N -L 8081:localhost:8081 <USER>@<SERVER>

, where ``<USER>@<SERVER>`` are the login name and the host name of the server, where docker containers are running.
A shortcut is available in the Makefile as ``adminer_tunnel``. You can then go to ``http://localhost:8081/`` in your
browser and login to the Postgres server (not MySQL!) using the ``POSTGRES_USER`` and ``POSTGRES_PASSWORD`` listed in
the environment variabless of the docker compose file.

(Optional) DB backups
^^^^^^^^^^^^^^^^^^^^^

You can use ``make dbbackup`` on the server to generate a PostgreSQL database dump with the current timestamp under
``data/backups/``. It's advisable to run this command regularly, e.g. via a cronjob, and then copy the database dumps
to a backup destination e.g. via ``make download_dbbackup``.

