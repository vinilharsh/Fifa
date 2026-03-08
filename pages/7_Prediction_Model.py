import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
from sklearn.ensemble import GradientBoostingRegressor
from sklearn.model_selection import train_test_split
from sklearn.metrics import r2_score, mean_absolute_error
from utils.data_loader import (
    load_player_data, SEASON_ORDER, clean_minutes_column, normalize_position,
)
from utils.theme import apply_plotly_theme, inject_custom_css

st.set_page_config(page_title="Prediction Model", page_icon="🤖", layout="wide")
inject_custom_css()

st.header("🤖 Next-Season Performance Prediction")
st.markdown(
    "Predicts a player's **Goals** and **Assists** for the following season "
    "based on current season performance, age, position, and expected metrics."
)


# --- Data preparation ---

FEATURE_COLS = [
    "Age", "Min", "90s", "Gls", "Ast",
    "xG_season", "xA_season", "xG_per90", "xA_per90",
]


@st.cache_data
def build_training_data():
    df = load_player_data()
    df = clean_minutes_column(df)
    df["primary_pos"] = df["Pos"].apply(normalize_position)

    df = df.dropna(subset=["xG/expexted season", "xA/expected season"])

    season_idx = {s: i for i, s in enumerate(SEASON_ORDER)}
    df["season_idx"] = df["Season"].map(season_idx)
    df = df.dropna(subset=["season_idx"])

    training_rows = []

    for player in df["Player"].unique():
        player_df = df[df["Player"] == player].sort_values("season_idx")

        for i in range(len(player_df) - 1):
            current = player_df.iloc[i]
            next_s = player_df.iloc[i + 1]

            if next_s["season_idx"] - current["season_idx"] != 1:
                continue

            training_rows.append({
                "Age": current["Age"],
                "primary_pos": current["primary_pos"],
                "Min": current["Min"],
                "90s": current["90s"],
                "Gls": current["Gls"],
                "Ast": current["Ast"],
                "xG_season": current["xG/expexted season"],
                "xA_season": current["xA/expected season"],
                "xG_per90": current["xG/per 90"],
                "xA_per90": current["xA/per 90"],
                "next_Gls": next_s["Gls"],
                "next_Ast": next_s["Ast"],
                "_player": player,
                "_current_season": current["Season"],
                "_next_season": next_s["Season"],
            })

    return pd.DataFrame(training_rows)


@st.cache_resource
def train_models(training_df):
    pos_dummies = pd.get_dummies(training_df["primary_pos"], prefix="pos")
    X = pd.concat([training_df[FEATURE_COLS], pos_dummies], axis=1)

    y_goals = training_df["next_Gls"]
    y_assists = training_df["next_Ast"]

    X_train, X_test, yg_train, yg_test, ya_train, ya_test = train_test_split(
        X, y_goals, y_assists, test_size=0.2, random_state=42
    )

    goals_model = GradientBoostingRegressor(
        n_estimators=200, max_depth=4, learning_rate=0.1,
        min_samples_split=10, random_state=42,
    )
    goals_model.fit(X_train, yg_train)

    assists_model = GradientBoostingRegressor(
        n_estimators=200, max_depth=4, learning_rate=0.1,
        min_samples_split=10, random_state=42,
    )
    assists_model.fit(X_train, ya_train)

    goals_pred = goals_model.predict(X_test)
    assists_pred = assists_model.predict(X_test)

    metrics = {
        "goals_r2": r2_score(yg_test, goals_pred),
        "goals_mae": mean_absolute_error(yg_test, goals_pred),
        "assists_r2": r2_score(ya_test, assists_pred),
        "assists_mae": mean_absolute_error(ya_test, assists_pred),
    }

    return (
        goals_model, assists_model,
        X.columns.tolist(), metrics,
        X_test, yg_test, ya_test, goals_pred, assists_pred,
    )


def predict_player(goals_model, assists_model, feature_names, player_row):
    features = {
        "Age": player_row["Age"],
        "Min": player_row["Min"],
        "90s": player_row["90s"],
        "Gls": player_row["Gls"],
        "Ast": player_row["Ast"],
        "xG_season": player_row["xG/expexted season"],
        "xA_season": player_row["xA/expected season"],
        "xG_per90": player_row["xG/per 90"],
        "xA_per90": player_row["xA/per 90"],
    }

    row = pd.DataFrame([features])

    for col in feature_names:
        if col not in row.columns:
            row[col] = 0

    pos = normalize_position(player_row["Pos"])
    pos_col = f"pos_{pos}"
    if pos_col in feature_names:
        row[pos_col] = 1

    row = row[feature_names]

    pred_goals = max(0, goals_model.predict(row)[0])
    pred_assists = max(0, assists_model.predict(row)[0])
    return pred_goals, pred_assists


# --- Train ---

with st.spinner("Building training data and training models..."):
    training_df = build_training_data()
    (
        goals_model, assists_model,
        feature_names, metrics,
        X_test, yg_test, ya_test, goals_pred, assists_pred,
    ) = train_models(training_df)

st.divider()

tab1, tab2, tab3 = st.tabs(["Model Performance", "Player Predictions", "Training Data"])

# --- Tab 1: Model Performance ---

