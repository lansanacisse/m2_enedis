# TODO Quels données veut-on récupérer de l'API ?
# Exporter les models en API
# Pouvoir mettre à jour les models avec de nouvelles données
# Enrichir l’apprentissage du modèle avec des données d’OpenData (ex : température) fonctionnalités bonus
# L’utilisateur peut rafraichir les données actuelles avec les nouvelles via l’API et la date de réception du DPE
# L’utilisateur peut réentrainer le modèle à partir de nouvelle données
# Les modèles sont accessibles via une API (Application Programming Interface





# len(liste_departement) # 91
# liste_departement

# Filtre supplémentaire ?
import pandas as pd

import requests
import json

######## CALL API #########

# Effectue une requête API pour récupérer des données basées sur les codes postaux du département du Rhône (69) et les exporte dans un fichier CSV.
# @param url: L'URL de base de l'API à appeler.
# @type url: str
# @return: Un DataFrame contenant les résultats complets des requêtes pour tous les codes postaux du département du Rhône.
# @rtype: pandas.DataFrame
# Le processus inclut :
# - Lecture des codes postaux à partir d'un fichier CSV.
# - Pour chaque code postal, effectuer une requête GET à l'API.
# - Si le nombre de résultats dépasse 10 000, gérer la pagination en utilisant le paramètre 'next'.
# - Agrégation des résultats dans un DataFrame.
# - Exportation des résultats dans un fichier CSV basé sur l'URL de base fournie.
# @note Le fichier CSV source des codes postaux doit être situé à "../data/adresses-69.csv".
# @note Les fichiers CSV de sortie sont nommés "existant_69.csv" ou "neufs_69.csv" selon l'URL de base.

# Lien de l'API pour récupérer les données de l'Ademe
existants = "https://data.ademe.fr/data-fair/api/v1/datasets/dpe-v2-logements-existants/lines"
neuf = "https://data.ademe.fr/data-fair/api/v1/datasets/dpe-v2-logements-neufs/lines"
# URL de base de l'API
def call_API(url):

  base_url = url

  nb_ligne = 0  # nombre de ligne total ce départements (aggrégation de toutes les communes)
  all_results = []  # dataframe complet de tout les codes postals pour ce département
  ######## Récupération de tous les codes postaux du département du Rhône(69)
  df_rhone = pd.read_csv("../data/adresses-69.csv", sep =";")
  df_rhone.columns
  liste_code_postal_rhone = df_rhone["code_postal"].unique()
  liste_code_postal_rhone= sorted(liste_code_postal_rhone.tolist())
  # Pour chaque code postal dans liste_code_postal_rhone
  for code_postal in liste_code_postal_rhone:
      # Paramètres de la requête (on va récupérer selon chaque code postal)
      params = {
          "page": 1,
          "size": 10_000,
          "q": code_postal,
          "q_fields": "Code_postal_(BAN)",
      }

      # Effectuer la requête GET avec les paramètres
      response = requests.get(base_url, params=params)

      # Vérifier le statut de la réponse
      print(f"Statut de la réponse : {response.status_code}")

      # Si la requête a été effectuée avec succès, traiter le contenu
      if response.status_code == 200:
          # Charger le contenu de la réponse en JSON
          content = response.json()

          # Afficher le nombre total de lignes dans la base de données
          print(f"Nombre de lignes pour ce code postal {code_postal} de la requête : {content['total']}")

          df = content['results']
          all_results.extend(df)  # On ajoute les données à notre df_total

          # Si le nombre de lignes dépasse 10 000, ajouter un filtre supplémentaire
          if content['total'] > 10_000:
              # Utiliser le mot clef after
              content = requests.get(content['next']).json()

              print(f"Nombre de lignes après ajout du filtre pour ce code postal {code_postal} : {content['total']}")
              df = content['results']
              all_results.extend(df)  # On ajoute les données à notre df_total

              # On vérifie si il n'y a pas à nouveau un next
              present_next = True
              while present_next:
                  try:
                      content = requests.get(content['next']).json()
                      print(f"Nombre de lignes après ajout du filtre pour ce code postal {code_postal} : {content['total']}")
                      df = content['results']
                      all_results.extend(df)  # On ajoute les données à notre df_total
                  except KeyError:
                      present_next = False
                  

          # On incrémente pour avoir le nombre de ligne total
          nb_ligne += content['total']

          # Afficher les données récupérées
          

          # Afficher les dimensions du DataFrame (nombre de lignes et de colonnes)
          print(f"Dimensions des données récupérées : {len(df)}, {len(df[0]) if df else 0}")

      else:
          print("Erreur lors de la requête")

  print(f"Nombre total de lignes de la requête : {nb_ligne}")

  # Construire un DataFrame complet des logements existants sur le département
  df_complet = pd.DataFrame(all_results)

  # Afficher les dimensions du DataFrame complet
  print(f"Dimensions du DataFrame complet : {df_complet.shape}")

  # Exporter le résultat dans un fichier CSV
  if(base_url == "https://data.ademe.fr/data-fair/api/v1/datasets/dpe-v2-logements-existants/lines"):
    df_complet.to_csv("existant_69.csv", index=False)
  if(base_url == "https://data.ademe.fr/data-fair/api/v1/datasets/dpe-v2-logements-neufs/lines"):
    df_complet.to_csv("neufs_69.csv", index=False)
  return df_complet




print(call_API(neuf))

# try:
#   df_existants = pd.read_csv("existant_69.csv")
#   df_neufs = pd.read_csv("neufs_69.csv")
#   print("Lecture des fichiers Ok")
# except:
#   print("Le fichier est introuvable")

# # Fusionner les deux dataframes avec uniquement les colonnes communes

# common_columns = set(df_existants.columns).intersection(set(df_neufs.columns))
# print(common_columns)
# print(len(common_columns)) # 131 colonnes en commun
# common_columns = list(common_columns)
# # Fusion des deux dataframes avec uniquement les colonnes communes
# df_merged = pd.concat([df_existants[common_columns], df_neufs[common_columns]], ignore_index=True)
# print(df_merged.shape)
# # Export to csv with the header
# df_merged.to_csv("merged_69.csv", index=False, sep=';', encoding='utf-8-sig')
# # test lecture
# df_merged = pd.read_csv("merged_69.csv", sep=';')
# print(df_merged.shape)
