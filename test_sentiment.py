# ============================================================
# test_sentiment.py
# Test de l'analyse de sentiment sur des avis fictifs
# Vérifie que le modèle HuggingFace fonctionne correctement
# ============================================================

from src.sentiment import analyze_sentiment  # fonction d'analyse de sentiment

# Liste d'avis fictifs pour tester les 3 cas possibles
# Couvre les cas positif, négatif et neutre
avis = [
    "Livraison rapide, produit conforme, très satisfait !",  # attendu : positif
    "Colis abîmé à la réception, vraiment déçu.",            # attendu : négatif
    "Commande correcte, rien à signaler."                     # attendu : neutre
]

# Analyse de chaque avis et affichage du résultat
for a in avis:
    # :10 → alignement du sentiment sur 10 caractères pour lisibilité
    print(f"{analyze_sentiment(a):10} → {a}")
