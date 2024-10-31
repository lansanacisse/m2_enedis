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


# Prediction function
def predict(type_prediction, model, **kwargs):
    """
    Fonction de prédiction unique pour l'étiquette DPE ou la consommation énergétique.
    type_prediction : str - "Étiquette DPE" ou "Consommation Énergétique"
    model : modèle de prédiction entraîné
    kwargs : caractéristiques du logement nécessaires pour la prédiction
    """
    if type_prediction == "Consommation Énergétique":
        # Mappage pour les valeurs textuelles
        chauffage_map = {"Central": 0, "Individuel": 1, "Collectif": 2}
        type_chauffage = chauffage_map.get(kwargs.get("type_chauffage"), 0)
        # Extraire les variables nécessaires pour la prédiction de la consommation
        X = pd.DataFrame(
            [
                [
                    kwargs.get("surface_habitable_logement"),
                    kwargs.get("ubat_w_m2_k"),
                    kwargs.get("etiquette_dpe"),
                    type_chauffage,
                ]
            ],
            columns=[
                "Surface_habitable_logement",
                "Ubat_W/m²_K",
                "Etiquette_DPE",
                "Type_énergie_principale_chauffage",
            ],
        )
        # Prédire la consommation énergétique
        prediction = model.predict(X)[0]
        return prediction
    elif type_prediction == "Étiquette DPE":
        # Mappage pour les valeurs textuelles
        etiquette_ges_map = {"A": 0, "B": 1, "C": 2, "D": 3, "E": 4, "F": 5, "G": 6}
        etiquette_ges = etiquette_ges_map.get(kwargs.get("etiquette_ges"), 0)
        # Extraire les variables nécessaires pour la prédiction de l'étiquette DPE
        X = pd.DataFrame(
            [
                [
                    kwargs.get("conso_chauffage"),
                    kwargs.get("conso_5_usages_finale"),
                    kwargs.get("emission_ges"),
                    etiquette_ges,
                    kwargs.get("cout_eclairage"),
                ]
            ],
            columns=[
                "Conso_chauffage_é_primaire",
                "Conso_5_usages_é_finale",
                "Emission_GES_5_usages_par_m²",
                "Etiquette_GES",
                "Coût_éclairage",
            ],
        )
        # Prédire l'étiquette DPE
        prediction = model.predict(X)[0]

        return prediction
