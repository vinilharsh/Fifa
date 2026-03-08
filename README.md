# ⚽ La Liga Player Analysis Dashboard

An interactive Streamlit dashboard for analyzing La Liga player statistics across 8 seasons (2015–2023), featuring rich visualizations, player comparisons, and a machine learning prediction model.

![Python](https://img.shields.io/badge/Python-3.8+-blue)
![Streamlit](https://img.shields.io/badge/Streamlit-1.0+-red)
![scikit-learn](https://img.shields.io/badge/scikit--learn-ML-orange)

---

## Features

- **Home Dashboard** — Season KPIs, animated bubble scatter plots, top scorers
- **Data Explorer** — Filter, sort, and search players with visual progress bars
- **Season Overview** — Treemaps, violin plots, heatmaps, and squad comparisons
- **Insights & Trends** — xG/xA analysis with OLS trendlines and reference lines
- **Top Players** — Rankings with horizontal bar charts and lollipop (Goals vs xG) charts
- **xG/xA Analysis** — Overperformer/underperformer detection, squad heatmaps by season
- **Radar Analysis** — Player shooting profile radars (14 metrics) with bar comparison
- **Prediction Model** — ML-powered next-season Goals & Assists predictions using Gradient Boosting

---

## Project Structure

```
Fifa-main/
├── main.py                     # App entry point (Home page)
├── requirements.txt            # Python dependencies
│
├── data/
│   ├── player.csv              # Main player stats (4,608 rows, 8 seasons)
│   ├── Shooting.csv            # Combined shooting stats (3,988 rows)
│   ├── seasons/                # Per-season player CSVs (7 files)
│   └── shooting/               # Per-season shooting CSVs (7 files)
│
├── utils/
│   ├── __init__.py
│   ├── data_loader.py          # Cached data loading & helper functions
│   └── theme.py                # CSS styling & Plotly chart theming
│
└── pages/
    ├── 1_Data_Explorer.py      # Filter, sort, search players
    ├── 2_Overview.py           # Season overview with distributions
    ├── 3_Insights.py           # Trends with trendlines & reference lines
    ├── 4_Top_Players.py        # Player rankings & comparisons
    ├── 5_xG_xA_Analysis.py     # Expected goals/assists deep dive
    ├── 6_Radar_Analysis.py     # Radar & bar chart comparisons
    └── 7_Prediction_Model.py   # ML prediction pipeline
```

---

## Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/your-username/Fifa-main.git
   cd Fifa-main
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the app**
   ```bash
   streamlit run main.py
   ```

   The dashboard will open at `http://localhost:8501`

---

## Dependencies

| Package | Purpose |
|---------|---------|
| streamlit | Web app framework |
| pandas | Data manipulation |
| numpy | Numerical computing |
| plotly | Interactive charts |
| matplotlib | Static plots (radar charts) |
| seaborn | Statistical visualization |
| scikit-learn | Prediction model (Gradient Boosting) |
| scipy | Scientific computing |
| mplsoccer | Soccer visualization |
| soccerplots | Radar chart library |
| Pillow | Image processing |

---

## Data

The dataset covers **La Liga** seasons from **2015/2016 to 2022/2023** with:

- **Player stats** — Goals, Assists, Minutes, Age, Position, Squad, xG, xA
- **Shooting stats** — Shots, Shots on Target, Shot Accuracy, Shot Distance, Goals per Shot

---

## Prediction Model

The prediction model uses **Gradient Boosting Regression** to forecast next-season performance:

- **Features:** Age, Position, Minutes, Goals, Assists, xG, xA, xG/90, xA/90
- **Targets:** Next season Goals and Assists
- **Training data:** Consecutive season pairs for players appearing in multiple seasons
- **Output:** R² score, MAE, feature importance, per-player predictions

---

## Tech Stack

- **Frontend:** Streamlit (multi-page app)
- **Visualization:** Plotly (interactive), Matplotlib (radar charts)
- **ML:** scikit-learn (GradientBoostingRegressor)
- **Data:** Pandas, NumPy

---

## License

This project is for educational and analytical purposes.
