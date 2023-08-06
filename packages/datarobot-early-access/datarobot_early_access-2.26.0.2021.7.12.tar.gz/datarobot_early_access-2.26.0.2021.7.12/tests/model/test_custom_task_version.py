from collections import defaultdict
from copy import deepcopy
import json
import os
from shutil import rmtree

import pytest
from requests_toolbelt import MultipartEncoder
import responses
from trafaret import DataError

from datarobot.models.custom_task_version import CustomTaskFileItem, CustomTaskVersion
from datarobot.utils import camelize, underscorize
from tests.model.utils import assert_custom_task_version, assert_items


@pytest.fixture
def task_id():
    return "60dcbf0e8cd36258f9f5fff7"


@pytest.fixture
def version_id():
    return "60dcbf2b8cd36258f9f5fff8"


@pytest.fixture
def version_url(unittest_endpoint, task_id, version_id):
    return "{}/customTasks/{}/versions/{}/".format(unittest_endpoint, task_id, version_id)


@pytest.fixture
def versions_base_url(unittest_endpoint, task_id):
    return "{}/customTasks/{}/versions/".format(unittest_endpoint, task_id)


@pytest.fixture
def custom_task_version(version_id, task_id):
    return {
        "id": version_id,
        "customTaskId": task_id,
        "created": "abc",
        "description": "this task is the coolest",
        "items": [],
        "isFrozen": True,
        "versionMajor": 1,
        "versionMinor": 2,
        "label": "1.2",
        "trainingHistory": [],
    }


@pytest.fixture
def items():
    return [
        {
            "fileSource": "local",
            "workspaceId": "60abd24fc3d97e6f5f732575",
            "filePath": "custom.py",
            "storagePath": "workspace/60abd24fc3/custom.py",
            "repositoryLocation": None,
            "repositoryName": None,
            "repositoryFilePath": None,
            "ref": None,
            "commitSha": None,
            "id": "60abd2abb66ce93dc37324d2",
            "created": "2021-05-24T16:22:03.423629Z",
            "fileName": "custom.py",
        },
        {
            "fileSource": "local",
            "workspaceId": "60abd24fc3d97e6f5f732575",
            "filePath": "createPipeline.py",
            "storagePath": "workspace/60abd24fc3/createPipeline.py",
            "repositoryLocation": "some location",
            "repositoryName": "erics-awesome-repo",
            "repositoryFilePath": "x/y.py",
            "ref": "no idea",
            "commitSha": "123abc",
            "id": "60abd2abb66ce93dc37324d3",
            "created": "2021-05-24T16:22:03.423995Z",
            "fileName": "createPipeline.py",
        },
    ]


@pytest.fixture
def training_history():
    return [
        {"projectId": "def", "modelId": "abc"},
        {"projectId": "ghi", "modelId": "jkl"},
    ]


@pytest.fixture
def custom_task_version_with_optional_values(custom_task_version, items, training_history):
    new_task_version = deepcopy(custom_task_version)
    new_task_version.update(
        {
            "requiredMetadata": {"REQUIRED_FIELD": "super important value"},
            "baseEnvironmentVersionId": "mno",
            "baseEnvironmentId": "pqr",
            "dependencies": [
                {
                    "packageName": "pandas",
                    "constraints": [{"constraintType": ">=", "version": "1.0"}],
                    "line": "pandas >= 1.0",
                    "lineNumber": 1,
                }
            ],
            "items": items,
            "trainingHistory": training_history,
        }
    )
    return new_task_version


@pytest.fixture
def custom_task_version_response_json(custom_task_version_with_optional_values):
    return deepcopy(custom_task_version_with_optional_values)


@pytest.fixture
def nullable_keys():
    return {
        "description",
        "baseEnvironmentId",
        "baseEnvironmentVersionId",
    }


@pytest.fixture
def list_response(custom_task_version_response_json):
    second_version = {k: _update_value(v) for k, v in custom_task_version_response_json.items()}

    return {
        "count": 2,
        "totalCount": 2,
        "next": None,
        "data": [custom_task_version_response_json, second_version],
    }


def add_mock_get_response(url, json_dict):
    add_mock_response(responses.GET, url, json.dumps(json_dict))


def add_mock_response(method, url, body):
    responses.add(method, url, status=200, content_type="application/json", body=body)


