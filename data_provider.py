import datetime
import joblib
import requests
import pandas as pd
import streamlit as st

@st.cache_data(ttl=3600)
def fetch_recent_completed_games(api_key, start_date):
    if not api_key:
        return []
    url = "https://api.balldontlie.io/v1/games"
    headers = {"Authorization": api_key}
    end_date = datetime.date.today().isoformat()
    params = {"start_date": start_date, "end_date": end_date, "per_page": 100}
    try:
        r = requests.get(url, headers=headers, params=params, timeout=5)
        if r.status_code == 200:
            return [g for g in r.json().get("data", []) if g.get("status") == "Final"]
    except:
        pass
    return []

@st.cache_data(ttl=1800)
def fetch_upcoming_games():
    api_key = st.secrets.get("CLE_API_BALLDONTLIE")
    if not api_key:
        return []
    url = "https://api.balldontlie.io/v1/games"
    headers = {"Authorization": api_key}
    today = datetime.date.today().isoformat()
    future = (datetime.date.today() + datetime.timedelta(days=14)).isoformat()
    params = {"start_date": today, "end_date": future, "per_page": 100}
    try:
        r = requests.get(url, headers=headers, params=params, timeout=5)
        if r.status_code == 200:
            all_games = r.json().get("data", [])
            return [g for g in all_games if "final" not in str(g.get("status", "")).lower()][:6]
    except:
        pass
    return []

@st.cache_resource
def load_prediction_resources():
    model = joblib.load("nba_model.pkl")
    stats_list = [
        'teamScore', 'opponentScore', 'assists', 'turnovers', 'reboundsTotal',
        'fieldGoalsPercentage', 'threePointersPercentage', 'freeThrowsPercentage',
        'offensiveRating', 'defensiveRating', 'netRating', 'pace', 'possessions'
    ]
    df = pd.read_csv("nba_production_data.csv")
    df['gameDate'] = pd.to_datetime(df['gameDate'])
    
    api_key = st.secrets.get("CLE_API_BALLDONTLIE")
    last_db_date = df['gameDate'].max().strftime('%Y-%m-%d')
    recent_games = fetch_recent_completed_games(api_key, last_db_date)
    
    if recent_games:
        new_rows = []
        for g in recent_games:
            pass 
        if new_rows:
            df = pd.concat([df, pd.DataFrame(new_rows)], axis=0, ignore_index=True)
            
    df = df.sort_values(by='gameDate').reset_index(drop=True)
    
    grouped = df.groupby('teamId')
    shifted = grouped[stats_list].shift(1)
    rolling = shifted.groupby(df['teamId']).rolling(5, min_periods=1).mean().reset_index(level=0, drop=True)
    
    wins_pre = grouped['seasonWins'].shift(1).fillna(0).rename('seasonWins_prematch')
    losses_pre = grouped['seasonLosses'].shift(1).fillna(0).rename('seasonLosses_prematch')
    
    features_block = pd.concat([rolling.add_suffix('_rolling_5'), wins_pre, losses_pre], axis=1)
    df = pd.concat([df, features_block], axis=1)
    
    return model, df, stats_list

def get_team_features(team_data, stats_list, team_name):
    mask = (team_data['teamName'].str.lower() == team_name.lower()) | \
           (team_data['teamCity'].str.lower() == team_name.lower())
    if team_data[mask].empty:
        return None
    team_games = team_data[mask]
    latest_game = team_games.iloc[-1]
    features = {
        'teamId': latest_game['teamId'],
        'teamAbbreviation': latest_game.get('teamAbbreviation', team_name[:3].upper()),
        'seasonWins': latest_game['seasonWins_prematch'],
        'seasonLosses': latest_game['seasonLosses_prematch'],
        'last_game_date': latest_game['gameDate']
    }
    for stat in stats_list:
        features[f'{stat}_rolling_5'] = latest_game[f'{stat}_rolling_5']
    return features

def match_team_name(team_data, api_name):
    all_db_teams = team_data['teamName'].unique()
    api_name_lower = api_name.lower()
    
    # Stratégie 1 : Correspondance par la mascotte anglaise (le dernier mot, ex: "clippers", "lakers", "thunder")
    api_words = api_name_lower.split()
    if api_words:
        mascot = api_words[-1]
        for t in all_db_teams:
            if mascot in t.lower():
                return t
                
    # Stratégie 2 : Repli classique si la structure de l'API change
    for t in all_db_teams:
        if t.lower() in api_name_lower or api_name_lower in t.lower():
            return t
            
    return None