from src.google_sheets import get_feedbacks
from src.sentiment import analyze_sentiment
from src.themes import extract_themes
from src.airtable_writer import push_to_airtable

def run_pipeline():
    print("📥 Lecture Google Sheets...")
    df = get_feedbacks()

    print("🔍 Analyse sentiment...")
    df["sentiment"] = df["commentaire"].apply(analyze_sentiment)

    print("🏷️ Extraction des thèmes...")
    themes = extract_themes(df["commentaire"].tolist())
    df["themes"] = str(themes)

    print("☁️ Envoi vers Airtable...")
    push_to_airtable(df)

    print("✅ Pipeline terminé !")
    return df

if __name__ == "__main__":
    run_pipeline()
