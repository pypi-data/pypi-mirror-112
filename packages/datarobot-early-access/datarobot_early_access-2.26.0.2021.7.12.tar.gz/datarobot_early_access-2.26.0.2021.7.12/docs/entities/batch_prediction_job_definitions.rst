.. _batch_prediction_job_definitions:

################################
Batch Prediction Job Definitions
################################

To submit a working Batch Prediction job, you must supply a variety of elements to the :func:`datarobot.models.BatchPredictionJob.score`
request payload depending on what type of prediction is required. Additionally, you must consider the type of intake
and output adapters used for a given job.

Every time a new Batch Prediction is created, the same amount of information must be stored somewhere outside of
DataRobot and re-submitted every time.

For example, a request could look like:

.. code-block:: python

    import datarobot as dr

    deployment_id = "5dc5b1015e6e762a6241f9aa"

    job = dr.BatchPredictionJob.score(
        deployment_id,
        intake_settings={
            "type": "s3",
            "url": "s3://bucket/container/file.csv",
            "credential_id": "5dc5b1015e6e762a6241f9bb"
        },
        output_settings={
            "type": "s3",
            "url": "s3://bucket/container/output.csv",
            "credential_id": "5dc5b1015e6e762a6241f9bb"
        },
    )

    job.wait_for_completion()

    with open("./predicted.csv", "wb") as f:
        job.download(f)

Job Definitions
***************

If your use case requires the same, or close to the same, type of prediction to be done multiple times, you can choose to
create a *Job Definition* of the Batch Prediction job and store this inside DataRobot for future use.

The method for creating job definitions is identical to the existing :func:`datarobot.models.BatchPredictionJob.score` method,
except for the addition of a ``enabled``, ``name`` and ``schedule`` parameter: :func:`datarobot.models.BatchPredictionJobDefinition.create`

.. code-block:: python

    >>> import datarobot as dr
    >>> job_spec = {
    ...    "num_concurrent": 4,
    ...    "deployment_id": "5dc5b1015e6e762a6241f9aa",
    ...    "intake_settings": {
    ...        "url": "s3://foobar/123",
    ...        "type": "s3",
    ...        "format": "csv",
    ...        "credential_id": "5dc5b1015e6e762a6241f9bb"
    ...    },
    ...    "output_settings": {
    ...        "url": "s3://foobar/123",
    ...        "type": "s3",
    ...        "format": "csv",
    ...        "credential_id": "5dc5b1015e6e762a6241f9bb"
    ...    },
    ...}
    >>> definition = BatchPredictionJobDefinition.create(
    ...    enabled=False,
    ...    batch_prediction_job=job_spec,
    ...    name="some_definition_name",
    ...    schedule=None
    ... )
    >>> definition
    BatchPredictionJobDefinition(foobar)

.. note:: The ``name`` parameter must be unique across your organization. If you attempt to create multiple definitions
    with the same name, the request will fail. If you wish to free up a name, you must first :func:`datarobot.models.BatchPredictionJobDefinition.delete`
    the existing definition before creating this one. Alternatively you can just :func:`datarobot.models.BatchPredictionJobDefinition.update`
    the existing definition with a new name.

Executing a job definition
**************************

Manual job execution
====================

If you wish to submit a stored job definition for scoring, you can either choose to do so on a scheduled basis, described
below, or by manually submitting the definition ID using :func:`datarobot.models.BatchPredictionJobDefinition.run_once`,
as such:

.. code-block:: python

    >>> import datarobot as dr
    >>> definition = dr.BatchPredictionJob.get("5dc5b1015e6e762a6241f9aa")
    >>> job = definition.run_once()
    >>> job.wait_for_completion()

Scheduled job execution
=======================

A Scheduled Batch Prediction job works just like a regular Batch Prediction job, except DataRobot handles the execution
of the job.

In order to schedule the execution of a Batch Prediction job, a definition must first be created, using
:func:`datarobot.models.BatchPredictionJobDefinition.create`, or updated, using
:func:`datarobot.models.BatchPredictionJobDefinition.update`, where ``enabled`` is set to ``True`` and a ``schedule``
payload is provided.

