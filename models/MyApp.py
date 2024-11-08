import streamlit as st
from accueil import accueil_page
from analyse import analyse_page
from contexte import contexte_page
from prediction import prediction_page
from contexte import contexte_page
from analyse import visualisation_graphique, afficher_carte
from prediction_API import prediction_api_page  # Import de la page de prédiction avec API
import subprocess
import time
import requests
# Fonction pour démarrer l'API FastAPI en arrière-plan
def start_api():
    process = subprocess.Popen(["python", "-m", "uvicorn", "api:app", "--host", "127.0.0.1", "--port", "8001", "--reload"])
    time.sleep(3)  # Pause initiale pour permettre le lancement
    return process

# Fonction pour vérifier si l'API est active
def is_api_running():
    url = "http://127.0.0.1:8001/docs"
    try:
        response = requests.get(url)
        return response.status_code == 200
    except requests.ConnectionError:
        return False

# Lancer l'API FastAPI
api_process = start_api()


# Configuration de la page
st.set_page_config(page_title="GreeTech App", page_icon="⚡", layout="wide")

# Afficher le logo avec une taille personnalisée
st.sidebar.image("../data/logo.png", width=300)
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
    visualisation(data)
    afficher_carte(data)
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
