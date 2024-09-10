import dash_bootstrap_components as dbc
from dash import Dash, dcc, html

from mlex_utils.dash_utils.dbc_utils.component_utils import ControlItem, header
from mlex_utils.dash_utils.job_manager import get_job_manager_aio


def get_control_panel():

    job_manager_aio = get_job_manager_aio(ui_style="dbc")

    control_panel = dbc.Accordion(
        [
            dbc.AccordionItem(
                [
                    ControlItem(
                        "Algorithm",
                        "selec-algorithm",
                        dcc.Dropdown(
                            id="algorithm-dropdown",
                            options=[
                                {"label": entry, "value": entry}
                                for entry in ["PCA", "UMAP"]
                            ],
                            value="PCA",
                        ),
                    ),
                    html.P(),
                    job_manager_aio,
                ],
                title="Model Configuration",
            ),
        ],
        style={"position": "sticky", "top": "10%", "width": "100%", "padding": "1px"},
    )
    return control_panel


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
                            get_control_panel(),
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

if __name__ == "__main__":
    app.run_server(debug=True)
