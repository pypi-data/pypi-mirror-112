Shapelets-Python
================
Python client for Shapelets.

Requirements
-------------

This library is only supported for versions of Python 3.7 and above.
This library requires Java SDK 1.8 to be installed in the system.

Installation
------------

.. code-block::

    $ pip install shapelets-solo
    $ python -m shapelets install


Connecting to Shapelets
-----------------------

To start using Shapelets, the user only has to import the *init_session()* method, and invoke it with the username and
password. By default, the client connects to an embedded server instance in the same machine. However, the library can
be used to interact with other existing deployments. The following code snippet shows the minimum required code to start
using Shapelets.

.. code-block::

    from shapelets import init_session

    client = init_session("admin", "admin")
    # Use client to store/retrieve time-series or to perform analysis on them.
    ...

After executing the blocking *init_session()* method, some processes are launched in background. After that, when all
processes are up and running the user will get back the control. The user should get some messages in the
python console similar to the next.

.. code-block::

    python OK: port:52000, backend:CPU, start:2021-06-21 10:37:09.997083, cwd:a1f5a7d4-d27c-11eb-879f-1826497d56fd, pid:16844
    kotlin OK: port:53666, backend:CPU, start:2021-06-21 10:37:10.008079, cwd:a1f64422-d27c-11eb-b3c4-1826497d56fd, pid:13568
    server OK: port:8443, backend:CPU, start:2021-06-21 10:37:10.018081, cwd:a1f7ca98-d27c-11eb-85c5-1826497d56fd, pid:3104
    server is starting, takes a few seconds...
    server is starting, takes a few seconds...
    server is up...
    Login as admin for address https://127.0.0.1


shapelets-solo CLI
------------------------

Shapelets comes along with at shapelets-CLI, this application lets us handle and manage library dependencies and
the slave process lifecycle. The user can start all background processes with the following command.

.. code-block::

    $ python -m shapelets start


In the same manner, we could stop all background processes by executing the following command.

.. code-block::

    $ python -m shapelets stop


If the user needs to know the status of the current background processes, he can execute the following command, it
also shows the timestamp when the process started and its pid.

.. code-block::

    $ python -m shapelets status
    python OK: port:52000, backend:CPU, start:2021-06-21 08:39:10.819721, cwd:266cf292-d26c-11eb-8703-1826497d56fd, pid:8964
    kotlin OK: port:53666, backend:CPU, start:2021-06-21 08:39:10.841743, cwd:267186c0-d26c-11eb-9808-1826497d56fd, pid:9292
    server OK: port:8443, backend:CPU, start:2021-06-21 08:39:10.864724, cwd:2674e1dc-d26c-11eb-a69b-1826497d56fd, pid:12268


Last but no least, one of the most important features of the shapelets CLI is the option to show the activity logs of
the background processes. To access the logs from the server or workers, the user just have to execute the tail
instruction with the pid of the process of interest.

.. code-block::

    $ python -m shapelets tail -p 12268

