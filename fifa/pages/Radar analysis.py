import streamlit as st
from soccerplots.radar_chart import Radar
import pandas as pd
selected_year = st.sidebar.selectbox("Select Year", ["2022/23", "2021/22", "2020/21","2019/20","2018/19","2017/18","2016/17","2015/16"])
if selected_year == "2022/23":
    df_2 = pd.read_csv("Shooting(2020-21).csv")
    df_2['SoT%'] = df_2['SoT%'].fillna(df_2.groupby('Pos')['SoT%'].transform('mean'))
    df_2['G/Sh'] = df_2['G/Sh'].fillna(df_2.groupby('Pos')['G/Sh'].transform('mean'))
    df_2['G/SoT'] = df_2['G/SoT'].fillna(df_2.groupby('Pos')['G/SoT'].transform('mean'))
    df_2['Dist'] = df_2['Dist'].fillna(df_2.groupby('Pos')['Dist'].transform('mean'))
    df_2['npxG/Sh'] = df_2['npxG/Sh'].fillna(df_2.groupby('Pos')['npxG/Sh'].transform('mean'))# Update with your actual data source
    df_2 = df_2.drop(['Rk','Nation','Pos','Squad','Age','Born','90s','FK','PK','PKatt','Season'],axis=1)
    #df_2= df_2[(df_2['Player']=='Lionel Messi') |(df_2['Player']=='Karim Benzema')|(df_2['Player']=='Gerard Moreno')|(df_2['Player']=='Luis Suárez')|(df_2['Player']=='Youssef En-Nesyri')|(df_2['Player']=='Alexander Isak')|(df_2['Player']=='Iago Aspas')|(df_2['Player']=='Antoine Griezmann')|(df_2['Player']=='José Luis Morales') | (df_2['Player']=='Rafa Mir')].reset_index()
    #df_2 = df_2.drop(['index'],axis=1)
# Manually filtered list of players with corresponding subtitles
    player_subtitles = {
        'Lionel Messi': 'Barcelona',
        'Karim Benzema': 'Real Madrid',
        'Gerard Moreno': 'Villarreal',
        'Luis Suárez': 'Atletico Madrid',
        'Youssef En-Nesyri': 'Sevilla',
        'Alexander Isak': 'Real Sociedad',
        'Iago Aspas': 'Celta Vigo',
        'Antoine Griezmann': 'Barcelona',
        'José Luis Morales': 'Levante',
        'Rafa Mir': 'Wolves'  # Update with the actual subtitle
    }

# Create Streamlit app
    st.title("Soccer Player Radar Analysis")

# Select player from the filtered list
    selected_player = st.selectbox("Select a player:", list(player_subtitles.keys()))

# Get data for the selected player
    player_data = df_2[df_2['Player'] == selected_player]  # Use your appropriate dataframe here

# Define parameters for the radar chart
    params = ['Gls', 'Sh', 'SoT', 'SoT%', 'Sh/90', 'SoT/90', 'G/Sh', 'G/SoT', 'Dist', 'xG', 'npxG', 'npxG/Sh', 'G-xG', 'np:G-xG']

# Calculate ranges for each parameter
    ranges = []
    a_values = []
    b_values = []


    for x in params:
        a = min(df_2[params][x])
        a = a - (a*.05)
    
        b = max(df_2[params][x])
        b = b + (b*.05)
    
  
    
    
        ranges.append((a,b))
    

# Extract player's values for each parameter
# Extract player's values for the selected player
    selected_player_values = player_data.iloc[0].values[1:]  # Use [1:] to exclude the player's name

# Convert values to a single-dimensional list
    values = selected_player_values.tolist()



# Extract player's values for each parameter


# Set title and subtitle for the radar chart
    title = {
        "title_name": selected_player,
        "title_color": "#000000",
        "subtitle_name": player_subtitles[selected_player],
        "subtitle_color": "#B6282F",
        "title_name_2": "Radar Chart",
        "subtitle_name_2": "FW",
        "subtitle_color_2": "#B6282F",
        "title_fontsize": 18,
        "subtitle_fontsize": 15,
    }

# Create a Radar instance
    radar = Radar(label_fontsize=12, range_fontsize=7.5)

# Plot the radar chart using soccerplots
    fig, ax = radar.plot_radar(
        ranges=ranges,
        params=params,
        values=[values],
        radar_color=['orange'],
        alphas=[0.4],
        title=title,
        compare=True
    )

# Add image to the radar chart
# Assuming you have a function add_image that can add an image to the chart

# Display the radar chart with Streamlit
    st.pyplot(fig)


    col1, col2 = st.columns(2)

    # Player selection
    selected_player1 = col1.selectbox("Select Player 1", list(player_subtitles.keys()))
    selected_player2 = col2.selectbox("Select Player 2", list(player_subtitles.keys()))



    # Get data for the selected player
    player_data1 = df_2[df_2['Player'] == selected_player1] 
    player_data2 = df_2[df_2['Player'] == selected_player2]  # Use your appropriate dataframe here


    # Calculate ranges for each parameter
    ranges = []
    a_values = []
    b_values = []


    for x in params:
        a = min(df_2[params][x])
        a = a - (a*.05)
    
        b = max(df_2[params][x])
        b = b + (b*.05)
    
  
    
    
        ranges.append((a,b))
    

    # Extract player's values for each parameter
    # Extract player's values for the selected player
    selected_player_values1 = player_data1.iloc[0].values[1:]  # Use [1:] to exclude the player's name
    selected_player_values2 = player_data2.iloc[0].values[1:]  # Use [1:] to exclude the player's name


    # Convert values to a single-dimensional list
    values1 = selected_player_values1.tolist()
    values2 = selected_player_values2.tolist()
    values=[values1,values2]







    # Set title and subtitle for the radar chart
    title = {
        "title_name": selected_player1,
        "title_color": "#000000",
        "subtitle_name": player_subtitles[selected_player1],
        "subtitle_color": "#B6282F",
        "title_name_2": selected_player2,
        "subtitle_name_2": player_subtitles[selected_player2],
        "subtitle_color_2": "#B6282F",
        "title_fontsize": 18,
        "subtitle_fontsize": 15,
    }

    # Create a Radar instance
    radar = Radar(label_fontsize=12, range_fontsize=7.5)

    # Plot the radar chart using soccerplots
    fig, ax = radar.plot_radar(
        ranges=ranges,
        params=params,
        values=values,  # Ensure this is a list of lists
        radar_color=['Red', 'Blue'],  # Adjust the colors as needed
        alphas=[0.75, 0.6],  # Ensure this has the same length as values and radar_color
        title=title,
        compare=True
    )



    # Display the radar chart with Streamlit
    st.pyplot(fig)



