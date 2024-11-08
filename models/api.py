from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
import pandas as pd
import joblib
import logging

app = FastAPI()

# Configurer le logging pour voir les erreurs
logging.basicConfig(level=logging.INFO)

# Charger les modèles (assurez-vous que les fichiers sont dans un dossier `models`)
models = {
    "consumption_xgboost": joblib.load("xgboost.pkl"),
    "consumption_rdforest": joblib.load("rdforest.pkl"),
    "consumption_linearreg": joblib.load("linearReg.pkl"),
    "label_knn": joblib.load("etiquette_knn_model.pkl"),
    #"label_rf": joblib.load("models/etiquette_random_forest_model.pkl")
}

# Dictionnaire de mapping pour les étiquettes DPE
label_mapping = {0: "A", 1: "B", 2: "C", 3: "D", 4: "E", 5: "F", 6: "G"}

etiquette_ges_mapping = {
    "A": 0,
    "B": 1,
    "C": 2,
    "D": 3,
    "E": 4,
    "F": 5,
    "G": 6
}

# Classe pour les données de consommation énergétique
class ConsumptionInput(BaseModel):
    Type_batiment: str = Field(..., alias="Type_bâtiment")
    Qualite_isolation_enveloppe: str = Field(..., alias="Qualité_isolation_enveloppe")
    Etiquette_GES: str
    Surface_habitable_logement: float
    Etiquette_DPE: str
    Type_installation_chauffage: str
    Ubat_W_m2_K: float = Field(..., alias="Ubat_W/m²_K")
    Qualite_isolation_murs: str = Field(..., alias="Qualité_isolation_murs")
    Type_energie_n1: str = Field(..., alias="Type_énergie_n°1")
    Qualite_isolation_plancher_bas: str = Field(..., alias="Qualité_isolation_plancher_bas")
    Methode_application_DPE: str = Field(..., alias="Méthode_application_DPE")
    Qualite_isolation_menuiseries: str = Field(..., alias="Qualité_isolation_menuiseries")

class LabelInput(BaseModel):
    Conso_chauffage_e_primaire: float
    Conso_5_usages_e_finale: float
    Emission_GES_5_usages_par_m2: float
    Etiquette_GES: str  # Changement en str pour accepter des valeurs comme "A", "B", etc.
    Cout_eclairage: float


@app.post("/predict/label")
async def predict_label(input_data: LabelInput, model_type: str = "knn"):
    model_key = f"label_{model_type.lower()}"
    if model_key not in models:
        raise HTTPException(status_code=400, detail="Modèle de classification non disponible.")

    numeric_etiquette_ges = etiquette_ges_mapping.get(input_data.Etiquette_GES)
    if numeric_etiquette_ges is None:
        raise HTTPException(status_code=400, detail="Etiquette_GES invalide.")

    try:
        mapped_data = {
            "Conso_chauffage_é_primaire": input_data.Conso_chauffage_e_primaire,
            "Conso_5_usages_é_finale": input_data.Conso_5_usages_e_finale,
            "Emission_GES_5_usages_par_m²": input_data.Emission_GES_5_usages_par_m2,
            "Etiquette_GES": numeric_etiquette_ges,
            "Coût_éclairage": input_data.Cout_eclairage
        }
        X = pd.DataFrame([mapped_data])
        prediction = models[model_key].predict(X)[0]
        label = label_mapping.get(prediction, "Unknown")
        return {"label_prediction": label}
    except Exception as e:
        logging.error("Erreur dans /predict/label: %s", e)
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/predict/consumption")
async def predict_consumption(input_data: ConsumptionInput, model_type: str = "xgboost"):
    model_key = f"consumption_{model_type.lower()}"
    if model_key not in models:
        raise HTTPException(status_code=400, detail="Modèle de régression non disponible.")

    try:
        data = pd.DataFrame([input_data.dict(by_alias=True)])
        prediction = models[model_key].predict(data)[0]
        prediction = float(prediction)  # Assure compatibilité JSON
        return {"consumption_prediction": prediction}
    except Exception as e:
        logging.error("Erreur dans /predict/consumption: %s", e)
        raise HTTPException(status_code=500, detail=str(e))
