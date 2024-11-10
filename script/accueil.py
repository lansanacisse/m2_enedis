import streamlit as st


def accueil_page():
    st.title("Analyse des données de performance énergétique")
    st.write(
        """
  Bienvenue dans l'application d'analyse et de prédiction de la performance énergétique des logements de la région Rhône-Alpes.
  Cette application a été spécialement conçue pour évaluer et prédire le Diagnostic de Performance Énergétique 
  (DPE) des logements situés en Rhône-Alpes. Elle permet d’explorer les données énergétiques locales en profondeur
  grâce à des outils de visualisation intuitifs et des filtres dynamiques. L’application utilise des modèles avancés
   d’apprentissage automatique pour fournir des estimations précises de l’étiquette DPE et de la consommation énergétique 
   des logements,
    """
    )

    st.image("../data/greentech.jpg", use_column_width=True)
