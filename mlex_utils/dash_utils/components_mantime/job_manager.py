import uuid

import dash_mantine_components as dmc
from dash import MATCH, Input, Output, State, callback, dcc, html
from dash_iconify import DashIconify

from mlex_utils.dash_utils.callbacks.manage_jobs import (
    _check_inference_job,
    _check_train_job,
)
from mlex_utils.dash_utils.components_mantime.advanced_options import (
    DmcAdvancedOptionsAIO,
)
from mlex_utils.dash_utils.components_mantime.component_utils import (
    DmcControlItem,
    _tooltip,
)


class DmcJobManagerAIO(html.Div):

    class ids:

        job_name_title = lambda aio_id: {  # noqa: E731
            "component": "DmcJobManagerAIO",
            "subcomponent": "job_name_title",
            "aio_id": aio_id,
        }

        job_name = lambda aio_id: {  # noqa: E731
            "component": "DmcJobManagerAIO",
            "subcomponent": "job_name",
            "aio_id": aio_id,
        }

        train_button = lambda aio_id: {  # noqa: E731
            "component": "DmcJobManagerAIO",
            "subcomponent": "train_button",
            "aio_id": aio_id,
        }

        train_dropdown_title = lambda aio_id: {  # noqa: E731
            "component": "DmcJobManagerAIO",
            "subcomponent": "train_dropdown_title",
            "aio_id": aio_id,
        }

        train_dropdown = lambda aio_id: {  # noqa: E731
            "component": "DmcJobManagerAIO",
            "subcomponent": "train_dropdown",
            "aio_id": aio_id,
        }

        advanced_options_modal_train = lambda aio_id: {  # noqa: E731
            "component": "DmcJobManagerAIO",
            "subcomponent": "advanced_options_modal_train",
            "aio_id": aio_id,
        }

        training_stats_title = lambda aio_id: {  # noqa: E731
            "component": "DmcJobManagerAIO",
            "subcomponent": "training_stats_title",
            "aio_id": aio_id,
        }

        training_stats = lambda aio_id: {  # noqa: E731
            "component": "DmcJobManagerAIO",
            "subcomponent": "training_stats",
            "aio_id": aio_id,
        }

        inference_button = lambda aio_id: {  # noqa: E731
            "component": "DmcJobManagerAIO",
            "subcomponent": "inference_button",
            "aio_id": aio_id,
        }

        inference_dropdown_title = lambda aio_id: {  # noqa: E731
            "component": "DmcJobManagerAIO",
            "subcomponent": "inference_dropdown_title",
            "aio_id": aio_id,
        }

        inference_dropdown = lambda aio_id: {  # noqa: E731
            "component": "DmcJobManagerAIO",
            "subcomponent": "inference_dropdown",
            "aio_id": aio_id,
        }

        advanced_options_modal_inference = lambda aio_id: {  # noqa: E731
            "component": "DmcJobManagerAIO",
            "subcomponent": "advanced_options_modal_inference",
            "aio_id": aio_id,
        }

        advanced_options_modal = lambda aio_id: {  # noqa: E731
            "component": "DmcJobManagerAIO",
            "subcomponent": "advanced_options_modal",
            "aio_id": aio_id,
        }

        check_job = lambda aio_id: {  # noqa: E731
            "component": "DmcJobManagerAIO",
            "subcomponent": "check_job",
            "aio_id": aio_id,
        }

        project_name_id = lambda aio_id: {  # noqa: E731
            "component": "DmcJobManagerAIO",
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
        DmcJobManagerAIO is an All-in-One component that is composed
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
                DmcControlItem(
                    "Name",
                    self.ids.job_name_title(aio_id),
                    dmc.TextInput(
                        placeholder="Name your job...",
                        id=self.ids.job_name(aio_id),
                    ),
                ),
                dmc.Space(h=10),
                dmc.Button(
                    "Train", id=self.ids.train_button(aio_id), **train_button_props
                ),
                dmc.Space(h=10),
                DmcControlItem(
                    "Trained Jobs",
                    self.ids.train_dropdown_title(aio_id),
                    dmc.Grid(
                        [
                            dmc.Select(
                                placeholder="Select a job...",
                                id=self.ids.train_dropdown(aio_id),
                            ),
                            dmc.ActionIcon(
                                _tooltip(
                                    "Advanced Options",
                                    children=[
                                        DashIconify(
                                            icon="mdi:settings-applications",
                                            width=30,
                                        ),
                                    ],
                                ),
                                size="xs",
                                variant="subtle",
                                id=self.ids.advanced_options_modal_train(aio_id),
                                n_clicks=0,
                                style={"margin": "auto"},
                            ),
                        ],
                        style={"margin": "0px"},
                    ),
                ),
                dmc.Space(h=25),
                DmcControlItem(
                    "Training Stats",
                    self.ids.training_stats_title(aio_id),
                    dmc.Anchor(
                        dmc.Text("Open in new window"),
                        id=self.ids.training_stats(aio_id),
                        href="",
                        target="_blank",
                        size="sm",
                    ),
                ),
                dmc.Space(h=10),
                dmc.Button(
                    "Inference",
                    id=self.ids.inference_button(aio_id),
                    **inference_button_props,
                ),
                dmc.Space(h=10),
                DmcControlItem(
                    "Inference Jobs",
                    self.ids.inference_dropdown_title(aio_id),
                    dmc.Grid(
                        [
                            dmc.Select(
                                placeholder="Select a job...",
                                id=self.ids.inference_dropdown(aio_id),
                            ),
                            dmc.ActionIcon(
                                _tooltip(
                                    "Advanced Options",
                                    children=[
                                        DashIconify(
                                            icon="mdi:settings-applications",
                                            width=30,
                                        ),
                                    ],
                                ),
                                size="xs",
                                variant="subtle",
                                id=self.ids.advanced_options_modal_inference(aio_id),
                                n_clicks=0,
                                style={"margin": "auto"},
                            ),
                        ],
                        style={"margin": "0px"},
                    ),
                ),
                dmc.Modal(
                    title="Advanced Options",
                    children=DmcAdvancedOptionsAIO(),
                    id=self.ids.advanced_options_modal(aio_id),
                    **modal_props,
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
        self, button_props, variant="light", style={"width": "100%", "margin": "5px"}
    ):
        button_props = button_props.copy() if button_props else {}
        button_props["variant"] = (
            variant if "variant" not in button_props else button_props["variant"]
        )
        button_props["style"] = (
            style if "style" not in button_props else button_props["style"]
        )
        return button_props

    def _update_modal_props(
        self, modal_props, style={"margin": "10px 10px 10px 250px"}
    ):
        modal_props = modal_props.copy() if modal_props else {}
        modal_props["style"] = (
            style if "style" not in modal_props else modal_props["style"]
        )
        return modal_props

    @staticmethod
    @callback(
        Output(ids.advanced_options_modal(MATCH), "opened"),
        Input(ids.advanced_options_modal_train(MATCH), "n_clicks"),
        Input(ids.advanced_options_modal_inference(MATCH), "n_clicks"),
        State(ids.advanced_options_modal(MATCH), "opened"),
        prevent_initial_call=True,
    )
    def toggle_modal(n1, n2, opened):
        return not opened

    def register_callbacks(self):

        @callback(
            Output(self.ids.train_dropdown(MATCH), "data"),
            Input(self.ids.check_job(MATCH), "n_intervals"),
        )
        def check_train_job(n_intervals):
            return _check_train_job(self._prefect_tags, self._mode)

        @callback(
            Output(self.ids.inference_dropdown(MATCH), "data"),
            Output(self.ids.inference_dropdown(MATCH), "value"),
            Input(self.ids.check_job(MATCH), "n_intervals"),
            Input(self.ids.train_dropdown(MATCH), "value"),
            State(self.ids.project_name_id(MATCH), "data"),
        )
        def check_inference_job(n_intervals, train_job_id, project_name):
            return _check_inference_job(
                train_job_id, project_name, self._prefect_tags, self._mode
            )
