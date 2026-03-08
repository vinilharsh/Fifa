import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from utils.data_loader import load_player_data, filter_by_season, clean_minutes_column
from utils.theme import apply_plotly_theme, inject_custom_css

st.set_page_config(page_title="Overview", page_icon="📊", layout="wide")
inject_custom_css()

st.header("📊 Season Overview")

with st.spinner("Loading data..."):
    data = load_player_data()
    data = clean_minutes_column(data)

st.sidebar.header("Filters")
selected_season = st.sidebar.selectbox(
    "Select Season", sorted(data["Season"].unique(), reverse=True)
)
filtered_data = filter_by_season(data, selected_season)

col1, col2, col3, col4 = st.columns(4)
col1.metric("Total Goals", int(filtered_data["Gls"].sum()))
col2.metric("Total Assists", int(filtered_data["Ast"].sum()))
col3.metric("Average Age", f"{filtered_data['Age'].mean():.1f}")
col4.metric("Total Players", filtered_data["Player"].nunique())

st.divider()

tab1, tab2, tab3, tab4 = st.tabs(["Distributions", "By Position", "By Squad", "Heatmap"])

with tab1:
    c1, c2 = st.columns(2)
    with c1:
        pos_counts = filtered_data["Pos"].value_counts().reset_index()
        fig = px.bar(
            pos_counts, x="count", y="Pos", orientation="h",
            title="Player Position Distribution",
            text_auto=True,
            color="count", color_continuous_scale="Teal",
        )
        fig.update_layout(
            yaxis=dict(categoryorder="total ascending"),
            coloraxis_showscale=False,
        )
        apply_plotly_theme(fig)
        st.plotly_chart(fig, use_container_width=True)

    with c2:
        nat = filtered_data["Nation"].value_counts().head(20).reset_index()
        nat.columns = ["Nation", "Count"]
        fig = px.treemap(
            nat, path=["Nation"], values="Count",
            title="Player Nationalities (Treemap)",
            color="Count", color_continuous_scale="Sunset",
        )
        fig.update_layout(coloraxis_showscale=False)
        apply_plotly_theme(fig)
        st.plotly_chart(fig, use_container_width=True)

with tab2:
    c1, c2 = st.columns(2)
    with c1:
        scatter = px.scatter(
            filtered_data, x="Gls", y="Ast", color="Pos",
            size="Min", size_max=25,
            hover_data={"Player": True, "Squad": True, "Age": True},
            labels={"Gls": "Goals", "Ast": "Assists"},
            title="Goals vs Assists (bubble size = minutes)",
            color_discrete_map={"FW": "#E74C3C", "MF": "#3498DB", "DF": "#2ECC71", "GK": "#F39C12"},
        )
        apply_plotly_theme(scatter)
        st.plotly_chart(scatter, use_container_width=True)

    with c2:
        avg = filtered_data.groupby("Pos")[["Gls", "Ast"]].mean().reset_index()
        fig = go.Figure()
        fig.add_trace(go.Bar(
            x=avg["Pos"], y=avg["Gls"], name="Avg Goals",
            marker_color="#E74C3C", text=avg["Gls"].round(1), textposition="auto",
        ))
        fig.add_trace(go.Bar(
            x=avg["Pos"], y=avg["Ast"], name="Avg Assists",
            marker_color="#3498DB", text=avg["Ast"].round(1), textposition="auto",
        ))
        fig.update_layout(title="Average Goals & Assists per Position", barmode="group")
        apply_plotly_theme(fig)
        st.plotly_chart(fig, use_container_width=True)

with tab3:
    fig = px.violin(
        filtered_data, x="Squad", y="Age",
        title="Age Distribution by Squad (Violin Plot)",
        color="Squad", box=True, points="outliers",
    )
    fig.update_layout(showlegend=False, xaxis_tickangle=-45)
    apply_plotly_theme(fig)
    st.plotly_chart(fig, use_container_width=True)

with tab4:
    squad_stats = filtered_data.groupby("Squad").agg(
        Goals=("Gls", "sum"),
        Assists=("Ast", "sum"),
        Players=("Player", "nunique"),
        Avg_Age=("Age", "mean"),
    ).reset_index()

    heat_data = squad_stats.set_index("Squad")[["Goals", "Assists", "Players"]].T

    fig = px.imshow(
        heat_data,
        title="Squad Performance Heatmap",
        color_continuous_scale="YlOrRd",
        text_auto=True,
        aspect="auto",
    )
    apply_plotly_theme(fig)
    st.plotly_chart(fig, use_container_width=True)
