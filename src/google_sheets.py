# ============================================================
# google_sheets.py
# Connexion à Google Sheets et lecture des réponses du Forms
# ============================================================

import gspread  # bibliothèque pour interagir avec Google Sheets
from google.oauth2.service_account import Credentials  # authentification Google
import pandas as pd  # manipulation des données en tableau
import json  # lecture du JSON des credentials
import os  # accès aux variables d'environnement

# Permissions nécessaires pour lire et écrire sur Google Sheets et Drive
SCOPES = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive"
]

def get_feedbacks() -> pd.DataFrame:
    """
    Se connecte à Google Sheets et retourne les réponses
    du formulaire sous forme de DataFrame pandas.
    Fonctionne en local, sur Streamlit Cloud et GitHub Actions.
    """

    # --- Authentification selon l'environnement ---

    # 1. Streamlit Cloud : credentials stockés dans st.secrets
    try:
        import streamlit as st
        if "GOOGLE_CREDENTIALS" in st.secrets:
            creds_dict = json.loads(st.secrets["GOOGLE_CREDENTIALS"])  # lecture du JSON
            creds = Credentials.from_service_account_info(creds_dict, scopes=SCOPES)

    # 2. GitHub Actions : credentials en variable d'environnement
    except:
        if os.getenv("GOOGLE_CREDENTIALS"):
            creds_dict = json.loads(os.getenv("GOOGLE_CREDENTIALS"))  # lecture du JSON
            creds = Credentials.from_service_account_info(creds_dict, scopes=SCOPES)

        # 3. Local : credentials dans le fichier credentials.json
        else:
            creds = Credentials.from_service_account_file("credentials.json", scopes=SCOPES)

    # Connexion au client Google Sheets avec les credentials
    client = gspread.authorize(creds)

    # Ouverture du Google Sheets lié au formulaire (premier onglet)
    sheet = client.open("feedback-ecommerce").sheet1

    # Récupération de toutes les lignes sous forme de liste de dictionnaires
    data = sheet.get_all_records()

    # Conversion en DataFrame pandas
    df = pd.DataFrame(data)

    # Renommage des colonnes avec des noms courts et utilisables en Python
    df.columns = [
        "timestamp",      # date et heure de soumission
        "email",          # adresse email du client
        "note_globale",   # note de 1 à 5
        "categorie",      # catégorie du problème
        "commentaire",    # texte libre du client
        "nps",            # score NPS de 0 à 10
        "nom"             # nom du client
    ]

    # Suppression des lignes sans commentaire (réponses incomplètes)
    df = df[df["commentaire"].str.strip() != ""]
    df = df.dropna(subset=["commentaire"])

    return df  # retourne le DataFrame nettoyé
