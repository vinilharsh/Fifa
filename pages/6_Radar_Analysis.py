import streamlit as st
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


def normalize_values(df):
    """Normalize all radar params to 0-100 scale for comparable radar display."""
    normed = df.copy()
    for p in RADAR_PARAMS:
        pmin = df[p].min()
        pmax = df[p].max()
        if pmax - pmin > 0:
            normed[p] = (df[p] - pmin) / (pmax - pmin) * 100
        else:
            normed[p] = 50
    return normed


def plot_single_radar(df_norm, df_raw, player, subtitle):
    player_norm = df_norm[df_norm["Player"] == player].iloc[0]
    player_raw = df_raw[df_raw["Player"] == player].iloc[0]

    values_norm = [player_norm[p] for p in RADAR_PARAMS]
    values_raw = [player_raw[p] for p in RADAR_PARAMS]
    hover_text = [f"{p}: {v:.2f}" for p, v in zip(RADAR_PARAMS, values_raw)]

    fig = go.Figure()
    fig.add_trace(go.Scatterpolar(
        r=values_norm + [values_norm[0]],
        theta=RADAR_PARAMS + [RADAR_PARAMS[0]],
        fill="toself",
        fillcolor="rgba(231, 76, 60, 0.25)",
        line=dict(color="#E74C3C", width=2),
        name=player,
        text=hover_text + [hover_text[0]],
        hoverinfo="text",
    ))
    fig.update_layout(
        title=dict(text=f"{player} — {subtitle}", font=dict(size=18)),
        polar=dict(
            bgcolor="rgba(0,0,0,0)",
            radialaxis=dict(visible=True, range=[0, 100], showticklabels=False, gridcolor="rgba(128,128,128,0.2)"),
            angularaxis=dict(gridcolor="rgba(128,128,128,0.2)", linecolor="rgba(128,128,128,0.3)"),
        ),
        height=550,
    )
    apply_plotly_theme(fig)
    st.plotly_chart(fig, use_container_width=True)


def plot_comparison_radar(df_norm, df_raw, player1, player2, subtitles):
    p1_norm = df_norm[df_norm["Player"] == player1].iloc[0]
    p2_norm = df_norm[df_norm["Player"] == player2].iloc[0]
    p1_raw = df_raw[df_raw["Player"] == player1].iloc[0]
    p2_raw = df_raw[df_raw["Player"] == player2].iloc[0]

    v1 = [p1_norm[p] for p in RADAR_PARAMS]
    v2 = [p2_norm[p] for p in RADAR_PARAMS]
    h1 = [f"{p}: {p1_raw[p]:.2f}" for p in RADAR_PARAMS]
    h2 = [f"{p}: {p2_raw[p]:.2f}" for p in RADAR_PARAMS]

    fig = go.Figure()
    fig.add_trace(go.Scatterpolar(
        r=v1 + [v1[0]], theta=RADAR_PARAMS + [RADAR_PARAMS[0]],
        fill="toself", fillcolor="rgba(231, 76, 60, 0.2)",
        line=dict(color="#E74C3C", width=2),
        name=f"{player1} ({subtitles[player1]})",
        text=h1 + [h1[0]], hoverinfo="text",
    ))
    fig.add_trace(go.Scatterpolar(
        r=v2 + [v2[0]], theta=RADAR_PARAMS + [RADAR_PARAMS[0]],
        fill="toself", fillcolor="rgba(52, 152, 219, 0.2)",
        line=dict(color="#3498DB", width=2),
        name=f"{player2} ({subtitles[player2]})",
        text=h2 + [h2[0]], hoverinfo="text",
    ))
    fig.update_layout(
        title=dict(text=f"{player1} vs {player2}", font=dict(size=18)),
        polar=dict(
            bgcolor="rgba(0,0,0,0)",
            radialaxis=dict(visible=True, range=[0, 100], showticklabels=False, gridcolor="rgba(128,128,128,0.2)"),
            angularaxis=dict(gridcolor="rgba(128,128,128,0.2)", linecolor="rgba(128,128,128,0.3)"),
        ),
        height=550,
        legend=dict(x=0.5, y=-0.1, xanchor="center", orientation="h"),
    )
    apply_plotly_theme(fig)
    st.plotly_chart(fig, use_container_width=True)


def plot_bar_comparison(df_raw, player1, player2, subtitles):
    data1 = df_raw[df_raw["Player"] == player1].iloc[0]
    data2 = df_raw[df_raw["Player"] == player2].iloc[0]
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
st.caption("Compare player shooting profiles using interactive radar charts and bar comparisons.")

st.sidebar.header("Filters")
selected_year = st.sidebar.selectbox("Select Year", list(SEASON_CONFIG.keys()))

config = SEASON_CONFIG[selected_year]
player_subtitles = config["players"]

with st.spinner("Preparing radar data..."):
    df_raw = prepare_shooting_data(config)
    df_norm = normalize_values(df_raw)

tab1, tab2, tab3 = st.tabs(["Single Player", "Player Comparison", "Bar Comparison"])

with tab1:
    selected_player = st.selectbox("Select a player:", list(player_subtitles.keys()))
    player_data = df_raw[df_raw["Player"] == selected_player].iloc[0]

    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Goals", f"{player_data['Gls']:.0f}")
    col2.metric("Shots", f"{player_data['Sh']:.0f}")
    col3.metric("xG", f"{player_data['xG']:.1f}")
    col4.metric("Shot Accuracy", f"{player_data['SoT%']:.1f}%")

    st.divider()
    plot_single_radar(df_norm, df_raw, selected_player, player_subtitles[selected_player])

with tab2:
    col1, col2 = st.columns(2)
    selected_player1 = col1.selectbox("Select Player 1", list(player_subtitles.keys()))
    selected_player2 = col2.selectbox("Select Player 2", list(player_subtitles.keys()))

    p1_data = df_raw[df_raw["Player"] == selected_player1].iloc[0]
    p2_data = df_raw[df_raw["Player"] == selected_player2].iloc[0]

    c1, c2, c3, c4 = st.columns(4)
    c1.metric(f"{selected_player1} Goals", f"{p1_data['Gls']:.0f}")
    c2.metric(f"{selected_player1} xG", f"{p1_data['xG']:.1f}")
    c3.metric(f"{selected_player2} Goals", f"{p2_data['Gls']:.0f}")
    c4.metric(f"{selected_player2} xG", f"{p2_data['xG']:.1f}")

    st.divider()
    plot_comparison_radar(df_norm, df_raw, selected_player1, selected_player2, player_subtitles)

with tab3:
    st.markdown("**Interactive bar comparison** — easier to read exact values than radar charts.")
    col1, col2 = st.columns(2)
    bar_player1 = col1.selectbox("Player 1", list(player_subtitles.keys()), key="bar_p1")
    bar_player2 = col2.selectbox("Player 2", list(player_subtitles.keys()), key="bar_p2")
    plot_bar_comparison(df_raw, bar_player1, bar_player2, player_subtitles)
