from dash import Dash, html, dcc, callback, Output, Input
import plotly.express as px
import pandas as pd

from app import app
from data import stats_kda, stats_side, stats_by_duration


@callback(Output("graph_kda", "figure"), Input("dropdown-selection", "value"))
def update_graph(value):
    print(stats_kda)
    df = stats_kda[stats_kda.localized_name == value]

    return px.line(df, x="start_date", y="kda")


@callback(Output("graph_side", "figure"), Input("dropdown-selection", "value"))
def update_graph(value):
    print(stats_by_duration)
    df = stats_by_duration[stats_by_duration.localized_name == value]

    return px.line(df, x="category", y="is_my_win")


@callback(Output("graph_category", "figure"), Input("dropdown-selection2", "value"))
def update_histogram(value):
    df = stats_by_duration[stats_by_duration.localized_name] == value

    return px.histogram(
        df,
        x="category",
        y="is_my_win",
        color="category",
        title="Количество is_my_win по категориям",
    )


if __name__ == "__main__":
    app.run(debug=True)