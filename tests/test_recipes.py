import unittest
import pandas as pd
from modules.recipe_engine import (
    get_text, load_recipes, save_recipe, update_recipe, delete_recipe, format_currency
)

class TestRecipeEngine(unittest.TestCase):
    def setUp(self):
        self.sample_recipe = {
            'name': 'Test Recipe',
            'description': 'A test recipe',
            'servings': 4,
            'prep_time': 10,
            'cook_time': 20,
            'category': 'Test',
            'instructions': 'Mix and cook.',
            'ingredients': [
                {'product_name': 'Flour', 'quantity': 2, 'unit': 'lb'},
                {'product_name': 'Water', 'quantity': 1, 'unit': 'gallon'}
            ]
        }

    def test_get_text(self):
        self.assertEqual(get_text('page_title', 'en'), '👨‍🍳 Recipe Builder')
        self.assertEqual(get_text('page_title', 'es'), '👨‍🍳 Constructor de Recetas')

    def test_format_currency(self):
        self.assertEqual(format_currency(123.45), '$123.45')
        self.assertEqual(format_currency(0), '$0.00')

    def test_save_and_load_recipe(self):
        save_recipe(self.sample_recipe)
        recipes = load_recipes()
        self.assertIn('Test Recipe', recipes)

    def test_update_recipe(self):
        save_recipe(self.sample_recipe)
        updated = self.sample_recipe.copy()
        updated['description'] = 'Updated!'
        update_recipe('Test Recipe', updated)
        recipes = load_recipes()
        self.assertEqual(recipes['Test Recipe']['description'], 'Updated!')

    def test_delete_recipe(self):
        save_recipe(self.sample_recipe)
        delete_recipe('Test Recipe')
        recipes = load_recipes()
        self.assertNotIn('Test Recipe', recipes)

if __name__ == '__main__':
    unittest.main()
