import streamlit as st
import pandas as pd
import os

# 1. CONFIGURATION (UNIQUE)
st.set_page_config(
    page_title="CRIMSON HQ", 
    layout="wide", 
    page_icon="🩸",
    initial_sidebar_state="collapsed"
)

# 2. IMPORTS DES MODULES
try:
    from styles import apply_global_styles, apply_immersive_mode
    # On importe uniquement les fonctions Cloud depuis database.py
    from database import init_folders, load_data, save_data
    import logic
except ImportError as e:
    st.error(f"Erreur d'importation : {e}")
except IndentationError as e:
    st.error(f"Erreur d'espace/indentation : {e}")

# 3. INITIALISATION
init_folders()
apply_global_styles()

# Initialisation des variables de session
if "current_page" not in st.session_state:
    st.session_state["current_page"] = "DASHBOARD"
if "logged_in" not in st.session_state:
    st.session_state["logged_in"] = True
if 'compo_save' not in st.session_state:
    st.session_state['compo_save'] = {}
if 'selected_strat_map' not in st.session_state:
    st.session_state['selected_strat_map'] = None

# --- CHARGEMENT DES DONNÉES DEPUIS GOOGLE SHEETS ---
if 'scrims_df' not in st.session_state:
    st.session_state['scrims_df'] = load_data("scrims")

if 'planning_df' not in st.session_state:
    st.session_state['planning_df'] = load_data("planning")

if 'dispos_df' not in st.session_state:
    st.session_state['dispos_df'] = load_data("dispos")

if 'agents_df' not in st.session_state:
    st.session_state['agents_df'] = load_data("agents")

# 4. INTERFACE UTILISATEUR
is_strat = st.session_state["current_page"] == "STRATÉGIE"
is_map_sel = st.session_state.get('selected_strat_map') is not None

if is_strat and is_map_sel:
    apply_immersive_mode()
    logic.show_strategy_map(st.session_state['selected_strat_map'])
else:
    st.markdown("<h1 class='valo-title'>CRIMSON</h1>", unsafe_allow_html=True)
    st.markdown("<p style='text-align:center; letter-spacing:10px; color:#666; margin-top:-40px; margin-bottom:40px;'>ELITE TACTICAL INTERFACE</p>", unsafe_allow_html=True)

    # Navigation
    pages = ["DASHBOARD", "MAPS & COMPOS", "MATCH ARCHIVE", "TACTICAL POOL", "PLANNING", "STRATÉGIE"]
    cols = st.columns(len(pages))
    for i, p in enumerate(pages):
        if cols[i].button(p, key=f"btn_{p}", use_container_width=True):
            st.session_state["current_page"] = p
            if p != "STRATÉGIE":
                st.session_state['selected_strat_map'] = None
            st.rerun()

    st.divider()

    # Routage
    menu = st.session_state["current_page"]
    if menu == "DASHBOARD":
        logic.show_dashboard()
    elif menu == "MAPS & COMPOS":
        logic.show_team_builder()
    elif menu == "MATCH ARCHIVE":
        logic.show_archive()
    elif menu == "TACTICAL POOL":
        logic.show_tactical_pool()
    elif menu == "PLANNING":
        logic.show_planning()
    elif menu == "STRATÉGIE":
        logic.show_map_selection()