elif selected_year == "2021/22":
    df_1=pd.read_csv("Shooting(2021-22).csv")
    df_1['SoT%'] = df_1['SoT%'].fillna(df_1.groupby('Pos')['SoT%'].transform('mean'))
    df_1['G/Sh'] = df_1['G/Sh'].fillna(df_1.groupby('Pos')['G/Sh'].transform('mean'))
    df_1['G/SoT'] = df_1['G/SoT'].fillna(df_1.groupby('Pos')['G/SoT'].transform('mean'))
    df_1['Dist'] = df_1['Dist'].fillna(df_1.groupby('Pos')['Dist'].transform('mean'))
    df_1['npxG/Sh'] = df_1['npxG/Sh'].fillna(df_1.groupby('Pos')['npxG/Sh'].transform('mean'))   
    df_1 = df_1.drop(['Rk','Nation','Pos','Squad','Age','Born','90s','FK','PK','PKatt','Season'],axis=1)
    #df_2= df_2[(df_2['Player']=='Lionel Messi') |(df_2['Player']=='Karim Benzema')|(df_2['Player']=='Gerard Moreno')|(df_2['Player']=='Luis Suárez')|(df_2['Player']=='Youssef En-Nesyri')|(df_2['Player']=='Alexander Isak')|(df_2['Player']=='Iago Aspas')|(df_2['Player']=='Antoine Griezmann')|(df_2['Player']=='José Luis Morales') | (df_2['Player']=='Rafa Mir')].reset_index()
    #df_2 = df_2.drop(['index'],axis=1)
# Manually filtered list of players with corresponding subtitles
    player_subtitles = {
        'Karim Benzema': 'Real Madrid',
        'Iago Aspas': 'Celta Vigo',
        'Vinicius Júnior': 'Real Madrid',
        'Raúl de Tomás': 'Espanyol',
        'Juanmi': 'Betis',
        'Enes Ünal': 'Getafe',
        'Joselu': 'Alavés',
        'José Luis Morales': 'Levante',
        'Ángel Correa': 'Atlético Madrid',
        'Memphis Depay': 'Barcelona'  
    }

# Create Streamlit app
    st.title("Soccer Player Radar Analysis")

# Select player from the filtered list
    selected_player = st.selectbox("Select a player:", list(player_subtitles.keys()))

# Get data for the selected player
    player_data = df_1[df_1['Player'] == selected_player]  # Use your appropriate dataframe here

# Define parameters for the radar chart
    params = ['Gls', 'Sh', 'SoT', 'SoT%', 'Sh/90', 'SoT/90', 'G/Sh', 'G/SoT', 'Dist', 'xG', 'npxG', 'npxG/Sh', 'G-xG', 'np:G-xG']

# Calculate ranges for each parameter
    ranges = []
    a_values = []
    b_values = []


    for x in params:
        a = min(df_1[params][x])
        a = a - (a*.05)
    
        b = max(df_1[params][x])
        b = b + (b*.05)
    
  
    
    
        ranges.append((a,b))
    

# Extract player's values for each parameter
# Extract player's values for the selected player
    selected_player_values = player_data.iloc[0].values[1:]  # Use [1:] to exclude the player's name

# Convert values to a single-dimensional list
    values = selected_player_values.tolist()



# Extract player's values for each parameter


# Set title and subtitle for the radar chart
    title = {
        "title_name": selected_player,
        "title_color": "#000000",
        "subtitle_name": player_subtitles[selected_player],
        "subtitle_color": "#B6282F",
        "title_name_2": "Radar Chart",
        "subtitle_name_2": "FW",
        "subtitle_color_2": "#B6282F",
        "title_fontsize": 18,
        "subtitle_fontsize": 15,
    }

# Create a Radar instance
    radar = Radar(label_fontsize=12, range_fontsize=7.5)

# Plot the radar chart using soccerplots
    fig, ax = radar.plot_radar(
        ranges=ranges,
        params=params,
        values=[values],
        radar_color=['orange'],
        alphas=[0.4],
        title=title,
        compare=True
    )

# Add image to the radar chart
# Assuming you have a function add_image that can add an image to the chart

# Display the radar chart with Streamlit
    st.pyplot(fig)

    col1, col2 = st.columns(2)

    # Player selection
    selected_player1 = col1.selectbox("Select Player 1", list(player_subtitles.keys()))
    selected_player2 = col2.selectbox("Select Player 2", list(player_subtitles.keys()))



    # Get data for the selected player
    player_data1 = df_1[df_1['Player'] == selected_player1] 
    player_data2 = df_1[df_1['Player'] == selected_player2]  # Use your appropriate dataframe here


    # Calculate ranges for each parameter
    ranges = []
    a_values = []
    b_values = []


    for x in params:
        a = min(df_1[params][x])
        a = a - (a*.05)
    
        b = max(df_1[params][x])
        b = b + (b*.05)
    
  
    
    
        ranges.append((a,b))
    

    # Extract player's values for each parameter
    # Extract player's values for the selected player
    selected_player_values1 = player_data1.iloc[0].values[1:]  # Use [1:] to exclude the player's name
    selected_player_values2 = player_data2.iloc[0].values[1:]  # Use [1:] to exclude the player's name


    # Convert values to a single-dimensional list
    values1 = selected_player_values1.tolist()
    values2 = selected_player_values2.tolist()
    values=[values1,values2]







    # Set title and subtitle for the radar chart
    title = {
        "title_name": selected_player1,
        "title_color": "#000000",
        "subtitle_name": player_subtitles[selected_player1],
        "subtitle_color": "#B6282F",
        "title_name_2": selected_player2,
        "subtitle_name_2": player_subtitles[selected_player2],
        "subtitle_color_2": "#B6282F",
        "title_fontsize": 18,
        "subtitle_fontsize": 15,
    }

    # Create a Radar instance
    radar = Radar(label_fontsize=12, range_fontsize=7.5)

    # Plot the radar chart using soccerplots
    fig, ax = radar.plot_radar(
        ranges=ranges,
        params=params,
        values=values,  # Ensure this is a list of lists
        radar_color=['Red', 'Blue'],  # Adjust the colors as needed
        alphas=[0.75, 0.6],  # Ensure this has the same length as values and radar_color
        title=title,
        compare=True
    )



    # Display the radar chart with Streamlit
    st.pyplot(fig)


