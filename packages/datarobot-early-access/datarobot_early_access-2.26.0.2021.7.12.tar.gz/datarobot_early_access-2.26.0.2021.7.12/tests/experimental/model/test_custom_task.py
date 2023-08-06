import copy
import json
import os

import pytest
import responses

from datarobot import Model
from datarobot._experimental.models.custom_task import CustomTask
from datarobot.enums import CUSTOM_MODEL_TARGET_TYPE, CUSTOM_TASK_TYPE
from datarobot.errors import ClientError
from datarobot.utils import underscorize
from tests.model.test_custom_model import assert_custom_model_common, mock_get_response


@pytest.fixture
def mocked_custom_estimator(mocked_models):
    return mocked_models["data"][0]


@pytest.fixture
def mocked_custom_transform(mocked_models):
    models = copy.deepcopy(mocked_models)
    models["data"][0].update({"targetType": "Transform"})

    return models["data"][0]


@pytest.fixture
def model_artifact_contents():
    # stolen from scoring code test
    return "some_random_file_contents" * 1000000


@pytest.fixture
def local_artifact_filename(tmpdir):
    return str(tmpdir.join("temp.zip"))


@pytest.mark.parametrize("custom_mock", ["mocked_custom_estimator", "mocked_custom_transform"])
class TestCustomTask(object):
    def test_from_server_data(self, custom_mock, request):
        task_dict = request.getfixturevalue(custom_mock)
        task = CustomTask.from_server_data(task_dict)
        assert_custom_model_common(task, task_dict, custom_task=True)

    @responses.activate
    def test_get_version(self, request, custom_mock, make_tasks_url):
        # arrange
        mocked_task = request.getfixturevalue(custom_mock)
        url = make_tasks_url(mocked_task["id"])
        mock_get_response(url, mocked_task)

        # act
        task = CustomTask.get(mocked_task["id"])

        # assert
        assert_custom_model_common(task, mocked_task, custom_task=True)
        assert responses.calls[0].request.method == "GET"
        assert responses.calls[0].request.url == url

    @responses.activate
    def test_list_tasks(self, request, custom_mock, make_tasks_url):
        mocked_task = request.getfixturevalue(custom_mock)
        url = make_tasks_url()
        mock_get_response(url, {"data": [mocked_task], "next": None})

        response = CustomTask.list()

        assert len(response) == 1
        assert_custom_model_common(response[0], mocked_task, custom_task=True)
        assert responses.calls[0].request.method == "GET"
        assert responses.calls[0].request.url == url

    @responses.activate
    def test_update(self, request, custom_mock, make_tasks_url):
        # arrange
        patch = {
            "description": "new description",
        }
        mocked_task = request.getfixturevalue(custom_mock)
        url = make_tasks_url(mocked_task["id"])
        mock_get_response(url, mocked_task)

        mocked_task.update(patch)

        responses.add(
            responses.PATCH,
            url,
            status=200,
            content_type="application/json",
            body=json.dumps(mocked_task),
        )

        # act
        model = CustomTask.get(mocked_task["id"])
        args = copy.deepcopy(patch)

        model.update(**{underscorize(k): v for k, v in args.items()})

        # assert
        assert_custom_model_common(model, mocked_task, custom_task=True)

        assert responses.calls[0].request.method == "GET"
        assert responses.calls[0].request.url == url
        assert responses.calls[1].request.method == "PATCH"
        assert responses.calls[1].request.url == url
        assert responses.calls[1].request.body == json.dumps(patch).encode()

    @responses.activate
    def test_refresh(self, request, custom_mock, make_tasks_url):
        # arrange
        mocked_task = request.getfixturevalue(custom_mock)
        url = make_tasks_url(mocked_task["id"])
        mock_get_response(url, mocked_task)

        mocked_task.update({"description": "new desc"})

        mock_get_response(url, mocked_task)

        # act
        model = CustomTask.get(mocked_task["id"])
        model.refresh()

        # assert
        assert_custom_model_common(model, mocked_task, custom_task=True)

        assert responses.calls[0].request.method == "GET"
        assert responses.calls[0].request.url == url
        assert responses.calls[1].request.method == "GET"
        assert responses.calls[1].request.url == url

    @responses.activate
    def test_delete(self, request, custom_mock, make_tasks_url):
        mocked_task = request.getfixturevalue(custom_mock)
        url = make_tasks_url(mocked_task["id"])

        mock_get_response(url, mocked_task)
        responses.add(
            responses.DELETE, url, status=204, content_type="application/json",
        )

        model = CustomTask.get(mocked_task["id"])
        model.delete()

        assert responses.calls[0].request.method == "GET"
        assert responses.calls[0].request.url == url
        assert responses.calls[1].request.method == "DELETE"
        assert responses.calls[1].request.url == url

    @responses.activate
    def test_download(self, request, custom_mock, make_tasks_url, tmpdir):
        # arrange
        mocked_task = request.getfixturevalue(custom_mock)
        url = make_tasks_url(mocked_task["id"])
        mock_get_response(url, mocked_task)
        responses.add(
            responses.GET,
            url + "download/",
            status=200,
            content_type="application/json",
            body=b"content",
        )

        downloaded_file = tmpdir.mkdir("sub").join("download")
        downloaded_file_path = str(downloaded_file)

        # act
        model = CustomTask.get(mocked_task["id"])
        model.download_latest_version(downloaded_file_path)

        # assert
        downloaded_file.read() == b"content"

        assert responses.calls[0].request.method == "GET"
        assert responses.calls[0].request.url == url
        assert responses.calls[1].request.method == "GET"
        assert responses.calls[1].request.url == url + "download/"

    @responses.activate
    def test_create(self, request, custom_mock, make_tasks_url):
        mocked_task = request.getfixturevalue(custom_mock)

        responses.add(
            responses.POST,
            make_tasks_url(),
            status=200,
            content_type="application/json",
            body=json.dumps(mocked_task),
        )

        if mocked_task["targetType"] == CUSTOM_TASK_TYPE.TRANSFORM:
            target_type = None
            task_type = CUSTOM_TASK_TYPE.TRANSFORM
        else:
            target_type = CUSTOM_MODEL_TARGET_TYPE.REGRESSION
            task_type = CUSTOM_TASK_TYPE.ESTIMATOR

        model = CustomTask.create(
            name=mocked_task["name"],
            task_type=task_type,
            target_type=target_type,
            description=mocked_task["description"],
        )

        assert_custom_model_common(model, mocked_task, custom_task=True)

        assert responses.calls[0].request.method == "POST"
        assert responses.calls[0].request.url == make_tasks_url()

    @responses.activate
    def test_create_copy(self, request, custom_mock, make_tasks_url):
        mocked_task = request.getfixturevalue(custom_mock)

        custom_task_to_copy = mocked_task["id"]

        url = make_tasks_url() + "fromCustomTask/"
        responses.add(
            responses.POST,
            url,
            status=200,
            content_type="application/json",
            body=json.dumps(mocked_task),
        )

        model = CustomTask.copy_custom_task(custom_task_to_copy)
        assert_custom_model_common(model, mocked_task, custom_task=True)

        req = responses.calls[0].request
        assert req.method == "POST"
        assert req.url == url
        assert json.loads(req.body) == {"customTaskId": custom_task_to_copy}


