import streamlit as st

def inject_premium_dark_theme():
    st.markdown("""
        <script src="https://cdn.tailwindcss.com?plugins=forms,container-queries"></script>
        <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap" rel="stylesheet"/>
        <style>
            /* Utilisation de sélecteurs ultra-spécifiques pour écraser le cache du Cloud */
            html body .stApp {
                background-color: #09090b !important;
                color: #ffffff !important;
                font-family: 'Inter', sans-serif;
            }
            
            html body [data-testid="stSidebar"] {
                background-color: #09090b !important;
                border-right: 1px solid rgba(255, 255, 255, 0.08) !important;
            }
            
            html body [data-testid="stWidgetLabel"] p, 
            html body [data-testid="stWidgetLabel"], 
            html body label, 
            html body .stSelectbox p, 
            html body .stNumberInput p, 
            html body .stSlider p,
            html body div[data-testid="stMarkdownContainer"] p {
                color: #ffffff !important;
                font-weight: 500 !important;
            }
            
            html body .stNumberInput input, html body .stSelectbox select, html body .stSlider div {
                background-color: #18181b !important;
                color: #ffffff !important;
                border: 1px solid rgba(255, 255, 255, 0.1) !important;
                border-radius: 6px !important;
            }
            
            html body .stButton>button { 
                width: 100% !important; 
                border-radius: 8px !important; 
                height: 3.5em !important; 
                font-weight: 700 !important; 
                background: linear-gradient(135deg, #f97316 0%, #ea580c 100%) !important;
                color: #ffffff !important; 
                border: none !important;
                box-shadow: 0 4px 14px rgba(249, 115, 22, 0.2) !important;
                transition: all 0.2s ease !important;
                text-transform: uppercase !important;
                letter-spacing: 0.05em !important;
            }
            html body .stButton>button:hover {
                transform: translateY(-1px) !important;
                box-shadow: 0 6px 20px rgba(249, 115, 22, 0.35) !important;
            }
            
            /* --- CENTRAGE DU BOUTON SUR LE CLOUD --- */
            html body div[data-testid="stElementContainer"]:has(.st-key-calc_btn),
            html body div[data-testid="stElementContainer"].st-key-calc_btn {
                display: flex !important;
                justify-content: center !important;
                width: 100% !important;
            }
            html body div[data-testid="stElementContainer"]:has(.st-key-calc_btn) .stButton,
            html body div[data-testid="stElementContainer"].st-key-calc_btn .stButton {
                width: auto !important;
                min-width: 320px !important;
            }
            
            /* --- CENTRAGE DES METRICS SUR LE CLOUD --- */
            html body div[data-testid="stMetric"], html body div[data-testid="metric"] {
                display: flex !important;
                flex-direction: column !important;
                align-items: center !important;
                text-align: center !important;
                width: 100% !important;
            }
            html body div[data-testid="stMetric"] div[data-testid="stMetricLabel"],
            html body div[data-testid="stMetric"] div[data-testid="stMetricValue"] {
                display: flex !important;
                justify-content: center !important;
                width: 100% !important;
            }
            
            .app-header {
                border-bottom: 1px solid rgba(255, 255, 255, 0.08);
                padding-bottom: 12px;
                margin-bottom: 24px;
            }
            .app-title {
                color: #ffffff !important;
                font-size: 24px;
                font-weight: 900;
                letter-spacing: -0.5px;
                margin: 0;
            }
            
            .ui-card { 
                background-color: #111113; 
                border: 1px solid rgba(255, 255, 255, 0.08); 
                border-radius: 12px; 
                padding: 24px; 
                text-align: center;
            }
            .team-logo {
                width: 90px;
                height: 90px;
                display: block;
                margin: 0 auto 14px auto;
                object-fit: contain;
            }
            .team-title {
                color: #ffffff !important;
                font-weight: 700 !important;
                font-size: 20px !important;
                margin: 0 !important;
                padding: 0 !important;
            }
            .team-subtitle {
                color: #f97316 !important;
                font-family: monospace;
                font-size: 13px;
                margin: 4px 0 16px 0;
                font-weight: 600;
            }
            
            .mini-card-btn {
                background-color: #111113;
                border: 1px solid rgba(255, 255, 255, 0.08);
                border-radius: 12px;
                padding: 16px;
                margin-bottom: 12px;
                display: flex;
                align-items: center;
                justify-content: space-between;
                width: 100%;
                cursor: pointer;
                transition: transform 0.15s ease, border-color 0.15s ease;
                outline: none;
            }
            .mini-card-btn:hover {
                transform: scale(1.02);
                border-color: rgba(249, 115, 22, 0.4);
            }
            .mini-team-bloc {
                display: flex;
                flex-direction: column;
                align-items: center;
                width: 40%;
            }
            .mini-logo {
                width: 40px;
                height: 40px;
                display: block;
                object-fit: contain;
                margin-bottom: 4px;
            }
            .mini-team-text {
                font-size: 14px;
                font-weight: 700;
                color: #ffffff;
                text-align: center;
            }
            .mini-vs-badge {
                font-size: 10px;
                font-family: monospace;
                color: #f97316;
                font-weight: 800;
                background-color: rgba(249, 115, 22, 0.08);
                padding: 4px 8px;
                border-radius: 6px;
                border: 1px solid rgba(249, 115, 22, 0.15);
            }
            
            .comparison-container {
                display: flex;
                gap: 16px;
                width: 100%;
            }
            .comparison-container .ui-card {
                flex: 1;
                width: 50%;
            }
            
            .metric-row {
                display: flex;
                justify-content: space-between;
                padding: 12px 0;
                border-bottom: 1px solid rgba(255, 255, 255, 0.05);
                font-size: 14px;
            }
            .metric-row:last-child {
                border-bottom: none;
            }
            .label-muted { 
                color: rgba(255, 255, 255, 0.5); 
                font-weight: 500; 
            }
            .value-highlight { 
                font-weight: 600; 
                color: #ffffff; 
            }
            
            .signal-panel {
                padding: 24px;
                border-radius: 12px;
                margin-top: 24px;
            }
            .signal-success {
                background-color: rgba(249, 115, 22, 0.03);
                border: 1px solid #f97316;
                color: #ffffff;
            }
            .signal-neutral {
                background-color: #111113;
                border: 1px solid rgba(255, 255, 255, 0.08);
                color: #ffffff;
            }
            .panel-title {
                margin: 0 !important;
                padding: 0 !important;
                color: #f97316 !important;
                font-size: 16px !important;
                font-weight: 700 !important;
                text-transform: uppercase;
                letter-spacing: 0.05em;
            }
            .panel-desc {
                margin: 6px 0 0 0;
                font-size: 14px;
                color: rgba(255, 255, 255, 0.8);
            }

            @media (max-width: 768px) {
                html body .stApp, .app-header, .stMarkdown, .stSubheader, .stTitle, h1, h2, h3, p, label {
                    text-align: center !important;
                }
                
                /* Ne s'applique pas au bloc contenant les cotes d'équipes */
                html body div[data-testid="stHorizontalBlock"]:not(:has(.st-key-home_odds)) {
                    flex-direction: column !important;
                    gap: 16px !important;
                }
                html body div[data-testid="column"]:not(:has(.st-key-home_odds) div[data-testid="column"]),
                html body div[data-testid="stColumn"]:not(:has(.st-key-home_odds) div[data-testid="stColumn"]) {
                    width: 100% !important;
                    max-width: 100% !important;
                    flex-basis: 100% !important;
                    display: flex !important;
                    flex-direction: column !important;
                    align-items: center !important;
                    text-align: center !important;
                }
                
                /* --- FORCE LE MOTEUR DU CLOUD À GARDER LE CÔTÉ À CÔTÉ SUR MOBILE --- */
                html body div[data-testid="stHorizontalBlock"]:has(.st-key-home_odds) {
                    display: flex !important;
                    flex-direction: row !important;
                    flex-wrap: nowrap !important;
                    gap: 12px !important;
                    width: 100% !important;
                }
                
                html body div[data-testid="stHorizontalBlock"]:has(.st-key-home_odds) div[data-testid="stColumn"],
                html body div[data-testid="stHorizontalBlock"]:has(.st-key-home_odds) div[data-testid="column"] {
                    width: 50% !important;
                    flex-basis: 50% !important;
                    max-width: 50% !important;
                    min-width: 0 !important;
                    display: flex !important;
                    flex-direction: column !important;
                    gap: 8px !important;
                }
                
                div[data-testid="stSelectbox"], div[data-testid="stNumberInput"], div[data-testid="stSlider"], .stButton {
                    width: 100% !important;
                    max-width: 100% !important;
                }
                div[data-testid="stWidgetLabel"] {
                    text-align: center !important;
                    width: 100% !important;
                }
                
                .comparison-container {
                    gap: 8px;
                }
                .comparison-container .ui-card {
                    padding: 12px 6px;
                }
                .comparison-container .team-logo {
                    width: 50px;
                    height: 50px;
                    margin-bottom: 8px;
                }
                .comparison-container .team-title {
                    font-size: 13px !important;
                }
                .comparison-container .team-subtitle {
                    font-size: 11px;
                    margin-bottom: 12px;
                }
                .comparison-container .metric-row {
                    flex-direction: column;
                    align-items: center;
                    gap: 2px;
                    padding: 6px 0;
                    font-size: 11px;
                }
                
                .mini-card-btn {
                    width: 100% !important;
                    max-width: 400px;
                    margin: 0 auto 12px auto !important;
                }
            }
        </style>
    """, unsafe_allow_html=True)