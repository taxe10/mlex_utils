import dash_mantine_components as dmc
from dash import Dash, html
from dash_iconify import DashIconify

from mlex_utils.dash_utils.dmc_utils.component_utils import (
    ControlItem,
    _accordion_item,
    _tooltip,
    drawer_section,
)
from mlex_utils.dash_utils.job_manager import get_job_manager_aio


def layout():
    """
    Returns the layout for the control panel in the app UI
    """
    job_manager = get_job_manager_aio("dmc")
    return drawer_section(
        "MLExchange Utils Example with DMC",
        dmc.Stack(
            style={"width": "400px"},
            children=[
                dmc.AccordionMultiple(
                    id="control-accordion",
                    value=["data-select", "image-transformations", "run-model"],
                    children=[
                        _accordion_item(
                            "Data selection",
                            "majesticons:data-line",
                            "data-select",
                            id="data-selection-controls",
                            children=[
                                dmc.Space(h=5),
                                ControlItem(
                                    "Dataset",
                                    "image-selector",
                                    dmc.Grid(
                                        [
                                            dmc.Select(
                                                id="project-name-src",
                                                data=[],
                                                placeholder="Select an image to view...",
                                            ),
                                            dmc.ActionIcon(
                                                _tooltip(
                                                    "Refresh dataset",
                                                    children=[
                                                        DashIconify(
                                                            icon="mdi:refresh-circle",
                                                            width=20,
                                                        ),
                                                    ],
                                                ),
                                                size="xs",
                                                variant="subtle",
                                                id="refresh-tiled",
                                                n_clicks=0,
                                                style={"margin": "auto"},
                                            ),
                                        ],
                                        style={"margin": "0px"},
                                    ),
                                ),
                                dmc.Space(h=10),
                            ],
                        ),
                        _accordion_item(
                            "Image transformations",
                            "fluent-mdl2:image-pixel",
                            "image-transformations",
                            id="image-transformation-controls",
                            children=html.Div(
                                [
                                    dmc.Space(h=5),
                                    ControlItem(
                                        "Brightness",
                                        "bightness-text",
                                        [
                                            dmc.Grid(
                                                [
                                                    dmc.Slider(
                                                        id={
                                                            "type": "slider",
                                                            "index": "brightness",
                                                        },
                                                        value=100,
                                                        min=0,
                                                        max=255,
                                                        step=1,
                                                        color="gray",
                                                        size="sm",
                                                        style={"width": "225px"},
                                                    ),
                                                    dmc.ActionIcon(
                                                        _tooltip(
                                                            "Reset brightness",
                                                            children=[
                                                                DashIconify(
                                                                    icon="fluent:arrow-reset-32-regular",
                                                                    width=15,
                                                                ),
                                                            ],
                                                        ),
                                                        size="xs",
                                                        variant="subtle",
                                                        id={
                                                            "type": "reset",
                                                            "index": "brightness",
                                                        },
                                                        n_clicks=0,
                                                        style={"margin": "auto"},
                                                    ),
                                                ],
                                                style={"margin": "0px"},
                                            )
                                        ],
                                    ),
                                    dmc.Space(h=20),
                                    ControlItem(
                                        "Contrast",
                                        "contrast-text",
                                        dmc.Grid(
                                            [
                                                dmc.Slider(
                                                    id={
                                                        "type": "slider",
                                                        "index": "contrast",
                                                    },
                                                    value=100,
                                                    min=0,
                                                    max=255,
                                                    step=1,
                                                    color="gray",
                                                    size="sm",
                                                    style={"width": "225px"},
                                                ),
                                                dmc.ActionIcon(
                                                    _tooltip(
                                                        "Reset contrast",
                                                        children=[
                                                            DashIconify(
                                                                icon="fluent:arrow-reset-32-regular",
                                                                width=15,
                                                            ),
                                                        ],
                                                    ),
                                                    size="xs",
                                                    variant="subtle",
                                                    id={
                                                        "type": "reset",
                                                        "index": "contrast",
                                                    },
                                                    n_clicks=0,
                                                    style={"margin": "auto"},
                                                ),
                                            ],
                                            style={"margin": "0px"},
                                        ),
                                    ),
                                    dmc.Space(h=10),
                                ]
                            ),
                        ),
                        _accordion_item(
                            "Model configuration",
                            "carbon:ibm-watson-machine-learning",
                            "run-model",
                            id="model-configuration",
                            children=[
                                ControlItem(
                                    "Model",
                                    "model-selector",
                                    dmc.Select(
                                        id="model-list",
                                        data=[],
                                        placeholder="Select a model...",
                                    ),
                                ),
                                dmc.Space(h=15),
                                html.Div(id="model-parameters"),
                                dmc.Space(h=25),
                                job_manager,
                            ],
                        ),
                    ],
                ),
            ],
        ),
    )


app = Dash(__name__)

app.layout = dmc.MantineProvider(
    theme={"colorScheme": "light"},
    children=layout(),
)

if __name__ == "__main__":
    app.run_server(debug=True, port=8051)
