import pandas as pd
import os
import requests

# --- 1. DÉFINITION DES CHEMINS ---
# Chemins des fichiers (Vérifie bien les noms !)
SCRIMS_DB = "data/scrims_database.csv"
AGENTS_DB = "data/agents_database.csv"
RANKS_DB = "data/ranks_database.csv"
PLANNING_DB = "data/planning.csv"  # <--- CETTE LIGNE EST MANQUANTE
DISPOS_DB = "data/dispos.csv

def init_folders():
    """Crée le dossier data et les répertoires d'images s'ils n'existent pas"""
    folders = ["data", "images_scrims", "match_proofs"]
    for folder in folders:
        if not os.path.exists(folder):
            os.makedirs(folder)

def load_csv(file, columns):
    """Charge un CSV ou retourne un DataFrame vide avec les colonnes spécifiées"""
    if os.path.exists(file):
        try:
            return pd.read_csv(file)
        except Exception:
            # Si le fichier est corrompu, on repart sur un fichier propre
            return pd.DataFrame(columns=columns)
    
    # Si le fichier n'existe pas, on le crée avec les colonnes par défaut
    df = pd.DataFrame(columns=columns)
    df.to_csv(file, index=False)
    return df

def load_data(file):
    """Fonction pour lire les données (utilisée par le Dashboard)"""
    if os.path.exists(file):
        try:
            return pd.read_csv(file).to_dict(orient='records')
        except:
            return []
    return []

def get_intel(name, tag, label):
    """Récupère les données MMR via l'API et met à jour la base de données locale"""
    try:
        # API HenrikDev pour Valorant
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

    # Backup : si l'API échoue, on charge les dernières données sauvegardées
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
    """Sauvegarde la maîtrise des agents (Tactical Pool)"""
    df = pd.DataFrame(list(agent_dict.items()), columns=['Key', 'Val'])
    df.to_csv(AGENTS_DB, index=False)

def save_scrim_db(df):
    """Sauvegarde l'historique global des matchs"""
    df.to_csv(SCRIMS_DB, index=False)

def update_intel_manual(label, current_rank, peak_rank):
    """Force la mise à jour manuelle des rangs"""
    new_data = pd.DataFrame([{"Player": label, "Current": current_rank, "Peak": peak_rank}])
    old_df = load_csv(RANKS_DB, ["Player", "Current", "Peak"])
    updated_df = pd.concat([old_df[old_df['Player'] != label], new_data], ignore_index=True)
    updated_df.to_csv(RANKS_DB, index=False)

