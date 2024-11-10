# M2 Enedis
Cette application permet d’analyser et de prédire le Diagnostic de Performance Énergétique (DPE) et la consommation énergétique des logements situés à Lyon (69). 
Elle utilise des modèles d’apprentissage automatique pour estimer l’étiquette DPE et la consommation énergétique en fonction des caractéristiques du logement.

## Fonctionnalités

- **Accueil** : Présentation de l'application et de ses fonctionnalités.
- **Contexte** : Permet d'explorer les données du projet et d'obtenir de nouvelles données en faisant appel à l'API.
- **Analyse** : Permet de suivre les différents KPI et de visualiser les données à l'aide de divers graphiques ainsi qu'une carte de géolocalisation.
- **Prédiction Locale** : Permet de réaliser des prédictions spécifiques à un logement en fonction de ses caractéristiques locales, en fournissant une estimation personnalisée du Diagnostic de Performance Énergétique (DPE) et de la consommation énergétique.
- **Prédiction avec API** : Permet de réaliser des prédictions en utilisant l'API pour obtenir des estimations automatisées du Diagnostic de Performance Énergétique (DPE) et de la consommation énergétique à partir des caractéristiques des logements.

## Prérequis

- Python 3.7 ou supérieur
- `pip` pour installer les dépendances

## Installation

1. Clonez le dépôt :

    ```bash
    git clone https://github.com/lansanacisse/m2_enedis.git
    cd m2_enedis
    ```

2. Installez les dépendances :

    ```bash
    cd script
    pip install -r requirements.txt
    ```

## Utilisation

1. Assurez-vous que les fichiers .pkl suivants sont bien présents pour la prédiction locale :

- **etiquette_knn_model.pkl**
- **etiquette_arbre_de_decision_model.pkl**
- **etiquette_random_forest_model.pkl**
- **consommation_xgboost_model.pkl**
- **consommation_arbre_de_decision_model.pkl**
- **consommation_random_forest_model.pkl**

Si ces fichiers sont manquants, pensez à exécuter le notebook `Mynotebook.ipynb` pour les générer.


2. Lancez l'application Streamlit :

    ```bash
    cd script
    streamlit run MyApp.py
    ```

3. Ouvrez votre navigateur et accédez à l'URL suivante :

    ```
    http://localhost:8501
    ```

## Auteurs

- [Lansana CISSE](https://github.com/lansanacisse)
- [Quentin Lim](https://github.com/QL2111)
- [Linh Nhi LE DINH](https://github.com/Linn2d)


## Documentation

[Documentation](docs/html/index.html)


## Liens

Insert gif or link to demo
