import trafaret as t

from datarobot._compat import Int, String
from datarobot.enums import CUSTOM_MODEL_TARGET_TYPE, CUSTOM_TASK_TYPE
from datarobot.models.api_object import APIObject
from datarobot.models.custom_model_version import CustomModelVersion
from datarobot.utils import encode_utf8_if_py2
from datarobot.utils.pagination import unpaginate


class CustomTask(APIObject):
    """ A custom task.

    .. versionadded:: v2.25

    Attributes
    ----------
    id: str
        id of the custom task
    name: str
        name of the custom task
    language: str
        programming language of the custom task.
        Can be "python", "r", "java" or "other"
    description: str
        description of the custom task
    task_type: datarobot.CUSTOM_TASK_TYPE
        whether the task is a custom estimator or a custom transform.
        Values: [`datarobot.CUSTOM_TASK_TYPE.ESTIMATOR`, `datarobot.CUSTOM_TASK_TYPE.TRANSFORM`]
    target_type: datarobot.TARGET_TYPE or None
        target type if task is an estimator.
        Values: [`datarobot.TARGET_TYPE.BINARY`, `datarobot.TARGET_TYPE.REGRESSION`,
        `datarobot.TARGET_TYPE.MULTICLASS`, `datarobot.TARGET_TYPE.ANOMALY`]
    calibrate_predictions: bool
        whether anomaly predictions should be calibrated to be between 0 and 1 by DR.
        only applies to custom estimators with target type  `datarobot.TARGET_TYPE.ANOMALY`.
    latest_version: datarobot.CustomModelVersion or None
        latest version of the custom task if one exists
    deployments_count: int
        number of a deployments of the custom task
    created_by: str
        username of a user who user who created the custom task
    updated_at: str
        ISO-8601 formatted timestamp of when the custom task was updated
    created_at: str
        ISO-8601 formatted timestamp of when the custom task was created
    """

    _path = "customTasks/"

    _converter = t.Dict(
        {
            t.Key("id"): String(),
            t.Key("task_type", optional=False, default=CUSTOM_TASK_TYPE.ESTIMATOR): String(),
            t.Key("target_type", optional=True, default=None): String(),
            t.Key("latest_version", optional=True, default=None): t.Or(
                CustomModelVersion.schema, t.Null()
            ),
            t.Key("created") >> "created_at": String(),
            t.Key("updated") >> "updated_at": String(),
            t.Key("name"): String(),
            t.Key("description"): String(allow_blank=True),
            t.Key("language", optional=True, default=None): String(),
            t.Key("created_by"): String(),
            t.Key("deployments_count"): Int(),
            t.Key("calibrate_predictions", optional=True, default=True): t.Bool(),
        }
    ).allow_extra("*")

    def __init__(self, **kwargs):
        self._set_values(**kwargs)

    def __repr__(self):
        return encode_utf8_if_py2(u"{}({!r})".format(self.__class__.__name__, self.name or self.id))

    def _set_values(
        self,
        id,
        name,
        description,
        latest_version,
        deployments_count,
        created_by,
        updated_at,
        created_at,
        target_type,
        task_type,
        language,
        calibrate_predictions,
    ):
        self.id = id
        self.name = name
        self.description = description
        self.task_type = task_type
        self.target_type = target_type
        self.language = language
        self.calibrate_predictions = calibrate_predictions

        if self.task_type == CUSTOM_TASK_TYPE.ESTIMATOR:
            if not self.target_type:
                raise ValueError(
                    "Custom {} must have a target type".format(CUSTOM_TASK_TYPE.ESTIMATOR)
                )
        elif self.task_type == CUSTOM_TASK_TYPE.TRANSFORM:
            if self.target_type is not None:
                raise ValueError(
                    "Custom {} cannot have a target type".format(CUSTOM_TASK_TYPE.TRANSFORM)
                )
            else:
                self.target_type = self.task_type
        else:
            raise ValueError(
                "{} is not allowed task_type. Please select {} or {}".format(
                    self.task_type, CUSTOM_TASK_TYPE.TRANSFORM, CUSTOM_TASK_TYPE.ESTIMATOR
                )
            )

        self.latest_version = CustomModelVersion(**latest_version) if latest_version else None
        self.deployments_count = deployments_count
        self.created_by = created_by
        self.updated_at = updated_at
        self.created_at = created_at

    @classmethod
    def list(cls, is_deployed=None, order_by=None, search_for=None):
        """List custom tasks available to the user.

        .. versionadded:: v2.25

        Parameters
        ----------
        search_for: str, optional
            string for filtering custom tasks - only tasks that contain the
            string in name or description will be returned.
            If not specified, all custom task will be returned
        order_by: str, optional
            property to sort custom tasks by.
            Supported properties are "created" and "updated".
            Prefix the attribute name with a dash to sort in descending order,
            e.g. order_by='-created'.
            By default, the order_by parameter is None which will result in
            custom tasks being returned in order of creation time descending

        Returns
        -------
        List[CustomTask]
            a list of custom tasks.

        Raises
        ------
        datarobot.errors.ClientError
            if the server responded with 4xx status
        datarobot.errors.ServerError
            if the server responded with 5xx status
        """
        payload = {
            "order_by": order_by,
            "search_for": search_for,
        }
        data = unpaginate(cls._path, payload, cls._client)
        return [cls.from_server_data(item) for item in data]

    @classmethod
    def get(cls, custom_task_id):
        """Get custom task by id.

        .. versionadded:: v2.25

        Parameters
        ----------
        custom_task_id: str
            id of the custom task

        Returns
        -------
        CustomTask
            retrieved custom task

        Raises
        ------
        datarobot.errors.ClientError
            if the server responded with 4xx status.
        datarobot.errors.ServerError
            if the server responded with 5xx status.
        """
        path = "{}{}/".format(cls._path, custom_task_id)
        data = cls._client.get(path).json()
        return cls.from_server_data(data)

    def download_latest_version(self, file_path):
        """Download the latest custom task version.

        .. versionadded:: v2.25

        Parameters
        ----------
        file_path: str
            path to create a file with custom task version content

        Raises
        ------
        datarobot.errors.ClientError
            if the server responded with 4xx status.
        datarobot.errors.ServerError
            if the server responded with 5xx status.
        """
        path = "{}{}/download/".format(self._path, self.id)
        response = self._client.get(path)
        with open(file_path, "wb") as f:
            f.write(response.content)

    @classmethod
    def create(
        cls, name, task_type, target_type=None, description=None, calibrate_predictions=True,
    ):
        """Create a custom task.

        .. versionadded:: v2.25

        Parameters
        ----------
        name: str
            name of the custom task
        language: str
            programming language of the custom task.
            Can be "python", "r", "java" or "other"
        description: str, optional
            description of the custom task
        task_type: datarobot.CUSTOM_TASK_TYPE
            whether the task is a custom estimator or a custom transform.
            Values: [`datarobot.CUSTOM_TASK_TYPE.ESTIMATOR`, `datarobot.CUSTOM_TASK_TYPE.TRANSFORM`]
        target_type: datarobot.TARGET_TYPE or None
            target type if task is an estimator.
            should be None if task is a transform.
            Values: [`datarobot.TARGET_TYPE.BINARY`, `datarobot.TARGET_TYPE.REGRESSION`,
            `datarobot.TARGET_TYPE.MULTICLASS`, `datarobot.TARGET_TYPE.ANOMALY`]
        calibrate_predictions: bool, optional
            whether anomaly predictions should be calibrated to be between 0 and 1 by DR.
            defaults to True.
            only applies to custom estimators with target type  `datarobot.TARGET_TYPE.ANOMALY`.

        Returns
        -------
        CustomTask
            created a custom task

        Raises
        ------
        datarobot.errors.ClientError
            if the server responded with 4xx status
        datarobot.errors.ServerError
            if the server responded with 5xx status
        """
        payload = dict(
            name=name, description=description, calibrate_predictions=calibrate_predictions,
        )
        if task_type == CUSTOM_TASK_TYPE.TRANSFORM:
            if target_type is not None:
                raise ValueError(
                    "Custom {} cannot have a target type".format(CUSTOM_TASK_TYPE.TRANSFORM)
                )
            else:
                payload["target_type"] = CUSTOM_TASK_TYPE.TRANSFORM
        elif task_type == CUSTOM_TASK_TYPE.ESTIMATOR:
            if target_type in CUSTOM_MODEL_TARGET_TYPE.TASK_TARGET_TYPES:
                payload["target_type"] = target_type
            elif target_type is None:
                raise ValueError(
                    "Custom {} must have a target type".format(CUSTOM_TASK_TYPE.ESTIMATOR)
                )
            else:
                raise ValueError("{} is not an allowed target type".format(target_type))
        else:
            raise ValueError(
                "{} is not allowed task_type. Please select {} or {}".format(
                    task_type, CUSTOM_TASK_TYPE.TRANSFORM, CUSTOM_TASK_TYPE.ESTIMATOR
                )
            )

        response = cls._client.post(cls._path, data=payload)
        return cls.from_server_data(response.json())

    @classmethod
    def copy_custom_task(
        cls, custom_task_id,
    ):
        """Create a custom task by copying existing one.

        .. versionadded:: v2.25

        Parameters
        ----------
        custom_task_id: str
            id of the custom task to copy

        Returns
        -------
        CustomTask
            created a custom task

        Raises
        ------
        datarobot.errors.ClientError
            if the server responded with 4xx status
        datarobot.errors.ServerError
            if the server responded with 5xx status
        """
        path = "{}fromCustomTask/".format(cls._path)
        response = cls._client.post(path, data={"custom_task_id": custom_task_id})
        return cls.from_server_data(response.json())

    def update(self, name=None, description=None, **kwargs):
        """Update custom task properties.

        .. versionadded:: v2.25

        Parameters
        ----------
        name: str, optional
            new custom task name
        language: str, optional
            new custom task programming language
        description: str, optional
            new custom task description

        Raises
        ------
        datarobot.errors.ClientError
            if the server responded with 4xx status.
        datarobot.errors.ServerError
            if the server responded with 5xx status.
        """
        payload = dict(name=name, description=description, **kwargs)
        url = "{}{}/".format(self._path, self.id)
        response = self._client.patch(url, data=payload)

        data = response.json()
        self._set_values(**self._safe_data(data, do_recursive=True))

    def refresh(self):
        """Update custom task with the latest data from server.

        .. versionadded:: v2.25

        Raises
        ------
        datarobot.errors.ClientError
            if the server responded with 4xx status
        datarobot.errors.ServerError
            if the server responded with 5xx status
        """
        url = self._path.format(self.id)
        path = "{}{}/".format(url, self.id)

        response = self._client.get(path)

        data = response.json()
        self._set_values(**self._safe_data(data, do_recursive=True))

    def delete(self):
        """Delete custom task.

        .. versionadded:: v2.25

        Raises
        ------
        datarobot.errors.ClientError
            if the server responded with 4xx status
        datarobot.errors.ServerError
            if the server responded with 5xx status
        """
        url = "{}{}/".format(self._path, self.id)
        self._client.delete(url)
