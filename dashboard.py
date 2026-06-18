# ============================================================
# dashboard.py
# Interface Streamlit de visualisation des feedbacks analysés
# Auto-refresh toutes les 30s + bouton de lancement manuel
# ============================================================

import streamlit as st                    # framework dashboard web
import plotly.express as px               # graphiques interactifs
from pyairtable import Api                # lecture des données depuis Airtable
import os                                 # accès aux variables d'environnement
import pandas as pd                       # manipulation des données
from dotenv import load_dotenv            # lecture du fichier .env
from streamlit_autorefresh import st_autorefresh  # auto-refresh du dashboard
from pipeline import run_pipeline         # pipeline d'analyse complet

# Chargement des variables d'environnement depuis le fichier .env
load_dotenv()

# --- Connexion Airtable ---
# Initialisation du client avec le token personnel
api = Api(os.getenv("AIRTABLE_TOKEN"))

# Connexion à la table Feedbacks
table = api.table(os.getenv("AIRTABLE_BASE_ID"), os.getenv("AIRTABLE_TABLE_NAME"))

def load_data():
    """
    Récupère tous les enregistrements depuis Airtable
    et les retourne sous forme de DataFrame pandas.
    """
    records = table.all()  # récupère tous les enregistrements
    rows = [r["fields"] for r in records]  # extrait uniquement les champs
    return pd.DataFrame(rows)  # conversion en DataFrame

# --- Configuration de la page Streamlit ---
st.set_page_config(
    page_title="Feedback Analyser",
    layout="wide"  # utilise toute la largeur de l'écran
)

# --- Auto-refresh ---
# Recharge le dashboard toutes les 30 secondes
# Relit uniquement Airtable, ne relance pas le pipeline
st_autorefresh(interval=30000, key="autorefresh")

st.title("📊 Analyseur de Feedbacks Clients E-commerce")

# --- Bouton de lancement manuel du pipeline ---
# Permet de forcer une analyse immédiate sans attendre GitHub Actions
if st.button("🔄 Actualiser", type="primary"):
    with st.spinner("Pipeline en cours..."):
        run_pipeline()  # exécute le pipeline complet
    st.success("Analyse terminée ✅")
    st.rerun()  # recharge le dashboard pour afficher les nouveaux avis

# --- Chargement des données depuis Airtable ---
df = load_data()

if df.empty:
    # Aucune donnée disponible → message d'avertissement
    st.warning("Aucune donnée disponible.")
else:
    # --- KPIs ---
    # Affichage des métriques principales en 4 colonnes
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Total avis", len(df))
    col2.metric("😊 Positifs", (df["sentiment"] == "positif").sum())
    col3.metric("😐 Neutres", (df["sentiment"] == "neutre").sum())
    col4.metric("😞 Négatifs", (df["sentiment"] == "négatif").sum())

    st.divider()  # ligne de séparation visuelle

    # --- Graphiques ---
    # Deux graphiques côte à côte
    col_left, col_right = st.columns(2)

    with col_left:
        st.subheader("Répartition des sentiments")
        # Camembert de répartition des sentiments
        fig_pie = px.pie(
            df,
            names="sentiment",  # colonne utilisée pour les parts
            color="sentiment",  # couleur selon le sentiment
            color_discrete_map={
                "positif": "#22c55e",  # vert
                "neutre":  "#94a3b8",  # gris
                "négatif": "#ef4444"   # rouge
            }
        )
        st.plotly_chart(fig_pie, use_container_width=True)

    with col_right:
        st.subheader("Avis par catégorie")
        # Histogramme empilé par catégorie et sentiment
        fig_bar = px.histogram(
            df,
            x="categorie",      # axe horizontal : catégories
            color="sentiment",  # couleur selon le sentiment
            color_discrete_map={
                "positif": "#22c55e",
                "neutre":  "#94a3b8",
                "négatif": "#ef4444"
            }
        )
        st.plotly_chart(fig_bar, use_container_width=True)

    st.divider()

    # --- Tableau filtrable ---
    st.subheader("Détail des avis")

    # Sélecteur de filtre par sentiment
    filtre = st.selectbox(
        "Filtrer par sentiment",
        ["Tous", "positif", "neutre", "négatif"]
    )

    # Application du filtre si différent de "Tous"
    if filtre != "Tous":
        df = df[df["sentiment"] == filtre]

    # Affichage du tableau avec les colonnes pertinentes
    st.dataframe(
        df[["timestamp", "nom", "categorie", "commentaire", "note_globale", "nps", "sentiment"]],
        use_container_width=True  # utilise toute la largeur disponible
    )
