# package imports
import dash
from dash import html, _dash_renderer
import dash_mantine_components as dmc
import dash_loading_spinners as dls

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
                                dmc.Title("Upload your *_pnl.csv and *_trade_history.csv file", order=1),
                                docUpload,
                                dls.Rise(
                                    html.Div(id='output-data-upload',
                                    style={
                                    'justify-content': 'center',
                                    'align-items': 'center',
                                    'height': '250px'}),
                                    color = "#c76067"
                                )
                            ]
                        ),
                    ]),
                footer
            ],
            padding="xl",
            zIndex=1400,
            header={"height": 100, "display":"flex", "alignItems":"center"},
            footer={"height": 75},
        )
    ]
)


