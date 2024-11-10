# Importation des bibliothèques nécessaires
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import plotly.express as px
from io import BytesIO
import streamlit as st
from scipy import stats as ss
from sklearn.neighbors import KNeighborsClassifier
from sklearn.linear_model import LinearRegression
from sklearn.tree import DecisionTreeRegressor
from sklearn.ensemble import RandomForestRegressor
from xgboost import XGBRegressor
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
import joblib
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px


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
    ax.set_title("Répartition des données par catégorie", fontsize=14, weight="bold")
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


# Créer un graphique en pgn
def save_fig_as_png(fig, filename):
    buf = BytesIO()
    fig.savefig(buf, format="png")
    st.download_button(
        label="Télécharger l'image",
        data=buf,
        file_name=f"{filename}.png",
        mime="image/png",
    )


# Fonction pour charger un modèle spécifique
def load_model(model_option, target_variable):
    models = {
        "Conso_5_usages_é_finale": {
            "XGBoost": "../models/consommation_xgboost_model.pkl",
            "Arbre de Décision": "../models/consommation_arbre_de_decision_model.pkl",
            "Forêt Aléatoire": "../models/consommation_random_forest.pkl",
        },
        "Etiquette_DPE": {
            "K-nearest neighbors": "../models/etiquette_knn_model.pkl",
            "Arbre de Décision": "../models/etiquette_arbre_de_decision_model.pkl",
            "Forêt Aléatoire": "../models/etiquette_random_forest_model.pkl",
        },
    }
    model_file = models[target_variable][model_option]
    model = joblib.load(model_file)
    return model


# Entraîner et sauvegarder les modèles
def train_and_save_models(data_path, target_variable):
    # Charger les données
    data = pd.read_csv(data_path)

    if target_variable == "Consommation Énergétique":
        X = data[
            [
                "Surface_habitable_logement",
                "Ubat_W/m²_K",
                "Etiquette_DPE",
                "Type_énergie_principale_chauffage",
            ]
        ]
        y = data["Conso_5_usages_é_finale"]

        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=0.2, random_state=42
        )

        xboost = XGBRegressor()
        xboost.fit(X_train, y_train)
        joblib.dump(xboost, "consommation_xgboost_model.pkl")

        dec_tree = DecisionTreeRegressor()
        dec_tree.fit(X_train, y_train)
        joblib.dump(dec_tree, "consommation_arbre_de_decision_model.pkl")

        rand_forest = RandomForestRegressor(n_estimators=100)
        rand_forest.fit(X_train, y_train)
        joblib.dump(rand_forest, "consommation_random_forest_model.pkl")

    elif target_variable == "Étiquette DPE":
        X = data[
            [
                "Conso_chauffage_é_primaire",
                "Conso_5_usages_é_finale",
                "Emission_GES_5_usages_par_m²",
                "Etiquette_GES",
                "Coût_éclairage",
            ]
        ]
        y = data["Etiquette_DPE"]

        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=0.2, random_state=42
        )

        knn = KNeighborsClassifier(n_neighbors=5)
        knn.fit(X_train, y_train)
        joblib.dump(knn, "etiquette_knn_model.pkl")

        dec_tree = DecisionTreeClassifier()
        dec_tree.fit(X_train, y_train)
        joblib.dump(dec_tree, "etiquette_arbre_de_decision_model.pkl")

        rand_forest = RandomForestClassifier(n_estimators=100)
        rand_forest.fit(X_train, y_train)
        joblib.dump(rand_forest, "etiquette_random_forest_model.pkl")

    print(f"Modèles pour {target_variable} entraînés et sauvegardés avec succès.")


