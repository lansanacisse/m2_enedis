import streamlit as st
from modeles import retrain_model, load_model

# Paramètres par défaut pour chaque modèle
default_params = {
    "Régression Linéaire": {"fit_intercept": True, "normalize": False},
    "Arbre de Décision": {
        "criterion": "gini",
        "max_depth": None,
        "min_samples_split": 2,
        "min_samples_leaf": 1,
    },
    "Forêt Aléatoire": {
        "n_estimators": 100,
        "criterion": "gini",
        "max_depth": None,
        "min_samples_split": 2,
        "min_samples_leaf": 1,
        "bootstrap": True,
    },
}


# Récupérer les paramètres du modèle à partir de la barre latérale
def get_model_params(model_option, default_params):
    params = {}
    if model_option == "Régression Linéaire":
        params["fit_intercept"] = st.sidebar.checkbox(
            "Ajouter une interception",
            value=default_params["Régression Linéaire"]["fit_intercept"],
        )
        params["normalize"] = st.sidebar.checkbox(
            "Normaliser les données",
            value=default_params["Régression Linéaire"]["normalize"],
        )
    elif model_option == "Arbre de Décision":
        params["criterion"] = st.sidebar.selectbox(
            "Critère",
            ["gini", "entropy"],
            index=["gini", "entropy"].index(
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
            ["gini", "entropy"],
            index=["gini", "entropy"].index(
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
    return params


# Prédire la consommation énergétique en fonction des caractéristiques du logement
def prediction_page():
    st.title("Prédiction DPE et Consommation Énergétique")

    model_option = st.sidebar.selectbox(
        "Choisissez un modèle de prédiction",
        ["Régression Linéaire", "Arbre de Décision", "Forêt Aléatoire"],
    )

    params = get_model_params(model_option, default_params)

    # Entraîner le modèle à nouveau avec les nouveaux paramètres si l'utilisateur le souhaite dans la barre latérale
    if st.sidebar.button("Réentraîner le modèle", key="retrain_button"):
        model = retrain_model(model_option, params)
        st.sidebar.success(f"Modèle {model_option} réentraîné avec succès.")
    else:
        model = load_model(model_option)

    # Saisie des caractéristiques du logement pour la prédiction
    st.header("Entrez les caractéristiques du logement")
    surface = st.number_input("Surface (m²)", key="surface")
    nb_pieces = st.number_input("Nombre de pièces", key="nb_pieces")
    annee_construction = st.number_input(
        "Année de construction", key="annee_construction"
    )

    if st.button("Prédire", key="predict_button"):
        cons_pred = predict(
            surface, nb_pieces, annee_construction, model_option, **params
        )
        st.write(f"Consommation Énergétique prédite: {cons_pred} kWh/m²/an")
