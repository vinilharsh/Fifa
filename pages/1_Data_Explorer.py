import streamlit as st
import plotly.express as px
from utils.data_loader import load_player_data, display_rename
from utils.theme import inject_custom_css, apply_plotly_theme

st.set_page_config(page_title="Data Explorer", page_icon="🔍", layout="wide")
inject_custom_css()

st.header("🔍 Data Explorer")

with st.spinner("Loading data..."):
    df = load_player_data()

st.sidebar.header("Filters")
selected_seasons = st.sidebar.multiselect(
    "Select Season(s)", sorted(df["Season"].unique(), reverse=True)
)
selected_squads = st.sidebar.multiselect("Select Squad(s)", sorted(df["Squad"].unique()))
selected_positions = st.sidebar.multiselect("Select Position(s)", df["Pos"].unique())

filtered_data = df.copy()
if selected_seasons:
    filtered_data = filtered_data[filtered_data["Season"].isin(selected_seasons)]
if selected_squads:
    filtered_data = filtered_data[filtered_data["Squad"].isin(selected_squads)]
if selected_positions:
    filtered_data = filtered_data[filtered_data["Pos"].isin(selected_positions)]

col1, col2, col3 = st.columns(3)
col1.metric("Players Found", len(filtered_data))
col2.metric("Squads", filtered_data["Squad"].nunique())
col3.metric("Seasons", filtered_data["Season"].nunique())

st.divider()

tab1, tab2 = st.tabs(["Filtered Data", "Player Search"])

with tab1:
    c1, c2 = st.columns([3, 1])
    sort_by = c1.selectbox("Sort By", df.columns)
    ascending = c2.checkbox("Ascending")
    sorted_data = filtered_data.sort_values(by=sort_by, ascending=ascending)

    max_gls = max(int(df["Gls"].max()), 1)
    max_ast = max(int(df["Ast"].max()), 1)

    st.dataframe(
        display_rename(sorted_data),
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

    st.divider()

    if len(filtered_data) > 0:
        c1, c2 = st.columns(2)
        with c1:
            pos_counts = filtered_data["Pos"].value_counts().reset_index()
            fig = px.bar(
                pos_counts, x="count", y="Pos", orientation="h",
                title="Position Distribution", text_auto=True,
                color="count", color_continuous_scale="Blues",
            )
            fig.update_layout(
                yaxis=dict(categoryorder="total ascending"),
                coloraxis_showscale=False,
            )
            apply_plotly_theme(fig)
            st.plotly_chart(fig, use_container_width=True)

        with c2:
            top5 = filtered_data.nlargest(5, "Gls")
            fig = px.bar(
                top5, x="Gls", y="Player", orientation="h",
                title="Top 5 Scorers in Selection", text_auto=True,
                color="Gls", color_continuous_scale="OrRd",
            )
            fig.update_layout(
                yaxis=dict(categoryorder="total ascending"),
                coloraxis_showscale=False,
            )
            apply_plotly_theme(fig)
            st.plotly_chart(fig, use_container_width=True)

with tab2:
    search_term = st.text_input("Enter player name")
    if search_term:
        search_results = df[df["Player"].str.contains(search_term, case=False, na=False)]
        st.dataframe(display_rename(search_results), use_container_width=True)
    else:
        st.info("Type a player name above to search.")
