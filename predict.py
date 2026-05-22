import os
import sys
import joblib
import datetime
import requests
import pandas as pd
import numpy as np
import streamlit as st

st.set_page_config(page_title="NBA AI Predictor & Bankroll Management", layout="centered")

@st.cache_data(ttl=3600)
def fetch_recent_completed_games(api_key, start_date):
    if not api_key:
        return []
    url = "https://api.balldontlie.io/v1/games"
    headers = {"Authorization": api_key}
    end_date = datetime.date.today().isoformat()
    params = {"start_date": start_date, "end_date": end_date, "per_page": 100}
    try:
        r = requests.get(url, headers=headers, params=params)
        if r.status_code == 200:
            return [g for g in r.json().get("data", []) if g.get("status") == "Final"]
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
    new_cols = {}
    for col in stats_list:
        new_cols[f'{col}_rolling_5'] = df.groupby('teamId')[col].transform(
            lambda x: x.shift(1).rolling(5, min_periods=1).mean()
        )
    new_cols['seasonWins_prematch'] = df.groupby('teamId')['seasonWins'].shift(1).fillna(0)
    new_cols['seasonLosses_prematch'] = df.groupby('teamId')['seasonLosses'].shift(1).fillna(0)
    
    df = pd.concat([df, pd.DataFrame(new_cols)], axis=1)
    return model, df, stats_list

try:
    model, team_data, stats_list = load_prediction_resources()
    prob_draw = 0.065
except Exception as e:
    st.error(f"Erreur lors du chargement des fichiers : {e}")
    st.stop()

def get_team_features(team_name):
    mask = (team_data['teamName'].str.lower() == team_name.lower()) | \
           (team_data['teamCity'].str.lower() == team_name.lower())
    if team_data[mask].empty:
        return None
    team_games = team_data[mask]
    latest_game = team_games.iloc[-1]
    features = {
        'seasonWins': latest_game['seasonWins_prematch'],
        'seasonLosses': latest_game['seasonLosses_prematch'],
        'last_game_date': latest_game['gameDate']
    }
    for stat in stats_list:
        features[f'{stat}_rolling_5'] = latest_game[f'{stat}_rolling_5']
    return features

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
        r = requests.get(url, headers=headers, params=params)
        if r.status_code == 200:
            all_games = r.json().get("data", [])
            upcoming = [g for g in all_games if "final" not in str(g.get("status", "")).lower()]
            return upcoming[:10]
    except:
        pass
    return []

def match_team_name(api_name):
    all_db_teams = team_data['teamName'].unique()
    api_name_lower = api_name.lower()
    for t in all_db_teams:
        if t.lower() in api_name_lower or api_name_lower in t.lower():
            return t
    all_db_cities = team_data['teamCity'].unique()
    for c in all_db_cities:
        if c.lower() in api_name_lower:
            mask = team_data['teamCity'].str.lower() == c.lower()
            return team_data[mask]['teamName'].iloc[0]
    return None

st.title("🏀 NBA Value Bet Detector")
st.markdown("Interface d'optimisation de capital connectée à BallDontLie API.")

st.sidebar.header("💰 Gestion de la Bankroll")
capital_dispo = st.sidebar.number_input("Capital disponible (€)", min_value=10.0, value=200.0, step=10.0)
mise_min = st.sidebar.number_input("Mise minimale (€)", min_value=1.0, value=10.0, step=1.0)
mise_max = st.sidebar.number_input("Mise maximale (€)", min_value=10.0, value=50.0, step=5.0)
kelly_fraction = st.sidebar.slider("Fraction de Kelly", min_value=0.1, max_value=1.0, value=0.5, step=0.1)

st.header("📅 Prochaines Rencontres NBA")
upcoming_matches = fetch_upcoming_games()

selected_home = ""
selected_away = ""

if upcoming_matches:
    match_options = []
    match_mapping = {}
    for idx, g in enumerate(upcoming_matches):
        h_info = g.get("home_team", {})
        v_info = g.get("visitor_team", {})
        h_name = h_info.get("full_name", h_info.get("name", "Unknown"))
        v_name = v_info.get("full_name", v_info.get("name", "Unknown"))
        g_date = g.get("date", "")
        label = f"🏠 {h_name} vs ✈️ {v_name} ({g_date})"
        match_options.append(label)
        match_mapping[label] = (h_name, v_name)
    
    selected_match_label = st.selectbox("Sélectionner un match à analyser", match_options)
    if selected_match_label:
        raw_home, raw_away = match_mapping[selected_match_label]
        selected_home = match_team_name(raw_home)
        selected_away = match_team_name(raw_away)
else:
    st.info("Aucun match à venir récupéré ou clé d'API absente. Saisie manuelle activée.")

