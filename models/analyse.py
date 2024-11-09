import streamlit as st
import pandas as pd
import folium
from streamlit_folium import folium_static
import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import plotly.express as px
from utils import (
    create_plotly_pie_chart,
    create_seaborn_bar_chart,
    create_plotly_histogram,
    create_plotly_line_chart,
    calculate_kpis,
    afficher_kpis,
)

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


def visualisation(data):
    kpis = calculate_kpis(data)
    afficher_kpis(kpis)

    st.sidebar.header("Sélection des mesures et filtres")

    # Définition des variables à utiliser
    consommation_vars = [
        "Type_bâtiment",
        "Qualité_isolation_enveloppe",
        "Etiquette_GES",
        "Surface_habitable_logement",
        "Etiquette_DPE",
        "Type_installation_chauffage",
        "Ubat_W/m²_K",
        "Qualité_isolation_murs",
        "Type_énergie_n°1",
        "Qualité_isolation_plancher_bas",
        "Méthode_application_DPE",
        "Qualité_isolation_menuiseries",
        "Conso_5_usages_é_finale",
    ]

    etiquette_vars = [
        "Conso_chauffage_é_primaire",
        "Conso_5_usages_é_finale",
        "Emission_GES_5_usages_par_m²",
        "Etiquette_GES",
        "Coût_éclairage",
        "Etiquette_DPE",
    ]

    all_vars = list(set(consommation_vars + etiquette_vars))

    # Sélection de la mesure à visualiser
    selected_measure = st.sidebar.selectbox(
        "Choisissez une mesure à visualiser",
        all_vars,
        index=all_vars.index("Etiquette_DPE") if "Etiquette_DPE" in all_vars else 0,
    )

    # Filtrage des modalités si la variable sélectionnée est catégorielle
    filtered_data = data[all_vars].copy()
    if filtered_data[selected_measure].dtype == "object":
        unique_values = filtered_data[selected_measure].unique().tolist()
        selected_modalities = st.sidebar.multiselect(
            f"Filtrer les modalités de {selected_measure}",
            unique_values,
            default=unique_values,
        )
        filtered_data = filtered_data[
            filtered_data[selected_measure].isin(selected_modalities)
        ]

    st.sidebar.header("Sélection des graphiques")

    # Sélection des types de graphiques avec "Barres" par défaut
    graph_options = ["Barres", "Camembert", "Histogramme", "Ligne"]
    selected_graphs = st.sidebar.multiselect(
        "Choisissez les graphiques à afficher", graph_options, default=["Barres"]
    )

    # Préparation des données
    values = filtered_data[selected_measure].dropna()

    def create_plotly_pie_chart(labels, sizes):
        fig = px.pie(
            names=labels,
            values=sizes,
            title="Répartition des valeurs",
            color_discrete_sequence=px.colors.sequential.Viridis,
        )
        fig.update_traces(textposition="inside", textinfo="percent+label")
        fig.update_layout(title_font_size=20)
        return fig

    def create_seaborn_bar_chart(labels, values):
        fig, ax = plt.subplots(figsize=(10, 6))
        sns.barplot(x=labels, y=values, palette="viridis", ax=ax)
        ax.set_title(
            "Répartition des données par catégorie", fontsize=14, weight="bold"
        )
        ax.set_xlabel("Catégories", fontsize=12)
        ax.set_ylabel("Valeurs", fontsize=12)
        plt.xticks(rotation=45)
        plt.tight_layout()
        return fig

    def create_plotly_histogram(values):
        fig = px.histogram(
            values,
            nbins=20,
            title="Distribution des valeurs",
            color_discrete_sequence=["skyblue"],
        )
        fig.update_layout(
            xaxis_title="Valeurs", yaxis_title="Fréquence", title_font_size=20
        )
        return fig

    def create_plotly_line_chart(x, y):
        fig = px.line(
            x=x, y=y, title="Évolution des valeurs", markers=True, line_shape="spline"
        )
        fig.update_layout(
            xaxis_title="Catégories", yaxis_title="Valeurs", title_font_size=20
        )
        return fig

    for graph in selected_graphs:
        if pd.api.types.is_numeric_dtype(filtered_data[selected_measure]):
            chart_data = filtered_data[selected_measure].value_counts().sort_index()
            labels = chart_data.index
            sizes = chart_data.values
        else:
            chart_data = filtered_data[selected_measure].value_counts()
            labels = chart_data.index
            sizes = chart_data.values

        if graph == "Barres":
            fig = create_seaborn_bar_chart(labels, sizes)
            st.pyplot(fig)
        elif graph == "Camembert":
            fig = create_plotly_pie_chart(labels, sizes)
            st.plotly_chart(fig)
        elif graph == "Histogramme":
            if pd.api.types.is_numeric_dtype(filtered_data[selected_measure]):
                fig = create_plotly_histogram(values)
                st.plotly_chart(fig)
            else:
                st.warning(
                    "L'histogramme n'est disponible que pour les variables numériques."
                )
        elif graph == "Ligne":
            fig = create_plotly_line_chart(labels, sizes)
            st.plotly_chart(fig)


def afficher_carte(data):
    st.title("Carte des étiquettes DPE")

    # Filtrer les données pour enlever les lignes contenant des NaN dans les colonnes 'lat' et 'lon'
    data = data.dropna(subset=["lat", "lon"])

    # Créer une carte Folium centrée sur la France
    m = folium.Map(location=[46.603354, 1.888334], zoom_start=6, ax_bounds=True)

    # Définir une palette de couleurs pour les étiquettes DPE
    dpe_colors = {
        "A": "green",  # Vert
        "B": "darkgreen",  # Vert plus foncé
        "C": "lightgreen",  # Vert clair
        "D": "yellow",  # Jaune
        "E": "yellow",  # Jaune
        "F": "orange",  # Orange
        "G": "red",  # Rouge
    }

    # Ajouter des marqueurs pour chaque point de données
    for _, row in data.iterrows():
        etiq = row["Etiquette_DPE"]
        color = dpe_colors.get(
            etiq, "gray"
        )  # Utiliser 'gray' par défaut si l'étiquette n'est pas dans le dictionnaire
        folium.Marker(
            location=[row["lat"], row["lon"]],
            popup=f"Étiquette DPE: {etiq}",
            icon=folium.Icon(color=color),
        ).add_to(m)

    # Afficher la carte dans Streamlit
    folium_static(m, width=1500, height=1000)
