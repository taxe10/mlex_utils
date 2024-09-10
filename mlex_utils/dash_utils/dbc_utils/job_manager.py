import uuid

import dash_bootstrap_components as dbc
from dash import MATCH, Input, Output, State, callback, dcc, html
from dash_iconify import DashIconify

from mlex_utils.dash_utils.dbc_utils.advanced_options import AdvancedOptionsAIO
from mlex_utils.dash_utils.dbc_utils.component_utils import ControlItem


class JobManagerAIO(html.Div):

    class ids:

        job_name_title = lambda aio_id: {  # noqa: E731
            "component": "JobManagerAIO",
            "subcomponent": "job_name_title",
            "aio_id": aio_id,
        }

        job_name = lambda aio_id: {  # noqa: E731
            "component": "JobManagerAIO",
            "subcomponent": "job_name",
            "aio_id": aio_id,
        }

        train_button = lambda aio_id: {  # noqa: E731
            "component": "JobManagerAIO",
            "subcomponent": "train_button",
            "aio_id": aio_id,
        }

        train_dropdown_title = lambda aio_id: {  # noqa: E731
            "component": "JobManagerAIO",
            "subcomponent": "train_dropdown_title",
            "aio_id": aio_id,
        }

        train_dropdown = lambda aio_id: {  # noqa: E731
            "component": "JobManagerAIO",
            "subcomponent": "train_dropdown",
            "aio_id": aio_id,
        }

        advanced_options_modal_train = lambda aio_id: {  # noqa: E731
            "component": "JobManagerAIO",
            "subcomponent": "advanced_options_modal_train",
            "aio_id": aio_id,
        }

        inference_button = lambda aio_id: {  # noqa: E731
            "component": "JobManagerAIO",
            "subcomponent": "inference_button",
            "aio_id": aio_id,
        }

        inference_dropdown_title = lambda aio_id: {  # noqa: E731
            "component": "JobManagerAIO",
            "subcomponent": "inference_dropdown_title",
            "aio_id": aio_id,
        }

        inference_dropdown = lambda aio_id: {  # noqa: E731
            "component": "JobManagerAIO",
            "subcomponent": "inference_dropdown",
            "aio_id": aio_id,
        }

        advanced_options_modal_inference = lambda aio_id: {  # noqa: E731
            "component": "JobManagerAIO",
            "subcomponent": "advanced_options_modal_inference",
            "aio_id": aio_id,
        }

        advanced_options_modal = lambda aio_id: {  # noqa: E731
            "component": "JobManagerAIO",
            "subcomponent": "advanced_options_modal",
            "aio_id": aio_id,
        }

    ids = ids

    def __init__(
        self, train_button_props=None, inference_button_props=None, aio_id=None
    ):
        """
        JobManagerAIO is an All-in-One component that is composed
        of a parent `html.Div` with a button to train and infer a model.
        - `train_button_props` - A dictionary of properties passed into the Button component for the train button.
        - `inference_button_props` - A dictionary of properties passed into the Button component for the inference button.
        - `aio_id` - The All-in-One component ID used to generate the markdown and dropdown components's dictionary IDs.
        """
        if aio_id is None:
            aio_id = str(uuid.uuid4())

        train_button_props = self._update_button_props(train_button_props)
        inference_button_props = self._update_button_props(inference_button_props)

        super().__init__(
            [
                ControlItem(
                    "Name",
                    self.ids.job_name_title(aio_id),
                    dbc.Input(
                        id=self.ids.job_name(aio_id),
                        type="text",
                        placeholder="Name your job...",
                        style={"width": "100%"},
                    ),
                ),
                html.Div(style={"height": "10px"}),
                dbc.Button(
                    "Train", id=self.ids.train_button(aio_id), **train_button_props
                ),
                html.Div(style={"height": "10px"}),
                ControlItem(
                    "Trained Jobs",
                    self.ids.train_dropdown_title(aio_id),
                    [
                        dbc.Row(
                            [
                                dbc.Col(
                                    dcc.Dropdown(
                                        id=self.ids.train_dropdown(aio_id),
                                        style={"width": "100%"},
                                    ),
                                    width=10,
                                ),
                                dbc.Col(
                                    dbc.Button(
                                        DashIconify(
                                            icon="mdi:settings",
                                            style={"padding": "0px"},
                                        ),
                                        id=self.ids.advanced_options_modal_train(
                                            aio_id
                                        ),
                                        color="secondary",
                                        style={"height": "36px", "line-height": "1"},
                                    ),
                                    width=2,
                                ),
                            ],
                            className="g-1",
                        ),
                    ],
                ),
                html.Div(style={"height": "10px"}),
                dbc.Button(
                    "Inference",
                    id=self.ids.inference_button(aio_id),
                    **inference_button_props,
                ),
                html.Div(style={"height": "10px"}),
                ControlItem(
                    "Inference Jobs",
                    self.ids.inference_dropdown_title(aio_id),
                    [
                        dbc.Row(
                            [
                                dbc.Col(
                                    dcc.Dropdown(
                                        id=self.ids.inference_dropdown(aio_id),
                                        style={"width": "100%"},
                                    ),
                                    width=10,
                                ),
                                dbc.Col(
                                    dbc.Button(
                                        DashIconify(icon="mdi:settings"),
                                        id=self.ids.advanced_options_modal_inference(
                                            aio_id
                                        ),
                                        color="secondary",
                                        style={"height": "36px", "line-height": "1"},
                                    ),
                                    width=1,
                                ),
                            ],
                            className="g-1",
                        ),
                    ],
                ),
                html.Div(style={"height": "10px"}),
                dbc.Modal(
                    [
                        dbc.ModalHeader("Advanced Options"),
                        dbc.ModalBody(AdvancedOptionsAIO()),
                    ],
                    id=self.ids.advanced_options_modal(aio_id),
                    style={"margin": "10px 10px 10px 10px"},
                    is_open=False,
                ),
            ]
        )

    def _update_button_props(
        self, button_props, color="primary", style={"width": "100%"}
    ):
        button_props = button_props.copy() if button_props else {}
        button_props["color"] = (
            color if "color" not in button_props else button_props["color"]
        )
        button_props["style"] = (
            style if "style" not in button_props else button_props["style"]
        )
        return button_props

    @callback(
        Output(ids.advanced_options_modal(MATCH), "is_open"),
        Input(ids.advanced_options_modal_train(MATCH), "n_clicks"),
        Input(ids.advanced_options_modal_inference(MATCH), "n_clicks"),
        State(ids.advanced_options_modal(MATCH), "is_open"),
        prevent_initial_call=True,
    )
    def toggle_modal(n1, n2, is_open):
        return not is_open