# Fonction pour réentraîner le modèle avec les nouveaux paramètres
def retrain_model(
    model_option, params, prediction_type, data_path="../data/preprocessed_data.csv"
):
    # Charger les données
    data = pd.read_csv(data_path)

    # Sélection des caractéristiques et du modèle en fonction du type de prédiction
    if prediction_type == "Étiquette DPE":
        X = data[
            [
                "Conso_chauffage_é_primaire",
                "Conso_5_usages_é_finale",
                "Emission_GES_5_usages_par_m²",
                "Etiquette_GES",
                "Coût_éclairage",
            ]
        ]
        y = data["Etiquette_DPE"]
        # Sélection du modèle spécifique pour l'Étiquette DPE
        if model_option == "K-nearest neighbors":
            model = KNeighborsClassifier(**params)
            model_filename = "etiquette_knn_model.pkl"
        elif model_option == "Forêt Aléatoire":
            model = RandomForestClassifier(**params)
            model_filename = "etiquette_random_forest_model.pkl"
        elif model_option == "Arbre de Décision":
            model = DecisionTreeClassifier(**params)
            model_filename = "etiquette_arbre_de_decision_model.pkl"
    elif prediction_type == "Consommation Énergétique":
        X = data[
            [
                "Surface_habitable_logement",
                "Ubat_W/m²_K",
                "Etiquette_DPE",
                "Type_énergie_principale_chauffage",
            ]
        ]
        y = data["Conso_5_usages_é_finale"]
        # Sélection du modèle spécifique pour la Consommation Énergétique
        if model_option == "XGBoost":
            model = XGBRegressor(**params)
            model_filename = "consommation_xgboost_model.pkl"
        elif model_option == "Forêt Aléatoire":
            model = RandomForestRegressor(**params)
            model_filename = "consommation_random_forest_model.pkl"
        elif model_option == "Arbre de Décision":
            model = DecisionTreeRegressor(**params)
            model_filename = "consommation_arbre_de_decision_model.pkl"

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42
    )

    # Entraîner le modèle
    model.fit(X_train, y_train)

    # Sauvegarder le modèle
    joblib.dump(model, model_filename)
    return model


# Mapping des valeurs pour les encodages
encoding_maps = {
    "Type_bâtiment": {"Maison": 0.0, "Appartement": 1.0, "Immeuble": 2.0},
    "Qualité_isolation_enveloppe": {
        "insuffisante": 0.0,
        "moyenne": 1.0,
        "bonne": 2.0,
        "très bonne": 3.0,
    },
    "Etiquette_GES": {
        "A": 0.0,
        "B": 1.0,
        "C": 2.0,
        "D": 3.0,
        "E": 4.0,
        "F": 5.0,
        "G": 6.0,
    },
    "Etiquette_DPE": {
        "A": 0.0,
        "B": 1.0,
        "C": 2.0,
        "D": 3.0,
        "E": 4.0,
        "F": 5.0,
        "G": 6.0,
    },
    "Type_installation_chauffage": {
        "individuel": 0.0,
        "collectif": 1.0,
        "mixte (collectif-individuel)": 2.0,
    },
    "Type_énergie_n°1": {
        "Gaz naturel": 0.0,
        "Électricité": 1.0,
        "Réseau de Chauffage urbain": 2.0,
        "Bois – Granulés (pellets) ou briquettes": 3.0,
        "Fioul domestique": 4.0,
    },
    "Méthode_application_DPE": {
        "dpe appartement individuel": 0.0,
        "dpe appartement généré à partir des données DPE immeuble": 1.0,
        "dpe maison individuelle": 2.0,
        "dpe issu d'une étude thermique réglementaire RT2012 bâtiment : appartement": 3.0,
        "dpe issu d'une étude thermique réglementaire RT2012 bâtiment : maison individuelle": 4.0,
        "dpe immeuble collectif": 5.0,
    },
    "Qualité_isolation_murs": {
        "insuffisante": 0.0,
        "moyenne": 1.0,
        "bonne": 2.0,
        "très bonne": 3.0,
    },
    "Qualité_isolation_plancher_bas": {
        "insuffisante": 0.0,
        "moyenne": 1.0,
        "bonne": 2.0,
        "très bonne": 3.0,
    },
    "Qualité_isolation_menuiseries": {
        "insuffisante": 0.0,
        "moyenne": 1.0,
        "bonne": 2.0,
        "très bonne": 3.0,
    },
}


# Fonction d'encodage des données d'entrée
def encode_input_data(input_data):
    encoded_data = {}
    for column, value in input_data.items():
        if column in encoding_maps:
            encoded_data[column] = float(encoding_maps[column].get(value, None))
        else:
            encoded_data[column] = value
    return encoded_data


