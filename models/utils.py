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
from sklearn.model_selection import train_test_split
import joblib


def create_pie_chart(labels, sizes):
    fig, ax = plt.subplots()
    ax.pie(sizes, labels=labels, autopct="%1.1f%%", startangle=90)
    ax.axis("equal")  # Assure que le graphique est un cercle
    return fig


def create_bar_chart(labels, sizes):
    fig, ax = plt.subplots()
    ax.bar(labels, sizes)
    return fig


def create_line_chart(labels, sizes):
    fig, ax = plt.subplots()
    ax.plot(
        labels, sizes, marker="o"
    )  # Ajout de marqueurs pour une meilleure lisibilité
    return fig


def create_histogram(sizes, labels):
    fig, ax = plt.subplots()
    ax.hist(sizes, bins=len(labels), edgecolor="black")
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
            "XGBoost": "consommation_xgboost_model.pkl",
            "Arbre de Décision": "consommation_arbre_de_decision_model.pkl",
            "Forêt Aléatoire": "consommation_random_forest_model.pkl",
        },
        "Etiquette_DPE": {
            "K-nearest neighbors": "etiquette_knn_model.pkl",
            "Arbre de Décision": "etiquette_arbre_de_decision_model.pkl",
            "Forêt Aléatoire": "etiquette_random_forest_model.pkl",
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


import pandas as pd

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
            "conso_chauffage",
            "conso_5_usages_finale",
            "emission_ges",
            "etiquette_GES",
            "cout_eclairage",
        ]

        X = pd.DataFrame(
            [
                [
                    encoded_data.get("conso_chauffage"),
                    encoded_data.get("conso_5_usages_finale"),
                    encoded_data.get("emission_ges"),
                    encoded_data.get("etiquette_GES"),
                    encoded_data.get("cout_eclairage"),
                ]
            ],
            columns=columns,
        )

        # Prédire l'étiquette DPE
        prediction = model.predict(X)[0]
        return prediction