elif selected_year == "2020/21":
    df_2 = pd.read_csv("Shooting(2020-21).csv")
    df_2['SoT%'] = df_2['SoT%'].fillna(df_2.groupby('Pos')['SoT%'].transform('mean'))
    df_2['G/Sh'] = df_2['G/Sh'].fillna(df_2.groupby('Pos')['G/Sh'].transform('mean'))
    df_2['G/SoT'] = df_2['G/SoT'].fillna(df_2.groupby('Pos')['G/SoT'].transform('mean'))
    df_2['Dist'] = df_2['Dist'].fillna(df_2.groupby('Pos')['Dist'].transform('mean'))
    df_2['npxG/Sh'] = df_2['npxG/Sh'].fillna(df_2.groupby('Pos')['npxG/Sh'].transform('mean'))# Update with your actual data source
    df_2 = df_2.drop(['Rk','Nation','Pos','Squad','Age','Born','90s','FK','PK','PKatt','Season'],axis=1)
    #df_2= df_2[(df_2['Player']=='Lionel Messi') |(df_2['Player']=='Karim Benzema')|(df_2['Player']=='Gerard Moreno')|(df_2['Player']=='Luis Suárez')|(df_2['Player']=='Youssef En-Nesyri')|(df_2['Player']=='Alexander Isak')|(df_2['Player']=='Iago Aspas')|(df_2['Player']=='Antoine Griezmann')|(df_2['Player']=='José Luis Morales') | (df_2['Player']=='Rafa Mir')].reset_index()
    #df_2 = df_2.drop(['index'],axis=1)
# Manually filtered list of players with corresponding subtitles
    player_subtitles = {
        'Lionel Messi': 'Barcelona',
        'Karim Benzema': 'Real Madrid',
        'Gerard Moreno': 'Villarreal',
        'Luis Suárez': 'Atletico Madrid',
        'Youssef En-Nesyri': 'Sevilla',
        'Alexander Isak': 'Real Sociedad',
        'Iago Aspas': 'Celta Vigo',
        'Antoine Griezmann': 'Barcelona',
        'José Luis Morales': 'Levante',
        'Rafa Mir': 'Wolves'  # Update with the actual subtitle
    }

# Create Streamlit app
    st.title("Soccer Player Radar Analysis")

# Select player from the filtered list
    selected_player = st.selectbox("Select a player:", list(player_subtitles.keys()))

# Get data for the selected player
    player_data = df_2[df_2['Player'] == selected_player]  # Use your appropriate dataframe here

# Define parameters for the radar chart
    params = ['Gls', 'Sh', 'SoT', 'SoT%', 'Sh/90', 'SoT/90', 'G/Sh', 'G/SoT', 'Dist', 'xG', 'npxG', 'npxG/Sh', 'G-xG', 'np:G-xG']

# Calculate ranges for each parameter
    ranges = []
    a_values = []
    b_values = []


    for x in params:
        a = min(df_2[params][x])
        a = a - (a*.05)
    
        b = max(df_2[params][x])
        b = b + (b*.05)
    
  
    
    
        ranges.append((a,b))
    

# Extract player's values for each parameter
# Extract player's values for the selected player
    selected_player_values = player_data.iloc[0].values[1:]  # Use [1:] to exclude the player's name

# Convert values to a single-dimensional list
    values = selected_player_values.tolist()



# Extract player's values for each parameter


# Set title and subtitle for the radar chart
    title = {
        "title_name": selected_player,
        "title_color": "#000000",
        "subtitle_name": player_subtitles[selected_player],
        "subtitle_color": "#B6282F",
        "title_name_2": "Radar Chart",
        "subtitle_name_2": "FW",
        "subtitle_color_2": "#B6282F",
        "title_fontsize": 18,
        "subtitle_fontsize": 15,
    }

# Create a Radar instance
    radar = Radar(label_fontsize=12, range_fontsize=7.5)

# Plot the radar chart using soccerplots
    fig, ax = radar.plot_radar(
        ranges=ranges,
        params=params,
        values=[values],
        radar_color=['orange'],
        alphas=[0.4],
        title=title,
        compare=True
    )

# Add image to the radar chart
# Assuming you have a function add_image that can add an image to the chart

# Display the radar chart with Streamlit
    st.pyplot(fig)

    col1, col2 = st.columns(2)

    # Player selection
    selected_player1 = col1.selectbox("Select Player 1", list(player_subtitles.keys()))
    selected_player2 = col2.selectbox("Select Player 2", list(player_subtitles.keys()))



    # Get data for the selected player
    player_data1 = df_2[df_2['Player'] == selected_player1] 
    player_data2 = df_2[df_2['Player'] == selected_player2]  # Use your appropriate dataframe here


    # Calculate ranges for each parameter
    ranges = []
    a_values = []
    b_values = []


    for x in params:
        a = min(df_2[params][x])
        a = a - (a*.05)
    
        b = max(df_2[params][x])
        b = b + (b*.05)
    
  
    
    
        ranges.append((a,b))
    

    # Extract player's values for each parameter
    # Extract player's values for the selected player
    selected_player_values1 = player_data1.iloc[0].values[1:]  # Use [1:] to exclude the player's name
    selected_player_values2 = player_data2.iloc[0].values[1:]  # Use [1:] to exclude the player's name


    # Convert values to a single-dimensional list
    values1 = selected_player_values1.tolist()
    values2 = selected_player_values2.tolist()
    values=[values1,values2]







    # Set title and subtitle for the radar chart
    title = {
        "title_name": selected_player1,
        "title_color": "#000000",
        "subtitle_name": player_subtitles[selected_player1],
        "subtitle_color": "#B6282F",
        "title_name_2": selected_player2,
        "subtitle_name_2": player_subtitles[selected_player2],
        "subtitle_color_2": "#B6282F",
        "title_fontsize": 18,
        "subtitle_fontsize": 15,
    }

    # Create a Radar instance
    radar = Radar(label_fontsize=12, range_fontsize=7.5)

    # Plot the radar chart using soccerplots
    fig, ax = radar.plot_radar(
        ranges=ranges,
        params=params,
        values=values,  # Ensure this is a list of lists
        radar_color=['Red', 'Blue'],  # Adjust the colors as needed
        alphas=[0.75, 0.6],  # Ensure this has the same length as values and radar_color
        title=title,
        compare=True
    )



    # Display the radar chart with Streamlit
    st.pyplot(fig)



