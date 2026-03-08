import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
from utils.data_loader import load_player_data, filter_by_season, get_display_label
from utils.theme import apply_plotly_theme, inject_custom_css

st.set_page_config(page_title="Insights", page_icon="💡", layout="wide")
inject_custom_css()

st.header("💡 Insights & Trends")

with st.spinner("Loading data..."):
    df = load_player_data()

st.sidebar.header("Filters")
selected_season = st.sidebar.selectbox(
    "Select Season", sorted(df["Season"].unique(), reverse=True)
)
filtered_data = filter_by_season(df, selected_season)

top_scorer = filtered_data.loc[filtered_data["Gls"].idxmax()]
top_assister = filtered_data.loc[filtered_data["Ast"].idxmax()]

col1, col2, col3, col4 = st.columns(4)
col1.metric("Average Age", f"{filtered_data['Age'].mean():.1f}")
col2.metric("Total Goals", int(filtered_data["Gls"].sum()))
col3.metric("Top Scorer", f"{top_scorer['Player']}", delta=f"{int(top_scorer['Gls'])} goals")
col4.metric("Top Assister", f"{top_assister['Player']}", delta=f"{int(top_assister['Ast'])} assists")

st.divider()

tab1, tab2, tab3 = st.tabs(["xG Analysis", "xA Analysis", "Distributions"])

with tab1:
    c1, c2 = st.columns(2)
    with c1:
        grouped = filtered_data.groupby("Squad")[["xG/per 90", "Gls/per 90"]].mean().reset_index()
        fig = px.bar(
            grouped, x="Squad", y=["xG/per 90", "Gls/per 90"],
            barmode="group", title="xG vs Goals per 90 by Squad",
            text_auto=".2f",
            labels={"value": "Per 90 Minutes", "variable": "Metric"},
        )
        fig.update_layout(xaxis_tickangle=-45)
        apply_plotly_theme(fig)
        st.plotly_chart(fig, use_container_width=True)

    with c2:
        xg_col = "xG/expexted season"
        fig = px.scatter(
            filtered_data,
            x=xg_col, y="Gls",
            color="Pos",
            size="90s", size_max=20,
            hover_data={"Player": True, "Squad": True},
            labels={xg_col: get_display_label(xg_col), "Gls": "Goals"},
            title="xG vs Actual Goals (bubble size = 90s played)",
            trendline="ols",
            color_discrete_map={"FW": "#E74C3C", "MF": "#3498DB", "DF": "#2ECC71", "GK": "#F39C12"},
        )
        max_val = max(filtered_data[xg_col].max(), filtered_data["Gls"].max())
        fig.add_shape(
            type="line", x0=0, y0=0, x1=max_val, y1=max_val,
            line=dict(color="rgba(255,255,255,0.3)", dash="dash", width=1),
        )
        apply_plotly_theme(fig)
        st.plotly_chart(fig, use_container_width=True)

with tab2:
    c1, c2 = st.columns(2)
    with c1:
        fig = px.scatter(
            filtered_data,
            x="xA/expected season", y="Ast",
            color="Pos",
            size="90s", size_max=20,
            hover_data={"Player": True, "Squad": True},
            labels={
                "xA/expected season": get_display_label("xA/expected season"),
                "Ast": "Assists",
            },
            title="xA vs Actual Assists (with trendline)",
            trendline="ols",
            color_discrete_map={"FW": "#E74C3C", "MF": "#3498DB", "DF": "#2ECC71", "GK": "#F39C12"},
        )
        max_val = max(
            filtered_data["xA/expected season"].max(),
            filtered_data["Ast"].max(),
        )
        fig.add_shape(
            type="line", x0=0, y0=0, x1=max_val, y1=max_val,
            line=dict(color="rgba(255,255,255,0.3)", dash="dash", width=1),
        )
        apply_plotly_theme(fig)
        st.plotly_chart(fig, use_container_width=True)

    with c2:
        grouped = filtered_data.groupby("Squad")[["xA/per 90", "Ast/per 90"]].mean().reset_index()
        fig = px.bar(
            grouped, x="Squad", y=["xA/per 90", "Ast/per 90"],
            barmode="group", title="xA vs Assists per 90 by Squad",
            text_auto=".2f",
            labels={"value": "Per 90 Minutes", "variable": "Metric"},
        )
        fig.update_layout(xaxis_tickangle=-45)
        apply_plotly_theme(fig)
        st.plotly_chart(fig, use_container_width=True)

with tab3:
    c1, c2 = st.columns(2)
    with c1:
        pos_counts = filtered_data["Pos"].value_counts().reset_index()
        fig = px.bar(
            pos_counts, x="count", y="Pos", orientation="h",
            title="Position Distribution",
            text_auto=True,
            color="count", color_continuous_scale="Viridis",
        )
        fig.update_layout(
            yaxis=dict(categoryorder="total ascending"),
            coloraxis_showscale=False,
        )
        apply_plotly_theme(fig)
        st.plotly_chart(fig, use_container_width=True)

    with c2:
        nat = filtered_data["Nation"].value_counts().head(15).reset_index()
        nat.columns = ["Nation", "Count"]
        fig = px.treemap(
            nat, path=["Nation"], values="Count",
            title="Top 15 Nationalities",
            color="Count", color_continuous_scale="Sunset",
        )
        fig.update_layout(coloraxis_showscale=False)
        apply_plotly_theme(fig)
        st.plotly_chart(fig, use_container_width=True)
