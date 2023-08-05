.. _installation_index:

============
Installation
============

This bot runs on Erin which is a bot framework. Follow the `instructions here <https://erin.readthedocs.io/en/latest/installation/database.html>`_ to setup a database for Erin.

For Users
=========

For production use, please install from pip.

::

    pip install opendebates

Then verify it is working by running this command:

::

    erin -V

For Developers
==============

Installing from source
----------------------

Open Debates is very easy to install from source. First clone the latest development
version from the master branch.

::

    git clone https://github.com/OpenDebates/OpenDebates.git


OpenDebates is very easy to install from source. First clone the latest development version from the master branch.

::

    git clone https://github.com/OpenDebates/OpenDebates.git
    cd OpenDebates/


Since OpenDebates has a lot of dependencies, it is managed by `Poetry <https://python-poetry.org/>`_.

First install poetry from the instructions provided `here <https://python-poetry.org/docs/#installation>`_. Then create a shell:

::

    poetry shell

You should now see your terminal change to show your are you now using a virtual environment.
Let's install the package dependencies now. This may take a while depending on your machine.


::

    poetry install

Then verify it is working by running this command:

::

    erin -V