elif selected_year == "2019/20":
    df_3=pd.read_csv("Shooting(2019-20).csv")
    df_3['SoT%'] = df_3['SoT%'].fillna(df_3.groupby('Pos')['SoT%'].transform('mean'))
    df_3['G/Sh'] = df_3['G/Sh'].fillna(df_3.groupby('Pos')['G/Sh'].transform('mean'))
    df_3['G/SoT'] = df_3['G/SoT'].fillna(df_3.groupby('Pos')['G/SoT'].transform('mean'))
    df_3['Dist'] = df_3['Dist'].fillna(df_3.groupby('Pos')['Dist'].transform('mean'))
    df_3['npxG/Sh'] = df_3['npxG/Sh'].fillna(df_3.groupby('Pos')['npxG/Sh'].transform('mean'))
    df_3 = df_3.drop(['Rk','Nation','Pos','Squad','Age','Born','90s','FK','PK','PKatt','Season'],axis=1)
    #df_2= df_2[(df_2['Player']=='Lionel Messi') |(df_2['Player']=='Karim Benzema')|(df_2['Player']=='Gerard Moreno')|(df_2['Player']=='Luis Suárez')|(df_2['Player']=='Youssef En-Nesyri')|(df_2['Player']=='Alexander Isak')|(df_2['Player']=='Iago Aspas')|(df_2['Player']=='Antoine Griezmann')|(df_2['Player']=='José Luis Morales') | (df_2['Player']=='Rafa Mir')].reset_index()
    #df_2 = df_2.drop(['index'],axis=1)
# Manually filtered list of players with corresponding subtitles
    player_subtitles = {
        'Lionel Messi': 'Barcelona',
        'Karim Benzema': 'Real Madrid',
        'Gerard Moreno': 'Villarreal',
        'Luis Suárez': 'Barcelona',
        'Raúl García': 'Athletic Club',
        'Iago Aspas': 'Celta Vigo',
        'Lucas Ocampos': 'Sevilla',
        'Ante Budimir': 'Mallorca',
        'Álvaro Morata': 'Atlético Madrid',
        'Santi Cazorla': 'Villarreal'
}

# Create Streamlit app
    st.title("Soccer Player Radar Analysis")

# Select player from the filtered list
    selected_player = st.selectbox("Select a player:", list(player_subtitles.keys()))

# Get data for the selected player
    player_data = df_3[df_3['Player'] == selected_player]  # Use your appropriate dataframe here

# Define parameters for the radar chart
    params = ['Gls', 'Sh', 'SoT', 'SoT%', 'Sh/90', 'SoT/90', 'G/Sh', 'G/SoT', 'Dist', 'xG', 'npxG', 'npxG/Sh', 'G-xG', 'np:G-xG']

# Calculate ranges for each parameter
    ranges = []
    a_values = []
    b_values = []


    for x in params:
        a = min(df_3[params][x])
        a = a - (a*.05)
    
        b = max(df_3[params][x])
        b = b + (b*.05)
    
  
    
    
        ranges.append((a,b))
    

# Extract player's values for each parameter
# Extract player's values for the selected player
    selected_player_values = player_data.iloc[0].values[1:]  # Use [1:] to exclude the player's name

# Convert values to a single-dimensional list
    values = selected_player_values.tolist()



# Extract player's values for each parameter


# Set title and subtitle for the radar chart
    title = {
        "title_name": selected_player,
        "title_color": "#000000",
        "subtitle_name": player_subtitles[selected_player],
        "subtitle_color": "#B6282F",
        "title_name_2": "Radar Chart",
        "subtitle_name_2": "FW",
        "subtitle_color_2": "#B6282F",
        "title_fontsize": 18,
        "subtitle_fontsize": 15,
    }

# Create a Radar instance
    radar = Radar(label_fontsize=12, range_fontsize=7.5)

# Plot the radar chart using soccerplots
    fig, ax = radar.plot_radar(
        ranges=ranges,
        params=params,
        values=[values],
        radar_color=['orange'],
        alphas=[0.4],
        title=title,
        compare=True
    )

# Add image to the radar chart
# Assuming you have a function add_image that can add an image to the chart

# Display the radar chart with Streamlit
    st.pyplot(fig)

    col1, col2 = st.columns(2)

    # Player selection
    selected_player1 = col1.selectbox("Select Player 1", list(player_subtitles.keys()))
    selected_player2 = col2.selectbox("Select Player 2", list(player_subtitles.keys()))



    # Get data for the selected player
    player_data1 = df_3[df_3['Player'] == selected_player1] 
    player_data2 = df_3[df_3['Player'] == selected_player2]  # Use your appropriate dataframe here


    # Calculate ranges for each parameter
    ranges = []
    a_values = []
    b_values = []


    for x in params:
        a = min(df_3[params][x])
        a = a - (a*.05)
    
        b = max(df_3[params][x])
        b = b + (b*.05)
    
  
    
    
        ranges.append((a,b))
    

    # Extract player's values for each parameter
    # Extract player's values for the selected player
    selected_player_values1 = player_data1.iloc[0].values[1:]  # Use [1:] to exclude the player's name
    selected_player_values2 = player_data2.iloc[0].values[1:]  # Use [1:] to exclude the player's name


    # Convert values to a single-dimensional list
    values1 = selected_player_values1.tolist()
    values2 = selected_player_values2.tolist()
    values=[values1,values2]







    # Set title and subtitle for the radar chart
    title = {
        "title_name": selected_player1,
        "title_color": "#000000",
        "subtitle_name": player_subtitles[selected_player1],
        "subtitle_color": "#B6282F",
        "title_name_2": selected_player2,
        "subtitle_name_2": player_subtitles[selected_player2],
        "subtitle_color_2": "#B6282F",
        "title_fontsize": 18,
        "subtitle_fontsize": 15,
    }

    # Create a Radar instance
    radar = Radar(label_fontsize=12, range_fontsize=7.5)

    # Plot the radar chart using soccerplots
    fig, ax = radar.plot_radar(
        ranges=ranges,
        params=params,
        values=values,  # Ensure this is a list of lists
        radar_color=['Red', 'Blue'],  # Adjust the colors as needed
        alphas=[0.75, 0.6],  # Ensure this has the same length as values and radar_color
        title=title,
        compare=True
    )



    # Display the radar chart with Streamlit
    st.pyplot(fig)


