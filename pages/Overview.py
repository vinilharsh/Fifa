import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# Load data
data = pd.read_csv("player.csv")  # Update with your actual data source

# Sidebar filters
st.sidebar.header("Filters")
selected_season = st.sidebar.selectbox("Select Season", data['Season'].unique())

# Filter data based on selected season
filtered_data = data[data['Season'] == selected_season]

# Main content
st.title("La Liga Player Analysis Dashboard")

# Overview Section
st.write(f"## Overview for {selected_season}")

# General statistics
total_goals = filtered_data['Gls'].sum()
total_assists = filtered_data['Ast'].sum()
average_age = filtered_data['Age'].mean()

st.write(f"Total Goals: {total_goals}")
st.write(f"Total Assists: {total_assists}")
st.write(f"Average Age: {average_age:.2f}")

# Scatter plot of goals vs assists
scatter_plot = px.scatter(
    filtered_data, x='Gls', y='Ast', color='Pos',
    labels={'Gls': 'Goals', 'Ast': 'Assists'},
    title='Goals vs Assists by Position'
)
st.plotly_chart(scatter_plot)

# Distribution of player positions
position_distribution = filtered_data['Pos'].value_counts()
st.write("## Player Position Distribution")
st.bar_chart(position_distribution)

# Distribution of player nationalities
nationality_distribution = filtered_data['Nation'].value_counts()
st.write("## Player Nationality Distribution")
fig = px.pie(nationality_distribution, names=nationality_distribution.index, title="Player Nationality Distribution")
st.plotly_chart(fig)

# Box plot of age distribution by squad
st.write("## Age Distribution by Squad (Box Plot)")
age_boxplot = px.box(filtered_data, x='Squad', y='Age', title='Age Distribution by Squad (Box Plot)')
st.plotly_chart(age_boxplot)

# Average goals and assists per position
avg_goals_assists = filtered_data.groupby('Pos')[['Gls', 'Ast']].mean().reset_index()
fig_avg = go.Figure()
fig_avg.add_trace(go.Bar(x=avg_goals_assists['Pos'], y=avg_goals_assists['Gls'], name='Average Goals'))
fig_avg.add_trace(go.Bar(x=avg_goals_assists['Pos'], y=avg_goals_assists['Ast'], name='Average Assists'))
fig_avg.update_layout(title='Average Goals and Assists per Position', xaxis_title='Position', yaxis_title='Average Count')
st.plotly_chart(fig_avg)
