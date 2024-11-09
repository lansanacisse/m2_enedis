import unittest
import pandas as pd
import numpy as np
from sklearn.preprocessing import LabelEncoder
from main import import_data, percent_missing, encodage_variables_categorielles, gestion_valeurs_manquantes, gestion_outliers, preprocess_data

class TestDataProcessing(unittest.TestCase):

    def setUp(self):
        """Prépare un DataFrame de test pour chaque fonction."""
        self.df = pd.DataFrame({
            'col_categorical': ['A', 'B', 'C', 'A', np.nan],
            'col_numeric': [1, 2, 5, np.nan, 100],
            'col_mixed': ['text', 3, 'A', np.nan, 4]
        })

    def test_import_data(self):
        """Vérifie l'importation de données depuis un fichier existant."""
        df = import_data('data/test_data.csv')
        self.assertIsInstance(df, pd.DataFrame)
        self.assertFalse(df.empty)

    def test_percent_missing(self):
        """Vérifie que le calcul du pourcentage de valeurs manquantes est correct."""
        percent_nan = percent_missing(self.df)
        expected_nan = pd.Series([20.0, 20.0], index=['col_categorical', 'col_numeric'])
        pd.testing.assert_series_equal(percent_nan, expected_nan)

    def test_encodage_variables_categorielles(self):
        """Vérifie que les variables catégorielles sont correctement encodées en valeurs numériques."""
        df_encoded = encodage_variables_categorielles(self.df.copy())
        self.assertIsInstance(df_encoded['col_categorical'][0], np.integer)
        self.assertTrue(df_encoded['col_mixed'].isnull().all())  # Colonne mixte avec valeurs non encodables supprimée

    def test_gestion_valeurs_manquantes(self):
        """Vérifie que les valeurs manquantes sont remplacées par la médiane."""
        df_no_missing = gestion_valeurs_manquantes(self.df.copy())
        self.assertFalse(df_no_missing.isnull().values.any())  # Plus de valeurs manquantes

    def test_gestion_outliers(self):
        """Vérifie que les outliers sont remplacés par la médiane."""
        df_no_outliers = gestion_outliers(self.df.copy())
        self.assertLessEqual(df_no_outliers['col_numeric'].max(), 5)  # Valeur extrême de 100 remplacée par la médiane

    def test_preprocess_data(self):
        """Vérifie que l'ensemble des étapes de prétraitement est effectué correctement."""
        df_processed = preprocess_data(self.df.copy())
        self.assertFalse(df_processed.isnull().values.any())  # Plus de valeurs manquantes
        self.assertTrue(all(isinstance(df_processed[col][0], (int, float)) for col in df_processed.columns))
        self.assertNotIn('col_mixed', df_processed.columns)  # Colonne mixte supprimée

if __name__ == '__main__':
    unittest.main()
