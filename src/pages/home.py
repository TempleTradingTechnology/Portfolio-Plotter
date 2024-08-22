# package imports
import dash
from dash import html, _dash_renderer
import dash_mantine_components as dmc

import pandas as pd

# components
from components.header import header
from components.docUpload import docUpload
from components.footer import footer

_dash_renderer._set_react_version("18.2.0")

dash.register_page(
    __name__,
    path='/',
    redirect_from=['/home'],
    title='Home'
)

# daily PNL Graph
df = pd.read_csv('../data/BuyandHold_EQL_DOLLAR_pnl.csv')

data = df.to_dict(orient='records')

layout = dmc.MantineProvider(
    forceColorScheme="light",
    id="mantine-provider",
    children= [
        dmc.AppShell(
            children=[
                header,
                dmc.AppShellMain(
                    children=[
                        dmc.Stack(
                            [
                                dmc.Title("Upload your *_pnl.csv file", order=1),
                                docUpload,
                                html.Div(id='output-data-upload'),
                            ]
                        ),
                    ]),
                    footer
            ],
            # bg="#f8f9fa",
            padding="xl",
            zIndex=1400,
            header={"height": 100, "display":"flex", "alignItems":"center"},
            footer={"height": 75},
        )
    ]
)