elif selected_year == "2018/19":
    df_4 = pd.read_csv("Shooting(2018-19).csv")
    df_4['SoT%'] = df_4['SoT%'].fillna(df_4.groupby('Pos')['SoT%'].transform('mean'))
    df_4['G/Sh'] = df_4['G/Sh'].fillna(df_4.groupby('Pos')['G/Sh'].transform('mean'))
    df_4['G/SoT'] = df_4['G/SoT'].fillna(df_4.groupby('Pos')['G/SoT'].transform('mean'))
    df_4['Dist'] = df_4['Dist'].fillna(df_4.groupby('Pos')['Dist'].transform('mean'))
    df_4['npxG/Sh'] = df_4['npxG/Sh'].fillna(df_4.groupby('Pos')['npxG/Sh'].transform('mean'))
    df_4['G/SoT'] = df_4['G/SoT'].fillna(df_4.groupby('Squad')['G/SoT'].transform('mean'))
    df_4 = df_4.drop(['Rk','Nation','Pos','Squad','Age','Born','90s','FK','PK','PKatt','Season'],axis=1)
    #df_2= df_2[(df_2['Player']=='Lionel Messi') |(df_2['Player']=='Karim Benzema')|(df_2['Player']=='Gerard Moreno')|(df_2['Player']=='Luis Suárez')|(df_2['Player']=='Youssef En-Nesyri')|(df_2['Player']=='Alexander Isak')|(df_2['Player']=='Iago Aspas')|(df_2['Player']=='Antoine Griezmann')|(df_2['Player']=='José Luis Morales') | (df_2['Player']=='Rafa Mir')].reset_index()
    #df_2 = df_2.drop(['index'],axis=1)
# Manually filtered list of players with corresponding subtitles
    player_subtitles = {
        'Lionel Messi': 'Barcelona',
        'Karim Benzema': 'Real Madrid',
        'Gerard Moreno': 'Villarreal',
        'Luis Suárez': 'Atletico Madrid',
        'Youssef En-Nesyri': 'Sevilla',
        'Alexander Isak': 'Real Sociedad',
        'Iago Aspas': 'Celta Vigo',
        'Antoine Griezmann': 'Barcelona',
        'José Luis Morales': 'Levante',
        'Rafa Mir': 'Wolves'  # Update with the actual subtitle
    }

# Create Streamlit app
    st.title("Soccer Player Radar Analysis")

# Select player from the filtered list
    selected_player = st.selectbox("Select a player:", list(player_subtitles.keys()))

# Get data for the selected player
    player_data = df_4[df_4['Player'] == selected_player]  # Use your appropriate dataframe here

# Define parameters for the radar chart
    params = ['Gls', 'Sh', 'SoT', 'SoT%', 'Sh/90', 'SoT/90', 'G/Sh', 'G/SoT', 'Dist', 'xG', 'npxG', 'npxG/Sh', 'G-xG', 'np:G-xG']

# Calculate ranges for each parameter
    ranges = []
    a_values = []
    b_values = []


    for x in params:
        a = min(df_4[params][x])
        a = a - (a*.05)
    
        b = max(df_4[params][x])
        b = b + (b*.05)
    
  
    
    
        ranges.append((a,b))
    

# Extract player's values for each parameter
# Extract player's values for the selected player
    selected_player_values = player_data.iloc[0].values[1:]  # Use [1:] to exclude the player's name

# Convert values to a single-dimensional list
    values = selected_player_values.tolist()



# Extract player's values for each parameter


# Set title and subtitle for the radar chart
    title = {
        "title_name": selected_player,
        "title_color": "#000000",
        "subtitle_name": player_subtitles[selected_player],
        "subtitle_color": "#B6282F",
        "title_name_2": "Radar Chart",
        "subtitle_name_2": "FW",
        "subtitle_color_2": "#B6282F",
        "title_fontsize": 18,
        "subtitle_fontsize": 15,
    }

# Create a Radar instance
    radar = Radar(label_fontsize=12, range_fontsize=7.5)

# Plot the radar chart using soccerplots
    fig, ax = radar.plot_radar(
        ranges=ranges,
        params=params,
        values=[values],
        radar_color=['orange'],
        alphas=[0.4],
        title=title,
        compare=True
    )

# Add image to the radar chart
# Assuming you have a function add_image that can add an image to the chart

# Display the radar chart with Streamlit
    st.pyplot(fig)

    col1, col2 = st.columns(2)

    # Player selection
    selected_player1 = col1.selectbox("Select Player 1", list(player_subtitles.keys()))
    selected_player2 = col2.selectbox("Select Player 2", list(player_subtitles.keys()))



    # Get data for the selected player
    player_data1 = df_4[df_4['Player'] == selected_player1] 
    player_data2 = df_4[df_4['Player'] == selected_player2]  # Use your appropriate dataframe here


    # Calculate ranges for each parameter
    ranges = []
    a_values = []
    b_values = []


    for x in params:
        a = min(df_4[params][x])
        a = a - (a*.05)
    
        b = max(df_4[params][x])
        b = b + (b*.05)
    
  
    
    
        ranges.append((a,b))
    

    # Extract player's values for each parameter
    # Extract player's values for the selected player
    selected_player_values1 = player_data1.iloc[0].values[1:]  # Use [1:] to exclude the player's name
    selected_player_values2 = player_data2.iloc[0].values[1:]  # Use [1:] to exclude the player's name


    # Convert values to a single-dimensional list
    values1 = selected_player_values1.tolist()
    values2 = selected_player_values2.tolist()
    values=[values1,values2]







    # Set title and subtitle for the radar chart
    title = {
        "title_name": selected_player1,
        "title_color": "#000000",
        "subtitle_name": player_subtitles[selected_player1],
        "subtitle_color": "#B6282F",
        "title_name_2": selected_player2,
        "subtitle_name_2": player_subtitles[selected_player2],
        "subtitle_color_2": "#B6282F",
        "title_fontsize": 18,
        "subtitle_fontsize": 15,
    }

    # Create a Radar instance
    radar = Radar(label_fontsize=12, range_fontsize=7.5)

    # Plot the radar chart using soccerplots
    fig, ax = radar.plot_radar(
        ranges=ranges,
        params=params,
        values=values,  # Ensure this is a list of lists
        radar_color=['Red', 'Blue'],  # Adjust the colors as needed
        alphas=[0.75, 0.6],  # Ensure this has the same length as values and radar_color
        title=title,
        compare=True
    )



    # Display the radar chart with Streamlit
    st.pyplot(fig)


elif selected_year == "2017/18":
    df_5 = pd.read_csv("Shooting(2017-18).csv")
    df_5['SoT%'] = df_5['SoT%'].fillna(df_5.groupby('Pos')['SoT%'].transform('mean'))
    df_5['G/Sh'] = df_5['G/Sh'].fillna(df_5.groupby('Pos')['G/Sh'].transform('mean'))
    df_5['G/SoT'] = df_5['G/SoT'].fillna(df_5.groupby('Pos')['G/SoT'].transform('mean'))
    df_5['Dist'] = df_5['Dist'].fillna(df_5.groupby('Pos')['Dist'].transform('mean'))
    df_5['npxG/Sh'] = df_5['npxG/Sh'].fillna(df_5.groupby('Pos')['npxG/Sh'].transform('mean'))
    df_5['G/SoT'] = df_5['G/SoT'].fillna(df_5.groupby('Squad')['G/SoT'].transform('mean'))
    df_5 = df_5.drop(['Rk','Nation','Pos','Squad','Age','Born','90s','FK','PK','PKatt','Season'],axis=1)
    #df_2= df_2[(df_2['Player']=='Lionel Messi') |(df_2['Player']=='Karim Benzema')|(df_2['Player']=='Gerard Moreno')|(df_2['Player']=='Luis Suárez')|(df_2['Player']=='Youssef En-Nesyri')|(df_2['Player']=='Alexander Isak')|(df_2['Player']=='Iago Aspas')|(df_2['Player']=='Antoine Griezmann')|(df_2['Player']=='José Luis Morales') | (df_2['Player']=='Rafa Mir')].reset_index()
    #df_2 = df_2.drop(['index'],axis=1)
