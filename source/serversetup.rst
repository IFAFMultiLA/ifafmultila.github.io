.. _serversetup:

Hosting learning applications and the web API
=============================================

This chapter is a guide server setup for the MultiLA software platform either on a server or a local development machine. Note that only Unix-based operating systems (Linux, MacOS) are covered by this guide. The software should run on Windows systems as well, but may require different setup steps.

Hosting learning applications
-----------------------------

Server setup
^^^^^^^^^^^^

The server needs to have R installed. It's highly recommended to use `renv`_ during development and also for deployment, so you should install this package also on the server.

For hosting learning applications, you need to install and setup a Shiny server as explained in the `Shiny administrator's guide <https://docs.posit.co/shiny-server/>`_. You must also install a recent version of `pandoc <https://pandoc.org/>`_ on the server (``sudo apt install pandoc`` on Debian or Ubuntu based Linux systems).

In order to deliver the learning applications via HTTPS, you should run the Shiny applications through a proxy (as explained `this blog post <https://emeraldreverie.org/1/01/01/>`_) such as Apache or Nginx. Make sure to use a valid SSL certificate for HTTPS, e.g. provided via `Let's Encrypt <https://letsencrypt.org/>`_. Configure the proxy to forward all HTTP requests to HTTPS.

Server security measures
^^^^^^^^^^^^^^^^^^^^^^^^

If you're hosting learning applications that include programming tasks, you should understand that anybody using your learning applications can run R code directly on your server. This has severe security implications, so you should make sure to have at least the following security measures in place:

1. The R process that runs the Shiny server (and hence the learning applications) should only have access to the learning applications. It's best to create a separate user for that process (or even for each learning application) and then follow the Shiny server setup guide on `Per-User Application Directories <https://docs.posit.co/shiny-server/#host-per-user-application-directories>`_ and `User Managed Applications <https://docs.posit.co/shiny-server/#let-users-manage-their-own-applications>`_.
2. Restrict R code execution on the server via RApparmor (see `learnr documentation <https://rstudio.github.io/learnr/articles/publishing.html#start-and-cleanup-hooks>`_) and consider using a custom AppArmor profile for R code exercises (see `RAppArmor documentation <https://github.com/jeroen/RAppArmor>`_).

For maximum security, you can also consider running each learning application inside a separate Docker container. Setting this up is however beyond the scope of this documentation.

Deploying a learning application and registering it in the backend system is explained in chapter ":ref:`tracking_data`".

.. _backend_installation:

Setting up the web API and the administration interface
-------------------------------------------------------

The following instructions all refer to the *webapi* component of the MultiLA software platform, which is a `Django`_ web application running inside a docker container. You must initially clone the current version from its `GitHub repository <https://github.com/IFAFMultiLA/webapi>`_. The administration interface supports the option to deploy apps directly via upload, which however requires some more setup work. The respective steps for enabling this feature are explained under ":ref:`setup_app_upload`".

Prerequisites
^^^^^^^^^^^^^

In order to deploy the MultiLA web API and administration interface, you need access to a server with the following things installed and set up:

- Docker with Docker Compose v2 (recommended: run Docker in *rootless* mode),
- an HTTP service such as Apache or nginx used as proxy and for delivering static files,
- a valid SSL certificate – **only run this service via HTTPS in production!**.

Initial deployment
^^^^^^^^^^^^^^^^^^

.. warning:: The following manual assumes that you have an understanding of the command-line interface and permissions system used on Linux servers. The manual doesn't go into detail about setting up the correct directory and file permissions, so that the server setup is secure. **If you're unsure about how to set up a Linux server in a secure way, you should get help from an expert.**

Make sure that you've cloned the `webapi GitHub repository <https://github.com/IFAFMultiLA/webapi>`_ locally and change to the directory of the cloned repository in your terminal.

1. Create a Docker Compose configuration like the following as ``docker/compose_prod.yml``:

