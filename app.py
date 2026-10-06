import pandas as pd
import numpy as np
import streamlit as st
import plotly.express as px
import matplotlib.pyplot as plt

from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import Pipeline
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import OneHotEncoder

st.set_page_config(page_title="IPL Analytics Hub", page_icon="🏏", layout="wide")

@st.cache_data
def load_data():
    data = pd.read_csv('final_dataset.csv')
    return data

df = load_data()


@st.cache_resource
def train_model(df):
    # 1. Create the binary target (1 if team1 won, 0 otherwise)
    df['team1_win'] = (df['winner'] == df['team1']).astype(int)
    
    # 2. Define Features and Target
    X = df[['team1', 'team2', 'toss_winner', 'toss_decision', 'venue']]
    y = df['team1_win']
    
    # 3. Build the Pipeline
    preprocessor = ColumnTransformer(
        transformers=[
            ('encoder', OneHotEncoder(sparse_output=False, handle_unknown='ignore'), 
             ['team1', 'team2', 'toss_winner', 'toss_decision', 'venue'])
        ]
    )
    model = Pipeline(steps=[
        ('preprocessor', preprocessor),
        ('classifier', LogisticRegression(max_iter=1000))
    ])
    
    # 4. Train and return the model
    model.fit(X, y)
    return model

# Train it once and store it in memory
ml_model = train_model(df)

st.sidebar.title("Navigation")
menu_select = st.sidebar.radio("Go to:", [
    "Tournament Overview", 
    "Head-to-Head Rivalry", 
    "Player Analytics", 
    "Strategic Insights",
    "Match Predictor"
])

# --- 1. TOURNAMENT OVERVIEW SECTION ---
if menu_select == "Tournament Overview":
    st.title("Tournament Overview")
    st.caption("Analyze historical season-wide footprints, champion timelines, and venue stats.")
    
    season_sel = st.selectbox("Select The Season", sorted(df['season'].unique(), reverse=True))
    filtered_df = df[df['season'] == season_sel]
    
    st.subheader("Season Key Metrics")
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric("Total Matches Played", filtered_df.shape[0], help="Total fixtures played including group stages and playoffs")
    with col2:
        st.metric("Venues Utilized", filtered_df['venue'].nunique(), help="Unique cricket stadiums used over the course of this season")
    with col3:
        final_match_winner = filtered_df.sort_values('date', ascending=False)['winner'].iloc[0]
        st.metric("Championship Winner", f"{final_match_winner}")
        
    st.subheader("Season Leaderboard")
    
    winner_count = filtered_df['winner'].value_counts().reset_index()
    winner_count.columns = ['Team', 'Wins']
    
    fig_plotly = px.bar(
        winner_count,
        x='Team',
        y='Wins',
        text_auto=True,
        title=f"Team Win Distributions — {season_sel} Season",
        color='Wins',
        color_continuous_scale='Viridis'
    )
    fig_plotly.update_layout(xaxis_title="Franchise Team", yaxis_title="Number of Victories", template="plotly_white")
    st.plotly_chart(fig_plotly, use_container_width=True)   

# --- 2. HEAD-TO-HEAD RIVALRY SECTION ---
elif menu_select == "Head-to-Head Rivalry":
    st.title("Head-to-Head Team Rivalry")
    st.caption("Compare face-off statistics, win ratios, and dominant franchises side-by-side.")
    
    all_teams = sorted(df['team1'].dropna().unique())
    
    team_col1, team_col2 = st.columns(2)
    with team_col1:
        team_A = st.selectbox("Select Team A", all_teams, index=0)
    with team_col2:
        team_B = st.selectbox("Select Team B", all_teams, index=1)
            
    if team_A == team_B:
        st.error("Validation Error: Please select two distinct franchise teams to compare historical rivalries.")
    else:
        rivalry_df = df[((df['team1'] == team_A) & (df['team2'] == team_B)) | 
                        ((df['team1'] == team_B) & (df['team2'] == team_A))]
            
        if rivalry_df.empty:
            st.info(f"No historical matches recorded between {team_A} and {team_B} in this dataset.")
        else:
            h2h_wins = rivalry_df['winner'].value_counts().reset_index()
            h2h_wins.columns = ['Team', 'Wins']
            
            st.subheader(f"Historical Face-offs: {len(rivalry_df)} Total Matches")
                
            fig = px.pie(
                h2h_wins, 
                values='Wins', 
                names='Team', 
                title=f"Win Share Allocation: {team_A} vs {team_B}",
                color_discrete_sequence=px.colors.qualitative.Bold
            )
            fig.update_traces(textposition='inside', textinfo='percent+label', marker=dict(line=dict(color='#ffffff', width=2)))
            st.plotly_chart(fig, use_container_width=True)

