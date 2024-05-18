from dash import callback, Output, Input, State
import plotly.express as px
import pandas as pd
import plotly.graph_objects as go


from app import app
from data import stats_kda, stats_by_duration, stats_side, winrate_by_hero


@callback(Output("graph_kda", "figure"), Input("dropdown-selection", "value"))
def update_graph(value):
    df = stats_kda[stats_kda.localized_name == value]

    return px.line(
        df,
        x="start_date",
        y="kda",
        title="КДА по героям",
    )


@callback(Output("graph_side", "figure"), Input("dropdown-selection1", "value"))
def update_graph(value):
    df = stats_side[stats_side.localized_name == value]

    return px.bar(
        df,
        x="win_side",
        y="value_win_side",
        title="Winrate по сторонам (Светлая, Темная)",
    )


@callback(Output("graph_category", "figure"), Input("dropdown-selection2", "value"))
def update_histogram(value):
    df = stats_by_duration[stats_by_duration.localized_name == value]
    return px.bar(
        df,
        x="category",
        y="is_my_win",
        color="category",
        title="Количество побед по категориям",
    )


@callback(
    Output("indicator_winrate_by_hero", "figure"),
    Input("dds_for_winrate_by_hero", "value"),
)
def update_histogram(value):
    indicator_winrate_by_hero = go.Figure(
        go.Indicator(
            mode="number+delta",
            value=winrate_by_hero[winrate_by_hero["localized_name"] == value][
                "winrate"
            ].mean(),
            number={"suffix": "%"},
            domain={"y": [0, 1], "x": [0.25, 0.25]},
            title={
                "text": "Winrate by Hero",
            },
        )
    )
    indicator_winrate_by_hero.update_layout(height=250)

    return indicator_winrate_by_hero


@callback(
    Output("change_photo_hero", "src"),
    Input("dds_for_winrate_by_hero", "value"),
)
def change_photo_hero(hero):
    return f"https://ru.dotabuff.com/assets/heroes/{hero.lower().replace(' ', '-')}.jpg"


@app.callback(
    Output("indicators", "is_open"),
    Output("kills_assists_deaths_graph", "is_open"),
    Output("indicator_button", "n_clicks"),
    Output("kills_assists_deaths_button", "n_clicks"),
    [Input("indicator_button", "n_clicks")],
    [Input("kills_assists_deaths_button", "n_clicks")],
    [State("indicators", "is_open")],
    [State("kills_assists_deaths_graph", "is_open")],
)
def toggle_collapse3(
    indicators_btn_pressed, kda_btn_pressed, is_indicators_open, is_kda_open
):
    if indicators_btn_pressed:
        if is_indicators_open:
            return False, False, 0, 0
        return True, False, 0, 0
    if kda_btn_pressed:
        if is_kda_open:
            return False, False, 0, 0
        return False, True, 0, 0
    return False, False, 0, 0


if __name__ == "__main__":
    app.run(debug=True)
