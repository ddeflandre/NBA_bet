import pandas as pd
import streamlit as st
import streamlit.components.v1 as components
import time
from theme import inject_premium_dark_theme
from data_provider import (
    load_prediction_resources,
    fetch_upcoming_games,
    get_team_features,
    match_team_name
)

st.set_page_config(page_title="Courtside AI", layout="wide")
inject_premium_dark_theme()

try:
    model, team_data, stats_list = load_prediction_resources()
    prob_draw = 0.065
except Exception as e:
    st.error(f"Erreur d'initialisation : {e}")
    st.stop()

all_teams = sorted(team_data['teamName'].unique())

if "selected_home" not in st.session_state:
    st.session_state.selected_home = all_teams[0]
if "selected_away" not in st.session_state:
    st.session_state.selected_away = all_teams[1]
if "scroll_trigger" not in st.session_state:
    st.session_state.scroll_trigger = False

if "load_match" in st.query_params:
    match_param = st.query_params["load_match"]
    st.markdown("""
        <div style="display: flex; flex-direction: column; align-items: center; justify-content: center; height: 70vh;">
            <div style="border: 4px solid rgba(255, 255, 255, 0.1); border-top: 4px solid #f97316; border-radius: 50%; width: 50px; height: 50px; animation: spin 1s linear infinite; margin-bottom: 24px;"></div>
            <h3 style="color: #ffffff; font-weight: 700; font-size: 18px; letter-spacing: 0.05em; text-transform: uppercase; margin: 0 0 8px 0;">Analyse de la rencontre en cours</h3>
            <p style="color: rgba(255, 255, 255, 0.5); font-size: 14px; margin: 0;">Alignement des fonctionnalités et mise à jour des cotes...</p>
        </div>
        <style>
            @keyframes spin {
                0% { transform: rotate(0deg); }
                100% { transform: rotate(360deg); }
            }
        </style>
    """, unsafe_allow_html=True)
    
    try:
        mh, mv = match_param.split("|")
        if mh in all_teams and mv in all_teams:
            st.session_state.selected_home = mh
            st.session_state.selected_away = mv
            st.session_state.scroll_trigger = True
    except ValueError:
        pass
        
    time.sleep(0.5)
    st.query_params.clear()
    st.rerun()

st.sidebar.markdown("""
    <div style="margin-bottom: 20px;">
        <h2 style="color: #ffffff; margin: 0; font-size: 18px; font-weight: 700;">🏀 Predictor Pro</h2>
        <span style="color: #f97316; font-size: 11px; font-weight: 600; font-family: monospace; letter-spacing: 1px;">API CONNECTED</span>
    </div>
""", unsafe_allow_html=True)

capital_dispo = st.sidebar.number_input("Capital disponible (€)", min_value=10.0, value=200.0, step=10.0)
mise_min = st.sidebar.number_input("Mise minimale (€)", min_value=1.0, value=10.0, step=1.0)
mise_max = st.sidebar.number_input("Mise maximale (€)", min_value=10.0, value=50.0, step=5.0)
kelly_fraction = st.sidebar.slider("Fraction de Kelly", min_value=0.1, max_value=1.0, value=0.5, step=0.1)

st.markdown("""
    <div class="app-header">
        <h1 class="app-title">NBA - Predict</h1>
    </div>
""", unsafe_allow_html=True)

st.subheader("📅 Prochaines rencontres")
upcoming_matches = fetch_upcoming_games()

