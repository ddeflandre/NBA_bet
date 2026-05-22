import streamlit as st

def inject_premium_dark_theme():
    st.markdown("""
        <script src="https://cdn.tailwindcss.com?plugins=forms,container-queries"></script>
        <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap" rel="stylesheet"/>
        <style>
            .stApp {
                background-color: #09090b !important;
                color: #ffffff !important;
                font-family: 'Inter', sans-serif;
            }
            
            [data-testid="stSidebar"] {
                background-color: #09090b !important;
                border-right: 1px solid rgba(255, 255, 255, 0.08) !important;
            }
            
            [data-testid="stWidgetLabel"] p, 
            [data-testid="stWidgetLabel"], 
            label, 
            .stSelectbox p, 
            .stNumberInput p, 
            .stSlider p,
            div[data-testid="stMarkdownContainer"] p {
                color: #ffffff !important;
                font-weight: 500 !important;
            }
            
            .stNumberInput input, .stSelectbox select, .stSlider div {
                background-color: #18181b !important;
                color: #ffffff !important;
                border: 1px solid rgba(255, 255, 255, 0.1) !important;
                border-radius: 6px !important;
            }
            
            .stButton>button { 
                width: 100%; 
                border-radius: 8px; 
                height: 3.5em; 
                font-weight: 700; 
                background: linear-gradient(135deg, #f97316 0%, #ea580c 100%) !important;
                color: #ffffff !important; 
                border: none !important;
                box-shadow: 0 4px 14px rgba(249, 115, 22, 0.2);
                transition: all 0.2s ease;
                text-transform: uppercase;
                letter-spacing: 0.05em;
            }
            .stButton>button:hover {
                transform: translateY(-1px);
                box-shadow: 0 6px 20px rgba(249, 115, 22, 0.35);
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
            
            /* --- NOUVEAU CONTENEUR DE MATCH GRID --- */
            .mini-card {
                background-color: #111113;
                border: 1px solid rgba(255, 255, 255, 0.08);
                border-radius: 12px;
                padding: 16px;
                margin-bottom: 12px;
                display: flex;
                align-items: center;
                justify-content: space-between;
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
        </style>
    """, unsafe_allow_html=True)