class TestArtifactDownload(object):
    @responses.activate
    def test_positive_case(
        self, project_id, model_id, model_artifact_contents, local_artifact_filename
    ):
        url = "https://host_name.com/projects/{}/models/{}/trainingArtifact/".format(
            project_id, model_id
        )
        responses.add(
            responses.GET, url, body=model_artifact_contents, status=200, match_querystring=True
        )
        model = Model(project_id=project_id, id=model_id)
        model.download_training_artifact(local_artifact_filename)
        assert os.path.isfile(local_artifact_filename)
        with open(local_artifact_filename) as f:
            contents = f.read()
            assert contents == model_artifact_contents
        os.unlink(local_artifact_filename)
        assert not os.path.isfile(local_artifact_filename)
        req = responses.calls[0].request
        assert req.method == "GET"
        assert req.url == url

    @responses.activate
    def test_error(self, project_id, model_id, model_artifact_contents, local_artifact_filename):
        url = "https://host_name.com/projects/{}/models/{}/trainingArtifact/".format(
            project_id, model_id
        )
        error_message = "some error"
        responses.add(
            responses.GET, url, status=404, match_querystring=True, json={"message": error_message},
        )
        model = Model(project_id=project_id, id=model_id)
        with pytest.raises(ClientError) as exc_info:
            model.download_training_artifact(local_artifact_filename)

        assert not os.path.isfile(local_artifact_filename)
        assert error_message in str(exc_info.value)
