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

Getting Started
===============

Requirements
------------

To develop and / or run an analysis you need some things:

1. Data in form of a `.csv` file
2. Meta data in form of a `.yml` file
3. A directory to store your scripts (can be generated)
4. A directory to store the outputs of the scripts (will be generated, if it
   does not exists)

Setting up the Environment
--------------------------

Because the scripts use `hifis-surveyval` as dependency, it is wise to set
up a dedicated environment for your analysis. We show an example workflow
using `Poetry <https://python-poetry.org/>`_ to achieve that, but other
solutions like `Pipenv <https://pipenv.pypa.io/en/latest/>`_ also work.

First, we need to install poetry on our system.

.. code-block:: bash

    pip install poetry

Afterwards, we need to create a project folder or clone a git repository,
where everything is stored. In the terminal, go to this directory.

Create a Project for the Analysis
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

If in an existing git repository already a ``pyproject.toml`` exists, you
can skip this step.

Follow the instructions of poetry and skip choosing the dependencies.

.. code-block:: bash

    poetry init

Install Dependencies
^^^^^^^^^^^^^^^^^^^^

The most important dependency is obviously ``hifis-surveyval``.

.. code-block:: bash

    poetry add hifis-surveyval

You can later add other dependencies of the analysis scripts with the same
command.

Initializing hifis-surveyval
----------------------------

If in an existing git repository already a ``hifis-surveyval.yml`` and a
directory for your scripts exist, you can skip this step.

We can create a config and an example script with the following command.

.. code-block:: bash

    poetry run hifis-surveyval init

If you only need the config or only an example script, see:

.. code-block:: bash

    poetry run hifis-surveyval init --help

Adding or Changing Analysis Scripts
-----------------------------------

Now you can freely add or edit ``.py`` files in the scripts folder
determined in the config file. Please do not use subpackages there.

You get access to the data and the tools via the arguments in the `run`
function of the script. An example script is shown below.

.. code-block:: python

    from hifis_surveyval.data_container import DataContainer
    from hifis_surveyval.hifis_surveyval import HIFISSurveyval

    def run(hifis_surveyval: HIFISSurveyval, data: DataContainer):
        """Execute example script."""
        for question in data.question_collection_ids:
            print(question)