# Manually filtered list of players with corresponding subtitles
    player_subtitles = {
        'Lionel Messi': 'Barcelona',
        'Cristiano Ronaldo': 'Real Madrid',
        'Luis Suárez': 'Barcelona',
        'Iago Aspas': 'Celta Vigo',
        'Cristhian Stuani': 'Girona',
        'Antoine Griezmann': 'Atlético Madrid',
        'Maxi Gómez': 'Celta Vigo',
        'Gareth Bale': 'Real Madrid',
        'Gerard Moreno': 'Espanyol',
        'Rodrigo': 'Valencia'
    }

# Create Streamlit app
    st.title("Soccer Player Radar Analysis")

# Select player from the filtered list
    selected_player = st.selectbox("Select a player:", list(player_subtitles.keys()))

# Get data for the selected player
    player_data = df_5[df_5['Player'] == selected_player]  # Use your appropriate dataframe here

# Define parameters for the radar chart
    params = ['Gls', 'Sh', 'SoT', 'SoT%', 'Sh/90', 'SoT/90', 'G/Sh', 'G/SoT', 'Dist', 'xG', 'npxG', 'npxG/Sh', 'G-xG', 'np:G-xG']

# Calculate ranges for each parameter
    ranges = []
    a_values = []
    b_values = []


    for x in params:
        a = min(df_5[params][x])
        a = a - (a*.05)
    
        b = max(df_5[params][x])
        b = b + (b*.05)
    
  
    
    
        ranges.append((a,b))
    

# Extract player's values for each parameter
# Extract player's values for the selected player
    selected_player_values = player_data.iloc[0].values[1:]  # Use [1:] to exclude the player's name

# Convert values to a single-dimensional list
    values = selected_player_values.tolist()



# Extract player's values for each parameter


# Set title and subtitle for the radar chart
    title = {
        "title_name": selected_player,
        "title_color": "#000000",
        "subtitle_name": player_subtitles[selected_player],
        "subtitle_color": "#B6282F",
        "title_name_2": "Radar Chart",
        "subtitle_name_2": "FW",
        "subtitle_color_2": "#B6282F",
        "title_fontsize": 18,
        "subtitle_fontsize": 15,
    }

# Create a Radar instance
    radar = Radar(label_fontsize=12, range_fontsize=7.5)

# Plot the radar chart using soccerplots
    fig, ax = radar.plot_radar(
        ranges=ranges,
        params=params,
        values=[values],
        radar_color=['orange'],
        alphas=[0.4],
        title=title,
        compare=True
    )

# Add image to the radar chart
# Assuming you have a function add_image that can add an image to the chart

# Display the radar chart with Streamlit
    st.pyplot(fig)

    col1, col2 = st.columns(2)

    # Player selection
    selected_player1 = col1.selectbox("Select Player 1", list(player_subtitles.keys()))
    selected_player2 = col2.selectbox("Select Player 2", list(player_subtitles.keys()))



    # Get data for the selected player
    player_data1 = df_5[df_5['Player'] == selected_player1] 
    player_data2 = df_5[df_5['Player'] == selected_player2]  # Use your appropriate dataframe here


    # Calculate ranges for each parameter
    ranges = []
    a_values = []
    b_values = []


    for x in params:
        a = min(df_5[params][x])
        a = a - (a*.05)
    
        b = max(df_5[params][x])
        b = b + (b*.05)
    
  
    
    
        ranges.append((a,b))
    

    # Extract player's values for each parameter
    # Extract player's values for the selected player
    selected_player_values1 = player_data1.iloc[0].values[1:]  # Use [1:] to exclude the player's name
    selected_player_values2 = player_data2.iloc[0].values[1:]  # Use [1:] to exclude the player's name


    # Convert values to a single-dimensional list
    values1 = selected_player_values1.tolist()
    values2 = selected_player_values2.tolist()
    values=[values1,values2]







    # Set title and subtitle for the radar chart
    title = {
        "title_name": selected_player1,
        "title_color": "#000000",
        "subtitle_name": player_subtitles[selected_player1],
        "subtitle_color": "#B6282F",
        "title_name_2": selected_player2,
        "subtitle_name_2": player_subtitles[selected_player2],
        "subtitle_color_2": "#B6282F",
        "title_fontsize": 18,
        "subtitle_fontsize": 15,
    }

    # Create a Radar instance
    radar = Radar(label_fontsize=12, range_fontsize=7.5)

    # Plot the radar chart using soccerplots
    fig, ax = radar.plot_radar(
        ranges=ranges,
        params=params,
        values=values,  # Ensure this is a list of lists
        radar_color=['Red', 'Blue'],  # Adjust the colors as needed
        alphas=[0.75, 0.6],  # Ensure this has the same length as values and radar_color
        title=title,
        compare=True
    )



    # Display the radar chart with Streamlit
    st.pyplot(fig)



