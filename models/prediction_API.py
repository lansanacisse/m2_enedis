import streamlit as st
import requests

def prediction_api_page():
    st.title("Prédiction avec API")

    # Choix du type de prédiction dans la barre latérale
    prediction_type = st.sidebar.radio(
        "Choisissez le type de prédiction :", ["Classification (DPE)", "Régression (Consommation Énergétique)"]
    )

    if prediction_type == "Classification (DPE)":
        model_option = st.sidebar.selectbox(
            "Sélectionnez le modèle pour l'étiquette DPE",
            ["KNN", "Random Forest"]
        )

        # Champs de saisie pour la prédiction de l'étiquette DPE
        conso_chauffage = st.number_input("Consommation de chauffage en énergie primaire")
        conso_5_usages = st.number_input("Consommation des 5 usages en énergie finale")
        emission_ges = st.number_input("Émission de GES pour les 5 usages par m²")
        
        etiquette_ges = st.selectbox("Étiquette GES", ["A", "B", "C", "D", "E", "F", "G"])
        cout_eclairage = st.number_input("Coût de l'éclairage")

        # Bouton pour effectuer la prédiction
        if st.button("Prédire l'étiquette DPE"):
            response = requests.post(
                "http://127.0.0.1:8001/predict/label",
                json={
                    "Conso_chauffage_e_primaire": conso_chauffage,
                    "Conso_5_usages_e_finale": conso_5_usages,
                    "Emission_GES_5_usages_par_m2": emission_ges,
                    "Etiquette_GES": etiquette_ges,
                    "Cout_eclairage": cout_eclairage
                },
                params={"model_type": model_option.lower()}
            )
            if response.status_code == 200:
                label_prediction = response.json().get("label_prediction")
                st.write(f"L'étiquette DPE prédite est : {label_prediction}")
            else:
                st.error("Erreur lors de la prédiction de l'étiquette DPE.")
                st.write("Détails de l'erreur :", response.text)

    elif prediction_type == "Régression (Consommation Énergétique)":
        model_option = st.sidebar.selectbox(
            "Sélectionnez le modèle pour la consommation énergétique",
            ["XGBoost", "Random Forest", "Régression Linéaire"]
        )

        # Champs de saisie pour la prédiction de la consommation énergétique
        type_batiment = st.selectbox("Type de bâtiment", ["appartement", "maison"])
        qualite_isolation_enveloppe = st.selectbox(
            "Qualité de l'isolation de l'enveloppe", ["bonne", "insuffisante", "moyenne", "très bonne"]
        )
        etiquette_ges = st.selectbox("Étiquette GES", ["A", "B", "C", "D", "E", "F", "G"])
        surface_habitable = st.number_input("Surface habitable (en m²)", min_value=0.0)
        etiquette_dpe = st.selectbox("Étiquette DPE", ["A", "B", "C", "D", "E", "F", "G"])
        type_installation_chauffage = st.selectbox(
            "Type d'installation de chauffage", ["collectif", "individuel", "mixte (collectif-individuel)"]
        )
        ubat_w_m2_k = st.number_input("Ubat (W/m².K)", min_value=0.0)
        qualite_isolation_murs = st.selectbox(
            "Qualité de l'isolation des murs", ["bonne", "insuffisante", "moyenne", "très bonne"]
        )
        type_energie_n1 = st.selectbox(
            "Type d'énergie n°1", [
                "Bois – Bûches", "Bois – Granulés (pellets) ou briquettes",
                "Bois – Plaquettes d’industrie", "Bois – Plaquettes forestières",
                "Charbon", "Fioul domestique", "GPL", "Gaz naturel", "Propane",
                "Réseau de Chauffage urbain", "Électricité",
                "Électricité d'origine renouvelable utilisée dans le bâtiment"
            ]
        )
        qualite_isolation_plancher_bas = st.selectbox(
            "Qualité de l'isolation du plancher bas", ["bonne", "insuffisante", "moyenne", "très bonne"]
        )
        methode_application_dpe = st.selectbox(
            "Méthode d'application du DPE", [
                "dpe appartement généré à partir des données DPE immeuble",
                "dpe appartement individuel", "dpe maison individuelle"
            ]
        )
        qualite_isolation_menuiseries = st.selectbox(
            "Qualité de l'isolation des menuiseries", ["bonne", "insuffisante", "moyenne", "très bonne"]
        )

        # Bouton pour effectuer la prédiction de consommation énergétique
        if st.button("Prédire la consommation énergétique"):

            model_type_map = {
                "XGBoost": "xgboost",
                "Random Forest": "rdforest",
                "Régression Linéaire": "linearreg" 
            }
            response = requests.post(
                "http://127.0.0.1:8001/predict/consumption",
                json={
                    "Type_bâtiment": type_batiment,
                    "Qualité_isolation_enveloppe": qualite_isolation_enveloppe,
                    "Etiquette_GES": etiquette_ges,
                    "Surface_habitable_logement": surface_habitable,
                    "Etiquette_DPE": etiquette_dpe,
                    "Type_installation_chauffage": type_installation_chauffage,
                    "Ubat_W/m²_K": ubat_w_m2_k,
                    "Qualité_isolation_murs": qualite_isolation_murs,
                    "Type_énergie_n°1": type_energie_n1,
                    "Qualité_isolation_plancher_bas": qualite_isolation_plancher_bas,
                    "Méthode_application_DPE": methode_application_dpe,
                    "Qualité_isolation_menuiseries": qualite_isolation_menuiseries
                },
                params={"model_type": model_type_map[model_option]}
            )
            if response.status_code == 200:
                consumption_prediction = response.json().get("consumption_prediction")
                st.write(f"La consommation énergétique prédite est : {consumption_prediction} kWh/m²/an")
            else:
                st.error("Erreur lors de la prédiction de la consommation énergétique.")
                st.write("Détails de l'erreur :", response.text)
