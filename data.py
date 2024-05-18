import pandas as pd
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


stats_side = stats[
    [
        "match_id",
        "radiant_win",
        "localized_name",
        "duration",
        "start_date",
    ]
]
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
    [
        "match_id",
        "radiant_win",
        "localized_name",
        "win_r",
        "win_d",
        "duration",
        "start_date",
    ]
]
winners_matches["is_my_win"] = (
    (winners_matches["radiant_win"] & (winners_matches["win_r"] == 1))
    | ((~winners_matches["radiant_win"]) & (winners_matches["win_d"] == 1))
).astype(int)
winners_matches = winners_matches[
    ["match_id", "is_my_win", "localized_name", "radiant_win", "duration", "start_date"]
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


# Винрейт по длительности матча

stats_by_duration = winners_matches
stats_by_duration["duration"] = stats_by_duration["duration"] / 60
stats_by_duration["category"] = pd.cut(
    stats_by_duration["duration"],
    bins=[0, 30, 40, 50, float("inf")],
    labels=["<30", "30-40", "40-50", "50<"],
    include_lowest=True,
)
stats_by_duration = stats_by_duration[
    ["match_id", "is_my_win", "localized_name", "category"]
]
stats_by_duration = (
    stats_by_duration.groupby(["localized_name", "category"], observed=True)[
        "is_my_win"
    ]
    .sum()
    .reset_index()
)

# ИНДИКАТОРЫ
# winrate по героям
winrate_by_hero = winners_matches[["match_id", "is_my_win", "localized_name"]]
winrate_by_hero = winrate_by_hero.groupby("localized_name").agg(
    {"match_id": "count", "is_my_win": "sum"}
)
winrate_by_hero["winrate"] = (
    winrate_by_hero["is_my_win"] / winrate_by_hero["match_id"]
) * 100
winrate_by_hero = winrate_by_hero.reset_index()[["localized_name", "winrate"]]


# Среднее время матча
avg_duration_game = stats[["match_id", "duration", "start_date"]].copy()
avg_duration_game["duration"] = avg_duration_game["duration"] / 60
avg_duration_game["start_date"] = pd.to_datetime(avg_duration_game["start_date"])
avg_duration_game["month"] = avg_duration_game["start_date"].dt.month
avg_duration_game = avg_duration_game.groupby("month").agg({"duration": "mean"})

# Среднее КДА

common_kda = stats[["start_date", "kda"]].copy()
common_kda["start_date"] = pd.to_datetime(common_kda["start_date"])
common_kda["month"] = common_kda["start_date"].dt.month
common_kda_last_month = common_kda[common_kda["month"] != 12]
common_kda = common_kda.groupby("month").agg({"kda": "mean"})
common_kda_last_month = common_kda_last_month.groupby("month").agg({"kda": "mean"})


# Общий винрейт

common_winrate = winners_matches.copy()
common_winrate["start_date"] = pd.to_datetime(common_winrate["start_date"])
common_winrate["month"] = common_winrate["start_date"].dt.month
common_winrate = common_winrate[["is_my_win", "month"]]
common_winrate = (
    common_winrate.groupby("month")["is_my_win"].agg(["count", "sum"]).reset_index()
)

common_winrate_last_month = common_winrate[common_winrate["month"] != 12]

common_winrate["win_percentage"] = (
    common_winrate["sum"] / common_winrate["count"]
) * 100
common_winrate = common_winrate.reset_index()
common_winrate = common_winrate.reset_index()


common_winrate_last_month["win_percentage"] = (
    common_winrate["sum"] / common_winrate["count"]
) * 100


stats_kills = (
    stats[["localized_name", "kills"]]
    .groupby("localized_name")
    .agg({"kills": "sum"})
    .reset_index()
)
stats_assists = (
    stats[["localized_name", "assists"]]
    .groupby("localized_name")
    .agg({"assists": "sum"})
    .reset_index()
)
stats_deaths = (
    stats[["localized_name", "deaths"]]
    .groupby("localized_name")
    .agg({"deaths": "sum"})
    .reset_index()
)
# print(stats)