@pytest.fixture()
def version_get_response(version_url, custom_task_version_response_json):
    add_mock_get_response(version_url, custom_task_version_response_json)


FILE_ITEM_RESPONSE_KEYS = [camelize(el.name) for el in CustomTaskFileItem.schema.keys]


class TestCustomTaskFileItem:
    def test_from_server_data_custom_model_file_item(self, items):
        assert_items([CustomTaskFileItem.from_server_data(el) for el in items], items)

    @pytest.mark.parametrize("key", FILE_ITEM_RESPONSE_KEYS)
    def test_from_server_data_no_optional_values(self, items, key):
        """Necessary because the class it inherits from allows created to be nullable."""
        item = items[0]
        item[key] = None
        with pytest.raises(DataError) as exec_info:
            CustomTaskFileItem.from_server_data(item)
        error = exec_info.value
        assert len(error.error) == 1
        assert error.error[underscorize(key)].error == "is required"


class TestCustomTaskVersionGetActionsAndUpdate:
    def test_from_server_data_minimal_response(self, custom_task_version):
        version = CustomTaskVersion.from_server_data(custom_task_version)
        assert_custom_task_version(version, custom_task_version)

    def test_from_server_data_full_response(self, custom_task_version_with_optional_values):
        version = CustomTaskVersion.from_server_data(custom_task_version_with_optional_values)
        assert_custom_task_version(version, custom_task_version_with_optional_values)

    def test_from_server_data_nullable_values(
        self, custom_task_version_response_json, nullable_keys
    ):
        for key in nullable_keys:
            custom_task_version_response_json[key] = None
        version = CustomTaskVersion.from_server_data(custom_task_version_response_json)
        assert_custom_task_version(version, custom_task_version_response_json)

    @responses.activate
    @pytest.mark.usefixtures("version_get_response")
    def test_get_custom_task_version(self, custom_task_version_response_json):
        task_id = custom_task_version_response_json["customTaskId"]
        version_id = custom_task_version_response_json["id"]
        version = CustomTaskVersion.get(task_id, version_id)
        assert_custom_task_version(version, custom_task_version_response_json)

        assert_single_api_call(
            responses.calls,
            responses.GET,
            "/customTasks/{}/versions/{}/".format(task_id, version_id),
        )

    @responses.activate
    def test_refresh_custom_task(self, custom_task_version_response_json, version_url):
        task_id = custom_task_version_response_json["customTaskId"]
        version_id = custom_task_version_response_json["id"]

        updated_response = {
            key: _update_value(value) for key, value in custom_task_version_response_json.items()
        }

        add_mock_get_response(version_url, custom_task_version_response_json)
        add_mock_get_response(version_url, updated_response)

        version = CustomTaskVersion.get(task_id, version_id)

        assert len(responses.calls) == 1
        assert_custom_task_version(version, custom_task_version_response_json)

        version.refresh()

        assert len(responses.calls) == 2
        assert_custom_task_version(version, updated_response)

    @responses.activate
    def test_list_response_single_list(self, list_response, task_id, versions_base_url):
        add_mock_get_response(versions_base_url, list_response)
        result = CustomTaskVersion.list(task_id)
        assert len(result) == len(list_response["data"])
        for actual, expected in zip(result, list_response["data"]):
            assert_custom_task_version(actual, expected)

        assert_single_api_call(
            responses.calls, responses.GET, "/customTasks/{}/versions/".format(task_id)
        )

    @responses.activate
    def test_list_response_multi_list(self, list_response, task_id, versions_base_url):
        next_page = deepcopy(list_response)
        next_data = next_page["data"]
        for el in next_data:
            for key in el:
                el[key] = _update_value(el[key])

        next_url = "https://www.coolguy.com/coolness/"
        list_response["next"] = next_url
        add_mock_get_response(versions_base_url, list_response)
        add_mock_get_response(next_url, next_page)
        result = CustomTaskVersion.list(task_id)
        assert len(result) == len(list_response["data"]) * 2
        for actual, expected in zip(result, list_response["data"] + next_data):
            assert_custom_task_version(actual, expected)

    @responses.activate
    @pytest.mark.usefixtures("version_get_response")
    def test_download(self, temporary_file, version_url, task_id, version_id):
        target_url = version_url + "download/"
        content = b"some stuff"
        add_mock_response(responses.GET, target_url, content)
        version = CustomTaskVersion.get(task_id, version_id)
        version.download(temporary_file)
        with open(temporary_file, "rb") as f:
            assert f.read() == content

        calls_after_get = responses.calls[1:]
        expected_url = "customTasks/{}/versions/{}/download/".format(task_id, version_id)
        assert_single_api_call(calls_after_get, responses.GET, expected_url)

    @responses.activate
    @pytest.mark.usefixtures("version_get_response")
    def test_update(self, version_url, task_id, version_id, custom_task_version_response_json):
        updated_json = deepcopy(custom_task_version_response_json)
        updated_json["requiredMetadata"] = {"TEST_UPDATE": "new_value", "otherThing": "OthErValue"}
        updated_json["description"] = "test_update description which is so awesome"

        add_mock_response(responses.PATCH, version_url, body=json.dumps(updated_json))

        version = CustomTaskVersion.get(task_id, version_id)
        version.update("dummy_value", {"DUMMY_VALUE": "value"})

        calls_after_get = responses.calls[1:]
        expected_url_ending = "customTasks/{}/versions/{}/".format(
            version.custom_task_id, version.id
        )
        assert_single_api_call(calls_after_get, responses.PATCH, expected_url_ending)

        call = calls_after_get[0]
        assert json.loads(call.request.body) == {
            "description": "dummy_value",
            "requiredMetadata": {"DUMMY_VALUE": "value"},
        }
        assert_custom_task_version(version, updated_json)

    @responses.activate
    @pytest.mark.usefixtures("version_get_response")
    def test_update_only_description(
        self, version_url, task_id, version_id, custom_task_version_response_json
    ):
        add_mock_response(
            responses.PATCH, version_url, body=json.dumps(custom_task_version_response_json)
        )

        version = CustomTaskVersion.get(task_id, version_id)
        version.update(description="only description")

        call = responses.calls[1]
        assert json.loads(call.request.body) == {"description": "only description"}

    @responses.activate
    @pytest.mark.usefixtures("version_get_response")
    def test_update_only_metadata(
        self, version_url, task_id, version_id, custom_task_version_response_json
    ):
        add_mock_response(
            responses.PATCH, version_url, body=json.dumps(custom_task_version_response_json)
        )

        version = CustomTaskVersion.get(task_id, version_id)
        version.update(required_metadata={"hello": "world"})

        call = responses.calls[1]
        assert json.loads(call.request.body) == {"requiredMetadata": {"hello": "world"}}


class TestCreateMethods:
    @staticmethod
    def _get_http_method(create_method):
        if create_method == CustomTaskVersion.create_clean:
            http_method = responses.POST
        else:
            http_method = responses.PATCH
        return http_method

    @responses.activate
    @pytest.mark.parametrize(
        "create_method",
        [CustomTaskVersion.create_clean, CustomTaskVersion.create_from_previous],
        ids=["create_clean", "create_from_previous"],
    )
    def test_minimal_request(
        self, versions_base_url, task_id, custom_task_version_response_json, create_method
    ):

        http_method = self._get_http_method(create_method)

        add_mock_response(
            http_method, versions_base_url, json.dumps(custom_task_version_response_json)
        )

        base_env_id = "abc123"
        response = create_method(task_id, base_env_id)

        assert_single_api_call(
            responses.calls, http_method, "customTasks/{}/versions/".format(task_id)
        )
        assert_custom_task_version(response, custom_task_version_response_json)

        request_body = responses.calls[0].request.body
        assert isinstance(request_body, MultipartEncoder)
        assert _fields_to_dict(request_body) == {
            "baseEnvironmentId": [base_env_id],
            "isMajorUpdate": ["True"],
        }

    @responses.activate
    @pytest.mark.parametrize(
        "create_method",
        [CustomTaskVersion.create_clean, CustomTaskVersion.create_from_previous],
        ids=["create_clean", "create_from_previous"],
    )
    @pytest.mark.parametrize("is_major_update", [True, False])
    def test_optional_values(
        self,
        versions_base_url,
        task_id,
        custom_task_version_response_json,
        create_method,
        is_major_update,
    ):

        http_method = self._get_http_method(create_method)

        add_mock_response(
            http_method, versions_base_url, json.dumps(custom_task_version_response_json)
        )

        base_env_id = "abc123"
        required_metadata = {"HI_THERE": "stuff"}
        create_method(
            task_id,
            base_env_id,
            is_major_update=is_major_update,
            required_metadata=required_metadata,
        )

        request_body = responses.calls[0].request.body
        assert _fields_to_dict(request_body) == {
            "baseEnvironmentId": [base_env_id],
            "isMajorUpdate": [str(is_major_update)],
            "requiredMetadata": [json.dumps(required_metadata)],
        }
        assert (
            responses.calls[0]
            .request.headers["Content-Type"]
            .startswith("multipart/form-data; boundary=")
        )

    @responses.activate
    @pytest.mark.parametrize(
        "create_method",
        [CustomTaskVersion.create_clean, CustomTaskVersion.create_from_previous],
        ids=["create_clean", "create_from_previous"],
    )
    def test_file_path(
        self,
        temporary_dir,
        versions_base_url,
        task_id,
        custom_task_version_response_json,
        create_method,
    ):
        top_file_name = "a-file.txt"
        sub_file_name = "sub-file.txt"
        top_file_path = os.path.join(temporary_dir, top_file_name)
        sub_file_path = os.path.join(temporary_dir, "sub-dir", sub_file_name)

        os.mkdir(os.path.dirname(sub_file_path))

        for file_name in (top_file_path, sub_file_path):
            with open(file_name, "wb") as f:
                f.write(b"some content")

        http_method = self._get_http_method(create_method)
        add_mock_response(
            http_method, versions_base_url, json.dumps(custom_task_version_response_json)
        )

        create_method(task_id, "abc", folder_path=temporary_dir)

        fields = _fields_to_dict(responses.calls[0].request.body)

        files = fields["file"]
        paths = fields["filePath"]

        parent_dir_size = len(temporary_dir + "/")
        relative_paths = {
            top_file_name: top_file_path[parent_dir_size:],
            sub_file_name: sub_file_path[parent_dir_size:],
        }
        for (filename, file_obj), file_path in zip(files, paths):
            assert relative_paths[filename] == file_path
            assert file_obj.closed

    @responses.activate
    @pytest.mark.parametrize(
        "create_method",
        [CustomTaskVersion.create_clean, CustomTaskVersion.create_from_previous],
        ids=["create_clean", "create_from_previous"],
    )
    def test_bad_file_path_raises_value_error(
        self,
        temporary_dir,
        versions_base_url,
        task_id,
        custom_task_version_response_json,
        create_method,
    ):
        garbage_file_path = os.path.join(temporary_dir, "garbage_dir")
        rmtree(garbage_file_path, ignore_errors=True)

        assert not os.path.exists(garbage_file_path)

        http_method = self._get_http_method(create_method)
        add_mock_response(
            http_method, versions_base_url, json.dumps(custom_task_version_response_json)
        )

        with pytest.raises(ValueError):
            create_method(task_id, "abc", folder_path=garbage_file_path)

    @responses.activate
    def test_create_from_previous_files_to_delete(
        self, versions_base_url, task_id, custom_task_version_response_json,
    ):
        add_mock_response(
            responses.PATCH, versions_base_url, json.dumps(custom_task_version_response_json)
        )

        CustomTaskVersion.create_from_previous(task_id, "abc123", files_to_delete=["abc", "def"])
        fields = _fields_to_dict(responses.calls[0].request.body)
        assert set(fields["filesToDelete"]) == {"abc", "def"}
        assert len(fields["filesToDelete"]) == 2


def _fields_to_dict(encoder):
    # type: (MultipartEncoder) -> defaultdict
    fields = defaultdict(list)
    for k, v in encoder.fields:
        fields[k].append(v)
    return fields


def _update_value(value):
    if isinstance(value, bool):
        return not value
    elif isinstance(value, int):
        return value + 1
    elif isinstance(value, str):
        return value + "x"
    elif isinstance(value, list):
        return value + value
    elif isinstance(value, dict):
        return {k + "x": v for k, v in value.items()}
    else:
        return value


def assert_single_api_call(calls, action, url_ending):
    # type: (responses.CallList, str, str) -> None
    assert len(calls) == 1
    assert calls[0].request.method == action
    assert calls[0].request.url.endswith(url_ending)
