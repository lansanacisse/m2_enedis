import streamlit as st
from utils import retrain_model, load_model, predict, encode_input_data
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import plotly.express as px
from io import BytesIO
import streamlit as st
from scipy import stats as ss
from sklearn.neighbors import KNeighborsClassifier
from xgboost import XGBRegressor
from sklearn.tree import DecisionTreeRegressor
from sklearn.ensemble import RandomForestRegressor
from sklearn.impute import SimpleImputer
from sklearn.model_selection import train_test_split
import joblib

# Paramètres par défaut pour chaque modèle

default_params = {
    "XGBoost": {
        "objective": "reg:squarederror",  # Objective for regression
        "n_estimators": 100,
        "learning_rate": 0.1,
        "max_depth": 6,
        "subsample": 1.0,
        "colsample_bytree": 1.0,
    },
    "Arbre de Décision": {
        "criterion": "entropy",
        "max_depth": None,
        "min_samples_split": 2,
        "min_samples_leaf": 1,
    },
    "Forêt Aléatoire": {
        "n_estimators": 100,
        "criterion": "entropy",
        "max_depth": None,
        "min_samples_split": 2,
        "min_samples_leaf": 1,
        "bootstrap": True,
    },
    "K-nearest neighbors": {
        "n_neighbors": 5,
        "weights": "uniform",
        "algorithm": "auto",
        "leaf_size": 30,
    },
}


# Récupérer les paramètres du modèle à partir de la barre latérale
def get_model_params(model_option, default_params):
    params = {}
    if model_option == "XGBoost":
        params["objective"] = st.sidebar.selectbox(
            "Objectif",
            ["reg:squarederror", "reg:logistic"],
            index=["reg:squarederror", "reg:logistic"].index(
                default_params["XGBoost"]["objective"]
            ),
        )
        params["n_estimators"] = st.sidebar.number_input(
            "Nombre d'estimateurs",
            min_value=1,
            value=default_params["XGBoost"]["n_estimators"],
        )
        params["learning_rate"] = st.sidebar.number_input(
            "Taux d'apprentissage",
            min_value=0.01,
            max_value=1.0,
            value=default_params["XGBoost"]["learning_rate"],
        )
        params["max_depth"] = st.sidebar.number_input(
            "Profondeur maximale",
            min_value=1,
            value=default_params["XGBoost"]["max_depth"],
        )
        params["subsample"] = st.sidebar.number_input(
            "Échantillonage",
            min_value=0.1,
            max_value=1.0,
            value=default_params["XGBoost"]["subsample"],
        )
        params["colsample_bytree"] = st.sidebar.number_input(
            "Échantillonage par arbre",
            min_value=0.1,
            max_value=1.0,
            value=default_params["XGBoost"]["colsample_bytree"],
        )
    elif model_option == "Arbre de Décision":
        params["criterion"] = st.sidebar.selectbox(
            "Critère",
            ["squared_error", "absolute_error", "friedman_mse", "poisson"],
            index=["squared_error", "absolute_error", "friedman_mse", "poisson"].index(
                default_params["Arbre de Décision"]["criterion"]
            ),
        )
        params["max_depth"] = st.sidebar.number_input(
            "Profondeur maximale",
            min_value=1,
            value=default_params["Arbre de Décision"]["max_depth"],
        )
        params["min_samples_split"] = st.sidebar.number_input(
            "Échantillons minimum pour division",
            min_value=2,
            value=default_params["Arbre de Décision"]["min_samples_split"],
        )
        params["min_samples_leaf"] = st.sidebar.number_input(
            "Échantillons minimum pour feuille",
            min_value=1,
            value=default_params["Arbre de Décision"]["min_samples_leaf"],
        )
    elif model_option == "Forêt Aléatoire":
        params["n_estimators"] = st.sidebar.number_input(
            "Nombre d'arbres",
            min_value=1,
            value=default_params["Forêt Aléatoire"]["n_estimators"],
        )
        params["criterion"] = st.sidebar.selectbox(
            "Critère",
            ["entropy", "gini", "log_loss"],
            index=["entropy", "gini", "log_loss"].index(
                default_params["Forêt Aléatoire"]["criterion"]
            ),
        )
        params["max_depth"] = st.sidebar.number_input(
            "Profondeur maximale",
            min_value=1,
            value=default_params["Forêt Aléatoire"]["max_depth"],
        )
        params["min_samples_split"] = st.sidebar.number_input(
            "Échantillons minimum pour division",
            min_value=2,
            value=default_params["Forêt Aléatoire"]["min_samples_split"],
        )
        params["min_samples_leaf"] = st.sidebar.number_input(
            "Échantillons minimum pour feuille",
            min_value=1,
            value=default_params["Forêt Aléatoire"]["min_samples_leaf"],
        )
        params["bootstrap"] = st.sidebar.checkbox(
            "Utiliser le bootstrap",
            value=default_params["Forêt Aléatoire"]["bootstrap"],
        )
    elif model_option == "K-nearest neighbors":
        params["n_neighbors"] = st.sidebar.number_input(
            "Nombre de voisins",
            min_value=1,
            value=default_params["K-nearest neighbors"]["n_neighbors"],
        )
        params["weights"] = st.sidebar.selectbox(
            "Poids",
            ["uniform", "distance"],
            index=["uniform", "distance"].index(
                default_params["K-nearest neighbors"]["weights"]
            ),
        )
        params["algorithm"] = st.sidebar.selectbox(
            "Algorithme",
            ["auto", "ball_tree", "kd_tree", "brute"],
            index=["auto", "ball_tree", "kd_tree", "brute"].index(
                default_params["K-nearest neighbors"]["algorithm"]
            ),
        )
        params["leaf_size"] = st.sidebar.number_input(
            "Taille des feuilles",
            min_value=1,
            value=default_params["K-nearest neighbors"]["leaf_size"],
        )
    return params


