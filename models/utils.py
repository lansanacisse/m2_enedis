# Importation des bibliothèques nécessaires
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import plotly.express as px
from io import BytesIO
import streamlit as st
from scipy import stats as ss
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
def load_model(model_option):
    models = {
        "Régression Linéaire": "linear_regression_model.pkl",
        "Arbre de Décision": "arbre_de_décision_model.pkl",
        "Forêt Aléatoire": "random_forest_model.pkl",
    }
    model_file = models[model_option]
    model = joblib.load(model_file)
    return model


# Entraîner et sauvegarder les modèles
def train_and_save_models(data_path="../data/preprocessed_data.csv"):
    data = pd.read_csv(data_path)
    X = data.drop(columns=["Etiquette_DPE", "Conso_5_usages_é_finale"])
    y_reg = data["Conso_5_usages_é_finales"]
    X_train, X_test, y_train, y_test = train_test_split(
        X, y_reg, test_size=0.2, random_state=42
    )

    lin_reg = LinearRegression()
    lin_reg.fit(X_train, y_train)
    joblib.dump(lin_reg, "linear_regression_model.pkl")

    dec_tree = DecisionTreeRegressor()
    dec_tree.fit(X_train, y_train)
    joblib.dump(dec_tree, "arbre_de_décision_model.pkl")

    rand_forest = RandomForestRegressor(n_estimators=100)
    rand_forest.fit(X_train, y_train)
    joblib.dump(rand_forest, "random_forest_model.pkl")

    print("Modèles entraînés et sauvegardés avec succès.")


# Fonction pour réentraîner le modèle avec les nouveaux paramètres
def retrain_model(model_option, params, data_path="../data/preprocessed_data.csv"):

    # Charger les données
    data = pd.read_csv(data_path)

    X = data[
        [
            "Conso_5_usages_par_m²_é_primaire",
            "Emission_GES_5_usages_par_m²",
            "Coût_éclairage",
        ]
    ]
    y = data["Conso_5_usages_é_finale"]
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42
    )

    # Sélection du modèle
    if model_option == "Régression Linéaire":
        model = LinearRegression(**params)
    elif model_option == "Arbre de Décision":
        model = DecisionTreeRegressor(**params)
    elif model_option == "Forêt Aléatoire":
        model = RandomForestRegressor(**params)

    # Entraîner le modèle
    model.fit(X_train, y_train)

    # Sauvegarder le modèle
    joblib.dump(model, f'{model_option.replace(" ", "_").lower()}_model.pkl')

    return model


# Prédire la consommation énergétique en fonction des caractéristiques du logement


def predict(
    conso_primaire,
    emission_GES,
    cout_eclairage,
    model_option,
    **kwargs,
):
    # Charger le modèle spécifié
    model = load_model(model_option)

    # Création du DataFrame pour les nouvelles données
    X_new = pd.DataFrame(
        [[conso_primaire, emission_GES, cout_eclairage]],
        columns=[
            "Conso_5_usages_par_m²_é_primaire",
            "Emission_GES_5_usages_par_m²",
            "Coût_éclairage",
        ],
    )

    # Vérification du type de modèle pour ajuster les paramètres si nécessaire
    if model_option in ["Régression Linéaire", "Arbre de Décision", "Forêt Aléatoire"]:
        model.set_params(**kwargs)

    # Prédiction et retour du résultat
    cons_pred = model.predict(X_new)[0]
    return cons_pred
