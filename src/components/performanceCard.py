
import dash
from dash import Dash

import dash_mantine_components as dmc


def create_performance_card(title, number):
    return dmc.Card(
        children=[
            dmc.Title(title, order=3),
            dmc.Title(number, order=1, mt="md"),
        ],
        # bg="yellow.5",
        # shadow="sm",
        withBorder=True,
        padding="xl",
        h="100%",
        mih=225,
        mah=225,
        miw=300,
        maw=300,
        radius="lg",
    )