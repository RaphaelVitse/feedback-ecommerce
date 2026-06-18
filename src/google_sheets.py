import gspread
from google.oauth2.service_account import Credentials
import pandas as pd

SCOPES = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive"
]

def get_feedbacks() -> pd.DataFrame:
    creds = Credentials.from_service_account_file(
        "credentials.json",
        scopes=SCOPES
    )
    client = gspread.authorize(creds)

    sheet = client.open("feedback-ecommerce").sheet1
    data = sheet.get_all_records()

    df = pd.DataFrame(data)

    # Renommage avec les vraies colonnes Google Forms
    df.columns = [
        "timestamp",
        "email",
        "note_globale",
        "categorie",
        "commentaire",
        "nps",
        "nom"
    ]

    # Nettoyage
    df = df[df["commentaire"].str.strip() != ""]
    df = df.dropna(subset=["commentaire"])

    return df