Alternatively, you can use a short-hand version with :func:`datarobot.models.BatchPredictionJobDefinition.run_on_schedule`
as such:

.. code-block:: python

    >>> import datarobot as dr
    >>> schedule = {
    ...    "day_of_week": [
    ...        1
    ...    ],
    ...    "month": [
    ...        "*"
    ...    ],
    ...    "hour": [
    ...        16
    ...    ],
    ...    "minute": [
    ...        0
    ...    ],
    ...    "day_of_month": [
    ...        1
    ...    ]
    ...}
    >>> definition = dr.BatchPredictionJob.get("5dc5b1015e6e762a6241f9aa")
    >>> job = definition.run_on_schedule(schedule)

If the created job was not enabled previously, this method will also enable it.

The ``Schedule`` payload
========================

The ``schedule`` payload defines at what intervals the job should run, which can be combined in various ways to construct
complex scheduling terms if needed. In all of the elements in the objects, you can supply either an asterisk ``["*"]``
denoting "every" time denomination or an array of integers (e.g. ``[1, 2, 3]``) to define a specific interval.

..  list-table:: The ``schedule`` payload elements
    :widths: 10, 10, 10, 5
    :header-rows: 1
    :class: tight-table

    * - Key
      - Possible values
      - Example
      - Description
    * - minute
      - ``["*"]`` or ``[0 ... 59]``
      - ``[15, 30, 45]``
      - The job will run at these minute values for every hour of the day.
    * - hour
      - ``["*"]`` or ``[0 ... 23]``
      - ``[12,23]``
      - The hour(s) of the day that the job will run.
    * - month
      - ``["*"]`` or ``[1 ... 12]``
      - ``["jan"]``
      - Strings, either 3-letter abbreviations or the full name of the month, can be used interchangeably (e.g., "jan" or "october").

        Months that are not compatible with ``day_of_month`` are ignored, for example ``{"day_of_month": [31], "month":["feb"]}``.
    * - day_of_week
      - ``["*"]`` or ``[0 ... 6]`` where (Sunday=0)
      - ``["sun"]``
      - The day(s) of the week that the job will run. Strings, either 3-letter abbreviations or the full name of the day, can be used interchangeably (e.g., "sunday", "Sunday", "sun", or "Sun", all map to ``[0]``).

        **NOTE:** This field is additive with ``day_of_month``, meaning the job will run both on the date specified by ``day_of_month`` and the day defined in this field.
    * - day_of_month
      - ``["*"]`` or ``[1 ... 31]``
      - ``[1, 25]``
      - The date(s) of the month that the job will run. Allowed values are either ``[1 ... 31]`` or ``["*"]`` for all days of the month.

        **NOTE:** This field is additive with ``day_of_week``, meaning the job will run both on the date(s) defined in this field and the day specified
        by ``day_of_week`` (for example, dates 1st, 2nd, 3rd, plus every Tuesday). If ``day_of_month`` is set to ``["*"]`` and ``day_of_week`` is defined,
        the scheduler will trigger on every day of  the month that matches ``day_of_week`` (for example, Tuesday the 2nd, 9th, 16th, 23rd, 30th).

        Invalid dates such as February 31st are ignored.

Disabling a scheduled job
*************************

Job definitions are only be executed by the scheduler if ``enabled`` is set to ``True``. If you have a job definition
that was previously running as a scheduled job, but should now be stopped, simply
:func:`datarobot.models.BatchPredictionJobDefinition.delete` to remove it completely, or :func:`datarobot.models.BatchPredictionJobDefinition.update`
it with ``enabled=False`` if you want to keep the definition, but stop the scheduled job from executing at intervals.
If a job is currently running, this will finish execution regardless.

.. code-block:: python

    >>> import datarobot as dr
    >>> definition = dr.BatchPredictionJobDefinition.get("5dc5b1015e6e762a6241f9aa")
    >>> definition.delete()
