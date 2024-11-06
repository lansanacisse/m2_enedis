import streamlit as st
from accueil import accueil_page
from analyse import analyse_page
from prediction import prediction_page
from contexte import contexte_page
from analyse import visualisation_graphique, afficher_carte

# Configuration de la page
st.set_page_config(page_title="GreeTech App", page_icon="⚡", layout="wide")

# Barre latérale de navigation avec icônes dans une liste déroulante
st.sidebar.header("GreeTech App ⚡")
options = {
    "🏠 Accueil": "accueil",
    "📊 Contexte": "contexte",
    "🔍 Analyse": "analyse",
    "🔮 Prédiction": "prediction"
}

# Liste déroulante pour la navigation
selected_page = st.sidebar.selectbox(
    "Sélectionner une page", 
    options=list(options.keys())
)

# Déterminer la page sélectionnée à partir de la sélection dans la liste déroulante
page_key = options[selected_page]

# Afficher le contenu de la page sélectionnée
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
    

# Pied de page avec logos
st.sidebar.markdown("---")
st.sidebar.info("© 2024 GreeTech App. Tous droits réservés.")
