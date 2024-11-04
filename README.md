
# M2 Enedis
Cette application permet d'analyser et de prédire le Diagnostic de Performance Énergétique (DPE) des logements en France. Elle utilise des modèles d'apprentissage automatique pour estimer l'étiquette DPE et la consommation énergétique en fonction des caractéristiques du logement.

## Fonctionnalités

- **Accueil** : Présentation de l'application et de ses fonctionnalités.
- **Données** : Affichage et visualisation des données de performance énergétique.
- **Analyse** : Analyse des données pour identifier les tendances et les anomalies.
- **Prédiction** : Prédiction du DPE et de la consommation énergétique à l'aide de modèles d'apprentissage automatique.

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
    pip install -r requirements.txt
    ```

## Utilisation

1. Lancez l'application Streamlit :

    ```bash
    streamlit run models/MyApp.py
    ```

2. Ouvrez votre navigateur et accédez à l'URL suivante :

    ```
    http://localhost:8501
    ```

## Structure du Projet

- `models/accueil.py` : Code pour la page d'accueil.
- `models/donnees.py` : Code pour la page de données.
- `models/analyse.py` : Code pour la page d'analyse.
- `models/prediction.py` : Code pour la page de prédiction.
- `models/MyApp.py` : Fichier principal pour lancer l'application.
- `data/` : Répertoire contenant les données de performance énergétique.
- `utils/` : Répertoire contenant les fonctions utilitaires.




## Auteurs

- [Lansana CISSE](https://github.com/lansanacisse)
- [Quentin Lim](https://github.com/QL2111)
- [Linh Nhi](https://github.com/Linn2d)


## Documentation

[Documentation](https://linktodocumentation)


## Liens

Insert gif or link to demo

