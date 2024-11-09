import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.preprocessing import StandardScaler, LabelEncoder
from sklearn.impute import SimpleImputer

# Import data
# @brief Importe les données à partir d'un fichier CSV
# @param chemin Chemin vers le fichier CSV
# @return pandas.DataFrame des données importées ou None si l'import échoue
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
## @brief Calcule le pourcentage de valeurs manquantes pour chaque colonne du DataFrame
# @param df pandas.DataFrame pour lequel on calcule les valeurs manquantes
# @return pandas.Series contenant les pourcentages de valeurs manquantes pour chaque colonne
def percent_missing(df):
  percent_nan = 100 * df.isnull().sum() / len(df)
  percent_nan = percent_nan[percent_nan > 0].sort_values()

  return percent_nan

# Encoding categorical variables
## @brief Encode les variables catégorielles en valeurs numériques
# @param df pandas.DataFrame contenant les variables catégorielles à encoder
# @return pandas.DataFrame avec les variables catégorielles encodées
def encodage_variables_categorielles(df):
  print("Encodage des variables catégorielles...")

  encoders = {}

  for column in df.select_dtypes(include=['object']).columns:
    # On regarde les types des colonnes et on s'assure qu'il n'y a pas de types mixtes
    if df[column].apply(type).nunique() > 1:
      # Si c'est le cas, on converti en string
      df[column] = df[column].astype(str)
    encoders[column] = LabelEncoder()
    encoders[column].fit(df[column])
    # On remplace les valeurs par les valeurs encodées
    try:
      df[column] = encoders[column].transform(df[column])
    except ValueError as e:
      # Print the error message and the problematic column
      print(f"Error encoding column '{column}': {e}")
      print(f"Dropping column '{column}' due to unseen values.")
      df = df.drop(columns=[column])
  return df

# Gestion des valeurs manquantes
## @brief Gère les valeurs manquantes en remplissant avec la médiane de chaque colonne
# @param df pandas.DataFrame contenant des valeurs manquantes
# @return pandas.DataFrame avec valeurs manquantes gérées
def gestion_valeurs_manquantes(df):
    print("Gestion des valeurs manquantes...")
    # Remplissage des valeurs manquantes avec la médiane pour les colonnes numériques
    numeric_columns = df.select_dtypes(include=['float64', 'int64']).columns
    if len(numeric_columns) > 0:  # Vérifie qu'il y a des colonnes numériques
      numeric_imputer = SimpleImputer(strategy='median')
      df[numeric_columns] = numeric_imputer.fit_transform(df[numeric_columns])

    # Remplissage des valeurs manquantes avec la valeur la plus fréquente pour les colonnes catégorielles
    categorical_columns = df.select_dtypes(include=['object']).columns
    if len(categorical_columns) > 0:  # Vérifie qu'il y a des colonnes catégorielles
      categorical_imputer = SimpleImputer(strategy='most_frequent')
      df[categorical_columns] = categorical_imputer.fit_transform(df[categorical_columns])

    return df


# Gestion outliers
## @brief Gère les valeurs aberrantes (outliers) pour les colonnes numériques
# @param df pandas.DataFrame contenant les données à traiter
# @return pandas.DataFrame avec outliers remplacés par la médiane
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

## @brief Standardise les données en utilisant StandardScaler
# @param df pandas.DataFrame contenant les données à standardiser
# @return pandas.DataFrame standardisé
def gestion_standardisation(df):
  print("Standardisation des données...")
  # print(df.shape)
  scaler = StandardScaler()
  df = pd.DataFrame(scaler.fit_transform(df), columns=df.columns)
  return df



# Preprocessing
## @brief Prépocesse le DataFrame en nettoyant et transformant les données
# 
# Effectue les étapes suivantes : suppression des doublons, des colonnes ayant >30% de valeurs manquantes,
# encodage des variables catégorielles, gestion des valeurs manquantes et des outliers.
#
# @param df pandas.DataFrame à prétraiter
# @return pandas.DataFrame après prétraitement
# @details
# Les étapes incluent :
# - Suppression des doublons
# - Suppression des colonnes avec >30% de valeurs manquantes
# - Encodage des variables catégorielles
# - Gestion des valeurs manquantes (par la médiane)
# - Gestion des outliers (remplacés par la médiane)
# 
# @note
# La normalisation est commentée car elle n'est pas nécessaire pour les arbres de décision.
# 
# @remark
# Les données prétraitées sont exportées dans un fichier CSV "preprocessed_data.csv"
def preprocess_data(df, sauvegarde=False):
  print("Prétraitement des données...")
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
  # Gestion des outliers
  df = gestion_outliers(df)
  # Gestion des valeurs manquantes
  df = gestion_valeurs_manquantes(df)
  # Normalisation des données
  # df = gestion_standardisation(df) # La normalisation n'est pas nécessaire pour les arbres de décision et fait crash le code
  # Export data
  if sauvegarde:
    print("Export des données...")
    df.to_csv('../data/preprocessed_data.csv', index=False)
    print("Export réussi sous le nom de 'preprocessed_data.csv'")
  return df

