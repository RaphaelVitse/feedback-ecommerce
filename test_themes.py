# ============================================================
# test_themes.py
# Test de l'extraction de thèmes sur des avis fictifs
# Vérifie que le modèle Groq/Llama retourne bien une liste
# ============================================================

from src.themes import extract_themes  # fonction d'extraction de thèmes

# Liste d'avis fictifs couvrant différentes problématiques e-commerce
# Permet de vérifier que le modèle détecte les bons thèmes
avis = [
    "Livraison rapide, produit conforme, très satisfait !",
    "Colis abîmé à la réception, vraiment déçu.",
    "Le SAV n'a jamais répondu à mes emails.",
    "Produit de mauvaise qualité, ne correspond pas à la description.",
    "Commande reçue en 24h, parfait !"
]

# Appel de la fonction d'extraction de thèmes
themes = extract_themes(avis)

# Affichage des thèmes détectés par le LLM
print("Thèmes détectés :", themes)
