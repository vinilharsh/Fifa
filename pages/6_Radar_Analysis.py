import streamlit as st
from soccerplots.radar_chart import Radar
import pandas as pd
import plotly.graph_objects as go
from utils.data_loader import load_shooting_season, load_shooting_data
from utils.theme import inject_custom_css, apply_plotly_theme

st.set_page_config(page_title="Radar Analysis", page_icon="🎯", layout="wide")
inject_custom_css()

RADAR_PARAMS = [
    "Gls", "Sh", "SoT", "SoT%", "Sh/90", "SoT/90", "G/Sh",
    "G/SoT", "Dist", "xG", "npxG", "npxG/Sh", "G-xG", "np:G-xG",
]

DROP_COLS = ["Rk", "Nation", "Pos", "Squad", "Age", "Born", "90s", "FK", "PK", "PKatt", "Season"]

FILLNA_COLS_BY_POS = ["SoT%", "G/Sh", "G/SoT", "Dist", "npxG/Sh"]

FALLBACK_COLS = ["Dist", "xG", "npxG", "G-xG", "np:G-xG", "npxG/Sh"]

SEASON_CONFIG = {
    "2022/23": {
        "csv": "Shooting(2020-21).csv",
        "players": {
            "Lionel Messi": "Barcelona",
            "Karim Benzema": "Real Madrid",
            "Gerard Moreno": "Villarreal",
            "Luis Suárez": "Atletico Madrid",
            "Youssef En-Nesyri": "Sevilla",
            "Alexander Isak": "Real Sociedad",
            "Iago Aspas": "Celta Vigo",
            "Antoine Griezmann": "Barcelona",
            "José Luis Morales": "Levante",
            "Rafa Mir": "Wolves",
        },
    },
    "2021/22": {
        "csv": "Shooting(2021-22).csv",
        "players": {
            "Karim Benzema": "Real Madrid",
            "Iago Aspas": "Celta Vigo",
            "Vinicius Júnior": "Real Madrid",
            "Raúl de Tomás": "Espanyol",
            "Juanmi": "Betis",
            "Enes Ünal": "Getafe",
            "Joselu": "Alavés",
            "José Luis Morales": "Levante",
            "Ángel Correa": "Atlético Madrid",
            "Memphis Depay": "Barcelona",
        },
    },
    "2020/21": {
        "csv": "Shooting(2020-21).csv",
        "players": {
            "Lionel Messi": "Barcelona",
            "Karim Benzema": "Real Madrid",
            "Gerard Moreno": "Villarreal",
            "Luis Suárez": "Atletico Madrid",
            "Youssef En-Nesyri": "Sevilla",
            "Alexander Isak": "Real Sociedad",
            "Iago Aspas": "Celta Vigo",
            "Antoine Griezmann": "Barcelona",
            "José Luis Morales": "Levante",
            "Rafa Mir": "Wolves",
        },
    },
    "2019/20": {
        "csv": "Shooting(2019-20).csv",
        "players": {
            "Lionel Messi": "Barcelona",
            "Karim Benzema": "Real Madrid",
            "Gerard Moreno": "Villarreal",
            "Luis Suárez": "Barcelona",
            "Raúl García": "Athletic Club",
            "Iago Aspas": "Celta Vigo",
            "Lucas Ocampos": "Sevilla",
            "Ante Budimir": "Mallorca",
            "Álvaro Morata": "Atlético Madrid",
            "Santi Cazorla": "Villarreal",
        },
    },
    "2018/19": {
        "csv": "Shooting(2018-19).csv",
        "extra_fillna": True,
        "players": {
            "Lionel Messi": "Barcelona",
            "Karim Benzema": "Real Madrid",
            "Gerard Moreno": "Villarreal",
            "Luis Suárez": "Atletico Madrid",
            "Youssef En-Nesyri": "Sevilla",
            "Alexander Isak": "Real Sociedad",
            "Iago Aspas": "Celta Vigo",
            "Antoine Griezmann": "Barcelona",
            "José Luis Morales": "Levante",
            "Rafa Mir": "Wolves",
        },
    },
    "2017/18": {
        "csv": "Shooting(2017-18).csv",
        "extra_fillna": True,
        "players": {
            "Lionel Messi": "Barcelona",
            "Cristiano Ronaldo": "Real Madrid",
            "Luis Suárez": "Barcelona",
            "Iago Aspas": "Celta Vigo",
            "Cristhian Stuani": "Girona",
            "Antoine Griezmann": "Atlético Madrid",
            "Maxi Gómez": "Celta Vigo",
            "Gareth Bale": "Real Madrid",
            "Gerard Moreno": "Espanyol",
            "Rodrigo": "Valencia",
        },
    },
    "2016/17": {
        "csv": "Shooting(2016-17).csv",
        "extra_fillna": True,
        "use_fallback": True,
        "players": {
            "Lionel Messi": "Barcelona",
            "Luis Suárez": "Barcelona",
            "Cristiano Ronaldo": "Real Madrid",
            "Iago Aspas": "Celta Vigo",
            "Aritz Aduriz": "Athletic Club",
            "Antoine Griezmann": "Atlético Madrid",
            "Álvaro Morata": "Real Madrid",
            "Sandro Ramírez": "Málaga",
            "Rubén Castro": "Betis",
            "Gerard Moreno": "Espanyol",
        },
    },
    "2015/16": {
        "csv": "Shooting(2015-16).csv",
        "extra_fillna": True,
        "use_fallback": True,
        "players": {
            "Luis Suárez": "Barcelona",
            "Cristiano Ronaldo": "Real Madrid",
            "Lionel Messi": "Barcelona",
            "Karim Benzema": "Real Madrid",
            "Neymar": "Barcelona",
            "Antoine Griezmann": "Atlético Madrid",
            "Aritz Aduriz": "Athletic Club",
            "Gareth Bale": "Real Madrid",
            "Rubén Castro": "Betis",
            "Borja Bastón": "Eibar",
        },
    },
}