# --- 3. PLAYER ANALYTICS SECTION ---
elif menu_select == "Player Analytics":
    st.title("Player Analytics & MVPs")
    st.caption("Identify top performers, match-winners, and crucial impact players.")
    
    team_sel = st.selectbox("Filter by Franchise Team", sorted(df['team1'].unique()))
    
    st.subheader(f"Top 5 Match Winners for {team_sel}")
    
    POM_df = df[df['winner'] == team_sel]['player_of_match'].value_counts().head(5).reset_index()
    POM_df.columns = ["Player Name", "Player of Match Awards"]
    
    if not POM_df.empty:
        POM_plot = px.bar(
            POM_df,
            x='Player of Match Awards',
            y='Player Name',
            title="Most 'Player of the Match' Awards in Winning Causes",
            orientation='h',
            color='Player of Match Awards',
            color_continuous_scale='Cividis'
        )
        POM_plot.update_layout(yaxis={'categoryorder':'total ascending'}, template="plotly_white")
        st.plotly_chart(POM_plot, use_container_width=True)
    else:
        st.info("No Player of the Match data available for this selection.")

# --- 4. STRATEGIC INSIGHTS SECTION ---
elif menu_select == "Strategic Insights":
    st.title("Strategic Deep-Dives")
    st.caption("Advanced macroscopic analysis highlighting multi-season tactical evolutions.")
    
    st.subheader("Evolution of Toss Decisions Over Time")
    
    result = df.groupby(['season', 'toss_decision'])['winner'].count().unstack()
        
    fig, ax = plt.subplots(figsize=(12, 5))
    ax.plot(result.index, result['bat'], color='#1E3A8A', marker='o', linewidth=2.5, label='Chose to Bat First (Defend)')
    ax.plot(result.index, result['field'], color='#DC2626', marker='o', linewidth=2.5, label='Chose to Field First (Chase)')
        
    ax.set_title("IPL Toss Decisions Paradigm Shift (2008 - 2026)", fontsize=14, fontweight='bold', pad=15)
    ax.set_xlabel('Tournament Season Year', fontsize=10)
    ax.set_ylabel('Total Decisions Made', fontsize=10)
    ax.set_ylim(0, result.max().max() + 10)
        
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.grid(axis='y', linestyle='--', alpha=0.3)
        
    plt.xticks(result.index, rotation=45)
    plt.legend(frameon=True, facecolor='#F9FAFB', edgecolor='none', fontsize=10)
    plt.tight_layout()
    st.pyplot(fig)

# --- 5. MATCH PREDICTOR SECTION ---
elif menu_select == "Match Predictor":
    st.title(" AI Match Predictor")
    st.caption("Simulate upcoming fixtures using a Logistic Regression model trained on historical IPL data.")
    
    all_teams = sorted(df['team1'].dropna().unique())
    all_venues = sorted(df['venue'].dropna().unique())
    

    col1, col2 = st.columns(2)
    with col1:
        team1 = st.selectbox("Team 1", all_teams, index=0)
    with col2:
        team2 = st.selectbox("Team 2", all_teams, index=1)
        
    col3, col4 = st.columns(2)
    with col3:
        toss_winner = st.selectbox("Toss Winner", [team1, team2])
    with col4:
        toss_decision = st.selectbox("Toss Decision", ['bat', 'field'])
        
    venue = st.selectbox("Venue", all_venues)
        
    st.markdown("---")
    
    if st.button(" Predict Match Outcome", type="primary", use_container_width=True):
        if team1 == team2:
            st.error("Please select two different teams.")
        else:
            input_data = pd.DataFrame({
                'team1': [team1],
                'team2': [team2],
                'toss_winner': [toss_winner],
                'toss_decision': [toss_decision],
                'venue': [venue]
            })
            
            probs = ml_model.predict_proba(input_data)[0]
            team2_prob = probs[0]
            team1_prob = probs[1]
            
            st.subheader("Win Probability Analysis")
            
            st.write(f"**{team1}**: {team1_prob * 100:.1f}%")
            st.progress(float(team1_prob))
            
            st.write(f"**{team2}**: {team2_prob * 100:.1f}%")
            st.progress(float(team2_prob))