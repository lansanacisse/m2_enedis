from pre_processing import *
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score
import pickle



def save_model(model, filename='RF_Classification_Etiquette.pkl'):
    """
    Sauvegarde le modèle au format pickle avec gestion des exceptions.

    Parameters:
    model: objet scikit-learn entraîné
    filename (str): chemin et nom du fichier pour sauvegarder le modèle
    """

    # Sauvegarde avec gestion d'exception
    try:
        with open(filename, 'wb') as file:
            pickle.dump(model, file)
        print(f"Modèle sauvegardé avec succès sous : {filename}")
    except Exception as e:
        print(f"Erreur lors de la sauvegarde du modèle : {e}")

def RF_classification_DPE(n_estimarors=100): # A remplir selon l'utilisateurs et ce qu'on veut faire
  df = import_data('data/merged_69.csv')
  df = preprocess_data(df)
  print(df.info()) # Voir le type des colonnes : ne devrait avoir que des float64 car Encoding des variables catégorielles

  target = "Etiquette_DPE"
  X = df.drop(columns=[target])
  y = df[target]


  X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42, stratify=y)
  RF_model = RandomForestClassifier(n_estimators=100, random_state=42)
  print("Entrainement du modèle...")
  RF_model.fit(X_train, y_train)
  y_pred = RF_model.predict(X_test)
  print("Résultats du modèle...")
  accuracy = accuracy_score(y_test, y_pred)
  print(f"Accuracy: {accuracy}")

  print("Meilleures features...")
  feature_importances = RF_model.feature_importances_
  indices = np.argsort(feature_importances)[::-1]
  top_n = 5  # Limite à 5
  top_features = X.columns[indices[:top_n]]
  top_importances = feature_importances[indices[:top_n]]
  for i, feature in enumerate(top_features):
    print(f"{i+1}. {feature}: {top_importances[i]}")

  print(f"Si on doit réduire la dimensions, il ne faudra garde que les {top_n} features ci-dessus")

  # Export du modèle
  print("Export du modèle...")
  save_model(RF_model, 'RF_Classification_Etiquette.pkl')
  return RF_model

print("Lancement de la classification...")
RF_model = RF_classification_DPE()