# Prédire la consommation énergétique ou l'étiquette DPE en fonction des caractéristiques du logement
def prediction_page():
    # Choix du type de prédiction dans la barre latérale
    prediction_type = st.sidebar.radio(
        "Que souhaitez-vous prédire ?", ["Étiquette DPE", "Consommation Énergétique"]
    )
    st.title(f"Prédiction {prediction_type}")

    # Choix du modèle de prédiction dans la barre latérale en fonction du type de prédiction
    if prediction_type == "Étiquette DPE":
        model_option = st.sidebar.selectbox(
            "Choisissez un modèle de prédiction",
            ["Forêt Aléatoire", "Arbre de Décision", "K-nearest neighbors",],
        )
        target_variable = "Etiquette_DPE"
    elif prediction_type == "Consommation Énergétique":
        model_option = st.sidebar.selectbox(
            "Choisissez un modèle de prédiction",
            ["XGBoost", "Forêt Aléatoire", "Arbre de Décision"],
        )
        target_variable = "Conso_5_usages_é_finale"

    # Récupération des paramètres du modèle
    params = get_model_params(model_option, default_params)

    # Option de réentraînement du modèle dans la barre latérale
    if st.sidebar.button("Réentraîner le modèle", key="retrain_button"):
        model = retrain_model(model_option, params, prediction_type)
        st.sidebar.success(f"Modèle {model_option} réentraîné avec succès.")
    else:
        model = load_model(model_option, target_variable)

    # Afficher les champs d'entrée selon le type de prédiction choisi
    st.header("Entrez les caractéristiques du logement")

    if prediction_type == "Consommation Énergétique":
        # Champs de sélection pour les variables à encoder
        type_batiment = st.selectbox(
            "Type de bâtiment", ["Maison", "Appartement", "Immeuble"]
        )
        qualite_isolation_enveloppe = st.selectbox(
            "Qualité de l'isolation de l'enveloppe",
            ["insuffisante", "moyenne", "bonne", "très bonne"],
        )
        etiquette_GES = st.selectbox(
            "Étiquette GES", ["A", "B", "C", "D", "E", "F", "G"]
        )
        surface_habitable_logement = st.number_input(
            "Surface habitable du logement (m²)", min_value=0.0
        )
        etiquette_DPE = st.selectbox(
            "Étiquette DPE", ["A", "B", "C", "D", "E", "F", "G"]
        )
        type_installation_chauffage = st.selectbox(
            "Type d'installation de chauffage",
            ["individuel", "collectif", "mixte (collectif-individuel)"],
        )
        Ubat_W_m2_K = st.number_input("Ubat (W/m².K)", min_value=0.0)
        qualite_isolation_murs = st.selectbox(
            "Qualité de l'isolation des murs",
            ["insuffisante", "moyenne", "bonne", "très bonne"],
        )
        type_energie_n1 = st.selectbox(
            "Type d'énergie n°1",
            [
                "Gaz naturel",
                "Électricité",
                "Réseau de Chauffage urbain",
                "Bois – Granulés (pellets) ou briquettes",
                "Fioul domestique",
            ],
        )
        qualite_isolation_plancher_bas = st.selectbox(
            "Qualité de l'isolation du plancher bas",
            ["insuffisante", "moyenne", "bonne", "très bonne"],
        )
        methode_application_DPE = st.selectbox(
            "Méthode d'application du DPE",
            [
                "dpe appartement individuel",
                "dpe appartement généré à partir des données DPE immeuble",
                "dpe maison individuelle",
                "dpe issu d'une étude thermique réglementaire RT2012 bâtiment : appartement",
                "dpe issu d'une étude thermique réglementaire RT2012 bâtiment : maison individuelle",
                "dpe immeuble collectif",
            ],
        )
        qualite_isolation_menuiseries = st.selectbox(
            "Qualité de l'isolation des menuiseries",
            ["insuffisante", "moyenne", "bonne", "très bonne"],
        )
        # Bouton pour lancer la prédiction de la consommation énergétique
        if st.button("Prédire la consommation énergétique", key="predict_button_conso"):
            # Organisation des données d'entrée
            input_data = {
                "Type_bâtiment": type_batiment,
                "Qualité_isolation_enveloppe": qualite_isolation_enveloppe,
                "Etiquette_GES": etiquette_GES,
                "Surface_habitable_logement": surface_habitable_logement,
                "Etiquette_DPE": etiquette_DPE,
                "Type_installation_chauffage": type_installation_chauffage,
                "Ubat_W/m²_K": Ubat_W_m2_K,
                "Qualité_isolation_murs": qualite_isolation_murs,
                "Type_énergie_n°1": type_energie_n1,
                "Qualité_isolation_plancher_bas": qualite_isolation_plancher_bas,
                "Méthode_application_DPE": methode_application_DPE,
                "Qualité_isolation_menuiseries": qualite_isolation_menuiseries,
            }

            # Vérifier si toutes les données nécessaires sont bien renseignées
            if any(value is None or value == 0.0 for value in input_data.values()):
                st.warning("Certaines valeurs ne sont pas renseignées correctement.")
            else:
                # Appel de la fonction de prédiction avec les données non encodées
                conso_energetique = predict(
                    type_prediction="Consommation Énergétique",
                    model=model,
                    **input_data,
                )
                st.write(
                    f"D'après les caractéristiques du logement, la consommation énergétique prédite est de {conso_energetique:.2f} kWh/m²/an"
                )

    elif prediction_type == "Étiquette DPE":
        # Champs d'entrée pour l'étiquette DPE
        conso_5_usages_par_m2_e_primaire = st.number_input(
            "Consommation 5 usages par m² en énergie primaire",
            key="conso_5_usages_par_m2_e_primaire",
        )
        conso_5_usages_m2_e_finale = st.number_input(
            "Consommation 5 usages par m² en énergie finale",
            key="conso_5_usages_m2_e_finale",
        )
        emission_GES = st.number_input(
            "Émission GES pour 5 usages par m²", key="emission_GES"
        )
        etiquette_GES = st.selectbox(
            "Étiquette GES", ["A", "B", "C", "D", "E", "F", "G"], key="etiquette_GES"
        )
        cout_eclairage = st.number_input("Coût éclairage", key="cout_eclairage")

        if st.button("Prédire l'étiquette DPE", key="predict_button_dpe"):
            # Vérifier si tous les champs sont renseignés
            if (
                not conso_5_usages_par_m2_e_primaire
                or not conso_5_usages_m2_e_finale
                or not emission_GES
                or not etiquette_GES
                or not cout_eclairage
            ):
                st.warning(
                    "Veuillez saisir toutes les caractéristiques du logement avant de lancer la prédiction."
                )
            else:
                etiq_dpe = predict(
                    type_prediction="Étiquette DPE",
                    model=model,
                    conso_5_usages_par_m2_e_primaire=conso_5_usages_par_m2_e_primaire,
                    conso_5_usages_m2_e_finale=conso_5_usages_m2_e_finale,
                    emission_ges=emission_GES,
                    etiquette_GES=etiquette_GES,
                    cout_eclairage=cout_eclairage,
                    **params,
                )
                etiquette_dpe_map = {
                    0: "A",
                    1: "B",
                    2: "C",
                    3: "D",
                    4: "E",
                    5: "F",
                    6: "G",
                }
                etiq_dpe = etiquette_dpe_map.get(etiq_dpe)
                st.write(
                    f"D'après les caractéristiques du logement, l'étiquette DPE prédite est: {etiq_dpe}"
                )
