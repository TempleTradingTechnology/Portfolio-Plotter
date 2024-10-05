import dash
from dash import html, dcc, html, dash_table, Input, Output, State, callback
import dash_mantine_components as dmc
import dash_loading_spinners as dls
import pandas as pd
import base64
import datetime
import io

from utils import performanceMetric

from components.performanceCard import create_performance_card

PNL_HEADER = "Date,cash,equity_exposure,total_value,cumulative_pnl,daily pnl returns"
TRADE_HISTORY_HEADER = "Ticker,Shares With Sign,Entry Date,Entry Price,Exit Date,Exit Price,Status,PnL"

docUpload = dcc.Upload(
    id='upload-data',
    children= html.Div([
            dmc.Flex([
                dmc.Text('Click Here ', size="lg", fw=700),
                dmc.Text('to upload your files or drag and drop.', size="lg", fw=500),
            ],
            gap="xs"),
            html.Div([
                'Supported files: .xls, .csv'
            ])
        ]),
    className='upload-box',
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

def parse_contents(list_of_contents, list_of_names, list_of_dates):

    pnl_df = None
    trade_history_df = None

    for contents, filename, data in zip(list_of_contents, list_of_names, list_of_dates):

        content_type, content_string = contents.split(',')

        decoded = base64.b64decode(content_string)

        try:
            if 'csv' in filename:

                if "pnl" in filename:

                    # Assume that the user uploaded a CSV file
                    pnl_df = pd.read_csv(
                        io.StringIO(decoded.decode('utf-8')))

                    if pnl_df.columns.tolist() != PNL_HEADER.split(','):
                        return html.Div([
                            dmc.Alert("There were no PNL file found",
                                                    title="File Error",
                                                    color="red",
                                                    withCloseButton=True)])

                elif "trade_history" in filename:
                    # Assume that the user uploaded a CSV file
                    trade_history_df = pd.read_csv(
                        io.StringIO(decoded.decode('utf-8')))

                    if trade_history_df.columns.tolist() != TRADE_HISTORY_HEADER.split(','):
                        return html.Div([
                            dmc.Alert("There were no Trade History file found",
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

    pnl_df.fillna(0, inplace=True)
    pnl_data = pnl_df.to_dict(orient='records')

    return (html.Div([
        dmc.Title(f"File Name: {filename}", order=1),
        html.Br(),
        dmc.Title(f"Performance Metrics", order=1),
        html.Br(),
        dmc.Divider(size="md"),
        html.Br(),
        dmc.Group(
                align={"sm": "center"},
                children=[
                    create_performance_card("Cumulative Return",
                    100 * pnl_df['cumulative_pnl'].iloc[-1] / 1000000,
                    number_format_spec="{:.0f}%"),

                    create_performance_card("Sharpe Ratio", performanceMetric.calculate_sharpe_ratio(
                        pnl_df['cumulative_pnl'].diff(periods = 1) / pnl_df['total_value'] )),

                    create_performance_card("Maximum Drawdown",
                    performanceMetric.calculate_max_drawdown(pnl_df['total_value']), number_format_spec="{:.4%}" ),
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
            data=pnl_data,
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
            data=pnl_data,
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
        ),
        html.Br(),
        dmc.Title(f"PNL Breakdown", order=1),
        html.Br(),
        dmc.Tabs(
        [
            dmc.TabsList(
                [
                    dmc.TabsTab("Ticker", value="Ticker"),
                    dmc.TabsTab("Year", value="Year"),
                ]
            ),
            html.Br(),
            dmc.TabsPanel(create_graph(trade_history_df, key="Ticker"), value="Ticker"),
            dmc.TabsPanel(create_graph(trade_history_df, key="Exit Year"), value="Year"),
        ],
            color="violet.6",
            value="Ticker"
        ),
        ]
    ))

@callback(Output('output-data-upload', 'children'),
            Input('upload-data', 'contents'),
            State('upload-data', 'filename'),
            State('upload-data', 'last_modified'))
def update_output(list_of_contents, list_of_names, list_of_dates):

    if list_of_contents is not None:
        children = parse_contents(list_of_contents, list_of_names, list_of_dates)

        return children

def create_graph(df, key):

    df = df.dropna()
    data = []

    if key == "Ticker":
        df["Ticker"] = df["Ticker"].str.upper()
        for k, v in df.groupby(["Ticker"])["PnL"]:
            data.append({"Ticker": list(k)[0], "PnL": v.sum()})

    elif key == "Exit Year":
        df["Exit Year"] = df.apply(lambda x: str(x["Exit Date"]).split("-")[0], axis=1)

        for k, v in df.groupby(["Exit Year"])["PnL"]:
            data.append({"Exit Year": list(k)[0], "PnL": v.sum()})


    return dmc.BarChart(
        h=300,
        dataKey=key,
        data=data,
        series=[
            {"name": "PnL", "color": "violet.6"},
        ],
    )