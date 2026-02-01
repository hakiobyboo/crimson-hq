import pandas as pd
import os
import requests

SCRIMS_DB = "scrims_database.csv"
AGENTS_DB = "agents_database.csv"
RANKS_DB = "ranks_database.csv"

def init_folders():
    for folder in ["images_scrims", "match_proofs"]:
        if not os.path.exists(folder): os.makedirs(folder)

def load_csv(file, columns):
    if os.path.exists(file):
        try: return pd.read_csv(file)
        except: return pd.DataFrame(columns=columns)
    return pd.DataFrame(columns=columns)

def get_intel(name, tag, label):
    try:
        url = f"https://api.henrikdev.xyz/valorant/v1/mmr/eu/{name}/{tag}"
        r = requests.get(url, headers={'User-Agent': 'Mozilla/5.0'}, timeout=5)
        if r.status_code == 200:
            d = r.json().get('data')
            if d:
                curr = d.get('currenttierpatched', 'Unknown')
                peak = d.get('highest_tier_patched', 'N/A')
                icon = d.get('images', {}).get('small')
                # Sauvegarde auto
                df = load_csv(RANKS_DB, ["Player", "Current", "Peak"])
                new_row = pd.DataFrame([{"Player": label, "Current": curr, "Peak": peak}])
                pd.concat([df[df['Player'] != label], new_row], ignore_index=True).to_csv(RANKS_DB, index=False)
                return curr, peak, icon, "LIVE"
    except: pass
    return "Offline", "N/A", None, "STABLE"