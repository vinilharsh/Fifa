import streamlit as st
import pandas as pd
import plotly.express as px
from utils.data_loader import load_player_data, filter_by_season, get_display_label
from utils.theme import apply_plotly_theme, inject_custom_css

st.set_page_config(page_title="xG/xA Analysis", page_icon="📈", layout="wide")
inject_custom_css()

st.header("📈 xG / xA Analysis")

with st.spinner("Loading data..."):
    df = load_player_data()

st.sidebar.header("Filters")
selected_season = st.sidebar.selectbox(
    "Select Season", sorted(df["Season"].unique(), reverse=True)
)
filtered_data = filter_by_season(df, selected_season)

total_xg = filtered_data["xG/expexted season"].sum()
total_xa = filtered_data["xA/expected season"].sum()
total_gls = filtered_data["Gls"].sum()
total_ast = filtered_data["Ast"].sum()

col1, col2, col3, col4 = st.columns(4)
col1.metric("Total xG", f"{total_xg:.1f}", delta=f"{total_gls - total_xg:.1f} overperformance")
col2.metric("Total Goals", int(total_gls))
col3.metric("Total xA", f"{total_xa:.1f}", delta=f"{total_ast - total_xa:.1f} overperformance")
col4.metric("Total Assists", int(total_ast))

st.divider()

XG_COL = "xG/expexted season"
XA_COL = "xA/expected season"

tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "xG vs Goals", "xA vs Assists", "Top Players", "By Squad", "Heatmap",
])

with tab1:
    c1, c2 = st.columns(2)
    with c1:
        fig = px.scatter(
            filtered_data,
            x=XG_COL, y="Gls", color="Pos",
            size="90s", size_max=22,
            hover_data={"Player": True, "Squad": True, "90s": True},
            labels={XG_COL: get_display_label(XG_COL), "Gls": "Goals"},
            title="xG vs Goals (bubble size = 90s played)",
            trendline="ols",
            color_discrete_map={"FW": "#E74C3C", "MF": "#3498DB", "DF": "#2ECC71", "GK": "#F39C12"},
        )
        max_val = max(filtered_data[XG_COL].max(), filtered_data["Gls"].max(), 1)
        fig.add_shape(
            type="line", x0=0, y0=0, x1=max_val, y1=max_val,
            line=dict(color="rgba(255,255,255,0.25)", dash="dash", width=1),
        )
        fig.add_annotation(
            x=max_val * 0.8, y=max_val * 0.65,
            text="Perfect prediction", showarrow=False,
            font=dict(color="rgba(255,255,255,0.4)", size=10),
            textangle=-35,
        )
        apply_plotly_theme(fig)
        st.plotly_chart(fig, use_container_width=True)

    with c2:
        filtered_data_copy = filtered_data.copy()
        filtered_data_copy["G-xG"] = filtered_data_copy["Gls"] - filtered_data_copy[XG_COL]
        top_over = filtered_data_copy.nlargest(10, "G-xG")
        top_under = filtered_data_copy.nsmallest(10, "G-xG")
        combined = pd.concat([top_over, top_under]).sort_values("G-xG")

        fig = px.bar(
            combined, x="G-xG", y="Player", orientation="h",
            title="Top Overperformers & Underperformers (Goals - xG)",
            text_auto=".1f",
            color="G-xG", color_continuous_scale="RdYlGn",
            color_continuous_midpoint=0,
        )
        fig.update_layout(
            yaxis=dict(categoryorder="total ascending"),
            coloraxis_showscale=False,
        )
        apply_plotly_theme(fig)
        st.plotly_chart(fig, use_container_width=True)

