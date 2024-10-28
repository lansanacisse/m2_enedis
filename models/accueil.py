import streamlit as st


def accueil_page():
    st.title("Analyse des données de performance énergétique")
    st.write(
        """
        Bienvenue dans l'application d'analyse des données de performance énergétique.
        Utilisez le menu de gauche pour naviguer entre les différentes pages de l'application.
        Cette application permet d'analyser et de prédire le Diagnostic de Performance Énergétique (DPE)
        des logements en France. Elle utilise des modèles d'apprentissage automatique pour estimer 
        l'étiquette DPE et la consommation énergétique en fonction des caractéristiques du logement.
    """
    )

    st.image("../data/greentech.jpg", use_column_width=True)
