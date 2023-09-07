import streamlit as st
import pandas as pd
import plotly.express as px

# Load data
data = pd.read_csv("player.csv")  # Update with your actual data source

# Sidebar filters
st.sidebar.header("Filters")
selected_season = st.sidebar.selectbox("Select Season", data['Season'].unique())

# Filter data based on selected season
filtered_data = data[data['Season'] == selected_season]

# Main content
st.title("La Liga Player Analysis Dashboard")

st.write(f"## Player Statistics for {selected_season}")

# Display basic statistics
total_players = filtered_data['Player'].nunique()
total_goals = filtered_data['Gls'].sum()
total_assists = filtered_data['Ast'].sum()

st.write(f"Total Players: {total_players}")
st.write(f"Total Goals: {total_goals}")
st.write(f"Total Assists: {total_assists}")

# Create interactive scatter plot using Plotly
scatter_plot = px.scatter(
    filtered_data, x='Gls', y='Ast', color='Pos',
    labels={'Gls': 'Goals', 'Ast': 'Assists'},
    title='Goals vs Assists by Position'
)
st.plotly_chart(scatter_plot)

# Display sample data
st.subheader("Sample Player Data")
st.write(filtered_data.head(10))
