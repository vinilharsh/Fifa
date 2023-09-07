import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# Load data
data = pd.read_csv(r"C:\Users\sharsh\Desktop\fifa\player.csv")  # Update with your actual data source

# Sidebar filters
st.sidebar.header("Filters")
selected_season = st.sidebar.selectbox("Select Season", data['Season'].unique())

# Filter data based on selected season
filtered_data = data[data['Season'] == selected_season]

# Main content
st.title("La Liga Player Analysis Dashboard")

# Top Players Section
st.write(f"## Top Players for {selected_season}")

# Sorting and filtering options
sort_options = ['xG/expexted season', 'xA/expected season', 'Gls', 'Ast']  # Corrected column names
selected_sort = st.selectbox("Sort by", sort_options)

filtered_data = filtered_data.sort_values(by=selected_sort, ascending=False)

# Display table of top players
st.write("### Top Players")
st.dataframe(filtered_data[['Player', 'Pos', 'Squad', 'Gls', 'Ast', 'xG/expexted season', 'xA/expected season']].head(10))

# Interactive filtering
st.write("### Filter Players")
position_filter = st.multiselect("Select Position", filtered_data['Pos'].unique())
squad_filter = st.multiselect("Select Squad", filtered_data['Squad'].unique())

if position_filter or squad_filter:
    filtered_data = filtered_data[
        (filtered_data['Pos'].isin(position_filter)) & (filtered_data['Squad'].isin(squad_filter))
    ]
    st.dataframe(filtered_data[['Player', 'Pos', 'Squad', 'Gls', 'Ast', 'xG/expexted season', 'xA/expected season']])


st.write("### Goals and Assists for Top Players")
bar_chart = px.bar(
    filtered_data.head(10), x='Player', y=['Gls', 'Ast'],
    title='Goals and Assists for Top Players'
)
st.plotly_chart(bar_chart)