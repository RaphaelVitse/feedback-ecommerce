# ============================================================
# clean_airtable.py
# Script de nettoyage complet de la table Airtable
# Supprime tous les enregistrements existants
# À utiliser uniquement en cas de doublons ou de reset complet
# ⚠️ ATTENTION : action irréversible
# ============================================================

from pyairtable import Api           # client API Airtable
import os                            # accès aux variables d'environnement
from dotenv import load_dotenv       # lecture du fichier .env

# Chargement des variables d'environnement depuis le fichier .env
load_dotenv()

# Connexion à Airtable avec le token personnel
api = Api(os.getenv("AIRTABLE_TOKEN"))

# Connexion à la table Feedbacks
table = api.table(os.getenv("AIRTABLE_BASE_ID"), os.getenv("AIRTABLE_TABLE_NAME"))

# Récupération de tous les enregistrements existants
all_records = table.all()

# Extraction des IDs uniques de chaque enregistrement
# L'ID Airtable est nécessaire pour identifier et supprimer un enregistrement
ids = [r["id"] for r in all_records]

# Suppression par batch de tous les enregistrements
# batch_delete envoie les suppressions en une seule requête API
table.batch_delete(ids)

print(f"{len(ids)} enregistrements supprimés ✅")
