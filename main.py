# main.py

# TODO :
# - Ajouter les imports nécessaires
# - Fonctions de l'API
# - Pour le moment ,ne pas utiliser ce fichier pour les tests, il est incomplet
#
#

from pre_processing import preprocess_data
from RF_Classification import run_classification
# from API import call_api() # à compléter

def main():
    # Étape 1 : Prétraitement des données
    print("Prétraitement des données...")
    preprocess_data()
    
    # Étape 2 : Exécution de la classification
    print("Exécution de la classification...")
    run_classification()
    
    # Étape 3 : Autres opérations (par exemple, des requêtes API si nécessaire)
    print("Appel d'API...")
    Api.some_api_function()  # Remplacez 'some_api_function' par la fonction réelle de votre fichier Api.py
    
    print("Processus terminé.")

if __name__ == "__main__":
    main()
