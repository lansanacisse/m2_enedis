import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.preprocessing import StandardScaler, LabelEncoder
from sklearn.impute import SimpleImputer


# import data
def import_data(chemin):
  # Import data
  try:
    data = pd.read_csv(chemin, sep=';')
    print("Import réussi")
  except FileNotFoundError:
    print("Fichier introuvable")
  except Exception as e:
    print("Echec dans la lecture du fichier")
    print(e)
  return data

# Remove missing values
def percent_missing(df):
  percent_nan = 100 * df.isnull().sum() / len(df)
  percent_nan = percent_nan[percent_nan > 0].sort_values()

  return percent_nan



# Encoding categorical variables
def encodage_variables_categorielles(df):
  print("Encodage des variables catégorielles...")

  encoders = {}

  for column in df.select_dtypes(include=['object']).columns:
    # Check if the column has mixed types
    if df[column].apply(type).nunique() > 1:
      # If mixed types, convert all values to strings
      df[column] = df[column].astype(str)
    encoders[column] = LabelEncoder()
    encoders[column].fit(df[column])
    # Use try-except block to handle unseen values during transform
    try:
      df[column] = encoders[column].transform(df[column])
    except ValueError as e:
      # Print the error message and the problematic column
      print(f"Error encoding column '{column}': {e}")
      print(f"Dropping column '{column}' due to unseen values.")
      df = df.drop(columns=[column])
  return df

# Gestion des valeurs manquantes
def gestion_valeurs_manquantes(df):
  print("Gestion des valeurs manquantes...")
  # Remplissage des valeurs manquantes avec la médiane
  imputer = SimpleImputer(strategy='median')
  df = pd.DataFrame(imputer.fit_transform(df), columns=df.columns)
  return df

# Gestion outliers
def gestion_outliers(df):
  print("Gestion des outliers...")
  numerical_columns = df.select_dtypes(include=['float64', 'int64']).columns
  for col in numerical_columns:
    Q1 = np.percentile(df[col], 25, method='midpoint')
    Q3 = np.percentile(df[col], 75, method='midpoint')
    IQR = Q3 - Q1
    lower = Q1 - 1.5*IQR
    upper = Q3 + 1.5*IQR
    # replace outliers by the median
    df[col] = np.where(df[col] < lower, np.median(df[col]), df[col])
    df[col] = np.where(df[col] > upper, np.median(df[col]), df[col])

  return df

def gestion_standardisation(df):
  print("Standardisation des données...")
  # print(df.shape)
  scaler = StandardScaler()
  df = pd.DataFrame(scaler.fit_transform(df), columns=df.columns)
  return df




# Preprocessing
def preprocess_data(df):
  # Import data
  # Remove duplicates
  df = df.drop_duplicates()
  # Remove missing values
  print("Removing missing values...")
  percent_nan = percent_missing(df)
  # print(percent_nan)
  #suppression des colonnes qui ont + de > 30% valeurs manquantes
  df = df.drop(percent_nan[percent_nan > 30].index, axis=1)
  # Encoding categorical variables
  df = encodage_variables_categorielles(df)
  # Gestion des valeurs manquantes
  df = gestion_valeurs_manquantes(df)
  # Gestion des outliers
  df = gestion_outliers(df)
  # Normalisation des données
  # df = gestion_standardisation(df) # La normalisation n'est pas nécessaire pour les arbres de décision et fait crash le code
  # Export data
  print("Export des données...")
  df.to_csv('data/preprocessed_data.csv', index=False)
  print("Export réussi")
  return df

# Test Values 
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score

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