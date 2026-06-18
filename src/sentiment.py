# ============================================================
# sentiment.py
# Analyse de sentiment des avis clients via HuggingFace
# Modèle BERT multilingue — fonctionne en français
# ============================================================

from transformers import pipeline  # pipeline NLP de HuggingFace

# Chargement du modèle de classification de sentiment
# nlptown/bert-base-multilingual-uncased-sentiment :
# - multilingue : fonctionne en français, anglais, etc.
# - retourne une note de 1 à 5 étoiles
# - téléchargé automatiquement au premier lancement (~670MB)
analyzer = pipeline(
    "sentiment-analysis",
    model="nlptown/bert-base-multilingual-uncased-sentiment"
)

def analyze_sentiment(text: str) -> str:
    """
    Analyse le sentiment d'un texte et retourne
    'positif', 'neutre' ou 'négatif'.

    Args:
        text: le commentaire client à analyser

    Returns:
        str: 'positif', 'neutre' ou 'négatif'
    """

    # Le modèle accepte maximum 512 tokens — on tronque si nécessaire
    result = analyzer(text[:512])[0]

    # Le modèle retourne un label de type "4 stars"
    # On extrait le chiffre pour le convertir en sentiment
    score = int(result["label"].split()[0])

    # Conversion de la note en sentiment
    if score >= 4:
        return "positif"   # 4 ou 5 étoiles → satisfait
    elif score == 3:
        return "neutre"    # 3 étoiles → mitigé
    else:
        return "négatif"   # 1 ou 2 étoiles → insatisfait
