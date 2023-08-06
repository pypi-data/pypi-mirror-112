.. _custom_tasks:

#############
Custom Tasks
#############

Custom tasks provide users the ability to train models with arbitrary code in an environment defined by the user.

for details on using environments, see: :ref:`custom-models-execution-environments`.


Manage Custom Tasks
*******************

Coming Soon!


.. _custom_task_versions:

Manage Custom Task Versions
******************************

Code for Custom Tasks can be uploaded by creating a Custom Task Version.
When creating a Custom Task Version, the version must be associated with a base execution
environment.  If the base environment supports additional task dependencies
(R or Python environments) and the Custom Task Version
contains a valid requirements.txt file, the task version will run in an environment based on
the base environment with the additional dependencies installed.

Create Custom Task Version
===========================

Upload actual custom task content by creating a clean Custom Task Version:

.. code-block:: python

    import os
    import datarobot as dr

    custom_task_id = '5b6b2315ca36c0108fc5d41b'
    custom_task_folder = "datarobot-user-tasks/task_templates/python3_pytorch"

    # add files from the folder to the custom task
    task_version = dr.CustomTaskVersion.create_clean(
        custom_task_id=custom_task_id,
        base_environment_id=execution_environment.id,
        folder_path=custom_task_folder,
    )


To create a new Custom Task Version from a previous one, with just some files added or removed, do the following:

.. code-block:: python

    import os
    import datarobot as dr

    new_files_folder = "datarobot-user-tasks/task_templates/my_files_to_add_to_pytorch_task"

    file_to_delete = task_version.items[0].id

    task_version_2 = dr.CustomTaskVersion.create_from_previous(
        custom_task_id=custom_task_id,
        base_environment_id=execution_environment.id,
        folder_path=new_files_folder,
    )

Please refer to :class:`~datarobot.models.custom_task_version.CustomTaskFileItem` for description of custom task file properties.


List Custom Task Versions
==========================

Use the following command to list Custom Task Versions available to the user:

.. code-block:: python

    import datarobot as dr

    dr.CustomTaskVersion.list(custom_task_id)

    >>> [CustomTaskVersion('v2.0'), CustomTaskVersion('v1.0')]

Retrieve Custom Task Version
=============================

To retrieve a specific Custom Task Version, run:

.. code-block:: python

    import datarobot as dr

    dr.CustomTaskVersion.get(custom_task_id, custom_task_version_id='5ebe96b84024035cc6a6560b')

    >>> CustomTaskVersion('v2.0')

Update Custom Task Version
===========================

To update Custom Task Version description execute the following:

.. code-block:: python

    import datarobot as dr

    custom_task_version = dr.CustomTaskVersion.get(
        custom_task_id,
        custom_task_version_id='5ebe96b84024035cc6a6560b',
    )

    custom_task_version.update(description='new description')

    custom_task_version.description
    >>> 'new description'

Download Custom Task Version
=============================

Download content of the Custom Task Version as a ZIP archive:

.. code-block:: python

    import datarobot as dr

    path_to_download = '/home/user/Documents/myTask.zip'

    custom_task_version = dr.CustomTaskVersion.get(
        custom_task_id,
        custom_task_version_id='5ebe96b84024035cc6a6560b',
    )

    custom_task_version.download(path_to_download)


Preparing a Custom Task Version for Use
****************************************

If your custom task version has dependencies, a dependency build must be completed before the task
can be used.  The dependency build installs your task's dependencies into the base environment
associated with the task version.

see: :ref:`custom-models-dependencies`
