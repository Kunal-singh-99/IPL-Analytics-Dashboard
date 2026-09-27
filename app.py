import pandas as pd
import numpy as np
import streamlit as st
import plotly.express as px
import matplotlib.pyplot as plt

st.set_page_config(page_title="IPL Analytics", page_icon="🏏", layout="wide")


@st.cache_data
def load_data():
    data = pd.read_csv('final_dataset.csv')
    return data

df = load_data()

menu_select = st.sidebar.radio("Navigation", ["Tournament Overview", "Head-to-Head Rivalry"])

if menu_select == "Tournament Overview":
    
    
    st.title(f"Welcome To {menu_select}")
    
    season_sel = st.selectbox("Select The Season",df['season'].unique())
    filtered_df = df[df['season'] == season_sel]
    
    col1 , col2 , col3 = st.columns(3)
    
    with col1:
        st.metric("Total Matches Played ",filtered_df.shape[0])
    with col2:
        st.metric("Total Venues (Cities) Used ",filtered_df['venue'].nunique())
    with col3:
        st.metric("Championship Winner", filtered_df.sort_values('date', ascending=False)['winner'].iloc[0])
        
        
    st.subheader("Visualization")
    
    winner_count = filtered_df['winner'].value_counts().reset_index()
    winner_count.columns = ['Team', 'Wins']
    fig_plotly = px.bar(
        winner_count,
        x='Team',
        y='Wins',
        text_auto=True,
        title=f"Total Wins in {season_sel} Season",
        color='Wins',
        color_continuous_scale='Bluered')
    fig_plotly.update_layout(showlegend=False)
    st.plotly_chart(fig_plotly, use_container_width=True)   
    
elif menu_select == "Head-to-Head Rivalry" :
    
    
    st.title(f"Welcome To {menu_select}")
    
    all_teams = sorted(df['team1'].dropna().unique())
    
    team_col1, team_col2 = st.columns(2)
    with team_col1:
        team_A = st.selectbox("Select Team A", all_teams, index=0)
    with team_col2:
        team_B = st.selectbox("Select Team B", all_teams, index=1)
            
    if team_A == team_B:
        st.warning("Please select two different teams to compare.")
    else:
        rivalry_df = df[((df['team1'] == team_A) & (df['team2'] == team_B)) | 
                        ((df['team1'] == team_B) & (df['team2'] == team_A))]
            
        if rivalry_df.empty:
            st.info(f"No matches found between {team_A} and {team_B}.")
        else:
            h2h_wins = rivalry_df['winner'].value_counts().reset_index()
            h2h_wins.columns = ['Team', 'Wins']
            
            st.write(f"Total Matches Played: **{len(rivalry_df)}**")
                
            fig = px.pie(
                h2h_wins, 
                values='Wins', 
                names='Team', 
                title=f"<b>{team_A} vs {team_B} Win Distribution</b>",
                color_discrete_sequence=["#DB190F", '#FFD700']
            )
            
            fig.update_traces(marker=dict(line=dict(color='white', width=2)))
                
            st.plotly_chart(fig, use_container_width=True)