if upcoming_matches:
    chunk_size = 3
    for i in range(0, len(upcoming_matches), chunk_size):
        match_chunk = upcoming_matches[i:i + chunk_size]
        cols_cards = st.columns(3)
        
        for idx, g in enumerate(match_chunk):
            h_info = g.get("home_team", {})
            v_info = g.get("visitor_team", {})
            h_name = h_info.get("full_name", h_info.get("name", "Unknown"))
            v_name = v_info.get("full_name", v_info.get("name", "Unknown"))
            
            matched_h = match_team_name(team_data, h_name)
            matched_v = match_team_name(team_data, v_name)
            
            features_h = get_team_features(team_data, stats_list, matched_h) if matched_h else None
            features_v = get_team_features(team_data, stats_list, matched_v) if matched_v else None
            
            logo_h_url = f"https://cdn.nba.com/logos/nba/{int(features_h['teamId'])}/global/L/logo.svg" if features_h else ""
            logo_v_url = f"https://cdn.nba.com/logos/nba/{int(features_v['teamId'])}/global/L/logo.svg" if features_v else ""
            
            with cols_cards[idx]:
                if matched_h and matched_v:
                    st.markdown(f"""
                        <form action="" method="get">
                            <button class="mini-card-btn" type="submit" name="load_match" value="{matched_h}|{matched_v}">
                                <div class="mini-team-bloc">
                                    <img src="{logo_h_url}" class="mini-logo">
                                    <div class="mini-team-text">{features_h['teamAbbreviation'] if features_h else h_name[:3].upper()}</div>
                                </div>
                                <div class="mini-vs-badge">VS</div>
                                <div class="mini-team-bloc">
                                    <img src="{logo_v_url}" class="mini-logo">
                                    <div class="mini-team-text">{features_v['teamAbbreviation'] if features_v else v_name[:3].upper()}</div>
                                </div>
                            </button>
                        </form>
                    """, unsafe_allow_html=True)
                else:
                    st.markdown(f"""
                        <div class="mini-card-btn" style="opacity: 0.5; cursor: not-allowed;">
                            <div class="mini-team-bloc"><div class="mini-team-text">{h_name[:3].upper()}</div></div>
                            <div class="mini-vs-badge">VS</div>
                            <div class="mini-team-bloc"><div class="mini-team-text">{v_name[:3].upper()}</div></div>
                        </div>
                    """, unsafe_allow_html=True)
else:
    st.info("Aucun match planifié disponible sur le flux API actuel.")

st.markdown("<br><hr style='border-color:rgba(255,255,255,0.08);'><br>", unsafe_allow_html=True)

st.markdown('<div id="focus-odds-section"></div>', unsafe_allow_html=True)

if st.session_state.scroll_trigger:
    components.html("""
        <script>
            window.parent.document.getElementById("focus-odds-section")?.scrollIntoView({
                behavior: "smooth",
                block: "start"
            });
        </script>
    """, height=0)
    st.session_state.scroll_trigger = False

st.subheader("⚔️ Equipes & Cotes")

c1, c2 = st.columns(2)
with c1:
    default_home_idx = all_teams.index(st.session_state.selected_home) if st.session_state.selected_home in all_teams else 0
    home_team = st.selectbox("Équipe Domicile", all_teams, index=default_home_idx)
    odds_home = st.number_input("Cote Domicile", min_value=1.01, value=1.80, step=0.01, key="home_odds")
with c2:
    away_options = [t for t in all_teams if t != home_team]
    if st.session_state.selected_away in away_options:
        default_away_idx = away_options.index(st.session_state.selected_away)
    else:
        default_away_idx = 0
    away_team = st.selectbox("Équipe Extérieur", away_options, index=default_away_idx)
    odds_away = st.number_input("Cote Extérieur", min_value=1.01, value=2.10, step=0.01, key="away_odds")

home_raw = get_team_features(team_data, stats_list, home_team)
away_raw = get_team_features(team_data, stats_list, away_team)

