from src.themes import extract_themes

avis = [
    "Livraison rapide, produit conforme, très satisfait !",
    "Colis abîmé à la réception, vraiment déçu.",
    "Le SAV n'a pas répondu à mes mails.",
    "Produit de mauvaise qualité, ne correspond pas à la description.",
    "Commande reçue en avance, emballage soigné !"
]

themes = extract_themes(avis)
print("Thèmes détectés :", themes)