def prepare_shooting_data(config):
    df = load_shooting_season(config["csv"]).copy()
    for col in FILLNA_COLS_BY_POS:
        df[col] = df[col].fillna(df.groupby("Pos")[col].transform("mean"))
    if config.get("extra_fillna"):
        df["G/SoT"] = df["G/SoT"].fillna(df.groupby("Squad")["G/SoT"].transform("mean"))
    if config.get("use_fallback"):
        fallback = load_shooting_data()
        for col in FALLBACK_COLS:
            df[col] = df[col].fillna(fallback[col].mean())
    df = df.drop(columns=[c for c in DROP_COLS if c in df.columns])
    return df


def calculate_ranges(df):
    ranges = []
    for param in RADAR_PARAMS:
        lo = df[param].min() * 0.95
        hi = df[param].max() * 1.05
        ranges.append((lo, hi))
    return ranges


def plot_single_radar(df, player, subtitle, ranges):
    player_data = df[df["Player"] == player]
    values = player_data.iloc[0].values[1:].tolist()
    title = {
        "title_name": player,
        "title_color": "#000000",
        "subtitle_name": subtitle,
        "subtitle_color": "#B6282F",
        "title_name_2": "Radar Chart",
        "subtitle_name_2": "FW",
        "subtitle_color_2": "#B6282F",
        "title_fontsize": 18,
        "subtitle_fontsize": 15,
    }
    radar = Radar(label_fontsize=12, range_fontsize=7.5)
    fig, ax = radar.plot_radar(
        ranges=ranges, params=RADAR_PARAMS, values=[values],
        radar_color=["orange"], alphas=[0.4], title=title, compare=True,
    )
    st.pyplot(fig)


def plot_comparison_radar(df, player1, player2, subtitles, ranges):
    data1 = df[df["Player"] == player1]
    data2 = df[df["Player"] == player2]
    values1 = data1.iloc[0].values[1:].tolist()
    values2 = data2.iloc[0].values[1:].tolist()
    title = {
        "title_name": player1,
        "title_color": "#000000",
        "subtitle_name": subtitles[player1],
        "subtitle_color": "#B6282F",
        "title_name_2": player2,
        "subtitle_name_2": subtitles[player2],
        "subtitle_color_2": "#B6282F",
        "title_fontsize": 18,
        "subtitle_fontsize": 15,
    }
    radar = Radar(label_fontsize=12, range_fontsize=7.5)
    fig, ax = radar.plot_radar(
        ranges=ranges, params=RADAR_PARAMS,
        values=[values1, values2],
        radar_color=["Red", "Blue"], alphas=[0.75, 0.6],
        title=title, compare=True,
    )
    st.pyplot(fig)


