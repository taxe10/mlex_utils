import uuid

import dash_bootstrap_components as dbc
from dash import MATCH, Input, Output, State, callback, dcc, html
from dash_iconify import DashIconify

from mlex_utils.dash_utils.callbacks.manage_jobs import (
    _check_inference_job,
    _check_train_job,
)
from mlex_utils.dash_utils.dbc_utils.advanced_options import DbcAdvancedOptionsAIO
from mlex_utils.dash_utils.dbc_utils.component_utils import DbcControlItem


class DbcJobManagerAIO(html.Div):

    class ids:

        job_name_title = lambda aio_id: {  # noqa: E731
            "component": "DbcJobManagerAIO",
            "subcomponent": "job_name_title",
            "aio_id": aio_id,
        }

        job_name = lambda aio_id: {  # noqa: E731
            "component": "DbcJobManagerAIO",
            "subcomponent": "job_name",
            "aio_id": aio_id,
        }

        train_button = lambda aio_id: {  # noqa: E731
            "component": "DbcJobManagerAIO",
            "subcomponent": "train_button",
            "aio_id": aio_id,
        }

        train_dropdown_title = lambda aio_id: {  # noqa: E731
            "component": "DbcJobManagerAIO",
            "subcomponent": "train_dropdown_title",
            "aio_id": aio_id,
        }

        train_dropdown = lambda aio_id: {  # noqa: E731
            "component": "DbcJobManagerAIO",
            "subcomponent": "train_dropdown",
            "aio_id": aio_id,
        }

        advanced_options_modal_train = lambda aio_id: {  # noqa: E731
            "component": "DbcJobManagerAIO",
            "subcomponent": "advanced_options_modal_train",
            "aio_id": aio_id,
        }

        inference_button = lambda aio_id: {  # noqa: E731
            "component": "DbcJobManagerAIO",
            "subcomponent": "inference_button",
            "aio_id": aio_id,
        }

        inference_dropdown_title = lambda aio_id: {  # noqa: E731
            "component": "DbcJobManagerAIO",
            "subcomponent": "inference_dropdown_title",
            "aio_id": aio_id,
        }

        inference_dropdown = lambda aio_id: {  # noqa: E731
            "component": "DbcJobManagerAIO",
            "subcomponent": "inference_dropdown",
            "aio_id": aio_id,
        }

        advanced_options_modal_inference = lambda aio_id: {  # noqa: E731
            "component": "DbcJobManagerAIO",
            "subcomponent": "advanced_options_modal_inference",
            "aio_id": aio_id,
        }

        advanced_options_modal = lambda aio_id: {  # noqa: E731
            "component": "DbcJobManagerAIO",
            "subcomponent": "advanced_options_modal",
            "aio_id": aio_id,
        }

        check_job = lambda aio_id: {  # noqa: E731
            "component": "DbcJobManagerAIO",
            "subcomponent": "check_job",
            "aio_id": aio_id,
        }

        project_name_id = lambda aio_id: {  # noqa: E731
            "component": "DbcJobManagerAIO",
            "subcomponent": "project_name_id",
            "aio_id": aio_id,
        }

    ids = ids

    def __init__(
        self,
        prefect_tags=[],
        mode="dev",
        train_button_props=None,
        inference_button_props=None,
        modal_props=None,
        aio_id=None,
    ):
        """
        DbcJobManagerAIO is an All-in-One component that is composed
        of a parent `html.Div` with a button to train and infer a model.
        - `prefect_tags` - A list of tags used to filter Prefect flow runs.
        - `mode` - The mode of the component. If "dev", the component will display sample data.
        - `train_button_props` - A dictionary of properties passed into the Button component for the train button.
        - `inference_button_props` - A dictionary of properties passed into the Button component for the inference button.
        - `modal_props` - A dictionary of properties passed into the Modal component for the advanced options modal.
        - `aio_id` - The All-in-One component ID used to generate the markdown and dropdown components's dictionary IDs.
        """
        if aio_id is None:
            aio_id = str(uuid.uuid4())

        train_button_props = self._update_button_props(train_button_props)
        inference_button_props = self._update_button_props(inference_button_props)
        modal_props = self._update_modal_props(modal_props)

        self._prefect_tags = prefect_tags
        self._mode = mode

        super().__init__(
            [
                DbcControlItem(
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
                DbcControlItem(
                    "Trained Jobs",
                    self.ids.train_dropdown_title(aio_id),
                    [
                        dbc.Row(
                            [
                                dbc.Col(
                                    dbc.Select(
                                        id=self.ids.train_dropdown(aio_id),
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
                DbcControlItem(
                    "Inference Jobs",
                    self.ids.inference_dropdown_title(aio_id),
                    [
                        dbc.Row(
                            [
                                dbc.Col(
                                    dbc.Select(
                                        id=self.ids.inference_dropdown(aio_id),
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
                        dbc.ModalBody(DbcAdvancedOptionsAIO()),
                    ],
                    id=self.ids.advanced_options_modal(aio_id),
                    style={"margin": "10px 10px 10px 10px"},
                    is_open=False,
                ),
                dcc.Interval(
                    id=self.ids.check_job(aio_id),
                    interval=5000,
                ),
                dcc.Store(
                    id=self.ids.project_name_id(aio_id),
                    data="",
                ),
            ]
        )

        self.register_callbacks()

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

    def _update_modal_props(self, modal_props, style={}):
        modal_props = modal_props.copy() if modal_props else {}
        modal_props["style"] = (
            style if "style" not in modal_props else modal_props["style"]
        )
        return modal_props

    @staticmethod
    @callback(
        Output(ids.advanced_options_modal(MATCH), "is_open"),
        Input(ids.advanced_options_modal_train(MATCH), "n_clicks"),
        Input(ids.advanced_options_modal_inference(MATCH), "n_clicks"),
        State(ids.advanced_options_modal(MATCH), "is_open"),
        prevent_initial_call=True,
    )
    def toggle_modal(n1, n2, is_open):
        return not is_open

    def register_callbacks(self):

        @callback(
            Output(self.ids.train_dropdown(MATCH), "options"),
            Input(self.ids.check_job(MATCH), "n_intervals"),
        )
        def check_train_job(n_intervals):
            return _check_train_job(self._prefect_tags, self._mode)

        @callback(
            Output(self.ids.inference_dropdown(MATCH), "options"),
            Output(self.ids.inference_dropdown(MATCH), "value"),
            Input(self.ids.check_job(MATCH), "n_intervals"),
            Input(self.ids.train_dropdown(MATCH), "value"),
            State(self.ids.project_name_id(MATCH), "data"),
            prevent_initial_call=True,
        )
        def check_inferece_job(n_intervals, train_job_id, project_name):
            return _check_inference_job(
                train_job_id, project_name, self._prefect_tags, self._mode
            )
