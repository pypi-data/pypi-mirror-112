import json

import pytest
import responses
from trafaret import DataError

from datarobot._experimental.models.model import CombinedModel
from datarobot._experimental.models.project import Project

_project_id = "projectId"
_target = "target"
_base_url = "https://host_name.com/projects/{}/combinedModels/".format(_project_id)
_valid_combined_model_id = "validCombinedModelId"
_invalid_combined_model_id = "validCombinedModelId"
_valid_combined_model_url = "{0}{1}/".format(_base_url, _valid_combined_model_id)
_invalid_combined_model_url = "{0}{1}/".format(_base_url, _invalid_combined_model_id)


@pytest.fixture
def combined_model_record():
    return {
        "combinedModelId": _valid_combined_model_id,
        "projectId": _project_id,
        "segmentationTaskId": "segmentationTaskId",
    }


@pytest.fixture
def combined_model_list_response(combined_model_record):
    return {"count": 1, "next": None, "previous": None, "data": [combined_model_record]}


@pytest.fixture
def combined_model_get_json(combined_model_record):
    return json.dumps(combined_model_record)


@pytest.fixture
def invalid_json():
    return json.dumps({"message": "Not Found"})


@pytest.fixture
def combined_model_list_json(combined_model_list_response):
    return json.dumps(combined_model_list_response)


@responses.activate
def test_combined_model_list(combined_model_list_json):
    responses.add(
        responses.GET,
        _base_url,
        body=combined_model_list_json,
        status=200,
        content_type="application/json",
    )
    project = Project(id=_project_id)
    combined_models = project.get_combined_models()
    assert len(combined_models) == 1
    combined_model = combined_models[0]

    assert isinstance(combined_model, CombinedModel)
    assert combined_model.id == _valid_combined_model_id
    assert combined_model.project_id == _project_id


@responses.activate
def test_combined_model_get_valid(combined_model_get_json):
    responses.add(
        responses.GET,
        _valid_combined_model_url,
        body=combined_model_get_json,
        status=200,
        content_type="application/json",
    )
    combined_model = CombinedModel.get(_project_id, _valid_combined_model_id)

    assert isinstance(combined_model, CombinedModel)
    assert combined_model.id == _valid_combined_model_id
    assert combined_model.project_id == _project_id


@responses.activate
def test_combined_model_invalid_get(invalid_json):
    responses.add(responses.GET, _invalid_combined_model_url, body=invalid_json)
    with pytest.raises(DataError):
        CombinedModel.get(_project_id, _invalid_combined_model_id)
