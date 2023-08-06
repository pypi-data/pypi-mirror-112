.. hifis-surveyval
.. Framework to help developing analysis scripts for the HIFIS Software survey.
..
.. SPDX-FileCopyrightText: 2021 HIFIS Software <support@hifis.net>
..
.. SPDX-License-Identifier: GPL-3.0-or-later
..
.. This program is free software: you can redistribute it and/or modify
.. it under the terms of the GNU General Public License as published by
.. the Free Software Foundation, either version 3 of the License, or
.. (at your option) any later version.
..
.. This program is distributed in the hope that it will be useful,
.. but WITHOUT ANY WARRANTY; without even the implied warranty of
.. MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
.. GNU General Public License for more details.
..
.. You should have received a copy of the GNU General Public License
.. along with this program. If not, see <http://www.gnu.org/licenses/>.

Developer Guide
===============

Setting Up the Development Environment
--------------------------------------

This section provides instructions for setting up your development environment.
If you follow the steps from top to bottom you should be ready to roll by
the end.

Get the Source
^^^^^^^^^^^^^^

The source code for the `hifis-surveyval` project lives at `Gitlab
<https://gitlab.hzdr.de/hifis/surveys/hifis-surveyval>`_.
You can use `git clone` to get it.
Chose one of the options.

.. code-block:: bash

   # via ssh (recommended)
   git clone git@gitlab.hzdr.de:hifis/surveys/hifis-surveyval.git

   # via https
   git clone https://gitlab.hzdr.de/hifis/surveys/hifis-surveyval.git

Create the Virtual Environment
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

The dependencies for this project are handles by `Poetry
<https://python-poetry.org/>`_.
You need to install poetry first.

.. code-block:: bash

    pip install poetry

Poetry also creates the virtual environment and installs the project's
dependencies.

.. code-block:: bash

    poetry install

Try It Out
^^^^^^^^^^

One way to test out the environment is to run the tests.  You can do this with the `make test`
target.

.. code-block:: bash

    make test

If the tests run and pass, you're ready to roll.

Make Changes to the Source Code
-------------------------------

We use the GitLab Development Cycle.
The short summary:

1. Create an issue
2. Create a merge request from the issue
3. Make your changes to the source code on the created branch
4. Run linter and test (see 'Using the `Makefile`')
5. Push your changes to GitLab

Run Changes
^^^^^^^^^^^

You can run the changed package in the local development environment without
prior building.

.. code-block:: bash

    poetry run hifis-surveyval <ARGS>

Using the `Makefile`
--------------------

This project includes a `Makefile <https://www.gnu.org/software/make/>`_
that you can use to perform common tasks such as running tests and building
documentation.

This section contains a brief description of the targets defined in the
``Makefile``.

``build``
^^^^^^^^^

Uses poetry to generate a Python package.

``clean``
^^^^^^^^^

Remove generated packages, documentation, temporary files, *etc*.

``coverage``
^^^^^^^^^^^^

Run the unit tests. It generates the coverage report to a HTML file to later
be included in the documentation.

``docs``
^^^^^^^^

Build the documentation for production.
After building the documentation, you can open it locally with ``$BROWSER
docs/build/html/index.html``.

.. note::

    You can also build the documents directly, bypassing validations like
    `linting` and `testing` using `Sphinx Makefile
    <https://github.com/mapnik/sphinx-docs/blob/master/Makefile>`_ directly.

    .. code-block:: bash

        cd docs
        make clean && make html
        make latexpdf

``lint``
^^^^^^^^

Run `FlakeHell <https://flakehell.readthedocs.io/>`_ against the project files.

FlakeHell is a wrapper for `Flake8 <https://gitlab.com/pycqa/flake8>`_ to
make it compatible to the ``pyproject.toml``, which we use.

``package``
^^^^^^^^^^^

Build the package for publishing. This includes the documentation.

``reformat``
^^^^^^^^^^^^

Runs `Sphinx Makefile
<https://github.com/mapnik/sphinx-docs/blob/master/Makefile>`_ an `Sphinx Makefile
<https://github.com/mapnik/sphinx-docs/blob/master/Makefile>`_ to make the
linter happy.

.. note::

    You might need to format the docstrings manually to satisfy the linter
    as well as sphinx.

``test``
^^^^^^^^

Run the unit tests. It generates the coverage report to the CLI.

Publishing
----------

The software is published on `PyPI
<https://pypi.org/project/hifis-surveyval/>`_.
This is done via GitLab CI on tags, but only via a manual trigger in the end.
There is no need to do it manually.

In case you need to do it manually anyway, please use poetry as shown below.

.. code-block:: bash

    make package
    poetry publish
