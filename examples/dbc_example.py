import uuid

import dash_bootstrap_components as dbc
from dash import Dash, Input, Output, callback, dcc, html
from models_utils import Models

from mlex_utils.dash_utils.dbc_utils.component_utils import (
    DbcControlItem as ControlItem,
)
from mlex_utils.dash_utils.dbc_utils.component_utils import header
from mlex_utils.dash_utils.mlex_components import MLExComponents


def get_control_panel(mlex_components, models):

    job_manager = mlex_components.get_job_manager()

    control_panel = dbc.Accordion(
        [
            dbc.AccordionItem(
                [
                    ControlItem(
                        "Algorithm",
                        "select-algorithm",
                        dcc.Dropdown(
                            id="model-list",
                            options=models.modelname_list,
                            value=(
                                models.modelname_list[0]
                                if models.modelname_list[0]
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


app = Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])
mlex_components = MLExComponents("dbc")
models = Models(modelfile_path="./examples/assets/models_dbc.json")

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
                            get_control_panel(mlex_components, models),
                            style={
                                "display": "flex",
                                "margin-top": "1em",
                                "max-width": "450px",
                            },
                        ),
                        dbc.Col(),
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


if __name__ == "__main__":
    app.run_server(debug=True)
