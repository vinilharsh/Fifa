import streamlit as st
import plotly.express as px
from utils.data_loader import load_player_data, filter_by_season, clean_minutes_column
from utils.theme import apply_plotly_theme, inject_custom_css

st.set_page_config(page_title="La Liga Dashboard", page_icon="⚽", layout="wide")
inject_custom_css()

st.title("⚽ La Liga Player Analysis Dashboard")
st.markdown(
    "Comprehensive player statistics and analytics across **8 La Liga seasons** (2015–2023)."
)

with st.spinner("Loading player data..."):
    data = load_player_data()
    data = clean_minutes_column(data)

st.sidebar.header("Filters")
selected_season = st.sidebar.selectbox(
    "Select Season", sorted(data["Season"].unique(), reverse=True)
)

filtered_data = filter_by_season(data, selected_season)

st.subheader(f"Season {selected_season}")

col1, col2, col3, col4 = st.columns(4)
col1.metric("Total Players", filtered_data["Player"].nunique())
col2.metric("Total Goals", int(filtered_data["Gls"].sum()))
col3.metric("Total Assists", int(filtered_data["Ast"].sum()))
col4.metric("Avg Age", f"{filtered_data['Age'].mean():.1f}")

st.divider()

tab1, tab2, tab3 = st.tabs(["Goals vs Assists", "Top Scorers", "All Seasons"])

with tab1:
    scatter = px.scatter(
        filtered_data,
        x="Gls", y="Ast", color="Pos",
        size="Min", size_max=30,
        hover_data={"Player": True, "Squad": True, "Age": True, "Min": True, "Pos": True, "Gls": True, "Ast": True},
        labels={"Gls": "Goals", "Ast": "Assists", "Pos": "Position", "Min": "Minutes"},
        title="Goals vs Assists by Position (bubble size = minutes played)",
        color_discrete_map={"FW": "#E74C3C", "MF": "#3498DB", "DF": "#2ECC71", "GK": "#F39C12"},
    )
    apply_plotly_theme(scatter)
    st.plotly_chart(scatter, use_container_width=True)

with tab2:
    top_scorers = filtered_data.nlargest(10, "Gls")
    fig = px.bar(
        top_scorers,
        x="Gls", y="Player",
        orientation="h",
        color="Gls",
        color_continuous_scale="OrRd",
        hover_data={"Squad": True, "Ast": True, "Age": True},
        title="Top 10 Goal Scorers",
        text_auto=True,
    )
    fig.update_layout(yaxis=dict(categoryorder="total ascending"), coloraxis_showscale=False)
    apply_plotly_theme(fig)
    st.plotly_chart(fig, use_container_width=True)

with tab3:
    all_data = clean_minutes_column(data.copy())
    anim_scatter = px.scatter(
        all_data,
        x="Gls", y="Ast", color="Pos",
        size="Min", size_max=25,
        animation_frame="Season",
        hover_data={"Player": True, "Squad": True},
        labels={"Gls": "Goals", "Ast": "Assists"},
        title="Goals vs Assists Across All Seasons (animated)",
        color_discrete_map={"FW": "#E74C3C", "MF": "#3498DB", "DF": "#2ECC71", "GK": "#F39C12"},
        range_x=[0, all_data["Gls"].quantile(0.99) + 5],
        range_y=[0, all_data["Ast"].quantile(0.99) + 5],
    )
    apply_plotly_theme(anim_scatter)
    st.plotly_chart(anim_scatter, use_container_width=True)

st.divider()

st.subheader("Sample Player Data")
st.dataframe(filtered_data.head(10), use_container_width=True)
