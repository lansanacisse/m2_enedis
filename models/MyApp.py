import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import plotly.express as px
from accueil import accueil_page
from donnees import donnees_page, visualisation_geographique
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
    visualisation_geographique()
elif page == "Analyse":
    analyse_page()
elif page == "Prédiction":
    prediction_page()
    # Bouton pour réentraîner le modèle
