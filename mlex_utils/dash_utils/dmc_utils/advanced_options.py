import uuid

import dash_mantine_components as dmc
from dash import html


class AdvancedOptionsAIO(html.Div):

    class ids:

        cancel_button = lambda aio_id: {  # noqa: E731
            "component": "JobManagerAIO",
            "subcomponent": "cancel_button",
            "aio_id": aio_id,
        }

        delete_button = lambda aio_id: {  # noqa: E731
            "component": "JobManagerAIO",
            "subcomponent": "delete_button",
            "aio_id": aio_id,
        }

        logs_area = lambda aio_id: {  # noqa: E731
            "component": "JobManagerAIO",
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

        cancel_button_props = self._update_button_props(cancel_button_props)
        delete_button_props = self._update_button_props(delete_button_props)

        super().__init__(
            [
                dmc.ScrollArea(
                    children=dmc.Paper(
                        [
                            dmc.Text(
                                "These are the logs...",
                                id=self.ids.logs_area(aio_id),
                            ),
                        ],
                        style={"width": "100%", "height": 200, "margin-bottom": "10px"},
                    ),
                ),
                dmc.Grid(
                    [
                        dmc.Col(
                            dmc.Button(
                                "Cancel Job",
                                id=self.ids.cancel_button(aio_id),
                                **cancel_button_props,
                            ),
                            span=6,
                        ),
                        dmc.Col(
                            dmc.Button(
                                "Delete Job",
                                id=self.ids.delete_button(aio_id),
                                **delete_button_props,
                            ),
                            span=6,
                        ),
                    ]
                ),
            ]
        )

    def _update_button_props(
        self,
        button_props,
        variant="light",
        color="red",
        style={"width": "100%", "margin": "5px"},
    ):
        button_props = button_props.copy() if button_props else {}
        button_props["variant"] = (
            variant if "variant" not in button_props else button_props["variant"]
        )
        button_props["color"] = (
            color if "color" not in button_props else button_props["color"]
        )
        button_props["style"] = (
            style if "style" not in button_props else button_props["style"]
        )
        return button_props
