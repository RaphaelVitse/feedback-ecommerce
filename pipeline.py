# ============================================================
# pipeline.py
# Orchestration du pipeline complet d'analyse des feedbacks
# Enchaîne : lecture → sentiment → thèmes → stockage
# ============================================================

from src.google_sheets import get_feedbacks      # lecture des avis depuis Google Sheets
from src.sentiment import analyze_sentiment      # analyse de sentiment HuggingFace
from src.themes import extract_themes            # extraction de thèmes Groq/Llama
from src.airtable_writer import push_to_airtable # envoi des résultats vers Airtable

def run_pipeline():
    """
    Exécute le pipeline complet d'analyse des feedbacks clients.
    Appelé soit manuellement depuis le dashboard Streamlit,
    soit automatiquement toutes les 30 minutes via GitHub Actions.

    Étapes :
        1. Lecture des avis depuis Google Sheets
        2. Analyse du sentiment de chaque avis (positif/neutre/négatif)
        3. Extraction des thèmes récurrents sur l'ensemble des avis
        4. Envoi des résultats enrichis vers Airtable
    """

    # --- Étape 1 : Lecture Google Sheets ---
    print("📥 Lecture Google Sheets...")
    df = get_feedbacks()  # retourne un DataFrame avec tous les avis du formulaire

    # --- Étape 2 : Analyse de sentiment ---
    print("🔍 Analyse sentiment...")
    # apply() applique la fonction analyze_sentiment sur chaque ligne du DataFrame
    # Crée une nouvelle colonne "sentiment" avec la valeur positif/neutre/négatif
    df["sentiment"] = df["commentaire"].apply(analyze_sentiment)

    # --- Étape 3 : Extraction des thèmes ---
    print("🏷️ Extraction des thèmes...")
    # Envoie tous les commentaires au LLM pour identifier les thèmes récurrents
    themes = extract_themes(df["commentaire"].tolist())
    # Les thèmes globaux sont ajoutés comme colonne identique sur toutes les lignes
    df["themes"] = str(themes)

    # --- Étape 4 : Envoi vers Airtable ---
    print("☁️ Envoi vers Airtable...")
    # Seuls les nouveaux avis (non présents dans Airtable) sont envoyés
    push_to_airtable(df)

    print("✅ Pipeline terminé !")
    return df  # retourne le DataFrame pour usage éventuel dans le dashboard

# Point d'entrée si le script est lancé directement
# ex: python pipeline.py
if __name__ == "__main__":
    run_pipeline()