with tab1:
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Goals R²", f"{metrics['goals_r2']:.3f}")
    col2.metric("Goals MAE", f"{metrics['goals_mae']:.2f}")
    col3.metric("Assists R²", f"{metrics['assists_r2']:.3f}")
    col4.metric("Assists MAE", f"{metrics['assists_mae']:.2f}")

    st.divider()

    c1, c2 = st.columns(2)

    with c1:
        max_val = max(yg_test.max(), goals_pred.max())
        fig = px.scatter(
            x=yg_test, y=goals_pred,
            labels={"x": "Actual Goals", "y": "Predicted Goals"},
            title="Predicted vs Actual Goals",
        )
        fig.add_shape(
            type="line", x0=0, y0=0, x1=max_val, y1=max_val,
            line=dict(color="red", dash="dash"),
        )
        apply_plotly_theme(fig)
        st.plotly_chart(fig, use_container_width=True)

    with c2:
        max_val = max(ya_test.max(), assists_pred.max())
        fig = px.scatter(
            x=ya_test, y=assists_pred,
            labels={"x": "Actual Assists", "y": "Predicted Assists"},
            title="Predicted vs Actual Assists",
        )
        fig.add_shape(
            type="line", x0=0, y0=0, x1=max_val, y1=max_val,
            line=dict(color="red", dash="dash"),
        )
        apply_plotly_theme(fig)
        st.plotly_chart(fig, use_container_width=True)

    st.divider()
    st.subheader("Feature Importance")

    c1, c2 = st.columns(2)

    with c1:
        imp = pd.DataFrame({
            "Feature": feature_names,
            "Importance": goals_model.feature_importances_,
        }).sort_values("Importance", ascending=True)
        fig = px.bar(
            imp, x="Importance", y="Feature",
            orientation="h", title="Goals Model — Feature Importance",
        )
        apply_plotly_theme(fig)
        st.plotly_chart(fig, use_container_width=True)

    with c2:
        imp = pd.DataFrame({
            "Feature": feature_names,
            "Importance": assists_model.feature_importances_,
        }).sort_values("Importance", ascending=True)
        fig = px.bar(
            imp, x="Importance", y="Feature",
            orientation="h", title="Assists Model — Feature Importance",
        )
        apply_plotly_theme(fig)
        st.plotly_chart(fig, use_container_width=True)


# --- Tab 2: Player Predictions ---

with tab2:
    df_full = load_player_data()
    df_full = clean_minutes_column(df_full)

    available_seasons = sorted(
        df_full.dropna(subset=["xG/expexted season"])["Season"].unique(),
        reverse=True,
    )
    selected_season = st.selectbox("Predict from season:", available_seasons)

    season_df = df_full[
        (df_full["Season"] == selected_season)
        & df_full["xG/expexted season"].notna()
    ]

    selected_player = st.selectbox(
        "Select Player:", sorted(season_df["Player"].unique())
    )

    player_row = season_df[season_df["Player"] == selected_player].iloc[0]

    pred_goals, pred_assists = predict_player(
        goals_model, assists_model, feature_names, player_row
    )

    st.divider()

    col1, col2, col3, col4 = st.columns(4)
    col1.metric(
        "Predicted Goals (Next Season)",
        f"{pred_goals:.1f}",
        delta=f"{pred_goals - player_row['Gls']:.1f} vs current",
    )
    col2.metric("Current Goals", int(player_row["Gls"]))
    col3.metric(
        "Predicted Assists (Next Season)",
        f"{pred_assists:.1f}",
        delta=f"{pred_assists - player_row['Ast']:.1f} vs current",
    )
    col4.metric("Current Assists", int(player_row["Ast"]))

    st.divider()

    st.subheader("Top 20 Predicted Performers")

    all_predictions = []
    for _, row in season_df.iterrows():
        pg, pa = predict_player(goals_model, assists_model, feature_names, row)
        all_predictions.append({
            "Player": row["Player"],
            "Squad": row["Squad"],
            "Position": row["Pos"],
            "Current Goals": int(row["Gls"]),
            "Predicted Goals": round(pg, 1),
            "Current Assists": int(row["Ast"]),
            "Predicted Assists": round(pa, 1),
        })

    pred_df = pd.DataFrame(all_predictions)

    c1, c2 = st.columns(2)

    with c1:
        st.markdown("**Top 20 — Predicted Goal Scorers**")
        st.dataframe(
            pred_df.sort_values("Predicted Goals", ascending=False).head(20),
            use_container_width=True,
        )

    with c2:
        st.markdown("**Top 20 — Predicted Assist Providers**")
        st.dataframe(
            pred_df.sort_values("Predicted Assists", ascending=False).head(20),
            use_container_width=True,
        )


# --- Tab 3: Training Data ---

with tab3:
    st.metric("Training Samples", len(training_df))
    st.dataframe(
        training_df[
            ["_player", "_current_season", "_next_season"]
            + FEATURE_COLS
            + ["next_Gls", "next_Ast"]
        ].rename(columns={
            "_player": "Player",
            "_current_season": "From Season",
            "_next_season": "To Season",
            "xG_season": "xG (Season)",
            "xA_season": "xA (Season)",
            "xG_per90": "xG/90",
            "xA_per90": "xA/90",
            "next_Gls": "Next Season Goals",
            "next_Ast": "Next Season Assists",
        }),
        use_container_width=True,
    )
