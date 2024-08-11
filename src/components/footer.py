
import dash
from dash import Dash, Input, Output, State, callback

import dash_mantine_components as dmc

footer = dmc.AppShellFooter(px=25,
                children=[
                    dmc.Text(
                        "© 2024 Temple Trading & Technology Club",
                        ta="center"
                    )
                ]
            )

