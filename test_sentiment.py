from src.sentiment import analyze_sentiment

avis = [
    "Livraison rapide, produit conforme, très satisfait !",
    "Colis abîmé à la réception, vraiment déçu.",
    "Commande correcte, rien à signaler."
]

for a in avis:
    print(f"{analyze_sentiment(a):10} → {a}")
