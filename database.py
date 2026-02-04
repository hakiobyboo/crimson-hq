import pandas as pd
import streamlit as st
from streamlit_gsheets import GSheetsConnection
import os
import requests

# --- 1. CONNEXION CLOUD ---
# On initialise la connexion une seule fois pour tout le projet
conn = st.connection("gsheets", type=GSheetsConnection)

# --- 2. FONCTIONS DE CHARGEMENT ET SAUVEGARDE (GOOGLE SHEETS) ---

def load_data(sheet_name):
    """Charge les données d'un onglet spécifique du Google Sheet"""
    try:
        # ttl=0 est crucial : il force Streamlit à relire le Google Sheet 
        # au lieu de garder une vieille version en mémoire.
        return conn.read(worksheet=sheet_name, ttl=0)
    except Exception:
        # Si l'onglet n'existe pas encore, on retourne un tableau vide
        return pd.DataFrame()

def save_data(df, sheet_name):
    """Sauvegarde un tableau (DataFrame) dans l'onglet spécifié du Google Sheet"""
    try:
        conn.update(worksheet=sheet_name, data=df)
        st.cache_data.clear() # On vide le cache pour que le site se mette à jour
        return True
    except Exception as e:
        st.error(f"Erreur de sauvegarde sur Google Sheets : {e}")
        return False

# --- 3. COMPATIBILITÉ ET ANCIENNES FONCTIONS ---
# On garde init_folders pour les images temporaires si besoin
def init_folders():
    folders = ["data", "images_scrims", "match_proofs"]
    for folder in folders:
        if not os.path.exists(folder):
            os.makedirs(folder)

# --- 4. API VALORANT (INTEL) ---
def get_intel(name, tag, label):
    """Récupère les données MMR via l'API HenrikDev et met à jour la DB locale"""
    try:
        url = f"https://api.henrikdev.xyz/valorant/v1/mmr/eu/{name}/{tag}"
        headers = {'User-Agent': 'Mozilla/5.0'}
        r = requests.get(url, headers=headers, timeout=5)
        
        if r.status_code == 200:
            d = r.json().get('data')
            if d:
                curr = d.get('currenttierpatched', 'Unknown')
                peak = d.get('highest_tier_patched', 'N/A')
                icon = d.get('images', {}).get('small')
                
                # Mise à jour auto de la DB locale
                new_data = pd.DataFrame([{"Player": label, "Current": curr, "Peak": peak}])
                old_df = load_csv(RANKS_DB, ["Player", "Current", "Peak"])
                updated_df = pd.concat([old_df[old_df['Player'] != label], new_data], ignore_index=True)
                updated_df.to_csv(RANKS_DB, index=False)
                
                return curr, peak, icon, "LIVE"
    except Exception:
        pass

    # Fallback sur les données sauvegardées en cas d'échec API
    saved_df = load_csv(RANKS_DB, ["Player", "Current", "Peak"])
    player_data = saved_df[saved_df['Player'] == label]
    
    if not player_data.empty:
        return (
            player_data['Current'].values[0], 
            player_data['Peak'].values[0], 
            None, 
            "OFFLINE (SAVED DATA)"
        )
    
    return "Disconnected", "N/A", None, "ERROR"

# --- 5. SAUVEGARDES ---
def save_agents_mastery(agent_dict):
    """Sauvegarde la maîtrise des agents (Tactical Pool)"""
    df = pd.DataFrame(list(agent_dict.items()), columns=['Key', 'Val'])
    df.to_csv(AGENTS_DB, index=False)

def save_scrim_db(df):
    """Sauvegarde l'historique global des matchs"""
    df.to_csv(SCRIMS_DB, index=False)

def update_intel_manual(label, current_rank, peak_rank):
    """Force la mise à jour manuelle des rangs dans le CSV"""
    new_data = pd.DataFrame([{"Player": label, "Current": current_rank, "Peak": peak_rank}])
    old_df = load_csv(RANKS_DB, ["Player", "Current", "Peak"])
    updated_df = pd.concat([old_df[old_df['Player'] != label], new_data], ignore_index=True)
    updated_df.to_csv(RANKS_DB, index=False)

