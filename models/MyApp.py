import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import plotly.express as px
from accueil import accueil_page
from donnees import donnees_page, visualisation_geograhique
from analyse import analyse_page
from prediction import prediction_page

# Barre de navigation latérale
st.sidebar.header("GreeTech App ⚡")
page = st.sidebar.selectbox("Pages", ["Acceuil", "Données", "Analyse", "Prédiction"])

# Pages de l'application
if page == "Acceuil":
    accueil_page()
elif page == "Données":
    donnees_page()
    visualisation_geograhique()
elif page == "Analyse":
    analyse_page()
elif page == "Prédiction":
    prediction_page()
    # Bouton pour réentraîner le modèle


# Sélecteur de thème
theme = st.sidebar.selectbox("Choisissez un thème", ["Clair", "Sombre"])

# Appliquer le thème sélectionné
if theme == "Clair":
    st.markdown(
        """
        <style>
        .main { background-color: #ffffff; color: #000000; }
        .sidebar .sidebar-content { background-color: #f0f2f6; }
        </style>
        """,
        unsafe_allow_html=True,
    )
else:
    st.markdown(
        """
        <style>
        .main { background-color: #0e1117; color: #ffffff; }
        .sidebar .sidebar-content { background-color: #262730; }
        </style>
        """,
        unsafe_allow_html=True,
    )