.. code-block:: yaml

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
          # optional for app upload feature: path where deployed apps should be placed
          # on your server
          # - '<PATH_TO_APP_UPLOAD_DIRECTORY>:/apps_deployed'
        ports:
          - "8000:8000"
        environment:
          - 'BASE_URL=<SET_BASE_URL_HERE>'
          - 'ALLOWED_HOSTS=<SET_SERVER_IP_HERE>'
          - 'POSTGRES_USER=admin'
          - 'POSTGRES_PASSWORD=<CHANGE_THIS>'
          - 'POSTGRES_DB=multila'
          - 'DJANGO_SETTINGS_MODULE=multila.settings_prod'
          - 'SECRET_KEY=<CHANGE_THIS>'
        depends_on:
          - db
        restart: always

2. Run ``python src/manage.py collectstatic`` inside the repository root directory to copy all static files to the ``static_files`` directory. Then upload all files to your server, e.g. to a directory ``~/webapi``.

3. Log in to the server. Create the directory ``/var/www/api_static_files/`` -- this is the directory, where "static files" such as CSS files or images for the administration interface will be located.

4. Change the directory to the location of the uploaded web API source (i.e. ``~/webapi``). Then do the following:

- copy the static files via ``cp -r static_files/* /var/www/api_static_files/`` (you must have the permissions to do so)
- run ``docker compose -f docker/compose_prod.yml build --no-cache`` to build the web API container
- run ``docker compose -f docker/compose_prod.yml create`` to create all necessary containers
- run ``docker compose -f docker/compose_prod.yml up -d`` to launch the containers
- run ``docker compose -f docker/compose_prod.yml exec web python manage.py migrate`` to initialize the DB
- run ``docker compose -f docker/compose_prod.yml exec web python manage.py createsuperuser`` to create a backend admin user; this is the password used for the first login to the administration interface -- **use a secure password**
- run ``docker compose -f docker/compose_prod.yml exec web python manage.py check --deploy`` to check the deployment
- run ``docker compose -f docker/compose_prod.yml exec web python manage.py test api`` to run the tests in the deployment environment
- you may run ``docker compose -f docker/compose_prod.yml logs -f`` to view the logs and/or ``curl http://0.0.0.0:8000/`` to check if the web server is running

5. On the server, setup your HTTP service (e.g. Apache or nginx) to do two tasks: 1) it must serve the static files at ``/var/www/api_static_files`` and 2) it must forward HTTP requests from outside to the server on to the docker container that runs the web application (proxy server).

An example configuration for the Apache webserver that delivers static files at ``https://<HOST>/api_static_files/`` and forwards all requests at ``https://<HOST>/api/`` to the Docker container would use the following::

    # setup static files (and prevent them to be passed through the proxy)
    ProxyPass /api_static_files !
    Alias /api_static_files /var/www/api_static_files

    # setup proxy for API
    ProxyPass /api/ http://0.0.0.0:8000/
    ProxyPassReverse /api/ http://0.0.0.0:8000/

All requests to ``https://<SERVER>/api/`` should then be forwarded to the web application.

Check that the deployment of the web API was successful by visiting ``https://<SERVER>/api/admin/`` and entering your backend admin user credentials from the ``createsuperuser`` step above.

(Optional) Publishing updates
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

In case there are updates to the web API component, you can do the following:

- If there are changes in the static files, you should run ``python src/manage.py collectstatic`` locally first.
- Publish updated files to the server (it's recommended to use ``rsync`` for that).
- If there are changes in the static files, you need to copy the static files via ``cp -r static_files/* /var/www/api_static_files/`` on the server.
- On the server, optional run ``docker compose -f docker/compose_prod.yml exec web python manage.py migrate`` to update the database.
- Run ``docker compose -f docker/compose_prod.yml restart web`` to restart the web application.

.. note:: If there are changes in the dependencies, you need to rebuild the container as decribed above under *Initial deployment*, point 4.

(Optional) DB administration interface
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

If you have enabled the ``adminer`` service in the docker compose file above, a small DB administration web interface
is running on port 8081 on the server. For security reasons, it is only accessible from localhost, i.e. you need to set
up an SSH tunnel to make it available remotely from your machine. You can do so on your machine by running::

    ssh -N -L 8081:localhost:8081 <USER>@<SERVER>

, where ``<USER>@<SERVER>`` are the login name and the host name of the server, where docker containers are running.
You can then go to ``http://localhost:8081/`` in your
browser and login to the Postgres server (not MySQL!) using the ``POSTGRES_USER`` and ``POSTGRES_PASSWORD`` listed in
the environment variabless of the docker compose file.

(Optional) DB backups
^^^^^^^^^^^^^^^^^^^^^

You can use

.. code-block::

    docker compose -f docker/compose_prod.yml exec db \
        /bin/bash -c 'pg_dump -U admin -F c multila \
        > /data_backup/multila-`date -Is | sed "s/://g" | cut -d+ -f 1`.pgdump'

on the server to generate a PostgreSQL database dump with the current timestamp under ``data/backups/``. It's advisable to run this command regularly, e.g. via a cronjob, and then copy the database dumps to a backup destination.

(Optional) Chatbot feature
^^^^^^^^^^^^^^^^^^^^^^^^^^

The MultiLA platform allows to integrate a chatbot in the learning apps as an adaptive learning assistant. The backend will communicate with a chat API provider for this purpose, e.g. with OpenAI's GPT model API. So far, only chat APIs that use OpenAI's web API format are supported (so hosting your own model via LM Studio for example works).

To set up this feature, you first need to install some additional packages inside the web container. To do so, uncomment the line ``# RUN pip install -r requirements_extra.txt`` in ``docker/Dockerfile_prod`` and rebuild the container.

Next, you need to edit the ``src/multila/settings_prod.py`` file of the web API backend and replace ``CHATBOT_API = None`` with the following code that you need to adapt to your set up (see code comments below):

.. code-block:: python

    CHATBOT_API = {
        # create a dictionary where labels map to provider options
        "providers": {  # note that the label is not allowed to use the string ' | '
            # this is an example using OpenAI's services
            "openai": {
                "key": os.environ.get("OPENAI_API_KEY"),
                "provider": "openai",
                "available_models": ["gpt-3.5-turbo", "gpt-4o-mini", "gpt-4o"],
            },
            # this is an example of how to use a self-hosted service using LM studio
            "lm-studio": {
                "key": "not needed",
                "provider": "openai",  # LM studio uses the OpenAI API format
                "setup_options": {"base_url": os.environ.get("MY_LLM_SERVER")},
                "request_options": dict(max_tokens=500, stop=None, temperature=0.5),
                "available_models": [
                    # list your installed models here
                    ...,
                ],
            },
            # set more providers here
        },
        "content_section_identifier_pattern": r"mainContentElem-\d+$",
         # default system role prompt template per language
         # use $doc_text placeholder to include the app's text representation in the prompt
        "system_role_templates": {
            "en": "You are a teacher in data science and statistics. Consider the following learning material enclosed "
            'by "---" marks. Before each content section in the document, there is a unique identifier for that '
            'section denoted as "mainContentElem-#". "#" is a placeholder for a number.'
            "\n\n---\n\n$doc_text\n\n---\n\nNow give a short answer to the following question and, if possible, refer to "
            "the learning material. If you are referring to the learning material, end your answer with a new paragraph "
            'containing only "mainContentElem-#" and replace "#" with the respective section number.',
            "de": "Du bist Lehrkraft im Bereich Data Science und Statistik. Berücksichtige das folgende "
            'Lehrmaterial, das durch "---"-Markierungen eingeschlossen ist. Vor jedem Inhaltsabschnitt im Dokument '
            'gibt es eine eindeutige Kennung für diesen Abschnitt, die mit "mainContentElem-#" angegeben ist. "#" '
            "ist ein Platzhalter für eine Zahl.\n\n---\n\n$doc_text\n\n---\n\nGib nun eine kurze Antwort auf "
            "die folgende Frage und beziehe dich, wenn möglich, auf das Lehrmaterial. Wenn du dich auf das "
            "Lehrmaterial beziehst, beende deine Antwort mit einem neuen Absatz, der ausschließlich den Text "
            '"mainContentElem-#" enthält und ersetze "#" durch die entsprechende Abschnittsnummer.',
        },
         # default user role prompt template per language
         # use $doc_text placeholder to include the app's text representation in the prompt and $question for the
         # actual user message
        "user_role_templates": {
            "en": "$question",
            "de": "$question",
        },
    }


.. note:: Any environment variable such as ``"OPENAI_API_KEY"`` or ``"MY_LLM_SERVER"`` used in the settings file above needs to be added to the Docker Compose configuration in the ``environment:`` section of the "web" container with its respective value.

After restarting the web service container, a new option labelled "Enable chatbot choosing a provider and model" will appear in the administration interface for all application configurations.

.. _setup_app_upload:

(Optional) App upload feature
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

In order to use the app upload feature, you first need to create a directory on the server, where uploaded apps will be placed. Hence this directory must be writable for the user that runs the *webapi* docker container and also for the user that runs the Shiny server. This directory will be called ``<APP_UPLOAD_DIRECTORY>`` below.

Next, you need to edit the Docker Compose configuration ``docker/compose_prod.yml`` to add the following environment variables for the ``web`` container:

.. code-block:: yaml

    services:

      # [ other services ... ]

      web:
        # [ other directives ... ]
        environment:
          # [ other directives ... ]
          # path where deployed apps should be placed on your server
          - 'APP_UPLOAD_PATH=<APP_UPLOAD_DIRECTORY>'
          # path to app logs (usually "log" inside the upload directory)
          - 'APP_LOG_PATH=<APP_UPLOAD_DIRECTORY>/log'
          # base URL for all apps, i.e. the Shiny server URL
          - 'APP_BASE_URL=<BASE_URL_FOR_UPLOADED_APPS>'
          # app removal mode; if "delete", remove the whole app directory; if
          # "remove.txt" write a remove.txt file in the app directory; otherwise
          # do nothing
          - 'APP_REMOVE_MODE=remove.txt'
          # optional path to a "trigger file" that is updated (via "touch") whenever
          # there was a change to any deployed app
          - 'APP_UPLOAD_TRIGGER_FILE=<APP_UPLOAD_DIRECTORY>/update'

Don't forget to recreate and relaunch the container after these changes. You should now see an "Upload app" field in the "Add application" form. If the file permissions are correctly set, uploading an app should already work. Next, we must set up a service, that will manage the actual deployment of the apps once they're uploaded or removed.

For this, we first create a management shell script that iterates through all apps in ``<APP_UPLOAD_DIRECTORY>`` and performs the management operations that are indicated by special files like ``install.txt``. Set ``<USER>`` to the system user that runs the Shiny apps. Set ``<GROUP>`` to the system group that should own the app directories. Also, create a directory for deleted apps and set the path in ``<GRAVEYARD_PATH>``. Alternatively, set this variable to an empty string to directly remove the files of deleted apps.

The following script is named ``manage_deployed_apps.sh`` and will be run as root, so you can place it for example in ``/root/bin``.

.. code-block:: bash

    #!/bin/bash

    target_usr=<USER>
    target_grp=<GROUP>
    target_permissions=0775
    graveyard_path="<GRAVEYARD_PATH>"

    if [ -n "$graveyard_path" ] && [ ! -d "$graveyard_path" ] ; then
        echo "error: graveyard_path is set to '$graveyard_path' but this directory doesn't exist."
        exit 1
    fi

    # Check if an argument is given
    if [ -z "$1" ]; then
        echo "error: no path provided."
        echo "usage: $0 <path>"
        exit 1
    fi

    deploy_path="$1"

    # Check if the path exists
    if [ ! -d "$deploy_path" ]; then
        echo "error: the path '$deploy_path' does not exist."
        exit 1
    fi

    echo "searching for apps in '$deploy_path' that require an action ..."

    # Iterate through all folders in the given path and print the folder names
    while IFS= read -r -d '' app; do
        if [ -f "$app/remove.txt" ] ; then
            baseapp=`basename "$app"`
            if [ -z "$graveyard_path" ] ; then
                echo "> removing app '$baseapp' ..."
                rm -r "$app"
            else
                echo "> moving app '$baseapp' to graveyard ..."
                if [[ $baseapp == *"~old-"* ]] ; then
                   app_graveyard="$graveyard_path/$baseapp"
                else
                   app_graveyard="$graveyard_path/$baseapp-`date -Is`"
                fi
                mv "$app" "$app_graveyard"
            fi
        elif [ -f "$app/install.txt" ] && [ -f "$app/renv.lock" ] ; then
            echo "> installing dependencies for '$(basename "$app")' ..."

            chown -R $target_usr:$target_grp "$app"

            runuser - $target_usr -c "(cd $app && R -e 'renv::activate()' && R -e 'renv::restore()')" > $app/install.log 2>&1

            if [ $? -eq 0 ] ; then
                runuser - $target_usr -c "rm $app/install.txt"
                runuser - $target_usr -c "rm -f $app/install_error.txt"
                runuser - $target_usr -c "touch $app/restart.txt"
                echo ">> done."
            else
                runuser - $target_usr -c "touch $app/install_error.txt"
                echo ">> installing dependencies failed. check $app/install.log file."
            fi

            chown -R $target_usr:$target_grp "$app"
            chmod $target_permissions "$app"
        fi
    done < <(find "$deploy_path" -mindepth 1 -maxdepth 1 -type d -print0)

    echo "done."

Next, we create a service that runs the above script every time the *trigger file* defined in the ``APP_UPLOAD_TRIGGER_FILE`` variable of the Docker Compose file above is updated. For this, you need to make sure that *inotify* is installed on the server (the package is named ``inotify-tools`` on Debian-based Linux systems). We then create a bash script named ``manage_deployed_apps-service.sh``, which will also be run as root and can be placed in ``/root/bin``.

.. code-block:: bash

    #!/bin/bash

    deploy_path="<APP_UPLOAD_DIRECTORY>"
    watch_file="$deploy_path/update"
    watch_file_owner=<USER>
    mgmt_script=/root/bin/manage_deployed_apps.sh

    if [ ! -d "$deploy_path" ] ; then
        >&2 echo "cannot access app deployment directory '$deploy_path'"
        exit 1
    fi

    touch $watch_file
    chown $watch_file_owner:$watch_file_owner $watch_file
    inotifywait -m --format '%e %w %f' $watch_file \
    | while read event dir filename; do
        sleep 1
        ./$mgmt_script $deploy_path
    done

Finally, we create a systemd service (if your server doesn't use systemd for service management, you must adapt the following steps for your respective service management software). For this, we first create a file ``/lib/systemd/system/multila_manage_deployed_apps.service`` as root with the following content::

    [Unit]
    Description=MultiLA watch script for managing apps deployed via admin web interface.

    [Service]
    ExecStart=/root/bin/manage_deployed_apps-service.sh

    [Install]
    WantedBy=multi-user.target

Then we enable and start the service (also as root)::

    systemctl enable multila_manage_deployed_apps.service
    systemctl start multila_manage_deployed_apps.service

Check that the service works by running ``systemctl status multila_manage_deployed_apps.service`` and by uploading an app via the administration interface. You can see the log for this service with the command ``journalctl -u multila_manage_deployed_apps.service -b``.
