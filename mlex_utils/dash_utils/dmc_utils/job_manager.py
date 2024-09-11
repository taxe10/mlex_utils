import uuid

import dash_mantine_components as dmc
from dash import MATCH, Input, Output, State, callback, html
from dash_iconify import DashIconify

from mlex_utils.dash_utils.dmc_utils.advanced_options import AdvancedOptionsAIO
from mlex_utils.dash_utils.dmc_utils.component_utils import ControlItem, _tooltip


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

        training_stats_title = lambda aio_id: {  # noqa: E731
            "component": "JobManagerAIO",
            "subcomponent": "training_stats_title",
            "aio_id": aio_id,
        }

        training_stats = lambda aio_id: {  # noqa: E731
            "component": "JobManagerAIO",
            "subcomponent": "training_stats",
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
        self,
        train_button_props=None,
        inference_button_props=None,
        modal_props=None,
        aio_id=None,
    ):
        """
        JobManagerAIO is an All-in-One component that is composed
        of a parent `html.Div` with a button to train and infer a model.
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

        super().__init__(
            [
                ControlItem(
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
                ControlItem(
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
                ControlItem(
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
                ControlItem(
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
                    children=AdvancedOptionsAIO(),
                    id=self.ids.advanced_options_modal(aio_id),
                    **modal_props,
                ),
            ]
        )

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
        self, modal_props, style={"margin": "10px 10px 10px 250px"}, opened=False
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
