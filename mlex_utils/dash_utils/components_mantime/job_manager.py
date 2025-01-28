import uuid

import dash_mantine_components as dmc
from dash import (
    MATCH,
    Input,
    Output,
    State,
    callback,
    callback_context,
    dcc,
    html,
    no_update,
)
from dash_iconify import DashIconify

from mlex_utils.dash_utils.callbacks.manage_jobs import (
    _cancel_job,
    _check_inference_job,
    _check_train_job,
    _delete_job,
    _get_job_logs,
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
            "subcomponent": "job-name-title",
            "aio_id": aio_id,
        }

        job_name = lambda aio_id: {  # noqa: E731
            "component": "DmcJobManagerAIO",
            "subcomponent": "job-name",
            "aio_id": aio_id,
        }

        train_button = lambda aio_id: {  # noqa: E731
            "component": "DmcJobManagerAIO",
            "subcomponent": "train-button",
            "aio_id": aio_id,
        }

        train_dropdown_title = lambda aio_id: {  # noqa: E731
            "component": "DmcJobManagerAIO",
            "subcomponent": "train-dropdown-title",
            "aio_id": aio_id,
        }

        train_dropdown = lambda aio_id: {  # noqa: E731
            "component": "DmcJobManagerAIO",
            "subcomponent": "train-dropdown",
            "aio_id": aio_id,
        }

        advanced_options_modal_train = lambda aio_id: {  # noqa: E731
            "component": "DmcJobManagerAIO",
            "subcomponent": "advanced-options-modal-train",
            "aio_id": aio_id,
        }

        training_stats_title = lambda aio_id: {  # noqa: E731
            "component": "DmcJobManagerAIO",
            "subcomponent": "training-stats-title",
            "aio_id": aio_id,
        }

        training_stats = lambda aio_id: {  # noqa: E731
            "component": "DmcJobManagerAIO",
            "subcomponent": "training-stats",
            "aio_id": aio_id,
        }

        inference_button = lambda aio_id: {  # noqa: E731
            "component": "DmcJobManagerAIO",
            "subcomponent": "inference-button",
            "aio_id": aio_id,
        }

        inference_dropdown_title = lambda aio_id: {  # noqa: E731
            "component": "DmcJobManagerAIO",
            "subcomponent": "inference-dropdown-title",
            "aio_id": aio_id,
        }

        inference_dropdown = lambda aio_id: {  # noqa: E731
            "component": "DmcJobManagerAIO",
            "subcomponent": "inference-dropdown",
            "aio_id": aio_id,
        }

        advanced_options_modal_inference = lambda aio_id: {  # noqa: E731
            "component": "DmcJobManagerAIO",
            "subcomponent": "advanced-options-modal-inference",
            "aio_id": aio_id,
        }

        advanced_options_modal = lambda aio_id: {  # noqa: E731
            "component": "DmcJobManagerAIO",
            "subcomponent": "advanced-options-modal",
            "aio_id": aio_id,
        }

        check_job = lambda aio_id: {  # noqa: E731
            "component": "DmcJobManagerAIO",
            "subcomponent": "check-job",
            "aio_id": aio_id,
        }

        project_name_id = lambda aio_id: {  # noqa: E731
            "component": "DmcJobManagerAIO",
            "subcomponent": "project-name-id",
            "aio_id": aio_id,
        }

        notifications_container = lambda aio_id: {  # noqa: E731
            "component": "DmcJobManagerAIO",
            "subcomponent": "notifications-container",
            "aio_id": aio_id,
        }

        model_parameters = lambda aio_id: {  # noqa: E731
            "component": "DmcJobManagerAIO",
            "subcomponent": "model-parameters",
            "aio_id": aio_id,
        }

        model_list_title = lambda aio_id: {  # noqa: E731
            "component": "DmcJobManagerAIO",
            "subcomponent": "model-list-title",
            "aio_id": aio_id,
        }

        model_list = lambda aio_id: {  # noqa: E731
            "component": "DmcJobManagerAIO",
            "subcomponent": "model-list",
            "aio_id": aio_id,
        }

        show_training_stats = lambda aio_id: {  # noqa: E731
            "component": "DmcJobManagerAIO",
            "subcomponent": "show-training-stats",
            "aio_id": aio_id,
        }

        show_training_stats_title = lambda aio_id: {  # noqa: E731
            "component": "DmcJobManagerAIO",
            "subcomponent": "show-training-stats-title",
            "aio_id": aio_id,
        }

    ids = ids

    def __init__(
        self,
        model_list=["Test Model"],
        prefect_tags=[],
        mode="dev",
        train_button_props=None,
        inference_button_props=None,
        show_training_stats_button_props=None,
        modal_props=None,
        aio_id=None,
        register_callbacks=True,
    ):
        """
        DmcJobManagerAIO is an All-in-One component that is composed
        of a parent `html.Div` with a button to train and infer a model.
        - `model_list` - A list of models
        - `prefect_tags` - A list of tags used to filter Prefect flow runs.
        - `mode` - The mode of the component. If "dev", the component will display sample data.
        - `train_button_props` - A dictionary of properties passed into the Button component for the train button.
        - `inference_button_props` - A dictionary of properties passed into the Button component for the inference button.
        - `show_training_stats_button_props` - A dictionary of properties passed into the Button component for the
            show training stats button.
        - `modal_props` - A dictionary of properties passed into the Modal component for the advanced options modal.
        - `aio_id` - The All-in-One component ID used to generate the markdown and dropdown components's dictionary IDs.
        - `register_callbacks` - A boolean that determines if the component's callbacks should be registered.
        """
        if aio_id is None:
            aio_id = str(uuid.uuid4())

        if train_button_props is None:
            train_button_props = {
                "variant": "light",
                "style": {"width": "100%", "margin": "5px"},
            }
        if inference_button_props is None:
            inference_button_props = {
                "variant": "light",
                "style": {"width": "100%", "margin": "5px"},
            }
        if show_training_stats_button_props is None:
            show_training_stats_button_props = {
                "size": "sm",
                "radius": "lg",
                "color": "gray",
                "disabled": True,
                "style": {"width": "100%"},
            }
        if modal_props is None:
            modal_props = {"style": {"margin": "10px 10px 10px 250px"}}

        self._prefect_tags = prefect_tags
        self._mode = mode

        super().__init__(
            [
                DmcControlItem(
                    "Algorithm",
                    self.ids.model_list_title(aio_id),
                    dmc.Select(
                        id=self.ids.model_list(aio_id),
                        data=model_list,
                        value=(model_list[0] if model_list[0] else None),
                    ),
                ),
                dmc.Space(h=15),
                html.Div(id=self.ids.model_parameters(aio_id)),
                dmc.Space(h=25),
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
                    "",
                    self.ids.show_training_stats_title(aio_id),
                    dmc.Button(
                        "Show Training Stats",
                        id=self.ids.show_training_stats(aio_id),
                        **show_training_stats_button_props,
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
                DmcAdvancedOptionsAIO(aio_id=aio_id),
                html.Div(id=self.ids.notifications_container(aio_id)),
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

        if register_callbacks:
            self.register_callbacks()

    @staticmethod
    @callback(
        Output(
            {
                "aio_id": MATCH,
                "component": "DmcAdvancedOptionsAIO",
                "subcomponent": "advanced-options-modal",
            },
            "opened",
        ),
        Output(
            {
                "aio_id": MATCH,
                "component": "DmcAdvancedOptionsAIO",
                "subcomponent": "job-id",
            },
            "data",
        ),
        Input(ids.advanced_options_modal_train(MATCH), "n_clicks"),
        Input(ids.advanced_options_modal_inference(MATCH), "n_clicks"),
        State(
            {
                "aio_id": MATCH,
                "component": "DmcAdvancedOptionsAIO",
                "subcomponent": "advanced-options-modal",
            },
            "opened",
        ),
        State(ids.train_dropdown(MATCH), "value"),
        State(ids.inference_dropdown(MATCH), "value"),
        prevent_initial_call=True,
    )
    def toggle_modal(n1, n2, is_open, train_job_id, inference_job_id):
        button_id = callback_context.triggered[0]["prop_id"].split(".")[0]
        if "train" in button_id:
            job_id = train_job_id
        else:
            job_id = inference_job_id
        return not is_open, job_id

    @staticmethod
    @callback(
        Output(ids.advanced_options_modal_train(MATCH), "disabled"),
        Input(ids.train_dropdown(MATCH), "value"),
    )
    def disable_advanced_train_options(train_job_id):
        if train_job_id is not None:
            return False
        return True

    @staticmethod
    @callback(
        Output(ids.advanced_options_modal_inference(MATCH), "disabled"),
        Input(ids.inference_dropdown(MATCH), "value"),
    )
    def disable_advanced_inference_options(inference_job_id):
        if inference_job_id is not None:
            return False
        return True

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
            prevent_initial_call=True,
        )
        def check_inference_job(n_intervals, train_job_id, project_name):
            return _check_inference_job(
                train_job_id, project_name, self._prefect_tags, self._mode
            )

        @callback(
            Output(
                {
                    "aio_id": MATCH,
                    "component": "DmcAdvancedOptionsAIO",
                    "subcomponent": "advanced-options-modal",
                },
                "opened",
                allow_duplicate=True,
            ),
            Input(
                {
                    "aio_id": MATCH,
                    "component": "DmcAdvancedOptionsAIO",
                    "subcomponent": "warning-confirm-cancel",
                },
                "n_clicks",
            ),
            State(
                {
                    "aio_id": MATCH,
                    "component": "DmcAdvancedOptionsAIO",
                    "subcomponent": "job-id",
                },
                "data",
            ),
            prevent_initial_call=True,
        )
        def cancel_job(n_clicks, job_id):
            _cancel_job(job_id, self._mode)
            return False

        @callback(
            Output(self.ids.train_dropdown(MATCH), "value", allow_duplicate=True),
            Output(self.ids.inference_dropdown(MATCH), "value", allow_duplicate=True),
            Output(
                {
                    "aio_id": MATCH,
                    "component": "DmcAdvancedOptionsAIO",
                    "subcomponent": "advanced-options-modal",
                },
                "opened",
                allow_duplicate=True,
            ),
            Input(
                {
                    "aio_id": MATCH,
                    "component": "DmcAdvancedOptionsAIO",
                    "subcomponent": "warning-confirm-delete",
                },
                "n_clicks",
            ),
            State(
                {
                    "aio_id": MATCH,
                    "component": "DmcAdvancedOptionsAIO",
                    "subcomponent": "job-id",
                },
                "data",
            ),
            State(self.ids.train_dropdown(MATCH), "value"),
            State(self.ids.inference_dropdown(MATCH), "value"),
            prevent_initial_call=True,
        )
        def delete_job(n_clicks, job_id, train_job_id, inference_job_id):
            _delete_job(job_id, self._mode)
            if job_id == train_job_id:
                return None, no_update, False
            return no_update, None, False

        @callback(
            Output(
                {
                    "aio_id": MATCH,
                    "component": "DmcAdvancedOptionsAIO",
                    "subcomponent": "logs-area",
                },
                "children",
            ),
            Input(
                {
                    "aio_id": MATCH,
                    "component": "DmcAdvancedOptionsAIO",
                    "subcomponent": "advanced-options-modal",
                },
                "opened",
            ),
            Input(self.ids.check_job(MATCH), "n_intervals"),
            State(
                {
                    "aio_id": MATCH,
                    "component": "DmcAdvancedOptionsAIO",
                    "subcomponent": "job-id",
                },
                "data",
            ),
            prevent_initial_call=True,
        )
        def get_logs(is_open, n_intervals, job_id):
            if job_id is None:
                return "No logs available"
            return _get_job_logs(job_id, self._mode)
