
import dash
from dash import Dash

import dash_mantine_components as dmc


def create_performance_card(title, number,
        number_format_spec="{:.4f}"):
    return dmc.Card(
        children=[
            dmc.Text(title, size="xl", fw=600),
            dmc.Title(number_format_spec.format(number), order=1,  mt="md"),
        ],
        # bg="yellow.5",
        shadow="sm",
        withBorder=True,
        padding="lg",
        style={"wordBreak": "break-all"},
        h=225,
        w=300,
        mih=225,
        mah=225,
        miw=300,
        maw=300,
        radius="lg",
    )