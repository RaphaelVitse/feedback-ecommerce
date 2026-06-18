import streamlit as st
import plotly.express as px
from pyairtable import Api
import os
import pandas as pd
from dotenv import load_dotenv
from streamlit_autorefresh import st_autorefresh
from pipeline import run_pipeline
import time

load_dotenv()

# Connexion Airtable
api = Api(os.getenv("AIRTABLE_TOKEN"))
table = api.table(os.getenv("AIRTABLE_BASE_ID"), os.getenv("AIRTABLE_TABLE_NAME"))

def load_data():
    records = table.all()
    rows = [r["fields"] for r in records]
    return pd.DataFrame(rows)

# Config page
st.set_page_config(page_title="Feedback Analyser", layout="wide")

# ✅ Auto-refresh toutes les 30s
count = st_autorefresh(interval=60000, key="autorefresh")

# Ajout d'un compteur decomptant le temps restant avant la prochaine reference
elapsed = time.time() % 60
remaining = int(60 - elapsed)

st.components.v1.html(f"""
<div style="
    font-family: sans-serif;
    color: #94a3b8;
    font-size: 0.85rem;
    padding: 8px 0;
">
    🔄 Prochaine mise à jour dans :
    <span id="countdown" style="
        font-weight: bold;
        color: #22c55e;
        font-size: 1rem;
    ">{remaining}s</span>
</div>

<script>
    let seconds = {remaining};
    const el = document.getElementById("countdown");

    const interval = setInterval(() => {{
        seconds--;
        if (seconds <= 0) {{
            el.textContent = "Mise à jour...";
            el.style.color = "#f59e0b";
            clearInterval(interval);
        }} else {{
            el.textContent = seconds + "s";
            // Passe au rouge quand < 5s
            el.style.color = seconds < 5 ? "#ef4444" : "#22c55e";
        }}
    }}, 1000);
</script>
""", height=40)



st.title("📊 Analyseur de Feedbacks Clients E-commerce")

# ✅ Pipeline automatique à chaque refresh (pas de bouton)
with st.spinner("Vérification des nouveaux avis..."):
    run_pipeline()

# Chargement données
df = load_data()

if df.empty:
    st.warning("Aucune donnée disponible.")
else:
    # KPIs
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Total avis", len(df))
    col2.metric("😊 Positifs", (df["sentiment"] == "positif").sum())
    col3.metric("😐 Neutres", (df["sentiment"] == "neutre").sum())
    col4.metric("😞 Négatifs", (df["sentiment"] == "négatif").sum())

    st.divider()

    col_left, col_right = st.columns(2)

    with col_left:
        st.subheader("Répartition des sentiments")
        fig_pie = px.pie(
            df, names="sentiment",
            color="sentiment",
            color_discrete_map={
                "positif": "#22c55e",
                "neutre": "#94a3b8",
                "négatif": "#ef4444"
            }
        )
        st.plotly_chart(fig_pie, use_container_width=True)

    with col_right:
        st.subheader("Avis par catégorie")
        fig_bar = px.histogram(
            df, x="categorie",
            color="sentiment",
            color_discrete_map={
                "positif": "#22c55e",
                "neutre": "#94a3b8",
                "négatif": "#ef4444"
            }
        )
        st.plotly_chart(fig_bar, use_container_width=True)

    st.divider()

    st.subheader("Détail des avis")
    filtre = st.selectbox("Filtrer par sentiment", ["Tous", "positif", "neutre", "négatif"])
    if filtre != "Tous":
        df = df[df["sentiment"] == filtre]

    st.dataframe(
        df[["timestamp", "nom", "categorie", "commentaire", "note_globale", "nps", "sentiment"]],
        use_container_width=True
    )

# ✅ Indicateur discret de dernière mise à jour
st.caption(f"🔄 Dernière vérification : refresh #{count}")
