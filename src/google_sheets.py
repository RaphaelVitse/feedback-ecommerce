import gspread
from google.oauth2.service_account import Credentials
import pandas as pd
import streamlit as st
import json
import os

SCOPES = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive"
]

def get_feedbacks() -> pd.DataFrame:
    # Lecture credentials depuis Streamlit secrets ou fichier local
    if "GOOGLE_CREDENTIALS" in st.secrets:
        creds_dict = json.loads(st.secrets["GOOGLE_CREDENTIALS"])
        creds = Credentials.from_service_account_info(creds_dict, scopes=SCOPES)
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
