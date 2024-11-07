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
    st.title("Analyse des données")
    

import streamlit as st
import pandas as pd
import numpy as np

import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px

import streamlit as st
import pandas as pd
import numpy as np
import seaborn as sns

def visualisation(data):
    kpis = calculate_kpis(data)  # Supposons que calculate_kpis est une fonction définie ailleurs
    afficher_kpis(kpis)  # Supposons que afficher_kpis est une fonction définie ailleurs

    st.sidebar.header("Sélection des mesures et filtres")
    
    # Liste des variables de consommation à utiliser
    consommation_vars = [
        'Type_bâtiment', 
        'Qualité_isolation_enveloppe', 
        'Etiquette_GES', 
        'Surface_habitable_logement', 
        'Etiquette_DPE', 
        'Type_installation_chauffage', 
        'Ubat_W/m²_K', 
        'Qualité_isolation_murs', 
        'Type_énergie_n°1', 
        'Qualité_isolation_plancher_bas', 
        'Méthode_application_DPE', 
        'Qualité_isolation_menuiseries',
        'Conso_5_usages_é_finale',
        "Conso_chauffage_é_primaire",
        "Emission_GES_5_usages_par_m²",
        "Coût_éclairage"
    ]
    
    # Filtrage du dataset pour ne garder que les variables de consommation
    data_filtered = data[consommation_vars]
    
    # Sélection des colonnes numériques et catégorielles parmi celles spécifiées
    numeric_columns = data_filtered.select_dtypes(include=[np.number]).columns.tolist()
    categorical_columns = data_filtered.select_dtypes(include=['object']).columns.tolist()
    all_columns = numeric_columns + categorical_columns
    
    # Sélection des mesures à visualiser avec Etiquette_DPE comme défaut
    default_measure = 'Etiquette_DPE' if 'Etiquette_DPE' in all_columns else all_columns[0]
    selected_measures = st.sidebar.multiselect("Choisissez les mesures à visualiser", all_columns, default=[default_measure])
    
    # Filtrage des modalités si la variable sélectionnée est catégorielle
    filtered_data = data_filtered.copy()
    for selected_measure in selected_measures:
        if selected_measure in categorical_columns:
            unique_values = data_filtered[selected_measure].unique().tolist()
            selected_modalities = st.sidebar.multiselect(f"Filtrer les modalités de {selected_measure}", unique_values, default=unique_values)
            filtered_data = filtered_data[filtered_data[selected_measure].isin(selected_modalities)]

    st.sidebar.header("Sélection des graphiques")

    # Sélection des types de graphiques avec histogramme par défaut
    graph_functions = {
        "Diagramme en aires": st.area_chart,
        "Barres": st.bar_chart,
        "Graphique en ligne": st.line_chart,
        "Scatterplot": st.scatter_chart,
        "Histogramme": st.bar_chart  # Utilisation de bar_chart pour l'histogramme
    }
    default_graph = ["Histogramme"]  # Histogramme sélectionné par défaut
    selected_graphs = st.sidebar.multiselect("Choisissez les graphiques à afficher", list(graph_functions.keys()), default=default_graph)

    # Palette de couleurs pour les graphiques
    palette = sns.color_palette("viridis", len(selected_measures)).as_hex()

    # Préparation des données pour chaque mesure sélectionnée
    for idx, selected_measure in enumerate(selected_measures):
        values = filtered_data[selected_measure].dropna()
        color = palette[idx % len(palette)]  # Couleur unique pour chaque mesure

        for graph in selected_graphs:
            if graph in graph_functions:
                st.subheader(f"{graph} - {selected_measure}")
                if graph == "Scatterplot":
                    if selected_measure in numeric_columns:
                        other_numeric = [col for col in numeric_columns if col != selected_measure]
                        if other_numeric:
                            x_axis = st.selectbox(f"Choisissez la variable pour l'axe X du {graph}", other_numeric)
                            st.scatter_chart(data=filtered_data, x=x_axis, y=selected_measure)
                        else:
                            st.warning("Pas assez de variables numériques pour créer un scatterplot.")
                    else:
                        st.warning("La variable sélectionnée n'est pas numérique. Impossible de créer un scatterplot.")
                elif graph == "Histogramme":
                    if selected_measure in numeric_columns:
                        # Ajout de couleur en stylisant le graphique d'histogramme
                        hist_data = values.value_counts().sort_index().to_frame(name=selected_measure)
                        hist_data = hist_data.style.background_gradient(cmap="viridis")
                        st.dataframe(hist_data)  # Utilisation de background_gradient pour colorier l'histogramme
                    else:
                        st.warning("L'histogramme nécessite une variable numérique.")
                else:
                    if selected_measure in numeric_columns:
                        if not values.empty:
                            graph_functions[graph](values, use_container_width=True)  # Utilisation de la largeur
                        else:
                            st.warning(f"Pas de données disponibles pour afficher le {graph}.")
                    else:
                        # Application de couleurs pour les graphiques de barres pour variables catégorielles
                        value_counts = values.value_counts()
                        st.bar_chart(value_counts, use_container_width=True)



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


