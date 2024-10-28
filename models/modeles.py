import pandas as pd
from sklearn.linear_model import LinearRegression
from sklearn.tree import DecisionTreeRegressor
from sklearn.ensemble import RandomForestRegressor
import joblib


# Fonction pour charger un modèle spécifique
def load_model(model_option):
    models = {
        "Régression Linéaire": "linear_regression_model.pkl",
        "Arbre de Décision": "decision_tree_model.pkl",
        "Forêt Aléatoire": "random_forest_model.pkl",
    }
    model_file = models[model_option]
    model = joblib.load(model_file)
    return model


# Entraîner et sauvegarder les modèles
def train_and_save_models():
    data = pd.read_csv("data.csv")
    X = data.drop(columns=["DPE", "consommation_energétique"])
    y_reg = data["consommation_energétique"]
    X_train, X_test, y_train, y_test = train_test_split(
        X, y_reg, test_size=0.2, random_state=42
    )

    lin_reg = LinearRegression()
    lin_reg.fit(X_train, y_train)
    joblib.dump(lin_reg, "linear_regression_model.pkl")

    dec_tree = DecisionTreeRegressor()
    dec_tree.fit(X_train, y_train)
    joblib.dump(dec_tree, "decision_tree_model.pkl")

    rand_forest = RandomForestRegressor(n_estimators=100)
    rand_forest.fit(X_train, y_train)
    joblib.dump(rand_forest, "random_forest_model.pkl")

    print("Modèles entraînés et sauvegardés avec succès.")


# Réentraîner un modèle spécifique avec de nouveaux paramètres
def retrain_model(model_option, params, data_path="data.csv"):
    data = pd.read_csv(data_path)
    X = data.drop(columns=["DPE", "consommation_energétique"])
    y = data["consommation_energétique"]
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42
    )

    if model_option == "Régression Linéaire":
        model = LinearRegression(**params)
    elif model_option == "Arbre de Décision":
        model = DecisionTreeRegressor(**params)
    elif model_option == "Forêt Aléatoire":
        model = RandomForestRegressor(**params)

    model.fit(X_train, y_train)
    joblib.dump(model, f'{model_option.replace(" ", "_").lower()}_model.pkl')
    return model


# Prédire la consommation énergétique en fonction des caractéristiques du logement


def predict(surface, nb_pieces, annee_construction, model_option, **kwargs):
    model = load_model(model_option)
    X_new = pd.DataFrame(
        [[surface, nb_pieces, annee_construction]],
        columns=["surface", "nb_pieces", "annee_construction"],
    )

    if model_option in ["Régression Linéaire", "Arbre de Décision", "Forêt Aléatoire"]:
        model.set_params(**kwargs)

    cons_pred = model.predict(X_new)[0]
    return cons_pred
