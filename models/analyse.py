import streamlit as st
import pandas as pd
from utils import (
   create_styled_line_chart,
   create_styled_histogram,
   create_styled_bar_chart,
   create_styled_pie_chart
)

def analyse_page():
    st.title("Analyse des Données")

    st.write(
        """
        Cette page permet d'analyser les données de performance énergétique des logements en France.
        Vous pouvez visualiser les données sous forme de graphiques pour mieux comprendre les tendances
        et les relations entre les différentes variables.
    """
    )
data = pd.read_csv("../data/merged_69.csv", sep=";")

def visualisation_graphique():
    # Charger les données
    data = pd.read_csv("../data/merged_69.csv", sep=";")

    st.title("Visualisation des Données")

    # Choix du graphique
    st.sidebar.subheader("Choix du graphique")
    option = st.sidebar.selectbox(
        "Type de graphique:", ("Barres", "Camembert", "Lignes", "Histogramme")
    )

    # Sélection de la variable à utiliser pour la visualisation
    st.sidebar.subheader("Choisissez une variable pour visualisation")
    filter_variable = st.sidebar.selectbox(
        "Choisissez une variable:", data.columns
    )

    # Filtrer les données selon la variable choisie
    filtered_data = data[filter_variable].dropna()

    # Affichage du graphique selon le choix de l'utilisateur
    if option == "Camembert":
        fig = create_styled_pie_chart(
            filtered_data.value_counts().index,
            filtered_data.value_counts(),
        )
        st.pyplot(fig)
        if st.button("Télécharger le Camembert en PNG"):
            save_fig_as_png(fig, "camembert")

    elif option == "Barres":
        fig = create_styled_bar_chart(
            filtered_data.value_counts().index,
            filtered_data.value_counts(),
        )
        st.pyplot(fig)
        if st.button("Télécharger les Barres en PNG"):
            save_fig_as_png(fig, "barres")

    elif option == "Lignes":
        fig = create_styled_line_chart(
            filtered_data.value_counts().index,
            filtered_data.value_counts(),
        )
        st.pyplot(fig)
        if st.button("Télécharger les Lignes en PNG"):
            save_fig_as_png(fig, "lignes")

    elif option == "Histogramme":
        fig = create_styled_histogram(
            filtered_data.value_counts(),
        )
        st.pyplot(fig)
        if st.button("Télécharger l'Histogramme en PNG"):
            save_fig_as_png(fig, "histogramme")


def afficher_carte(data):
    """
    Affiche une carte avec des marqueurs pour chaque point dans les données.
    """
    # Créer une carte centrée sur la France
    m = folium.Map(location=[46.603354, 1.888334], zoom_start=5)

    # Ajouter des marqueurs à la carte
    for index, row in data.iterrows():
        folium.Marker(
            location=[row['lat'], row['lon']],
            popup=row.get('name', 'No name')  # Utilise 'No name' si la colonne 'name' n'existe pas
        ).add_to(m)

    # Afficher la carte dans Streamlit
    folium_static(m)