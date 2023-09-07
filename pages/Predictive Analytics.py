import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# Load data
df = pd.read_csv('player.csv')  # Update with your actual data source

# Sidebar filters
st.sidebar.header("Filters")
selected_season = st.sidebar.selectbox("Select Season", df['Season'].unique())

# Filter data based on selected season
filtered_data = df[df['Season'] == selected_season]

# Main content
st.title("La Liga Player Analysis Dashboard")

# Predictive Analytics Section
st.write("## Predictive Analytics")

# Display xG statistics
st.write("### xG Statistics")
total_xg = filtered_data['xG/expexted season'].sum()
average_xg_per_90 = (filtered_data['xG/expexted season'] / filtered_data['90s']).mean()

st.write(f"Total xG: {total_xg:.2f}")
st.write(f"Average xG per 90 minutes: {average_xg_per_90:.2f}")

# Display the bar plot of xG by Squad and Player
st.write("### Bar Plot: xG by Squad and Player")
fig_bar = px.bar(df, x="Squad", y="xG/expexted season", color="Player")
st.plotly_chart(fig_bar)

# Display the line plot of xG by Squad and Player
st.write("### Line Plot: xG by Squad and Player")
fig_line = px.line(df, x="Squad", y="xG/expexted season", color="Player")
st.plotly_chart(fig_line)

# Display the scatter plot of xG vs Goals by Squad
st.write("### Scatter Plot: xG vs Goals by Squad")
fig_scatter = px.scatter(df, x="xG/expexted season", y="Gls", color="Squad")
st.plotly_chart(fig_scatter)

# Display grouped line plot of xG and Goals per 90 by Squad
st.write("### Grouped Line Plot: xG and Goals per 90 by Squad")
grouped_df = df.groupby('Squad')[['xG/per 90', 'Gls/per 90']].sum()
fig_grouped_line = px.line(grouped_df)
st.plotly_chart(fig_grouped_line)

# Display grouped line plot of xG and Goals per season by Squad
st.write("### Grouped Line Plot: xG and Goals per Season by Squad")
grouped_df_season = df.groupby('Squad')[['xG/expexted season','Gls']].sum()
fig_grouped_line_season = px.line(grouped_df_season)
st.plotly_chart(fig_grouped_line_season)



# Display xG vs Goals Scatter Plot
st.write("### xG vs Goals Scatter Plot")
xg_goals_scatter = px.scatter(filtered_data, x="xG/expexted season", y="Gls", text="Player", title="xG vs Goals")
xg_goals_scatter.update_traces(textposition='top center')
xg_goals_scatter.update_layout(xaxis_title="xG (Expected Goals)", yaxis_title="Goals")
st.plotly_chart(xg_goals_scatter)

# Display xA vs Assists Scatter Plot
st.write("### xA vs Assists Scatter Plot")
xa_assists_scatter = px.scatter(filtered_data, x="xA/expected season", y="Ast", text="Player", title="xA vs Assists")
xa_assists_scatter.update_traces(textposition='top center')
xa_assists_scatter.update_layout(xaxis_title="xA (Expected Assists)", yaxis_title="Assists")
st.plotly_chart(xa_assists_scatter)


# Display xA vs Assists Line Plot
st.write("### Grouped Line Plot: xA and Ast per Season by Squad")
grouped_df_season = df.groupby('Squad')[['xA/expected season','Ast']].sum()
fig_grouped_line_season = px.line(grouped_df_season)
st.plotly_chart(fig_grouped_line_season)

st.write("### Grouped Line Plot: xA and Assists per 90 by Squad")
grouped_df = df.groupby('Squad')[['xA/per 90', 'Ast/per 90']].sum()
fig_grouped_line = px.line(grouped_df)
st.plotly_chart(fig_grouped_line)
