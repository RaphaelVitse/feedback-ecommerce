# ============================================================
# test_sheets.py
# Test de la connexion à Google Sheets
# Vérifie que les avis sont bien récupérés depuis le formulaire
# ============================================================

from src.google_sheets import get_feedbacks  # fonction de lecture Google Sheets

# Appel de la fonction de lecture
df = get_feedbacks()

# Affichage du nombre d'avis récupérés
print(f"{len(df)} avis récupérés")

# Affichage des 5 premières lignes pour vérification visuelle
print(df.head())
