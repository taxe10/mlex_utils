import uuid

import dash_bootstrap_components as dbc
from dash import Dash, Input, Output, callback, html
from models_utils import Models

from mlex_utils.dash_utils.components_bootstrap.component_utils import (
    DbcControlItem as ControlItem,
)
from mlex_utils.dash_utils.components_bootstrap.component_utils import header
from mlex_utils.dash_utils.mlex_components import MLExComponents


def get_control_panel(job_manager, models):
    model_list = [{"label": model, "value": model} for model in models.modelname_list]
    control_panel = dbc.Accordion(
        [
            dbc.AccordionItem(
                [
                    ControlItem(
                        "Algorithm",
                        "select-algorithm",
                        dbc.Select(
                            id="model-list",
                            options=model_list,
                            value=(
                                model_list[0]["value"]
                                if model_list[0]["value"]
                                else None
                            ),
                        ),
                    ),
                    html.Div(id="model-parameters"),
                    html.P(),
                    job_manager,
                ],
                title="Model Configuration",
            ),
        ],
        style={"position": "sticky", "top": "10%", "width": "100%", "padding": "1px"},
    )
    return control_panel


# Get MLExchange dash components
mlex_components = MLExComponents("dbc")
job_manager = mlex_components.get_job_manager()

# Get models
models = Models(modelfile_path="./examples/assets/models_dbc.json")

app = Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])
app.title = "Utils Example"
app._favicon = "mlex.ico"

app_header = header(
    "MLExchange | Utils Example",
    "https://mlexchange.als.lbl.gov",
    "https://mlexchange.als.lbl.gov/docs",
    app.get_asset_url("mlex.png"),
)

app.layout = html.Div(
    [
        app_header,
        dbc.Container(
            children=[
                dbc.Row(
                    [
                        dbc.Col(
                            get_control_panel(job_manager, models),
                            style={
                                "display": "flex",
                                "margin-top": "1em",
                                "max-width": "450px",
                            },
                        ),
                        dbc.Col(
                            dbc.Card(
                                children=[
                                    dbc.CardHeader("Model Parameters"),
                                    dbc.CardBody(
                                        children=[
                                            html.Div(
                                                id="model-params-out",
                                            )
                                        ]
                                    ),
                                ],
                                style={"margin-top": "1em"},
                            ),
                        ),
                    ]
                ),
            ],
            fluid=True,
        ),
    ],
)


@callback(
    Output("model-parameters", "children"),
    Input("model-list", "value"),
)
def update_model_parameters(model_name):
    model = models[model_name]
    if model["gui_parameters"]:
        item_list = mlex_components.get_parameter_items(
            _id={"type": str(uuid.uuid4())}, json_blob=model["gui_parameters"]
        )
        return item_list
    else:
        return html.Div("Model has no parameters")


@callback(
    Output("model-params-out", "children"),
    Input("model-parameters", "children"),
)
def update_model_parameters_output(model_parameter_container):
    model_parameters, parameter_errors = mlex_components.get_parameters_values(
        model_parameter_container
    )
    return str(model_parameters)


if __name__ == "__main__":
    app.run_server(debug=True)
