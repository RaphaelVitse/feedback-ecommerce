import gspread
from google.oauth2.service_account import Credentials
import pandas as pd
import json
import os

SCOPES = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive"
]

def get_feedbacks() -> pd.DataFrame:
    # 1. Streamlit Cloud
    try:
        import streamlit as st
        if "GOOGLE_CREDENTIALS" in st.secrets:
            creds_dict = json.loads(st.secrets["GOOGLE_CREDENTIALS"])
            creds = Credentials.from_service_account_info(creds_dict, scopes=SCOPES)
    # 2. GitHub Actions (variable d'environnement)
    except:
        if os.getenv("GOOGLE_CREDENTIALS"):
            creds_dict = json.loads(os.getenv("GOOGLE_CREDENTIALS"))
            creds = Credentials.from_service_account_info(creds_dict, scopes=SCOPES)
        # 3. Local (fichier credentials.json)
        else:
            creds = Credentials.from_service_account_file("credentials.json", scopes=SCOPES)

    client = gspread.authorize(creds)
    sheet = client.open("feedback-ecommerce").sheet1
    data = sheet.get_all_records()

    df = pd.DataFrame(data)
    df.columns = [
        "timestamp", "email", "note_globale",
        "categorie", "commentaire", "nps", "nom"
    ]
    df = df[df["commentaire"].str.strip() != ""]
    df = df.dropna(subset=["commentaire"])
    return df