def predict(type_prediction, model, **kwargs):
    """
    Fonction de prédiction unique pour l'étiquette DPE ou la consommation énergétique.
    type_prediction : str - "Étiquette DPE" ou "Consommation Énergétique"
    model : modèle de prédiction entraîné
    kwargs : caractéristiques du logement nécessaires pour la prédiction
    """
    if type_prediction == "Consommation Énergétique":
        # Encodage des données d'entrée
        encoded_data = encode_input_data(kwargs)

        # Extraire les variables nécessaires pour la prédiction de la consommation
        columns = [
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
        ]

        X = pd.DataFrame(
            [
                [
                    encoded_data.get("Type_bâtiment"),
                    encoded_data.get("Qualité_isolation_enveloppe"),
                    encoded_data.get("Etiquette_GES"),
                    encoded_data.get("Surface_habitable_logement"),
                    encoded_data.get("Etiquette_DPE"),
                    encoded_data.get("Type_installation_chauffage"),
                    encoded_data.get("Ubat_W/m²_K"),
                    encoded_data.get("Qualité_isolation_murs"),
                    encoded_data.get("Type_énergie_n°1"),
                    encoded_data.get("Qualité_isolation_plancher_bas"),
                    encoded_data.get("Méthode_application_DPE"),
                    encoded_data.get("Qualité_isolation_menuiseries"),
                ]
            ],
            columns=columns,
        )

        # Prédire la consommation énergétique
        prediction = model.predict(X)[0]
        return prediction
    elif type_prediction == "Étiquette DPE":
        # Encodage des données d'entrée
        encoded_data = encode_input_data(kwargs)

        # Extraire les variables nécessaires pour la prédiction de l'étiquette DPE
        columns = [
            "Conso_5_usages_par_m²_é_primaire",
            "Conso_5_usages/m²_é_finale",
            "Emission_GES_5_usages_par_m²",
            "Etiquette_GES",
            "Coût_éclairage",
        ]

        X = pd.DataFrame(
            [
                [
                    encoded_data.get("Conso_5_usages_par_m²_é_primaire"),
                    encoded_data.get("Conso_5_usages/m²_é_finale"),
                    encoded_data.get("Emission_GES_5_usages_par_m²"),
                    encoded_data.get("Etiquette_GES"),
                    encoded_data.get("Coût_éclairage"),
                ]
            ],
            columns=columns,
        )

        # Prédire l'étiquette DPE
        prediction = model.predict(X)[0]
        return prediction


def calculate_kpis(data):
    kpis = {}

    # KPI 1: Consommation moyenne des logements
    moyenne_conso = data["Conso_5_usages_é_finale"].mean()
    kpis["conso_energetique_moyenne"] = moyenne_conso

    # KPI 2: Pourcentage de logements au-dessus de la consommation moyenne
    kpis["pct_logements_au_dessus_moyenne"] = (
        data["Conso_5_usages_é_finale"] > moyenne_conso
    ).mean() * 100

    # KPI 3: Taux de logements « passoires énergétiques » (étiquette DPE F ou G)
    passoires_energetiques = data["Etiquette_DPE"].isin(["F", "G"]).sum()
    kpis["taux_passoires_energetiques"] = (passoires_energetiques / len(data)) * 100

    # KPI 4: Etiquette DPE la plus fréquente
    kpis["etiquette_dpe_frequente"] = data["Etiquette_DPE"].mode()[0]

    return kpis


def afficher_kpis(kpis):
    st.title("Indicateurs Clés de Performance (KPI)")
    st.markdown("---")

    # Noms lisibles pour les KPI avec textes réduits
    kpis_readable = {
        "conso_energetique_moyenne": "Consommation Energétique Moyenne (en kWh/logement)",
        "pct_logements_au_dessus_moyenne": " Poucentage de Logements au-dessus de la Moyenne",
        "taux_passoires_energetiques": "Taux de Passoires Energétiques (en %)",
        "etiquette_dpe_frequente": "Etiquette DPE la plus fréquente",
    }

    # Couleurs et icônes pour les KPI
    colors = {
        "conso_energetique_moyenne": "#AED6F1",  # Bleu
        "pct_logements_au_dessus_moyenne": "#ABEBC6 ",  # Vert
        "taux_passoires_energetiques": "#f0b27a",  # Orange
        "etiquette_dpe_frequente": "#d5d8dc",  # Gris
    }

    icons = {
        "conso_energetique_moyenne": "🔋",  # Batterie
        "pct_logements_au_dessus_moyenne": "🏠",  # Maison
        "taux_passoires_energetiques": "⚡",  # Éclair
        "etiquette_dpe_frequente": "🏷️",  # Étiquette
    }

    # Disposer les KPI en colonnes
    col1, col2, col3, col4 = st.columns(4)
    cols = [col1, col2, col3, col4]
    kpi_keys = list(kpis.keys())

    for i in range(4):
        with cols[i]:
            value = kpis[kpi_keys[i]]
            # Limiter l'affichage des chiffres à 10 chiffres significatifs
            if isinstance(value, (int, float)):
                value = f"{value:.7g}"
            st.markdown(
                f'<div style="background-color: {colors[kpi_keys[i]]}; padding: 20px; border-radius: 5px; text-align: center; height: 150px; display: flex; flex-direction: column; justify-content: center;">'
                f"<h4>{icons[kpi_keys[i]]} {kpis_readable[kpi_keys[i]]}</h4>"
                f"<h4>{value}</h4>"
                f"</div>",
                unsafe_allow_html=True,
            )

    st.markdown("---")
