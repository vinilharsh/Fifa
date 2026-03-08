import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
from utils.data_loader import load_player_data, filter_by_season, DISPLAY_LABELS, display_rename, get_display_label
from utils.theme import apply_plotly_theme, inject_custom_css

st.set_page_config(page_title="Top Players", page_icon="🏆", layout="wide")
inject_custom_css()

st.header("🏆 Top Players")

with st.spinner("Loading data..."):
    data = load_player_data()

st.sidebar.header("Filters")
selected_season = st.sidebar.selectbox(
    "Select Season", sorted(data["Season"].unique(), reverse=True)
)
filtered_data = filter_by_season(data, selected_season)

SORT_OPTIONS = {
    "Goals": "Gls",
    "Assists": "Ast",
    "xG (Season)": "xG/expexted season",
    "xA (Season)": "xA/expected season",
}

selected_label = st.selectbox("Sort by", list(SORT_OPTIONS.keys()))
selected_sort = SORT_OPTIONS[selected_label]

filtered_data = filtered_data.sort_values(by=selected_sort, ascending=False)

top_scorer = filtered_data.iloc[0] if len(filtered_data) > 0 else None
top_assister = filtered_data.sort_values("Ast", ascending=False).iloc[0] if len(filtered_data) > 0 else None

if top_scorer is not None:
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Top Scorer", top_scorer["Player"], delta=f"{int(top_scorer['Gls'])} goals")
    col2.metric("Top Assister", top_assister["Player"], delta=f"{int(top_assister['Ast'])} assists")
    col3.metric("Most Minutes", filtered_data.nlargest(1, "90s").iloc[0]["Player"])
    col4.metric("Total Players", len(filtered_data))

st.divider()

# Filters
st.subheader("Filter Players")
c1, c2 = st.columns(2)
position_filter = c1.multiselect("Select Position", filtered_data["Pos"].unique())
squad_filter = c2.multiselect("Select Squad", sorted(filtered_data["Squad"].unique()))

if position_filter or squad_filter:
    mask = True
    if position_filter:
        mask = filtered_data["Pos"].isin(position_filter)
    if squad_filter:
        mask = mask & filtered_data["Squad"].isin(squad_filter)
    filtered_data = filtered_data[mask]

st.divider()

tab1, tab2, tab3 = st.tabs(["Top Players Table", "Goals & Assists Chart", "Goals vs xG"])

with tab1:
    show_cols = ["Player", "Pos", "Squad", "Gls", "Ast", "xG/expexted season", "xA/expected season"]
    max_gls = max(int(data["Gls"].max()), 1)
    max_ast = max(int(data["Ast"].max()), 1)
    st.dataframe(
        display_rename(filtered_data[show_cols].head(15)),
        use_container_width=True,
        column_config={
            "Gls": st.column_config.ProgressColumn(
                "Goals", min_value=0, max_value=max_gls, format="%d",
            ),
            "Ast": st.column_config.ProgressColumn(
                "Assists", min_value=0, max_value=max_ast, format="%d",
            ),
        },
    )

with tab2:
    top10 = filtered_data.head(10)
    c1, c2 = st.columns(2)

    with c1:
        fig = px.bar(
            top10, x="Gls", y="Player", orientation="h",
            title="Top 10 — Goals",
            text_auto=True,
            color="Gls", color_continuous_scale="OrRd",
        )
        fig.update_layout(
            yaxis=dict(categoryorder="total ascending"),
            coloraxis_showscale=False,
        )
        apply_plotly_theme(fig)
        st.plotly_chart(fig, use_container_width=True)

    with c2:
        top10_ast = filtered_data.sort_values("Ast", ascending=False).head(10)
        fig = px.bar(
            top10_ast, x="Ast", y="Player", orientation="h",
            title="Top 10 — Assists",
            text_auto=True,
            color="Ast", color_continuous_scale="Blues",
        )
        fig.update_layout(
            yaxis=dict(categoryorder="total ascending"),
            coloraxis_showscale=False,
        )
        apply_plotly_theme(fig)
        st.plotly_chart(fig, use_container_width=True)

with tab3:
    xg_col = "xG/expexted season"
    top15 = filtered_data.head(15).copy()
    top15 = top15.sort_values("Gls", ascending=True)

    fig = go.Figure()

    fig.add_trace(go.Bar(
        y=top15["Player"], x=top15[xg_col],
        name="xG (Expected)", orientation="h",
        marker_color="rgba(52, 152, 219, 0.6)",
        text=top15[xg_col].round(1), textposition="auto",
    ))
    fig.add_trace(go.Scatter(
        y=top15["Player"], x=top15["Gls"],
        name="Goals (Actual)", mode="markers",
        marker=dict(color="#E74C3C", size=12, symbol="diamond"),
    ))

    fig.update_layout(
        title="Goals vs Expected Goals (xG) — Lollipop Chart",
        xaxis_title="Count",
        barmode="overlay",
    )
    apply_plotly_theme(fig)
    st.plotly_chart(fig, use_container_width=True)

    st.caption("Bar = xG (expected), Diamond = Actual Goals. Players above their xG bar are overperformers.")
