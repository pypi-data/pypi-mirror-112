.. _feature_discovery:

#################
Feature Discovery
#################
The Feature Discovery Project allows the user to generate features automatically
from the secondary datasets which is connect to the Primary dataset(Training dataset).
User can create such connection using Relationships Configuration.

Register Primary Dataset to start Project
*****************************************
To start the Feature Discovery Project you need to upload the primary (training) dataset
:ref:`projects`

.. code-block:: python

    import datarobot as dr
    primary_dataset = dr.Dataset.create_from_file(file_path='your-training_file.csv')
    project = dr.Project.create_from_dataset(primary_dataset.id, project_name='Lending Club')

Now, register all the secondary datasets which you want to connect with primary (training) dataset
and among themselves.

Register Secondary Dataset(s) in AI Catalog
*******************************************
You can register the dataset using
:meth:`Dataset.create_from_file<datarobot.Dataset.create_from_file>` which can take either a path to a
local file or any stream-able file object.

.. code-block:: python

    profile_dataset = dr.Dataset.create_from_file(file_path='your_profile_file.csv')
    transaction_dataset = dr.Dataset.create_from_file(file_path='your_transaction_file.csv')

Create Dataset Definitions and Relationships using helper functions
*******************************************************************

Create the :ref:`DatasetDefinition <dataset_definition>` and :ref:`Relationship <relationship>` for the profile and transaction dataset created above using helper functions.

.. code-block:: python

    profile_catalog_id = profile_dataset.id
    profile_catalog_version_id = profile_dataset.version_id

    transac_catalog_id = transaction_dataset.id
    transac_catalog_version_id = transaction_dataset.version_id

    profile_dataset_definition = dr.DatasetDefinition(
        identifier='profile',
        catalog_id=profile_catalog_id,
        catalog_version_id=profile_catalog_version_id
    )

    transaction_dataset_definition = dr.DatasetDefinition(
        identifier='transaction',
        catalog_id=transac_catalog_id,
        catalog_version_id=transac_catalog_version_id,
        primary_temporal_key='Date'
    )

    profile_transaction_relationship = dr.Relationship(
        dataset1_identifier='profile',
        dataset2_identifier='transaction',
        dataset1_keys=['CustomerID'],
        dataset2_keys=['CustomerID']
    )

    primary_profile_relationship = dr.Relationship(
        dataset2_identifier='profile',
        dataset1_keys=['CustomerID'],
        dataset2_keys=['CustomerID'],
        feature_derivation_window_start=-14,
        feature_derivation_window_end=-1,
        feature_derivation_window_time_unit='DAY',
        prediction_point_rounding=1,
        prediction_point_rounding_time_unit='DAY'
    )

    dataset_definitions = [profile_dataset_definition, transaction_dataset_definition]
    relationships = [primary_profile_relationship, profile_transaction_relationship]

Create Relationships Configuration
**********************************

Create the Relationship Configuration using dataset definitions and relationships created above


.. code-block:: python

    # Create the relationships configuration to define connection between the datasets
    relationship_config = dr.RelationshipsConfiguration.create(dataset_definitions=dataset_definitions, relationships=relationships)

* For more details refer -- :doc:`Relationships Configuration </entities/relationships_configuration>`

Create Feature Discovery Project
********************************

Once done with relationships configuration you can start the Feature Discovery project

.. code-block:: python

    # Set the date-time partition column which is date here
    partitioning_spec = dr.DatetimePartitioningSpecification('date')

    # Set the target for the project and start Feature discovery
    project.set_target(target='BadLoan', relationships_configuration_id=relationship_config.id, mode='manual', partitioning_method=partitioning_spec)
    Project(train.csv)


Start Training a Model
**********************

To start training a model, refer to :doc:`Model </entities/model>`

Create Secondary Datasets Configuration for prediction
******************************************************

Create the Secondary dataset configuration using :ref:`Secondary Dataset <secondary_dataset>`


.. code-block:: python

    new_secondary_dataset_config = dr.SecondaryDatasetConfigurations.create(
        project_id=project.id,
        name='My config',
        secondary_datasets=secondary_datasets
    )

* For more details, refer to :doc:`Secondary Dataset Config </entities/secondary_dataset_config>`

Perform Prediction over trained model
*************************************
To start prediction over a trained model, refer to :doc:`Predictions </entities/predict_job>`

.. code-block:: python

    dataset_from_path = project.upload_dataset(
        './data_to_predict.csv',
        secondary_datasets_config_id=new_secondary_dataset_config.id
    )

    predict_job_1 = model.request_predictions(dataset_from_path.id)

Common Errors
-------------
Dataset registration Failed
^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. code-block:: python

    datasetdr.Dataset.create_from_file(file_path='file.csv')
    datarobot.errors.AsyncProcessUnsuccessfulError: The job did not complete successfully.

Solution

* Check the internet connectivity sometimes network flakiness cause upload error
* Is the dataset file too big then you might want to upload using URL rather than file


Creating relationships configuration throws some error
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. code-block:: python

    datarobot.errors.ClientError: 422 client error: {u'message': u'Invalid field data',
    u'errors': {u'datasetDefinitions': {u'1': {u'identifier': u'value cannot contain characters: $ - " . { } / \\'},
    u'0': {u'identifier': u'value cannot contain characters: $ - " . { } / \\'}}}}

Solution:

* Check the identifier name passed in datasets_definitions and relationships
* ``Pro tip: Dont use name of the dataset if you didnt specified the name of the dataset explicitly while registration``

.. code-block:: python

    datarobot.errors.ClientError: 422 client error: {u'message': u'Invalid field data',
    u'errors': {u'datasetDefinitions': {u'1': {u'primaryTemporalKey': u'date column doesnt exist'},
    }}}

Solution:

* Check if the name of the column passed as primaryTemporalKey is correct, its case-senstive