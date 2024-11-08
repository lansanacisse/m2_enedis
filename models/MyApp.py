import streamlit as st
import subprocess
import time
from accueil import accueil_page
from analyse import analyse_page
from contexte import contexte_page
from prediction import prediction_page
from prediction_API import prediction_api_page  # Import de la page de prédiction avec API
from analyse import visualisation_graphique, afficher_carte

#Logo
st.logo("../data/logo.png", size="large")

# Fonction pour démarrer l'API FastAPI en arrière-plan
def start_api():
    return subprocess.Popen(["python", "-m", "uvicorn", "api:app", "--host", "127.0.0.1", "--port", "8001", "--reload"])

# Démarrer l'API
api_process = start_api()
time.sleep(5)  # Pause pour donner le temps à l'API de démarrer

# Configuration de la page Streamlit
st.set_page_config(page_title="GreeTech App", page_icon="⚡", layout="wide")

# Barre latérale de navigation
st.sidebar.header("GreeTech App ⚡")
options = {
    "🏠 Accueil": "accueil",
    "📊 Contexte": "contexte",
    "🔍 Analyse": "analyse",
    "🔮 Prédiction Locale": "prediction",
    "🔮 Prédiction avec API": "prediction_api"  # Nouvelle option pour prédiction avec API
}

# Liste déroulante pour la navigation
selected_page = st.sidebar.selectbox(
    "Sélectionner une page", 
    options=list(options.keys())
)

# Afficher le contenu de la page sélectionnée
page_key = options[selected_page]
if page_key == "accueil":
    accueil_page()
elif page_key == "contexte":
    contexte_page()
elif page_key == "analyse":
    analyse_page()
    visualisation_graphique()
    afficher_carte()
elif page_key == "prediction":
    prediction_page()
elif page_key == "prediction_api":
    prediction_api_page()

# Pied de page avec logos
st.sidebar.markdown("---")
st.sidebar.info("© 2024 GreeTech App. Tous droits réservés.")

# Assurer la fermeture de l'API quand Streamlit est arrêté
def stop_api():
    api_process.terminate()

# Lorsque Streamlit se termine, arrêter l'API
st.sidebar.button("Arrêter l'application", on_click=stop_api)
