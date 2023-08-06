from datarobot.utils import camelize


def assert_version(version, version_json):
    assert version.id == version_json["id"]
    assert version.environment_id == version_json["environmentId"]
    assert version.label == version_json["label"]
    assert version.description == version_json["description"]
    assert version.build_status == version_json["buildStatus"]
    assert version.created_at == version_json["created"]
    assert version.docker_context_size == version_json.get("dockerContextSize")
    assert version.docker_image_size == version_json.get("dockerImageSize")


def assert_custom_model_version(version, version_json):
    model_version_only_keys = (
        "custom_model_id",
        "network_egress_policy",
        "maximum_memory",
        "replicas",
    )
    for key in model_version_only_keys:
        assert_key(version, version_json, key)

    _assert_custom_version_common_fields(version, version_json)


def assert_custom_task_version(version, version_json):
    assert_key(version, version_json, "custom_task_id")

    _assert_custom_version_common_fields(version, version_json)


def _assert_custom_version_common_fields(version, version_json):
    non_optional = [
        "id",
        "label",
        "description",
        "version_minor",
        "version_major",
        "is_frozen",
        "created_at",
    ]
    for obj_key in non_optional:
        assert_key(version, version_json, obj_key)

    optional = [
        "base_environment_id",
        "required_metadata",
        "base_environment_version_id",
    ]
    for obj_key in optional:
        assert_optional_key(version, version_json, obj_key)

    if version.base_environment_id is not None:
        assert version.base_environment_version_id is not None

    object_items = version.items
    json_items = version_json["items"]
    assert_items(object_items, json_items)

    obj_dependencies = version.dependencies
    json_dependencies = version_json.get("dependencies", [])
    assert_dependencies(obj_dependencies, json_dependencies)


def assert_items(object_items, json_items):
    assert len(object_items) == len(json_items)
    for item, item_json in zip(object_items, json_items):
        for key in ("id", "file_name", "file_path", "file_source", "created_at"):
            assert_key(item, item_json, key)


def assert_dependencies(obj_dependencies, json_dependencies):
    assert len(obj_dependencies) == len(json_dependencies)
    for dependency, dependency_json in zip(obj_dependencies, json_dependencies):
        for key in ("package_name", "line", "line_number"):
            assert_key(dependency, dependency_json, key)

        for constraint, constraint_json in zip(
            dependency.constraints, dependency_json["constraints"]
        ):
            for key in ("version", "constraint_type"):
                assert_key(constraint, constraint_json, key)


def assert_key(api_obj, json_data, obj_attribute):
    is_optional_key = False
    _assert_attribute(api_obj, json_data, obj_attribute, is_optional_key)


def assert_optional_key(api_obj, json_data, obj_attribute):
    is_optional_key = True
    _assert_attribute(api_obj, json_data, obj_attribute, is_optional_key)


def _assert_attribute(api_obj, json_data, obj_attribute, is_json_value_optional):
    json_attribute = camelize(obj_attribute)
    if obj_attribute == "created_at":
        json_attribute = "created"

    if is_json_value_optional:
        json_value = json_data.get(json_attribute)
    else:
        json_value = json_data[json_attribute]
    obj_value = getattr(api_obj, obj_attribute)

    assert obj_value == json_value, (obj_attribute, obj_value, json_value)


def assert_custom_model_version_dependency_build(
    build_info, build_info_json, custom_model_id, custom_model_version_id
):
    assert build_info.custom_model_id == custom_model_id
    assert build_info.custom_model_version_id == custom_model_version_id

    assert build_info.started_at == build_info_json["buildStart"]
    assert build_info.completed_at == build_info_json["buildEnd"]
    assert build_info.build_status == build_info_json["buildStatus"]
