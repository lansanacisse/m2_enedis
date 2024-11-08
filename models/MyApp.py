import streamlit as st
from accueil import accueil_page
from analyse import analyse_page
from contexte import contexte_page
from prediction import prediction_page
from contexte import contexte_page
from analyse import visualisation_graphique, afficher_carte

# Configuration de la page
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
