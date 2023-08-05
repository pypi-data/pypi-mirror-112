.. _installing_bot:

==================
Installing the bot
==================

For Users
=========

For production use, please install from pip.

::

    pip install erin

Then verify it is working by running this command:

::

    $ erin -V

For Developers
==============

Installing from source
----------------------

Erin is very easy to install from source. First clone the latest development version from the master branch.

::

    git clone https://github.com/OpenDebates/Erin.git
    cd Erin/


Since Erin has a lot of dependencies, it is managed by `Poetry <https://python-poetry.org/>`_. Please do not use `pipenv <https://pipenv.pypa.io/en/latest/>`_ however.
It's incompatible with Erin's dependencies and may cause more problems in the future. If you wish to submit a pull request to fix this problem please `read more here <https://github.com/pypa/pipenv/issues/1578>`_

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
