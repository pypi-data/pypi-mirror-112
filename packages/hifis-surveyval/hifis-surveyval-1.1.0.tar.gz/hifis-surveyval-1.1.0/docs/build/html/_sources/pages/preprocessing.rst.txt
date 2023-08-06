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

Preprocessing
=============

HIFIS-Surveyval comes with the possibility to run a preprocessing script
before all analysis scripts. Where it is located and how it is named is set
in the settings.

Preprocessing is skipped in case no preprocessing script exists.

You can create an empty preprocessing script with the following command:

.. code-block:: bash

    hifis-surveyval init -p

Within the preprocessing script, you need to have a function called
``preprocessing(…)``, which receives a ``DataContainer`` Object as argument
and is expected to return a ``DataContainer``-instance.

The data you receive is the parsed raw data from your survey's CSV, enriched with the metadata you provided.
You can do whatever you like within the script and modify the data as you wish.
Common use-cases would be to filter the data, like dropping incomplete questionnaires.
If you are concerned about reproducibility it is highly recommended to also publish the preprocessing script along with you raw data and metadata.

All analysis scripts run afterwards will receive a copy of the
`DataContainer` returned by the preprocessing script.

Cleaning Invalid Data
---------------------

A usual task in preprocessing is to remove data that is invalid for any reason.
The ``DataContainer`` keeps track of participant IDs for those participants
that submitted incomplete answer sets.
An answer set is considered incomplete if not all questions that are marked
as `mandatory` have been answered.
You can manually mark the answer sets of participants as invalid by using
the ``mark_as_invalid(…)``-method of the ``DataContainer``-instance.
This can be used to also exclude data that you found to be unfitting after
manual inspection.

Contrary, there is also a ``mark_as_valid(…)``-method to manually override
decisions made by the framework.

After you have marked the answer sets accordingly, you can call the
``remove_invalid_answers()``-method to clean up all marked answer sets
across all questions and collections.
Please note that this will change your data container irrevocably.

For fine tuning, the ``QuestionCollection``- and ``Question``-classes also
offer methods to remove answers of selected participants directly.

See also the provided example script for implementation details.
