# ============================================================
# debug_airtable.py
# Script de débogage pour comparer les timestamps
# entre Google Sheets et Airtable
# Utilisé pour diagnostiquer les problèmes de doublons
# ============================================================

from pyairtable import Api               # client API Airtable
import os                                # accès aux variables d'environnement
from dotenv import load_dotenv           # lecture du fichier .env
from src.google_sheets import get_feedbacks  # lecture des avis Google Sheets

# Chargement des variables d'environnement depuis le fichier .env
load_dotenv()

# Connexion à Airtable avec le token personnel
api = Api(os.getenv("AIRTABLE_TOKEN"))
table = api.table(os.getenv("AIRTABLE_BASE_ID"), os.getenv("AIRTABLE_TABLE_NAME"))

# --- Récupération des timestamps depuis Airtable ---
# On ne récupère que la colonne timestamp pour alléger la requête
existing = table.all(fields=["timestamp"])

# Construction d'un ensemble de timestamps existants dans Airtable
existing_timestamps = {r["fields"].get("timestamp") for r in existing}

# Affichage des 3 premiers timestamps Airtable pour comparaison
print("Airtable timestamps:", list(existing_timestamps)[:3])

# --- Récupération des timestamps depuis Google Sheets ---
df = get_feedbacks()

# Affichage des 3 premiers timestamps Google Sheets pour comparaison
print("Sheets timestamps:", df["timestamp"].tolist()[:3])

# Si les formats sont différents entre les deux sources,
# le filtre anti-doublon dans airtable_writer.py ne fonctionnera pas
# → les timestamps doivent être identiques pour éviter les doublons
