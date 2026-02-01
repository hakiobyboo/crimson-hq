import pandas as pd
import os
import requests

# --- DÉFINITION DES CHEMINS ---
SCRIMS_DB = "scrims_database.csv"
AGENTS_DB = "agents_database.csv"
RANKS_DB = "ranks_database.csv"

def init_folders():
    """Crée les répertoires nécessaires s'ils n'existent pas"""
    folders = ["images_scrims", "match_proofs"]
    for folder in folders:
        if not os.path.exists(folder):
            os.makedirs(folder)

def load_csv(file, columns):
    """Charge un fichier CSV ou retourne un DataFrame vide avec les bonnes colonnes"""
    if os.path.exists(file):
        try:
            return pd.read_csv(file)
        except Exception:
            return pd.DataFrame(columns=columns)
    return pd.DataFrame(columns=columns)

def get_intel(name, tag, label):
    """Récupère les données MMR via l'API et met à jour la base de données locale"""
    try:
        # Tentative d'appel API (HenrikDev)
        url = f"https://api.henrikdev.xyz/valorant/v1/mmr/eu/{name}/{tag}"
        headers = {'User-Agent': 'Mozilla/5.0'}
        r = requests.get(url, headers=headers, timeout=5)
        
        if r.status_code == 200:
            d = r.json().get('data')
            if d:
                curr = d.get('currenttierpatched', 'Unknown')
                peak = d.get('highest_tier_patched', 'N/A')
                icon = d.get('images', {}).get('small')
                
                # Mise à jour automatique de la DB locale
                new_data = pd.DataFrame([{"Player": label, "Current": curr, "Peak": peak}])
                old_df = load_csv(RANKS_DB, ["Player", "Current", "Peak"])
                updated_df = pd.concat([old_df[old_df['Player'] != label], new_data], ignore_index=True)
                updated_df.to_csv(RANKS_DB, index=False)
                
                return curr, peak, icon, "LIVE"
    except Exception:
        pass

    # Si l'API échoue, on tente de charger la dernière valeur connue en local
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

def save_agents_mastery(agent_dict):
    """Sauvegarde les cases cochées du Tactical Pool dans le CSV"""
    df = pd.DataFrame(list(agent_dict.items()), columns=['Key', 'Val'])
    df.to_csv(AGENTS_DB, index=False)

def save_scrim_db(df):
    """Sauvegarde l'historique des matchs"""
    df.to_csv(SCRIMS_DB, index=False)

def update_intel_manual(label, current_rank, peak_rank):
    """Force la mise à jour manuelle des rangs dans le CSV"""
    new_data = pd.DataFrame([{"Player": label, "Current": current_rank, "Peak": peak_rank}])
    old_df = load_csv(RANKS_DB, ["Player", "Current", "Peak"])
    # On retire l'ancienne entrée et on ajoute la nouvelle
    updated_df = pd.concat([old_df[old_df['Player'] != label], new_data], ignore_index=True)
    updated_df.to_csv(RANKS_DB, index=False)
