from groq import Groq
import os
import re
from dotenv import load_dotenv

load_dotenv()

client = Groq(api_key=os.getenv("GROQ_API_KEY"))

def extract_themes(feedbacks: list[str]) -> list[str]:
    combined = "\n---\n".join(feedbacks[:20])

    response = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=[{
            "role": "user",
            "content": f"""Analyse ces avis clients e-commerce et identifie les 5 thèmes
principaux récurrents. Retourne UNIQUEMENT une liste Python, sans backticks, sans explication.

Avis :
{combined}

Format attendu : ["thème1", "thème2", "thème3", "thème4", "thème5"]"""
        }]
    )

    raw = response.choices[0].message.content.strip()
    # Nettoie les backticks markdown si présents
    raw = re.sub(r"```.*?```", "", raw, flags=re.DOTALL).strip()
    # Extrait la liste entre crochets
    match = re.search(r"\[.*?\]", raw, re.DOTALL)
    if match:
        themes = eval(match.group())
    else:
        themes = ["Non détecté"]
    return themes