elif selected_year == "2016/17":
    df=pd.read_csv("shooting.csv")
    df_6 = pd.read_csv("Shooting(2016-17).csv")
    df_6['SoT%'] = df_6['SoT%'].fillna(df_6.groupby('Pos')['SoT%'].transform('mean'))
    df_6['G/Sh'] = df_6['G/Sh'].fillna(df_6.groupby('Pos')['G/Sh'].transform('mean'))
    df_6['G/SoT'] = df_6['G/SoT'].fillna(df_6.groupby('Pos')['G/SoT'].transform('mean'))
    df_6['Dist'] = df_6['Dist'].fillna(df.groupby('Player')['Dist'].transform('mean'))
    df_6['Dist'] = df_6['Dist'].fillna(df.groupby('Pos')['Dist'].transform('mean'))
    df_6['xG'] = df_6['xG'].fillna(df.groupby('Player')['xG'].transform('mean'))
    df_6['npxG'] = df_6['npxG'].fillna(df.groupby('Player')['npxG'].transform('mean'))
    df_6['G-xG'] = df_6['G-xG'].fillna(df.groupby('Player')['G-xG'].transform('mean'))
    df_6['np:G-xG'] = df_6['np:G-xG'].fillna(df.groupby('Player')['np:G-xG'].transform('mean'))
    df_6['npxG/Sh'] = df_6['npxG/Sh'].fillna(df.groupby('Player')['npxG/Sh'].transform('mean'))
    df_6['npxG/Sh'] = df_6['npxG/Sh'].fillna(df.groupby('Pos')['npxG/Sh'].transform('mean'))
    df_6 = df_6.drop(['Rk','Nation','Pos','Squad','Age','Born','90s','FK','PK','PKatt','Season'],axis=1)
    #df_2= df_2[(df_2['Player']=='Lionel Messi') |(df_2['Player']=='Karim Benzema')|(df_2['Player']=='Gerard Moreno')|(df_2['Player']=='Luis Suárez')|(df_2['Player']=='Youssef En-Nesyri')|(df_2['Player']=='Alexander Isak')|(df_2['Player']=='Iago Aspas')|(df_2['Player']=='Antoine Griezmann')|(df_2['Player']=='José Luis Morales') | (df_2['Player']=='Rafa Mir')].reset_index()
    #df_2 = df_2.drop(['index'],axis=1)     
# Manually filtered list of players with corresponding subtitles
    player_subtitles = {
        'Lionel Messi': 'Barcelona',
        'Luis Suárez': 'Barcelona',
        'Cristiano Ronaldo': 'Real Madrid',
        'Iago Aspas': 'Celta Vigo',
        'Aritz Aduriz': 'Athletic Club',
        'Antoine Griezmann': 'Atlético Madrid',
        'Álvaro Morata': 'Real Madrid',
        'Sandro Ramírez': 'Málaga',
        'Rubén Castro': 'Betis',
        'Gerard Moreno': 'Espanyol'
    }


# Create Streamlit app
    st.title("Soccer Player Radar Analysis")

# Select player from the filtered list
    selected_player = st.selectbox("Select a player:", list(player_subtitles.keys()))

# Get data for the selected player
    player_data = df_6[df_6['Player'] == selected_player]  # Use your appropriate dataframe here

# Define parameters for the radar chart
    params = ['Gls', 'Sh', 'SoT', 'SoT%', 'Sh/90', 'SoT/90', 'G/Sh', 'G/SoT', 'Dist', 'xG', 'npxG', 'npxG/Sh', 'G-xG', 'np:G-xG']

# Calculate ranges for each parameter
    ranges = []
    a_values = []
    b_values = []


    for x in params:
        a = min(df_6[params][x])
        a = a - (a*.05)
    
        b = max(df_6[params][x])
        b = b + (b*.05)
    
  
    
    
        ranges.append((a,b))
    

# Extract player's values for each parameter
# Extract player's values for the selected player
    selected_player_values = player_data.iloc[0].values[1:]  # Use [1:] to exclude the player's name

# Convert values to a single-dimensional list
    values = selected_player_values.tolist()



# Extract player's values for each parameter


# Set title and subtitle for the radar chart
    title = {
        "title_name": selected_player,
        "title_color": "#000000",
        "subtitle_name": player_subtitles[selected_player],
        "subtitle_color": "#B6282F",
        "title_name_2": "Radar Chart",
        "subtitle_name_2": "FW",
        "subtitle_color_2": "#B6282F",
        "title_fontsize": 18,
        "subtitle_fontsize": 15,
    }

# Create a Radar instance
    radar = Radar(label_fontsize=12, range_fontsize=7.5)

# Plot the radar chart using soccerplots
    fig, ax = radar.plot_radar(
        ranges=ranges,
        params=params,
        values=[values],
        radar_color=['orange'],
        alphas=[0.4],
        title=title,
        compare=True
    )

# Add image to the radar chart
# Assuming you have a function add_image that can add an image to the chart

# Display the radar chart with Streamlit
    st.pyplot(fig)

    col1, col2 = st.columns(2)

    # Player selection
    selected_player1 = col1.selectbox("Select Player 1", list(player_subtitles.keys()))
    selected_player2 = col2.selectbox("Select Player 2", list(player_subtitles.keys()))



    # Get data for the selected player
    player_data1 = df_6[df_6['Player'] == selected_player1] 
    player_data2 = df_6[df_6['Player'] == selected_player2]  # Use your appropriate dataframe here


    # Calculate ranges for each parameter
    ranges = []
    a_values = []
    b_values = []


    for x in params:
        a = min(df_6[params][x])
        a = a - (a*.05)
    
        b = max(df_6[params][x])
        b = b + (b*.05)
    
  
    
    
        ranges.append((a,b))
    

    # Extract player's values for each parameter
    # Extract player's values for the selected player
    selected_player_values1 = player_data1.iloc[0].values[1:]  # Use [1:] to exclude the player's name
    selected_player_values2 = player_data2.iloc[0].values[1:]  # Use [1:] to exclude the player's name


    # Convert values to a single-dimensional list
    values1 = selected_player_values1.tolist()
    values2 = selected_player_values2.tolist()
    values=[values1,values2]







    # Set title and subtitle for the radar chart
    title = {
        "title_name": selected_player1,
        "title_color": "#000000",
        "subtitle_name": player_subtitles[selected_player1],
        "subtitle_color": "#B6282F",
        "title_name_2": selected_player2,
        "subtitle_name_2": player_subtitles[selected_player2],
        "subtitle_color_2": "#B6282F",
        "title_fontsize": 18,
        "subtitle_fontsize": 15,
    }

    # Create a Radar instance
    radar = Radar(label_fontsize=12, range_fontsize=7.5)

    # Plot the radar chart using soccerplots
    fig, ax = radar.plot_radar(
        ranges=ranges,
        params=params,
        values=values,  # Ensure this is a list of lists
        radar_color=['Red', 'Blue'],  # Adjust the colors as needed
        alphas=[0.75, 0.6],  # Ensure this has the same length as values and radar_color
        title=title,
        compare=True
    )



    # Display the radar chart with Streamlit
    st.pyplot(fig)




