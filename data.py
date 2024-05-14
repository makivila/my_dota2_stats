import pandas as pd
import plotly.express as px
import requests


user = requests.get("https://api.opendota.com/api/players/1253662502")
matches = requests.get("https://api.opendota.com/api/players/1253662502/matches")
matches_is_rediant_win = requests.get(
    "https://api.opendota.com/api/players/1253662502/matches?is_radiant=1&win=1"
)
matches_is_dire_win = requests.get(
    "https://api.opendota.com/api/players/1253662502/matches?is_radiant=0&win=1"
)
heros = requests.get("https://api.opendota.com/api/heroes")


df_matches = pd.json_normalize(matches.json())
matches_is_rediant_win = pd.json_normalize(matches_is_rediant_win.json())
matches_is_dire_win = pd.json_normalize(matches_is_dire_win.json())
df_heros = pd.json_normalize(heros.json())
# Соединила таблицу с матчами и героями
stats = pd.merge(df_matches, df_heros, left_on="hero_id", right_on="id")

# Выбрала нужные поля из таблиц
stats = stats[
    [
        "match_id",
        "radiant_win",
        "duration",
        "hero_id",
        "kills",
        "deaths",
        "assists",
        "localized_name",
        "attack_type",
        "roles",
        "start_time",
    ]
]
# Проверила на наличие пустых значений.Их нет.
stats.isna().sum()

# Количество игр на герое
number_heros = stats.groupby("localized_name").agg({"match_id": "nunique"})
number_heros = number_heros.rename(columns={"match_id": "match_id_count"})
# Выберем только тех героев, на которых я сыграла более 1 раза

number_heros = number_heros[number_heros["match_id_count"] > 5].reset_index()

# Показатели КДА по каждому герою

# stats["kda"] = (stats["kills"] + stats["assists"]) / stats["deaths"]
stats["kda"] = (stats["kills"] + stats["assists"]) / (stats["deaths"].replace(0, 1))
stats["start_date"] = pd.to_datetime(stats.start_time, unit="s")
stats["start_date"] = stats["start_date"].dt.date
# Пример вывода для наглядности
stats_kda = stats[["localized_name", "kda", "start_date"]]
stats_kda = (
    stats_kda.groupby(["start_date", "localized_name"])
    .agg({"kda": "mean"})
    .reset_index()
)

# За какую строну (Тьма, Свет) я выигрываю чаще всего, по героям


stats_side = stats[["match_id", "radiant_win", "localized_name", "duration"]]
matches_is_rediant_win["win_r"] = 1
matches_is_dire_win["win_d"] = 1
winners_matches = pd.merge(
    stats_side,
    matches_is_rediant_win[["match_id", "win_r"]],
    on="match_id",
    how="left",
)
winners_matches = pd.merge(
    winners_matches,
    matches_is_dire_win[["match_id", "win_d"]],
    on="match_id",
    how="left",
)

winners_matches[
    ["match_id", "radiant_win", "localized_name", "win_r", "win_d", "duration"]
]
winners_matches["is_my_win"] = (
    (winners_matches["radiant_win"] & (winners_matches["win_r"] == 1))
    | ((~winners_matches["radiant_win"]) & (winners_matches["win_d"] == 1))
).astype(int)
winners_matches = winners_matches[
    ["match_id", "is_my_win", "localized_name", "radiant_win", "duration"]
].reset_index()
stats_side = (
    winners_matches[winners_matches["is_my_win"] == 1]
    .groupby("localized_name")
    .agg({"radiant_win": lambda x: (x == True).sum(), "is_my_win": "count"})
)
stats_side.columns = ["radiant_win_count", "total_win_count"]
stats_side["radiant_win_percent"] = (
    stats_side["radiant_win_count"] / stats_side["total_win_count"]
) * 100
stats_side["dire_win_percent"] = 100 - stats_side["radiant_win_percent"]

stats_side = stats_side.reset_index()[
    ["localized_name", "radiant_win_percent", "dire_win_percent"]
]

stats_side = pd.melt(
    stats_side,
    id_vars=["localized_name"],
    var_name="win_side",
    value_name="value_win_side",
)

print(stats_side)
# Винрейт по длительности матча

stats_by_duration = winners_matches
stats_by_duration["duration"] = stats_by_duration["duration"] / 60
stats_by_duration["category"] = pd.cut(
    stats_by_duration["duration"],
    bins=[0, 30, 40, 50, float("inf")],
    labels=[1, 2, 3, 4],
    include_lowest=True,
)
stats_by_duration = stats_by_duration[
    ["match_id", "is_my_win", "localized_name", "category"]
]
stats_by_duration = (
    stats_by_duration.groupby(["localized_name", "category"])["is_my_win"]
    .sum()
    .reset_index()
)
