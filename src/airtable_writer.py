from pyairtable import Api
import os
from dotenv import load_dotenv

load_dotenv()

api = Api(os.getenv("AIRTABLE_TOKEN"))
table = api.table(os.getenv("AIRTABLE_BASE_ID"), os.getenv("AIRTABLE_TABLE_NAME"))

def push_to_airtable(df):
    # Récupère les timestamps déjà présents dans Airtable
    existing = table.all(fields=["timestamp"])
    existing_timestamps = {r["fields"].get("timestamp") for r in existing}

    records = []
    for _, row in df.iterrows():
        # Skip si déjà envoyé
        if str(row["timestamp"]) in existing_timestamps:
            continue
        records.append({
            "timestamp": str(row["timestamp"]),
            "nom": str(row["nom"]),
            "categorie": str(row["categorie"]),
            "commentaire": str(row["commentaire"]),
            "note_globale": int(row["note_globale"]) if row["note_globale"] != "" else 0,
            "nps": int(row["nps"]) if row["nps"] != "" else 0,
            "sentiment": str(row["sentiment"]),
            "themes": str(row["themes"])
        })

    if records:
        table.batch_create(records)
        print(f"{len(records)} nouveaux enregistrements envoyés vers Airtable ✅")
    else:
        print("Aucun nouvel enregistrement à envoyer.")
