import streamlit as st
import pandas as pd
import folium
from streamlit_folium import folium_static
import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import plotly.express as px
from utils import create_plotly_pie_chart, create_seaborn_bar_chart, create_plotly_histogram, create_plotly_line_chart, calculate_kpis , afficher_kpis

# Charger les données une fois pour les partager entre les fonctions
data = pd.read_csv("../data/sample.csv", sep=";")

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
    st.title("Carte des étiquettes DPE")

    # Filtrer les données pour enlever les lignes contenant des NaN dans les colonnes 'lat' et 'lon'
    data = data.dropna(subset=['lat', 'lon'])

    # Créer une carte Folium centrée sur la France
    m = folium.Map(location=[46.603354, 1.888334], zoom_start=6)

    # Définir une palette de couleurs pour les étiquettes DPE
    dpe_colors = {
        'A': 'green',          # Vert
        'B': 'darkgreen',      # Vert plus foncé
        'C': 'lightgreen',     # Vert clair
        'D': 'yellow',         # Jaune
        'E': 'yellow',         # Jaune
        'F': 'orange',         # Orange
        'G': 'red'             # Rouge
    }

    # Ajouter des marqueurs pour chaque point de données
    for _, row in data.iterrows():
        etiq = row['Etiquette_DPE']
        color = dpe_colors.get(etiq, 'gray')  # Utiliser 'gray' par défaut si l'étiquette n'est pas dans le dictionnaire
        folium.Marker(
            location=[row['lat'], row['lon']],
            popup=f"Étiquette DPE: {etiq}",
            icon=folium.Icon(color=color)
        ).add_to(m)

    # Afficher la carte dans Streamlit
    folium_static(m)