def plot_bar_comparison(df, player1, player2, subtitles):
    data1 = df[df["Player"] == player1].iloc[0]
    data2 = df[df["Player"] == player2].iloc[0]

    vals1 = [data1[p] for p in RADAR_PARAMS]
    vals2 = [data2[p] for p in RADAR_PARAMS]

    fig = go.Figure()
    fig.add_trace(go.Bar(
        y=RADAR_PARAMS, x=vals1, name=f"{player1} ({subtitles[player1]})",
        orientation="h", marker_color="rgba(231, 76, 60, 0.7)",
        text=[f"{v:.1f}" for v in vals1], textposition="auto",
    ))
    fig.add_trace(go.Bar(
        y=RADAR_PARAMS, x=vals2, name=f"{player2} ({subtitles[player2]})",
        orientation="h", marker_color="rgba(52, 152, 219, 0.7)",
        text=[f"{v:.1f}" for v in vals2], textposition="auto",
    ))
    fig.update_layout(
        title=f"{player1} vs {player2} — Stat Comparison",
        barmode="group",
        yaxis=dict(categoryorder="array", categoryarray=RADAR_PARAMS),
        height=600,
    )
    apply_plotly_theme(fig)
    st.plotly_chart(fig, use_container_width=True)


# --- App ---

st.header("🎯 Radar Analysis")
st.caption("Compare player shooting profiles using radar charts and bar comparisons.")

st.sidebar.header("Filters")
selected_year = st.sidebar.selectbox("Select Year", list(SEASON_CONFIG.keys()))

config = SEASON_CONFIG[selected_year]
player_subtitles = config["players"]

with st.spinner("Preparing radar data..."):
    df = prepare_shooting_data(config)
    ranges = calculate_ranges(df)

tab1, tab2, tab3 = st.tabs(["Single Player", "Player Comparison", "Bar Comparison"])

with tab1:
    selected_player = st.selectbox("Select a player:", list(player_subtitles.keys()))

    player_data = df[df["Player"] == selected_player].iloc[0]
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Goals", f"{player_data['Gls']:.0f}")
    col2.metric("Shots", f"{player_data['Sh']:.0f}")
    col3.metric("xG", f"{player_data['xG']:.1f}")
    col4.metric("Shot Accuracy", f"{player_data['SoT%']:.1f}%")

    st.divider()
    plot_single_radar(df, selected_player, player_subtitles[selected_player], ranges)

with tab2:
    col1, col2 = st.columns(2)
    selected_player1 = col1.selectbox("Select Player 1", list(player_subtitles.keys()))
    selected_player2 = col2.selectbox("Select Player 2", list(player_subtitles.keys()))

    p1_data = df[df["Player"] == selected_player1].iloc[0]
    p2_data = df[df["Player"] == selected_player2].iloc[0]

    c1, c2, c3, c4 = st.columns(4)
    c1.metric(f"{selected_player1} Goals", f"{p1_data['Gls']:.0f}")
    c2.metric(f"{selected_player1} xG", f"{p1_data['xG']:.1f}")
    c3.metric(f"{selected_player2} Goals", f"{p2_data['Gls']:.0f}")
    c4.metric(f"{selected_player2} xG", f"{p2_data['xG']:.1f}")

    st.divider()
    plot_comparison_radar(df, selected_player1, selected_player2, player_subtitles, ranges)

with tab3:
    st.markdown("**Interactive bar comparison** — easier to read exact values than radar charts.")
    col1, col2 = st.columns(2)
    bar_player1 = col1.selectbox("Player 1", list(player_subtitles.keys()), key="bar_p1")
    bar_player2 = col2.selectbox("Player 2", list(player_subtitles.keys()), key="bar_p2")
    plot_bar_comparison(df, bar_player1, bar_player2, player_subtitles)
