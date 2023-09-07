import streamlit as st
import pandas as pd

# Load data
df = pd.read_csv('player.csv')  # Update with your actual data source

# Sidebar filters
st.sidebar.header("Data Explorer Filters")

# Filter by Season
selected_seasons = st.sidebar.multiselect("Select Season(s)", df['Season'].unique())

# Filter by Squad
selected_squads = st.sidebar.multiselect("Select Squad(s)", df['Squad'].unique())

# Filter by Position
selected_positions = st.sidebar.multiselect("Select Position(s)", df['Pos'].unique())

# Main content
st.title("La Liga Player Analysis Dashboard")

# Data Explorer Section
st.write("## Data Explorer")

# Apply filters
filtered_data = df[
    (df['Season'].isin(selected_seasons)) &
    (df['Squad'].isin(selected_squads)) &
    (df['Pos'].isin(selected_positions))
]

# Display filtered data
st.write("### Filtered Data")
st.dataframe(filtered_data)

# Sorting options
st.write("### Sorting Options")
sort_by = st.selectbox("Sort By", df.columns)
ascending = st.checkbox("Ascending")
sorted_data = filtered_data.sort_values(by=sort_by, ascending=ascending)
st.dataframe(sorted_data)

# Search
st.write("### Search by Player Name")
search_term = st.text_input("Enter player name")
search_results = df[df['Player'].str.contains(search_term, case=False)]
st.dataframe(search_results)
