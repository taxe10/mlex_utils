import uuid

import dash_bootstrap_components as dbc
from dash import html


class DbcAdvancedOptionsAIO(html.Div):

    class ids:

        cancel_button = lambda aio_id: {  # noqa: E731
            "component": "DbcJobManagerAIO",
            "subcomponent": "cancel_button",
            "aio_id": aio_id,
        }

        delete_button = lambda aio_id: {  # noqa: E731
            "component": "DbcJobManagerAIO",
            "subcomponent": "delete_button",
            "aio_id": aio_id,
        }

        logs_area = lambda aio_id: {  # noqa: E731
            "component": "DbcJobManagerAIO",
            "subcomponent": "logs_area",
            "aio_id": aio_id,
        }

    ids = ids

    def __init__(
        self,
        cancel_button_props=None,
        delete_button_props=None,
        logs_area_props=None,
        aio_id=None,
    ):
        """
        JobExecutionAIO is an All-in-One component that is composed
        of a parent `html.Div` with a button to cancel, delete, and advance a job.
        - `cancel_button_props` - A dictionary of properties passed into the Button component for the cancel button.
        - `delete_button_props` - A dictionary of properties passed into the Button component for the delete button.
        - `logs_area_props` - A dictionary of properties passed into the Textarea component for the logs area.
        - `aio_id` - The All-in-One component ID used to generate the markdown and dropdown components's dictionary IDs.
        """
        if aio_id is None:
            aio_id = str(uuid.uuid4())

        cancel_button_props, delete_button_props = self._update_props(
            cancel_button_props, delete_button_props
        )

        super().__init__(
            [
                html.H6(
                    id=self.ids.logs_area(aio_id),
                    children="These are the logs...",
                    style={"width": "100%", "height": 200, "margin-bottom": "10px"},
                ),
                dbc.Row(
                    [
                        dbc.Col(
                            dbc.Button(
                                "Cancel Job",
                                id=self.ids.cancel_button(aio_id),
                                **cancel_button_props,
                            )
                        ),
                        dbc.Col(
                            dbc.Button(
                                "Delete Job",
                                id=self.ids.delete_button(aio_id),
                                **delete_button_props,
                            )
                        ),
                    ]
                ),
            ]
        )

    def _update_props(self, cancel_button_props, delete_button_props):
        cancel_button_props = cancel_button_props.copy() if cancel_button_props else {}
        delete_button_props = delete_button_props.copy() if delete_button_props else {}

        cancel_button_props = self._update_button_props(
            cancel_button_props, "danger", {"width": "100%"}
        )
        delete_button_props = self._update_button_props(
            delete_button_props, "danger", {"width": "100%"}
        )
        return cancel_button_props, delete_button_props

    def _update_button_props(self, button_props, color, style):
        button_props["color"] = color
        button_props["style"] = style
        return button_props
