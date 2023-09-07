import streamlit as st
import pandas as pd
import plotly.express as px

# Load data
df = pd.read_csv('player.csv')  # Update with your actual data source

# Sidebar filters
st.sidebar.header("Filters")
selected_season = st.sidebar.selectbox("Select Season", df['Season'].unique())

# Filter data based on selected season
filtered_data = df[df['Season'] == selected_season]

# Main content
st.title("La Liga Player Analysis Dashboard")

# Insights and Trends Section
st.write("## Insights and Trends")

# Calculate average age of players
average_age = filtered_data['Age'].mean()
st.write(f"### Average Age of Players in {selected_season}:")
st.write(f"The average age of players in {selected_season} season is {average_age:.2f} years.")

# Display a line chart showing xG and Goals per 90
st.write("### xG and Goals per 90 Trend:")
grouped_df = filtered_data.groupby('Squad')[['xG/per 90', 'Gls/per 90']].sum()
fig_grouped_line = px.line(grouped_df)
st.plotly_chart(fig_grouped_line)


# Display a scatter plot showing xA vs Assists
st.write("### xA vs Assists Trend:")
fig_xa_assists_trend = px.scatter(filtered_data, x="xA/expected season", y="Ast", text="Player", title="xA vs Assists Trend")
fig_xa_assists_trend.update_traces(textposition='top center')
fig_xa_assists_trend.update_layout(xaxis_title="xA (Expected Assists)", yaxis_title="Assists")
st.plotly_chart(fig_xa_assists_trend)

# Calculate the total number of goals and assists in the selected season
total_goals = filtered_data['Gls'].sum()
total_assists = filtered_data['Ast'].sum()
st.write(f"### Total Goals and Assists in {selected_season}:")
st.write(f"Total Goals: {total_goals}")
st.write(f"Total Assists: {total_assists}")

# Display a bar chart showing the distribution of players by position
st.write("### Player Position Distribution:")
fig_position_distribution = px.bar(filtered_data, x="Pos", title="Player Position Distribution")
fig_position_distribution.update_layout(xaxis_title="Position", yaxis_title="Number of Players")
st.plotly_chart(fig_position_distribution)

# Calculate and display the top goal scorer in the selected season
top_goal_scorer = filtered_data[filtered_data['Gls'] == filtered_data['Gls'].max()]['Player'].values[0]
top_goal_scorer_goals = filtered_data[filtered_data['Player'] == top_goal_scorer]['Gls'].values[0]
st.write(f"### Top Goal Scorer in {selected_season}:")
st.write(f"The top goal scorer in {selected_season} season is {top_goal_scorer} with {top_goal_scorer_goals} goals.")


# Display a pie chart showing the distribution of players by nationality
st.write("### Player Nationality Distribution:")
nationality_counts = filtered_data['Nation'].value_counts()
fig_nationality_distribution = px.pie(nationality_counts, names=nationality_counts.index, values=nationality_counts.values, title="Player Nationality Distribution")
st.plotly_chart(fig_nationality_distribution)
