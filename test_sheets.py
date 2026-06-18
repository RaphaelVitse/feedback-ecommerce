from src.google_sheets import get_feedbacks

df = get_feedbacks()
print(f"{len(df)} avis récupérés")
print(df.head())