st.header("⚔️ Configuration des Cotes")
all_teams = sorted(team_data['teamName'].unique())

col1, col2 = st.columns(2)
with col1:
    default_home_idx = all_teams.index(selected_home) if selected_home in all_teams else 0
    home_team = st.selectbox("Équipe à domicile", all_teams, index=default_home_idx)
    odds_home = st.number_input("Cote Betclic (Domicile)", min_value=1.01, value=1.80, step=0.01, key="home_odds")
with col2:
    default_away_idx = all_teams.index(selected_away) if selected_away in all_teams else min(1, len(all_teams)-1)
    away_team = st.selectbox("Équipe à l'extérieur", [t for t in all_teams if t != home_team], index=default_away_idx if selected_away != home_team else 0)
    odds_away = st.number_input("Cote Betclic (Extérieur)", min_value=1.01, value=2.10, step=0.01, key="away_odds")

if st.button("Lancer l'analyse prédictive", type="primary"):
    home_raw = get_team_features(home_team)
    away_raw = get_team_features(away_team)
    
    if not home_raw or not away_raw:
        st.error("Données historiques insuffisantes pour l'une des équipes sélectionnées.")
    else:
        today = pd.Timestamp.now()
        home_rest = (today - home_raw['last_game_date']).days
        away_rest = (today - away_raw['last_game_date']).days
        
        match_dict = {
            'weekNumber': 25,
            'home_rest_days': home_rest,
            'home_seasonWins': home_raw['seasonWins'],
            'home_seasonLosses': home_raw['seasonLosses']
        }
        for stat in stats_list:
            match_dict[f'home_{stat}_rolling_5'] = home_raw[f'{stat}_rolling_5']
            
        match_dict['away_rest_days'] = away_rest
        match_dict['away_seasonWins'] = away_raw['seasonWins']
        match_dict['away_seasonLosses'] = away_raw['seasonLosses']
        for stat in stats_list:
            match_dict[f'away_{stat}_rolling_5'] = away_raw[f'{stat}_rolling_5']
            
        X_new = pd.DataFrame([match_dict])
        cols_order = model.get_booster().feature_names
        X_new = X_new[cols_order]
        
        prob_home_win = model.predict_proba(X_new)[0, 1]
        prob_away_win = 1.0 - prob_home_win
        
        prob_home_reg = prob_home_win * (1.0 - prob_draw)
        prob_away_reg = prob_away_win * (1.0 - prob_draw)
        
        ev_home = (prob_home_reg * (odds_home - 1.0)) - (1.0 - prob_home_reg)
        ev_away = (prob_away_reg * (odds_away - 1.0)) - (1.0 - prob_away_reg)
        
        st.subheader("📊 Distribution des Probabilités (Modèle 1N2)")
        m_col1, m_col2, m_col3 = st.columns(3)
        m_col1.metric(label=f"Victoire {home_team}", value=f"{prob_home_reg * 100:.1f}%")
        m_col2.metric(label="Match Nul (48 min)", value=f"{prob_draw * 100:.1f}%")
        m_col3.metric(label=f"Victoire {away_team}", value=f"{prob_away_reg * 100:.1f}%")
        
        st.subheader("💡 Analyse de l'Espérance Mathématique")
        
        chosen_side = None
        chosen_ev = 0.0
        chosen_odds = 0.0
        chosen_team = ""
        
        if ev_home > 0.02 and ev_home > ev_away:
            chosen_side = 1
            chosen_ev = ev_home
            chosen_odds = odds_home
            chosen_team = home_team
            st.success(f"Value Bet détecté sur {home_team} | EV : +{ev_home:.4f}")
        elif ev_away > 0.02 and ev_away > ev_home:
            chosen_side = 0
            chosen_ev = ev_away
            chosen_odds = odds_away
            chosen_team = away_team
            st.success(f"Value Bet détecté sur {away_team} | EV : +{ev_away:.4f}")
        else:
            st.info("Aucune valeur mathématique exploitable trouvée sur ce match. Abstention.")
            
        if chosen_side is not None:
            f_kelly = chosen_ev / (chosen_odds - 1.0)
            mise_suggeree = f_kelly * capital_dispo * kelly_fraction
            
            if mise_suggeree < mise_min:
                mise_suggeree = mise_min
            if mise_suggeree > mise_max:
                mise_suggeree = mise_max
            if mise_suggeree > capital_dispo:
                mise_suggeree = capital_dispo
                
            st.subheader("🎯 Recommandation Sportive")
            st.warning(f"ORDRE D'ACHAT : Miser sur la victoire de **{chosen_team}**")
            st.metric(label="Mise optimale conseillée", value=f"{mise_suggeree:.2f} €")