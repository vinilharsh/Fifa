import streamlit as st

POSITION_COLORS = {
    "FW": "#E74C3C",
    "MF": "#3498DB",
    "DF": "#2ECC71",
    "GK": "#F39C12",
    "Unknown": "#95A5A6",
}

PLOTLY_COLOR_SEQUENCE = [
    "#E74C3C", "#3498DB", "#2ECC71", "#F39C12",
    "#9B59B6", "#1ABC9C", "#E67E22", "#34495E",
    "#E91E63", "#00BCD4", "#8BC34A", "#FF9800",
]


def apply_plotly_theme(fig):
    fig.update_layout(
        template="plotly_dark",
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font=dict(family="Segoe UI, sans-serif", size=13),
        title=dict(font=dict(size=20, color="#FFFFFF")),
        legend=dict(
            bgcolor="rgba(0,0,0,0)",
            borderwidth=0,
            font=dict(size=11),
        ),
        margin=dict(l=40, r=40, t=60, b=40),
        colorway=PLOTLY_COLOR_SEQUENCE,
        hoverlabel=dict(
            bgcolor="#1E1E2E",
            font_size=13,
            font_family="Segoe UI, sans-serif",
            bordercolor="#444",
        ),
        hovermode="closest",
    )
    fig.update_xaxes(
        gridcolor="rgba(128,128,128,0.15)",
        zeroline=False,
        title_font=dict(size=13),
    )
    fig.update_yaxes(
        gridcolor="rgba(128,128,128,0.15)",
        zeroline=False,
        title_font=dict(size=13),
    )
    return fig


def inject_custom_css():
    st.markdown(
        """
        <style>
        /* Metric cards */
        [data-testid="stMetric"] {
            background: linear-gradient(135deg, #1E1E2E 0%, #2A2A3E 100%);
            border: 1px solid #3A3A5A;
            border-radius: 12px;
            padding: 16px 20px;
            box-shadow: 0 4px 12px rgba(0,0,0,0.3);
            transition: transform 0.2s ease, box-shadow 0.2s ease;
        }
        [data-testid="stMetric"]:hover {
            transform: translateY(-2px);
            box-shadow: 0 6px 20px rgba(0,0,0,0.5);
        }
        [data-testid="stMetric"] label {
            color: #9A9ABF;
            font-size: 0.85rem;
            text-transform: uppercase;
            letter-spacing: 0.5px;
        }
        [data-testid="stMetric"] [data-testid="stMetricValue"] {
            font-weight: 700;
        }

        /* Tabs */
        .stTabs [data-baseweb="tab-list"] {
            gap: 8px;
        }
        .stTabs [data-baseweb="tab"] {
            border-radius: 8px 8px 0 0;
            padding: 8px 20px;
        }

        /* Dataframes */
        [data-testid="stDataFrame"] {
            border-radius: 8px;
            overflow: hidden;
        }

        /* Sidebar */
        section[data-testid="stSidebar"] {
            background: linear-gradient(180deg, #0E1117 0%, #1A1A2E 100%);
            color: #E0E0E0;
        }
        section[data-testid="stSidebar"] h1,
        section[data-testid="stSidebar"] h2,
        section[data-testid="stSidebar"] h3,
        section[data-testid="stSidebar"] label,
        section[data-testid="stSidebar"] p,
        section[data-testid="stSidebar"] span,
        section[data-testid="stSidebar"] div {
            color: #E0E0E0 !important;
        }
        section[data-testid="stSidebar"] [data-baseweb="select"] span {
            color: #FFFFFF !important;
        }

        /* Dividers */
        hr {
            border-color: rgba(128,128,128,0.2) !important;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )
