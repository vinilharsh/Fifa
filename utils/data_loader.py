import os
import streamlit as st
import pandas as pd

DATA_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "data")
SEASONS_DIR = os.path.join(DATA_DIR, "seasons")
SHOOTING_DIR = os.path.join(DATA_DIR, "shooting")

SEASON_ORDER = [
    "2015/2016", "2016/2017", "2017/2018", "2018/2019",
    "2019/2020", "2020/2021", "2021/2022", "2022/2023",
]

DISPLAY_LABELS = {
    "xG/expexted season": "xG (Season)",
    "xA/expected season": "xA (Season)",
    "xG/per 90": "xG/90",
    "xA/per 90": "xA/90",
    "Gls/per 90": "Goals/90",
    "Ast/per 90": "Assists/90",
}


def get_display_label(col_name):
    return DISPLAY_LABELS.get(col_name, col_name)


def display_rename(df):
    return df.rename(columns=DISPLAY_LABELS)


@st.cache_data
def load_player_data():
    return pd.read_csv(os.path.join(DATA_DIR, "player.csv"))


@st.cache_data
def load_shooting_data():
    return pd.read_csv(os.path.join(DATA_DIR, "Shooting.csv"))


@st.cache_data
def load_shooting_season(filename):
    return pd.read_csv(os.path.join(SHOOTING_DIR, filename))


def filter_by_season(df, season):
    return df[df["Season"] == season]


def clean_minutes_column(df):
    df = df.copy()
    if df["Min"].dtype == object:
        df["Min"] = df["Min"].str.replace(",", "").astype(float)
    return df


def normalize_position(pos):
    if pd.isna(pos):
        return "Unknown"
    pos = pos.strip()
    if "," in pos:
        return pos.split(",")[0].strip()
    for primary in ["GK", "DF", "MF", "FW"]:
        if pos.startswith(primary):
            return primary
    return pos
