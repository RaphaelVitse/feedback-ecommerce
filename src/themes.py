# ============================================================
# themes.py
# Extraction des thèmes récurrents via Groq / Llama 3.1
# API gratuite sans carte bancaire requise
# ============================================================

from groq import Groq  # client API Groq
import os              # accès aux variables d'environnement
import re              # expressions régulières pour parser la réponse
from dotenv import load_dotenv  # lecture du fichier .env

# Chargement des variables d'environnement depuis le fichier .env
load_dotenv()

# Initialisation du client Groq avec la clé API
client = Groq(api_key=os.getenv("GROQ_API_KEY"))

def extract_themes(feedbacks: list[str]) -> list[str]:
    """
    Envoie les avis clients au modèle Llama 3.1 et retourne
    les 5 thèmes principaux détectés.

    Args:
        feedbacks: liste des commentaires clients

    Returns:
        list[str]: liste de 5 thèmes récurrents
    """

    # Concaténation des 20 premiers avis séparés par un délimiteur
    # On limite à 20 pour ne pas dépasser la fenêtre de contexte du modèle
    combined = "\n---\n".join(feedbacks[:20])

    # Appel à l'API Groq avec le modèle Llama 3.1
    response = client.chat.completions.create(
        model="llama-3.1-8b-instant",  # modèle rapide et gratuit
        messages=[{
            "role": "user",
            "content": f"""Analyse ces avis clients e-commerce et identifie les 5 thèmes
principaux récurrents. Retourne UNIQUEMENT une liste Python, sans backticks, sans explication.

Avis :
{combined}

Format attendu : ["thème1", "thème2", "thème3", "thème4", "thème5"]"""
        }]
    )

    # Récupération du texte brut de la réponse
    raw = response.choices[0].message.content.strip()

    # Nettoyage des balises markdown si le modèle en a ajouté
    # ex: ```python [...] ``` → [...]
    raw = re.sub(r"```.*?```", "", raw, flags=re.DOTALL).strip()

    # Extraction de la liste entre crochets avec une expression régulière
    match = re.search(r"\[.*?\]", raw, re.DOTALL)

    if match:
        # Conversion de la chaîne en liste Python
        themes = eval(match.group())
    else:
        # Valeur par défaut si le modèle ne retourne pas le bon format
        themes = ["Non détecté"]

    return themes  # retourne la liste des 5 thèmes
