# ============================================================
# airtable_writer.py
# Envoi des avis analysés vers Airtable
# Inclut un système anti-doublon basé sur le timestamp
# ============================================================

from pyairtable import Api  # client API Airtable
import os                   # accès aux variables d'environnement
from dotenv import load_dotenv  # lecture du fichier .env

# Chargement des variables d'environnement depuis le fichier .env
load_dotenv()

# Initialisation du client Airtable avec le token personnel
api = Api(os.getenv("AIRTABLE_TOKEN"))

# Connexion à la table Feedbacks via l'ID de la base et le nom de la table
table = api.table(os.getenv("AIRTABLE_BASE_ID"), os.getenv("AIRTABLE_TABLE_NAME"))

def push_to_airtable(df):
    """
    Envoie les avis analysés vers Airtable.
    Vérifie les doublons avant l'envoi via le timestamp.

    Args:
        df: DataFrame pandas contenant les avis enrichis
            (sentiment + thèmes ajoutés par le pipeline)
    """

    # Récupération de tous les timestamps déjà présents dans Airtable
    # Permet de ne pas renvoyer des avis déjà traités
    existing = table.all(fields=["timestamp"])

    # Construction d'un ensemble (set) de timestamps existants
    # Le set permet une recherche rapide en O(1)
    existing_timestamps = {r["fields"].get("timestamp") for r in existing}

    # Construction de la liste des nouveaux enregistrements à envoyer
    records = []
    for _, row in df.iterrows():

        # Si le timestamp existe déjà dans Airtable → on ignore cet avis
        if str(row["timestamp"]) in existing_timestamps:
            continue

        # Sinon on prépare l'enregistrement au format Airtable
        records.append({
            "timestamp":    str(row["timestamp"]),
            "nom":          str(row["nom"]),
            "categorie":    str(row["categorie"]),
            "commentaire":  str(row["commentaire"]),
            # Conversion en entier avec valeur par défaut 0 si vide
            "note_globale": int(row["note_globale"]) if row["note_globale"] != "" else 0,
            "nps":          int(row["nps"]) if row["nps"] != "" else 0,
            "sentiment":    str(row["sentiment"]),
            "themes":       str(row["themes"])
        })

    # Envoi par batch uniquement s'il y a de nouveaux enregistrements
    if records:
        # batch_create envoie plusieurs enregistrements en une seule requête API
        table.batch_create(records)
        print(f"{len(records)} nouveaux enregistrements envoyés vers Airtable ✅")
    else:
        # Aucun nouvel avis détecté → pas d'envoi
        print("Aucun nouvel enregistrement à envoyer.")
