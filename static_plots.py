import plotly.express as px
import plotly.graph_objects as go


from data import (
    number_heros,
    common_winrate,
    common_winrate_last_month,
    common_kda,
    common_kda_last_month,
    stats_kills,
    stats_assists,
    stats_deaths,
)

percent_matches_by_hero = px.pie(
    number_heros,
    values="match_id_count",
    names="localized_name",
    title="Процент сыгранных матчей на данном герое",
)


indicator_winrate = go.Figure(
    go.Indicator(
        mode="number+delta",
        value=common_winrate["win_percentage"].mean(),
        delta={
            "position": "top",
            "reference": common_winrate_last_month["win_percentage"].mean(),
            "relative": True,
        },
        domain={"x": [0, 1], "y": [0, 1]},
        title={"text": "Winrate"},
    )
)

indicator_winrate.update_layout(height=250)

indicator_kda = go.Figure(
    go.Indicator(
        mode="number+delta",
        value=common_kda["kda"].mean(),
        delta={
            "position": "top",
            "reference": common_kda_last_month["kda"].mean(),
            "relative": True,
        },
        domain={"x": [0, 1], "y": [0, 1]},
        title={"text": "KDA"},
    )
)
indicator_kda.update_layout(height=250)


fig_kills_assists_deaths = go.Figure()

fig_kills_assists_deaths.add_trace(
    go.Scatter(
        x=stats_kills["localized_name"],
        y=stats_kills["kills"],
        mode="lines+markers",
        name="Убийства",
        line=dict(color="red", width=2),
        marker=dict(size=6, symbol="circle", color="black"),
        yaxis="y2",
    )
)
fig_kills_assists_deaths.add_trace(
    go.Scatter(
        x=stats_assists["localized_name"],
        y=stats_assists["assists"],
        mode="lines+markers",
        name="Помощь",
        line=dict(color="green", width=2),
        marker=dict(size=6, symbol="circle", color="black"),
        yaxis="y2",
    )
)
fig_kills_assists_deaths.add_trace(
    go.Scatter(
        x=stats_deaths["localized_name"],
        y=stats_deaths["deaths"],
        mode="lines+markers",
        name="Смерти",
        line=dict(color="blue", width=2),
        marker=dict(size=6, symbol="circle", color="black"),
        yaxis="y2",
    )
)
fig_kills_assists_deaths.update_layout(
    title="Убийства, смерти и помощь по героям",
    xaxis_title="Герой",
    font=dict(family="Arial, sans-serif", size=9, color="darkgray"),
    yaxis_title="Количество убийств",
)
