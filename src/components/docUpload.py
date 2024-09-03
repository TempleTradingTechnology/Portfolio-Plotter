import dash
from dash import html, dcc, html, dash_table, Input, Output, State, callback
import dash_mantine_components as dmc
import pandas as pd
import base64
import datetime
import io

from utils import performanceMetric

from components.performanceCard import create_performance_card


docUpload = dcc.Upload(
    id='upload-data',
    children=html.Div([
        dmc.Flex([
            dmc.Text('Click Here ', size="lg", fw=700),
            dmc.Text('to upload your PNL file or drag and drop.', size="lg", fw=500),
        ],
        gap="xs"),
        html.Div([
            'Supported files: .xls, .csv'
        ])
    ]),
    style={
        'display': 'flex',
        'justify-content': 'center',
        'flex-direction': 'column',
        'align-items': 'center',
        'width': '100%',
        'height': '317px',
        'border-radius': "20px",
        'border': '3px #B1B1B1 dashed',
        'textAlign': 'center',
        'margin': '10px'
    },
    # Allow multiple files to be uploaded
    multiple=True
)

def parse_contents(contents, filename, date):

    pnl_header = "Date,cash,equity_exposure,total_value,cumulative_pnl,daily pnl returns"

    content_type, content_string = contents.split(',')


    decoded = base64.b64decode(content_string)
    try:
        if 'csv' in filename:
            # Assume that the user uploaded a CSV file
            df = pd.read_csv(
                io.StringIO(decoded.decode('utf-8')))

            if df.columns.tolist() != pnl_header.split(','):
                return html.Div([
                    dmc.Alert("There were no PNL file found",
                                            title="File Error",
                                            color="red",
                                            withCloseButton=True)])
        elif 'xls' in filename:
            # Assume that the user uploaded an excel file
            df = pd.read_excel(io.BytesIO(decoded))
    except Exception as e:
        print(e)
        return html.Div([
            'There was an error processing this file.'
        ])

    data = df.to_dict(orient='records')

    print(df.columns)

    return html.Div([
        dmc.Title(f"File Name: {filename}", order=1),
        html.Br(),
        dmc.Title(f"Performance Metrics", order=1),
        html.Br(),
        dmc.Divider(size="md"),
        html.Br(),
        dmc.Group(
                align={"sm": "center"},
                children=[
                    create_performance_card("Cumulative Return", 100 * df['cumulative_pnl'].iloc[-1] / 1-000-000),
                    create_performance_card("Sharpe Ratio", performanceMetric.calculate_sharpe_ratio(
                        df['cumulative_pnl'].diff(periods = 1) / df['total_value'])),
                    create_performance_card("Maximum Drawdown", performanceMetric.calculate_max_drawdown(df['total_value'])),
                ]
            ),
        html.Br(),
        dmc.Title(f"Equity Curve", order=1),
        html.Br(),
        dmc.Divider(size="md"),
        html.Br(),
        dmc.LineChart(
            h=300,
            dataKey="Date",
            data=data,
            withLegend=True,
            series=[
                {"name": "total_value", "color": "indigo.6"},
            ],
            curveType="linear",
            gridAxis="xy",
            tickLine="xy",
            xAxisLabel="Date",
            yAxisLabel="Equity",
            withDots=False,
            xAxisProps={"angle": -20},
            legendProps={"verticalAlign": "bottom", "height": 50},
            lineChartProps={"syncId": "equity-curve"},
        ),
        html.Br(),
        dmc.Title(f"Daily Profit & Loss Curve", order=1),
        html.Br(),
        dmc.Divider(size="md"),
        html.Br(),
        dmc.LineChart(
            h=300,
            dataKey="Date",
            data=data,
            withLegend=True,
            series=[
                {"name": "daily pnl returns", "color": "teal.6"},
            ],
            curveType="linear",
            tickLine="xy",
            gridAxis="xy",
            xAxisLabel="Date",
            yAxisLabel="PNL Returns",
            withDots=False,
            xAxisProps={"angle": -20},
            legendProps={"verticalAlign": "bottom", "height": 50},
            lineChartProps={"syncId": "equity-curve"},
        )
        # html.H5(filename),
        # html.H6(datetime.datetime.fromtimestamp(date)),
    ]
    )

@callback(Output('output-data-upload', 'children'),
            Input('upload-data', 'contents'),
            State('upload-data', 'filename'),
            State('upload-data', 'last_modified'))
def update_output(list_of_contents, list_of_names, list_of_dates):
    if list_of_contents is not None:
        children = [
            parse_contents(c, n, d) for c, n, d in
            zip(list_of_contents, list_of_names, list_of_dates)]
        return children