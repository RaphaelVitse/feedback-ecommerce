# 📊 Analyseur de Feedbacks Clients E-commerce

Pipeline d'automatisation IA qui collecte, analyse et visualise les avis clients en temps réel, avec alertes automatiques sur les avis négatifs.

## 🎯 Cas d'usage

Toute entreprise e-commerce recevant des avis clients a besoin de :
- Identifier rapidement les clients insatisfaits
- Comprendre les thèmes récurrents de mécontentement
- Alerter le SAV en temps réel sur les avis négatifs

Ce projet automatise entièrement ce processus.

## 🏗️ Architecture
[Google Forms] → [Google Sheets] → [Pipeline Python] → [Airtable] → [Streamlit]

↓

[Make → Slack]

## 🛠️ Stack technique

| Outil | Rôle |
|---|---|
| Google Forms + Sheets | Collecte des avis |
| Python + gspread | Lecture des données |
| HuggingFace (BERT multilingue) | Analyse de sentiment |
| Groq / Llama 3.1 | Extraction de thèmes |
| Airtable | Stockage des résultats enrichis |
| Streamlit + Plotly | Dashboard interactif |
| Make | Automatisation alerte SAV |
| Slack | Notification temps réel |

## 🚀 Installation

### 1. Cloner le projet
```bash
git clone https://github.com/ton-user/feedback-ecommerce.git
cd feedback-ecommerce
```

### 2. Créer l'environnement virtuel
```bash
pyenv local 3.12.9
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### 3. Configurer les variables d'environnement
```bash
cp .env.example .env
```
Remplir le fichier `.env` :
GROQ_API_KEY=gsk_...

AIRTABLE_TOKEN=pat_...

AIRTABLE_BASE_ID=app...

AIRTABLE_TABLE_NAME=Feedbacks

### 4. Ajouter le fichier credentials Google
Placer le fichier `credentials.json` (Google Service Account) à la racine du projet.

## ▶️ Lancement

```bash
source venv/bin/activate
python -m streamlit run dashboard.py
```

## 📋 Fonctionnalités

- **Collecte automatique** : les réponses Google Forms arrivent en temps réel dans Google Sheets
- **Analyse de sentiment** : classification positif / neutre / négatif via BERT multilingue (fonctionne en français)
- **Extraction de thèmes** : identification des 5 thèmes récurrents via Llama 3.1
- **Anti-doublon** : le pipeline ne retraite pas les avis déjà analysés
- **Dashboard temps réel** : auto-refresh toutes les 30 secondes
- **Alerte SAV** : Make envoie une notification Slack à chaque nouvel avis négatif

## 📁 Structure du projet
feedback-ecommerce/

├── src/

│   ├── google_sheets.py      # Lecture Google Sheets

│   ├── sentiment.py          # Analyse HuggingFace

│   ├── themes.py             # Extraction Groq/Llama

│   └── airtable_writer.py    # Push Airtable

├── pipeline.py               # Orchestration

├── dashboard.py              # Interface Streamlit

├── requirements.txt

├── .env.example

└── README.md

## 🔧 Stack 100% gratuite

- HuggingFace : modèle local, aucune clé requise
- Groq : tier gratuit sans CB
- Airtable : tier gratuit
- Make : tier gratuit
- Streamlit : open source