with tab2:
    c1, c2 = st.columns(2)
    with c1:
        fig = px.scatter(
            filtered_data,
            x=XA_COL, y="Ast", color="Pos",
            size="90s", size_max=22,
            hover_data={"Player": True, "Squad": True, "90s": True},
            labels={XA_COL: get_display_label(XA_COL), "Ast": "Assists"},
            title="xA vs Assists (bubble size = 90s played)",
            trendline="ols",
            color_discrete_map={"FW": "#E74C3C", "MF": "#3498DB", "DF": "#2ECC71", "GK": "#F39C12"},
        )
        max_val = max(filtered_data[XA_COL].max(), filtered_data["Ast"].max(), 1)
        fig.add_shape(
            type="line", x0=0, y0=0, x1=max_val, y1=max_val,
            line=dict(color="rgba(255,255,255,0.25)", dash="dash", width=1),
        )
        apply_plotly_theme(fig)
        st.plotly_chart(fig, use_container_width=True)

    with c2:
        filtered_data_copy = filtered_data.copy()
        filtered_data_copy["A-xA"] = filtered_data_copy["Ast"] - filtered_data_copy[XA_COL]
        top_over = filtered_data_copy.nlargest(10, "A-xA")
        top_under = filtered_data_copy.nsmallest(10, "A-xA")
        combined = pd.concat([top_over, top_under]).sort_values("A-xA")

        fig = px.bar(
            combined, x="A-xA", y="Player", orientation="h",
            title="Top Overperformers & Underperformers (Assists - xA)",
            text_auto=".1f",
            color="A-xA", color_continuous_scale="RdYlGn",
            color_continuous_midpoint=0,
        )
        fig.update_layout(
            yaxis=dict(categoryorder="total ascending"),
            coloraxis_showscale=False,
        )
        apply_plotly_theme(fig)
        st.plotly_chart(fig, use_container_width=True)

with tab3:
    c1, c2 = st.columns(2)
    with c1:
        top15_xg = filtered_data.nlargest(15, XG_COL)
        fig = px.bar(
            top15_xg, x=XG_COL, y="Player", orientation="h",
            title="Top 15 Players by xG",
            text_auto=".1f",
            color=XG_COL, color_continuous_scale="OrRd",
            hover_data={"Squad": True, "Gls": True},
            labels={XG_COL: get_display_label(XG_COL)},
        )
        fig.update_layout(
            yaxis=dict(categoryorder="total ascending"),
            coloraxis_showscale=False,
        )
        apply_plotly_theme(fig)
        st.plotly_chart(fig, use_container_width=True)

    with c2:
        top15_xa = filtered_data.nlargest(15, XA_COL)
        fig = px.bar(
            top15_xa, x=XA_COL, y="Player", orientation="h",
            title="Top 15 Players by xA",
            text_auto=".1f",
            color=XA_COL, color_continuous_scale="Blues",
            hover_data={"Squad": True, "Ast": True},
            labels={XA_COL: get_display_label(XA_COL)},
        )
        fig.update_layout(
            yaxis=dict(categoryorder="total ascending"),
            coloraxis_showscale=False,
        )
        apply_plotly_theme(fig)
        st.plotly_chart(fig, use_container_width=True)

with tab4:
    c1, c2 = st.columns(2)
    with c1:
        grouped = filtered_data.groupby("Squad")[["xG/per 90", "Gls/per 90"]].mean().reset_index()
        grouped = grouped.sort_values("xG/per 90", ascending=True)
        fig = px.bar(
            grouped, x=["xG/per 90", "Gls/per 90"], y="Squad",
            orientation="h", barmode="group",
            title="xG vs Goals per 90 by Squad",
            text_auto=".2f",
        )
        apply_plotly_theme(fig)
        st.plotly_chart(fig, use_container_width=True)

    with c2:
        grouped = filtered_data.groupby("Squad")[["xA/per 90", "Ast/per 90"]].mean().reset_index()
        grouped = grouped.sort_values("xA/per 90", ascending=True)
        fig = px.bar(
            grouped, x=["xA/per 90", "Ast/per 90"], y="Squad",
            orientation="h", barmode="group",
            title="xA vs Assists per 90 by Squad",
            text_auto=".2f",
        )
        apply_plotly_theme(fig)
        st.plotly_chart(fig, use_container_width=True)

with tab5:
    st.subheader("Squad xG Overperformance by Season")

    heatmap_data = df.dropna(subset=[XG_COL]).copy()
    heatmap_data["G-xG"] = heatmap_data["Gls"] - heatmap_data[XG_COL]

    pivot = heatmap_data.groupby(["Squad", "Season"])["G-xG"].sum().reset_index()
    pivot_table = pivot.pivot(index="Squad", columns="Season", values="G-xG")
    pivot_table = pivot_table.fillna(0)

    fig = px.imshow(
        pivot_table,
        title="Goals - xG by Squad & Season (Green = Overperformance)",
        color_continuous_scale="RdYlGn",
        color_continuous_midpoint=0,
        text_auto=".1f",
        aspect="auto",
    )
    apply_plotly_theme(fig)
    st.plotly_chart(fig, use_container_width=True)

    st.caption("Positive (green) = scored more than expected. Negative (red) = scored less than expected.")
