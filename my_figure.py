import plotly.express as px


from data import number_heros

fig = px.pie(
    number_heros,
    values="match_id_count",
    names="localized_name",
    title="Процент сыгранных матчей на данном герое",
)
