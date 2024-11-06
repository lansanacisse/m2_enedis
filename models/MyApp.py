import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import plotly.express as px
from accueil import accueil_page
from analyse import analyse_page
from prediction import prediction_page
from contexte import contexte_page, visualisation_geographique


# Barre de navigation latérale
st.sidebar.header("GreeTech App ⚡")
page = st.sidebar.selectbox("Pages", ["Acceuil", "Contexte", "Analyse", "Prédiction"])

# Pages de l'application
if page == "Acceuil":
    accueil_page()
elif page == "Contexte":
    contexte_page()
    visualisation_geographique()
elif page == "Analyse":
    analyse_page()
elif page == "Prédiction":
    prediction_page()
    # Bouton pour réentraîner le modèle
