import uuid

import pytest

from mlex_utils.dash_utils.mlex_components import MLExComponents

model_parameters = [
    {
        "type": "float",
        "name": "float_param",
        "title": "Float Parameter",
        "param_key": "float_param",
        "value": 1,
        "comp_group": "group_1",
    },
    {
        "type": "int",
        "name": "int_param",
        "title": "Integer Parameter",
        "param_key": "int_param",
        "value": 1,
        "comp_group": "group_1",
    },
    {
        "type": "str",
        "name": "str_param",
        "title": "String Parameter",
        "param_key": "str_param",
        "value": "test",
        "comp_group": "group_1",
    },
    {
        "type": "slider",
        "name": "slider",
        "title": "Slider",
        "param_key": "slider",
        "min": 1,
        "max": 1000,
        "value": 30,
        "comp_group": "group_1",
    },
    {
        "type": "dropdown",
        "name": "dropdown",
        "title": "Dropdown",
        "param_key": "dropdown",
        "comp_group": "group_1",
    },
    {
        "type": "radio",
        "name": "radio",
        "title": "Radio",
        "param_key": "radio",
        "options": [
            {"label": "Option 1", "value": 1},
            {"label": "Option 2", "value": 2},
        ],
        "comp_group": "group_1",
    },
    {
        "type": "bool",
        "name": "bool",
        "title": "Bool",
        "param_key": "bool",
        "comp_group": "group_1",
    },
]


@pytest.mark.parametrize("component_type", ["dbc", "dmc"])
def test_get_job_manager(component_type):
    mlex_components = MLExComponents(component_type)
    job_manager = mlex_components.get_job_manager()
    assert job_manager is not None

    assert job_manager.toggle_modal(1, 0, False)
    assert not job_manager.toggle_modal(0, 1, True)


@pytest.mark.parametrize("component_type", ["dbc", "dmc"])
def test_get_parameters(component_type):
    mlex_components = MLExComponents(component_type)
    parameters = mlex_components.get_parameter_items(
        _id={"type": str(uuid.uuid4())}, json_blob=model_parameters
    )
    assert parameters is not None