elif selected_year == "2015/16":
    df=pd.read_csv("shooting.csv")
    df_7 = pd.read_csv("Shooting(2015-16).csv")
    df_7['SoT%'] = df_7['SoT%'].fillna(df_7.groupby('Pos')['SoT%'].transform('mean'))
    df_7['G/Sh'] = df_7['G/Sh'].fillna(df_7.groupby('Pos')['G/Sh'].transform('mean'))
    df_7['G/SoT'] = df_7['G/SoT'].fillna(df_7.groupby('Pos')['G/SoT'].transform('mean'))
    df_7['Dist'] = df_7['Dist'].fillna(df.groupby('Player')['Dist'].transform('mean'))
    df_7['Dist'] = df_7['Dist'].fillna(df.groupby('Pos')['Dist'].transform('mean'))
    df_7['xG'] = df_7['xG'].fillna(df.groupby('Player')['xG'].transform('mean'))
    df_7['npxG'] = df_7['npxG'].fillna(df.groupby('Player')['npxG'].transform('mean'))
    df_7['G-xG'] = df_7['G-xG'].fillna(df.groupby('Player')['G-xG'].transform('mean'))
    df_7['np:G-xG'] = df_7['np:G-xG'].fillna(df.groupby('Player')['np:G-xG'].transform('mean'))
    df_7['npxG/Sh'] = df_7['npxG/Sh'].fillna(df.groupby('Player')['npxG/Sh'].transform('mean'))
    df_7['npxG/Sh'] = df_7['npxG/Sh'].fillna(df.groupby('Pos')['npxG/Sh'].transform('mean'))
    df_7 = df_7.drop(['Rk','Nation','Pos','Squad','Age','Born','90s','FK','PK','PKatt','Season'],axis=1)
    #df_2= df_2[(df_2['Player']=='Lionel Messi') |(df_2['Player']=='Karim Benzema')|(df_2['Player']=='Gerard Moreno')|(df_2['Player']=='Luis Suárez')|(df_2['Player']=='Youssef En-Nesyri')|(df_2['Player']=='Alexander Isak')|(df_2['Player']=='Iago Aspas')|(df_2['Player']=='Antoine Griezmann')|(df_2['Player']=='José Luis Morales') | (df_2['Player']=='Rafa Mir')].reset_index()
    #df_2 = df_2.drop(['index'],axis=1)
# Manually filtered list of players with corresponding subtitles
    player_subtitles = {
        'Luis Suárez': 'Barcelona',
        'Cristiano Ronaldo': 'Real Madrid',
        'Lionel Messi': 'Barcelona',
        'Karim Benzema': 'Real Madrid',
        'Neymar': 'Barcelona',
        'Antoine Griezmann': 'Atlético Madrid',
        'Aritz Aduriz': 'Athletic Club',
        'Gareth Bale': 'Real Madrid',
        'Rubén Castro': 'Betis',
        'Borja Bastón': 'Eibar'
}


# Create Streamlit app
    st.title("Soccer Player Radar Analysis")

# Select player from the filtered list
    selected_player = st.selectbox("Select a player:", list(player_subtitles.keys()))

# Get data for the selected player
    player_data = df_7[df_7['Player'] == selected_player]  # Use your appropriate dataframe here

# Define parameters for the radar chart
    params = ['Gls', 'Sh', 'SoT', 'SoT%', 'Sh/90', 'SoT/90', 'G/Sh', 'G/SoT', 'Dist', 'xG', 'npxG', 'npxG/Sh', 'G-xG', 'np:G-xG']

# Calculate ranges for each parameter
    ranges = []
    a_values = []
    b_values = []


    for x in params:
        a = min(df_7[params][x])
        a = a - (a*.05)
    
        b = max(df_7[params][x])
        b = b + (b*.05)
    
  
    
    
        ranges.append((a,b))
    

# Extract player's values for each parameter
# Extract player's values for the selected player
    selected_player_values = player_data.iloc[0].values[1:]  # Use [1:] to exclude the player's name

# Convert values to a single-dimensional list
    values = selected_player_values.tolist()



# Extract player's values for each parameter


# Set title and subtitle for the radar chart
    title = {
        "title_name": selected_player,
        "title_color": "#000000",
        "subtitle_name": player_subtitles[selected_player],
        "subtitle_color": "#B6282F",
        "title_name_2": "Radar Chart",
        "subtitle_name_2": "FW",
        "subtitle_color_2": "#B6282F",
        "title_fontsize": 18,
        "subtitle_fontsize": 15,
    }

# Create a Radar instance
    radar = Radar(label_fontsize=12, range_fontsize=7.5)

# Plot the radar chart using soccerplots
    fig, ax = radar.plot_radar(
        ranges=ranges,
        params=params,
        values=[values],
        radar_color=['orange'],
        alphas=[0.4],
        title=title,
        compare=True
    )

# Add image to the radar chart
# Assuming you have a function add_image that can add an image to the chart

# Display the radar chart with Streamlit
    st.pyplot(fig)

    col1, col2 = st.columns(2)

    # Player selection
    selected_player1 = col1.selectbox("Select Player 1", list(player_subtitles.keys()))
    selected_player2 = col2.selectbox("Select Player 2", list(player_subtitles.keys()))



    # Get data for the selected player
    player_data1 = df_7[df_7['Player'] == selected_player1] 
    player_data2 = df_7[df_7['Player'] == selected_player2]  # Use your appropriate dataframe here


    # Calculate ranges for each parameter
    ranges = []
    a_values = []
    b_values = []


    for x in params:
        a = min(df_7[params][x])
        a = a - (a*.05)
    
        b = max(df_7[params][x])
        b = b + (b*.05)
    
  
    
    
        ranges.append((a,b))
    

    # Extract player's values for each parameter
    # Extract player's values for the selected player
    selected_player_values1 = player_data1.iloc[0].values[1:]  # Use [1:] to exclude the player's name
    selected_player_values2 = player_data2.iloc[0].values[1:]  # Use [1:] to exclude the player's name


    # Convert values to a single-dimensional list
    values1 = selected_player_values1.tolist()
    values2 = selected_player_values2.tolist()
    values=[values1,values2]







    # Set title and subtitle for the radar chart
    title = {
        "title_name": selected_player1,
        "title_color": "#000000",
        "subtitle_name": player_subtitles[selected_player1],
        "subtitle_color": "#B6282F",
        "title_name_2": selected_player2,
        "subtitle_name_2": player_subtitles[selected_player2],
        "subtitle_color_2": "#B6282F",
        "title_fontsize": 18,
        "subtitle_fontsize": 15,
    }

    # Create a Radar instance
    radar = Radar(label_fontsize=12, range_fontsize=7.5)

    # Plot the radar chart using soccerplots
    fig, ax = radar.plot_radar(
        ranges=ranges,
        params=params,
        values=values,  # Ensure this is a list of lists
        radar_color=['Red', 'Blue'],  # Adjust the colors as needed
        alphas=[0.75, 0.6],  # Ensure this has the same length as values and radar_color
        title=title,
        compare=True
    )



    # Display the radar chart with Streamlit
    st.pyplot(fig)