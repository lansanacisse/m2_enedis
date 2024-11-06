import streamlit as st
import numpy as np
import pandas as pd
from io import BytesIO
import matplotlib.pyplot as plt



def contexte_page():
    st.header("Données")
    st.write(
        """
        Les données utilisées dans cette application sont des informations sur la performance énergétique 
        des logements en France. Les données sont collectées par le Ministère de la Transition Écologique et 
        Solidaire et sont disponibles sur le site data.gouv.fr.
    """
    )

    # Charger les données
    data = pd.read_csv("../data/sample.csv", sep=";")

    # Filtres
    st.sidebar.subheader("Filtres")

    # Choisir une variable à filtrer avec "Etiquette_DPE" comme valeur par défaut
    filter_variable = st.sidebar.selectbox(
        "Choisissez une variable pour filtrer les données:",
        data.columns,
        index=list(data.columns).index("Etiquette_DPE"),
    )

    # Créer dynamiquement des filtres basés sur les occurrences des valeurs de la variable choisie
    if filter_variable:
        unique_values = data[filter_variable].unique()
        selected_values = st.sidebar.multiselect(
            f"Choisissez les valeurs de {filter_variable}:",
            unique_values,
            default=unique_values[:3]
        )

    # Appliquer les filtres
    filtered_data = data
    if filter_variable and selected_values:
        filtered_data = filtered_data[
            filtered_data[filter_variable].isin(selected_values)
        ]


    
   # Sélection du nombre de lignes à afficher
    st.sidebar.subheader("Nombre de lignes à afficher")
    max_lines = len(filtered_data)
    num_lines = st.sidebar.slider(
        "Sélectionner le nombre de lignes à afficher:", 
        min_value=1, 
        max_value=max_lines, 
        value=min(100, max_lines)  # Définir la valeur par défaut à 100 ou au maximum de lignes disponibles
    )

    # Afficher un tableau filtré avec le nombre de lignes limité
    st.subheader("Tableau des Données Filtrées")
    st.write(filtered_data.head(num_lines))


    # Bouton de téléchargement CSV
    csv = filtered_data.to_csv(index=False).encode('utf-8')
    st.download_button(
        label="Télécharger les données en CSV",
        data=csv,
        file_name='donnees_filtres.csv',
        mime='text/csv',
    )


