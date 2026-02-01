import streamlit as st
from styles import apply_global_styles, apply_immersive_mode
from database import init_folders, load_csv, SCRIMS_DB
import logic

# Configuration initiale
st.set_page_config(page_title="CRIMSON PROTOCOL", layout="wide")
init_folders()
apply_global_styles()

# Session State
if "logged_in" not in st.session_state: st.session_state["logged_in"] = False
if "current_page" not in st.session_state: st.session_state["current_page"] = "DASHBOARD"
if 'selected_strat_map' not in st.session_state: st.session_state['selected_strat_map'] = None
if 'scrims_df' not in st.session_state: st.session_state['scrims_df'] = load_csv(SCRIMS_DB, ["Date", "Map", "Resultat", "Score", "Screenshot"])

# --- LOGIN ---
if not st.session_state["logged_in"]:
    st.markdown("<h1 class='valo-title'>CRIMSON ACCESS</h1>", unsafe_allow_html=True)
    c1, c2, c3 = st.columns([1,2,1])
    with c2:
        u = st.text_input("UNIT ID")
        p = st.text_input("ENCRYPTION KEY", type="password")
        if st.button("INITIALIZE"):
            if u == "titi12012008@gmail.com" and p == "Tn12janv2008":
                st.session_state["logged_in"] = True
                st.rerun()
else:
    # --- GESTION DU MODE IMMERSIF ---
    # Si on est dans STRATÉGIE et qu'une MAP est choisie -> On active l'immersion
    if st.session_state["current_page"] == "STRATÉGIE" and st.session_state['selected_strat_map'] is not None:
        apply_immersive_mode()
        if st.button("⬅ QUITTER VALOPLANT"):
            st.session_state['selected_strat_map'] = None
            st.rerun()
    else:
        # Menu normal
        st.markdown("<h1 class='valo-title'>CRIMSON HQ</h1>", unsafe_allow_html=True)
        m_cols = st.columns(6)
        pages = ["DASHBOARD", "INTEL TRACKER", "MATCH ARCHIVE", "TACTICAL POOL", "PLANNING", "STRATÉGIE"]
        for idx, p in enumerate(pages):
            if m_cols[idx].button(p, use_container_width=True):
                st.session_state["current_page"] = p
                st.rerun()
        st.divider()

    # Affichage des pages
    menu = st.session_state["current_page"]
    if menu == "DASHBOARD": logic.show_dashboard()
    elif menu == "INTEL TRACKER": logic.show_intel()
    elif menu == "STRATÉGIE":
        if st.session_state['selected_strat_map'] is None:
            # Liste des maps (simplifiée pour l'exemple)
            maps = ["Abyss", "Ascent", "Bind", "Breeze", "Haven", "Icebox", "Lotus", "Sunset"]
            cols = st.columns(4)
            for i, m in enumerate(maps):
                if cols[i%4].button(m.upper()):
                    st.session_state['selected_strat_map'] = m
                    st.rerun()
        else:
            logic.show_strategy_map(st.session_state['selected_strat_map'])