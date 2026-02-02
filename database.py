import pandas as pd
import os
import requests

# --- 1. DÉFINITION DES CHEMINS ---
# Centralisation des bases de données dans le dossier /data
SCRIMS_DB = "data/scrims_database.csv"
AGENTS_DB = "data/agents_database.csv"
RANKS_DB = "data/ranks_database.csv"
PLANNING_DB = "data/planning.csv" 
DISPOS_DB = "data/dispos.csv"

# --- 2. CHARGEMENT DES DONNÉES ---
def load_data(file):
    """Retourne les données sous forme de liste de dictionnaires (utilisé pour le Dashboard)"""
    if os.path.exists(file):
        try:
            return pd.read_csv(file).to_dict(orient='records')
        except Exception:
            return []
    return []

def load_csv(file, columns):
    """Charge un CSV ou crée un DataFrame vide avec les colonnes spécifiées"""
    if os.path.exists(file):
        try:
            return pd.read_csv(file)
        except Exception:
            # Si le fichier est corrompu, on repart sur un fichier propre
            return pd.DataFrame(columns=columns)
    
    # Si le fichier n'existe pas, on le crée proprement avec les colonnes par défaut
    df = pd.DataFrame(columns=columns)
    # On s'assure que le dossier data existe avant de sauvegarder
    if not os.path.exists("data"):
        os.makedirs("data")
    df.to_csv(file, index=False)
    return df

# --- 3. GESTION DES DOSSIERS ---
def init_folders():
    """Crée les répertoires nécessaires s'ils n'existent pas"""
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
