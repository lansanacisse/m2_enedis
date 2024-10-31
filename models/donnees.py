import streamlit as st
import numpy as np
import pandas as pd
from io import BytesIO
import matplotlib.pyplot as plt
from utils import (
    save_fig_as_png,
    create_pie_chart,
    create_bar_chart,
    create_line_chart,
    create_histogram,
)


def donnees_page():
    st.header("Données")
    st.write(
        """
        Les données utilisées dans cette application sont des informations sur la performance énergétique 
        des logements en France. Les données sont collectées par le Ministère de la Transition Écologique et 
        Solidaire et sont disponibles sur le site data.gouv.fr.
    """
    )

    # Charger les données
    data = pd.read_csv("../data/preprocessed_data.csv")

    # Filtres
    st.sidebar.subheader("Filtres")
    dpe_filter = st.sidebar.multiselect(
        "Sélectionner les étiquettes DPE:",
        data["Etiquette_DPE"].unique(),
        default=[data["Etiquette_DPE"].unique()[0]],  # Sélection par défaut
    )
    postal_code_filter = st.sidebar.multiselect(
        "Sélectionner les codes postaux:",
        data["Code_postal_(BAN)"].unique(),
        default=[data["Code_postal_(BAN)"].unique()[0]],  # Sélection par défaut
    )

    # Appliquer les filtres
    filtered_data = data
    if dpe_filter:
        filtered_data = filtered_data[filtered_data["Etiquette_DPE"].isin(dpe_filter)]
    if postal_code_filter:
        filtered_data = filtered_data[
            filtered_data["Code_postal_(BAN)"].isin(postal_code_filter)
        ]

    # Afficher un tableau filtré
    st.subheader("Tableau des Données Filtrées")
    st.write(filtered_data)

    st.title("Visualisation des Données")

    # Choix du graphique
    st.sidebar.subheader("Choix du graphique")
    option = st.sidebar.selectbox(
        "Type de graphique:", ("Barres", "Camembert", "Lignes", "Histogramme")
    )

    # Affichage du graphique selon le choix de l'utilisateur
    if option == "Camembert":
        fig = create_pie_chart(
            data["Etiquette_DPE"].value_counts().index,
            data["Etiquette_DPE"].value_counts(),
        )
        st.pyplot(fig)
        if st.button("Télécharger le Camembert en PNG"):
            save_fig_as_png(fig, "camembert")

    elif option == "Barres":
        fig = create_bar_chart(
            data["Etiquette_DPE"].value_counts().index,
            data["Etiquette_DPE"].value_counts(),
        )
        st.pyplot(fig)
        if st.button("Télécharger le Barres en PNG"):
            save_fig_as_png(fig, "barres")

    elif option == "Lignes":
        fig = create_line_chart(
            data["Etiquette_DPE"].value_counts().index,
            data["Etiquette_DPE"].value_counts(),
        )
        st.pyplot(fig)
        if st.button("Télécharger le Lignes en PNG"):
            save_fig_as_png(fig, "lignes")

    elif option == "Histogramme":
        fig = create_histogram(
            data["Etiquette_DPE"].value_counts(),
            data["Etiquette_DPE"].value_counts().index,
        )
        st.pyplot(fig)
        if st.button("Télécharger l'Histogramme en PNG"):
            save_fig_as_png(fig, "histogramme")


# Données géographiques
def visualisation_geograhique():
    st.sidebar.subheader("Carte géographique")
    show_map = st.sidebar.checkbox("Afficher la carte", value=True)

    if show_map:
        st.subheader("Carte géographique des données")
        # Exemple de données géographiques
        map_data = pd.DataFrame(
            np.random.randn(1000, 2) / [50, 50] + [48.8566, 2.3522],
            columns=["lat", "lon"],
        )
        st.map(map_data)