if home_raw and away_raw:
    st.markdown("<br>", unsafe_allow_html=True)
    
    st.markdown(f"""
        <div class="comparison-container">
            <div class="ui-card">
                <img src="https://cdn.nba.com/logos/nba/{int(home_raw['teamId'])}/global/L/logo.svg" class="team-logo">
                <h3 class="team-title">{home_team}</h3>
                <p class="team-subtitle">{int(home_raw['seasonWins'])}W - {int(home_raw['seasonLosses'])}L</p>
                <div class="metric-row"><span class="label-muted">Offensive Rating</span><span class="value-highlight">{home_raw['offensiveRating_rolling_5']:.1f}</span></div>
                <div class="metric-row"><span class="label-muted">Defensive Rating</span><span class="value-highlight">{home_raw['defensiveRating_rolling_5']:.1f}</span></div>
                <div class="metric-row"><span class="label-muted">Net Rating</span><span class="value-highlight">{home_raw['netRating_rolling_5']:.1f}</span></div>
                <div class="metric-row"><span class="label-muted">Pace (Rythme)</span><span class="value-highlight">{home_raw['pace_rolling_5']:.1f}</span></div>
            </div>
            <div class="ui-card">
                <img src="https://cdn.nba.com/logos/nba/{int(away_raw['teamId'])}/global/L/logo.svg" class="team-logo">
                <h3 class="team-title">{away_team}</h3>
                <p class="team-subtitle">{int(away_raw['seasonWins'])}W - {int(away_raw['seasonLosses'])}L</p>
                <div class="metric-row"><span class="label-muted">Offensive Rating</span><span class="value-highlight">{away_raw['offensiveRating_rolling_5']:.1f}</span></div>
                <div class="metric-row"><span class="label-muted">Defensive Rating</span><span class="value-highlight">{away_raw['defensiveRating_rolling_5']:.1f}</span></div>
                <div class="metric-row"><span class="label-muted">Net Rating</span><span class="value-highlight">{away_raw['netRating_rolling_5']:.1f}</span></div>
                <div class="metric-row"><span class="label-muted">Pace (Rythme)</span><span class="value-highlight">{away_raw['pace_rolling_5']:.1f}</span></div>
            </div>
        </div>
    """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)
    
    if st.button("Voir le pronostique", key="calc_btn"):
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
        
        st.subheader("📊 Probabilités victoire")
        res_c1, res_c2, res_c3 = st.columns(3)
        res_c1.metric(label=f"Victoire {home_team}", value=f"{prob_home_reg * 100:.1f}%")
        res_c2.metric(label="Match Nul (48 min)", value=f"{prob_draw * 100:.1f}%")
        res_c3.metric(label=f"Victoire {away_team}", value=f"{prob_away_reg * 100:.1f}%")
        
        chosen_side = None
        chosen_ev = 0.0
        chosen_odds = 0.0
        chosen_team = ""
        
        if ev_home > 0.02 and ev_home > ev_away:
            chosen_side = 1
            chosen_ev = ev_home
            chosen_odds = odds_home
            chosen_team = home_team
        elif ev_away > 0.02 and ev_away > ev_home:
            chosen_side = 0
            chosen_ev = ev_away
            chosen_odds = odds_away
            chosen_team = away_team
            
        if chosen_side is not None:
            f_kelly = chosen_ev / (chosen_odds - 1.0)
            mise_suggeree = f_kelly * capital_dispo * kelly_fraction
            mise_suggeree = max(mise_min, min(mise_suggeree, mise_max))
            if mise_suggeree > capital_dispo:
                mise_suggeree = capital_dispo
                
            st.markdown(f"""
                <div class="signal-panel signal-success">
                    <h3 class="panel-title">🎯 Signal Value Bet Aligné</h3>
                    <p class="panel-desc">Avantage détecté sur <b>{chosen_team}</b> (EV : +{chosen_ev*100:.1f}%). Allocation conseillée : <b>{mise_suggeree:.2f} €</b></p>
                </div>
            """, unsafe_allow_html=True)
        else:
            st.markdown("""
                <div class="signal-panel signal-neutral">
                    <h3 class="panel-title">⚠️ Absence d'Écart de Valeur</h3>
                    <p class="panel-desc">Aucun trade recommandé sur ce match, tu risques de perdre plus d'argent que d'en gagner</p>
                </div>
            """, unsafe_allow_html=True)
else:
    st.error("Données de match indisponibles.")