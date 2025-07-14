import unittest
import pandas as pd
from modules.variance_engine import (
    calculate_variance,
    calculate_theoretical_cost,
    calculate_actual_cost,
    get_variance_status,
    format_currency,
    get_text
)

class TestVarianceEngine(unittest.TestCase):
    def setUp(self):
        """Set up test data"""
        # Create sample recipes
        self.recipes = {
            "Test Recipe": {
                "name": "Test Recipe",
                "ingredients": [
                    {"product_name": "Flour", "quantity": 2, "unit": "lb"},
                    {"product_name": "Water", "quantity": 1, "unit": "gallon"}
                ]
            }
        }
        
        # Create sample products DataFrame
        self.products_df = pd.DataFrame({
            'Product Name': ['Flour', 'Water', 'Salt'],
            'Cost per Unit': [5.0, 2.0, 1.0],
            'Unit': ['lb', 'gallon', 'oz']
        })

    def test_get_text(self):
        """Test text translation functionality"""
        # Test English translation
        self.assertEqual(get_text("page_title", "en"), "📊 Variance Calculator")
        self.assertEqual(get_text("theoretical_cost", "en"), "Theoretical Cost")
        
        # Test Spanish translation
        self.assertEqual(get_text("page_title", "es"), "📊 Calculadora de Varianza")
        self.assertEqual(get_text("theoretical_cost", "es"), "Costo Teórico")
        
        # Test unknown key
        self.assertEqual(get_text("unknown_key", "en"), "unknown_key")

    def test_calculate_variance(self):
        """Test variance calculation"""
        theoretical_cost = 100
        actual_cost = 90
        variance, variance_percentage = calculate_variance(theoretical_cost, actual_cost)
        
        self.assertEqual(variance, -10)  # 90 - 100 = -10
        self.assertEqual(variance_percentage, -10.0)  # (-10/100) * 100 = -10%

    def test_calculate_variance_positive(self):
        """Test positive variance (over budget)"""
        theoretical_cost = 100
        actual_cost = 120
        variance, variance_percentage = calculate_variance(theoretical_cost, actual_cost)
        
        self.assertEqual(variance, 20)  # 120 - 100 = 20
        self.assertEqual(variance_percentage, 20.0)  # (20/100) * 100 = 20%

    def test_calculate_variance_zero_theoretical(self):
        """Test variance calculation with zero theoretical cost"""
        theoretical_cost = 0
        actual_cost = 50
        variance, variance_percentage = calculate_variance(theoretical_cost, actual_cost)
        
        self.assertEqual(variance, 50)  # 50 - 0 = 50
        self.assertEqual(variance_percentage, 0)  # Should be 0 when theoretical is 0

    def test_calculate_theoretical_cost(self):
        """Test theoretical cost calculation"""
        total_cost, ingredient_costs = calculate_theoretical_cost("Test Recipe", self.recipes, self.products_df)
        
        # Expected: (2 lb * $5/lb) + (1 gallon * $2/gallon) = $10 + $2 = $12
        expected_cost = (2 * 5.0) + (1 * 2.0)
        self.assertEqual(total_cost, expected_cost)
        self.assertEqual(len(ingredient_costs), 2)

    def test_calculate_theoretical_cost_unknown_recipe(self):
        """Test theoretical cost calculation for unknown recipe"""
        total_cost, ingredient_costs = calculate_theoretical_cost("Unknown Recipe", self.recipes, self.products_df)
        
        self.assertEqual(total_cost, 0)
        self.assertEqual(len(ingredient_costs), 0)

    def test_calculate_actual_cost(self):
        """Test actual cost calculation"""
        actual_ingredients = [
            {"product_name": "Flour", "quantity": 2.5, "unit": "lb"},
            {"product_name": "Water", "quantity": 1.2, "unit": "gallon"}
        ]
        
        total_cost, ingredient_costs = calculate_actual_cost(actual_ingredients, self.products_df)
        
        # Expected: (2.5 lb * $5/lb) + (1.2 gallon * $2/gallon) = $12.5 + $2.4 = $14.9
        expected_cost = (2.5 * 5.0) + (1.2 * 2.0)
        self.assertEqual(total_cost, expected_cost)
        self.assertEqual(len(ingredient_costs), 2)

    def test_calculate_actual_cost_empty(self):
        """Test actual cost calculation with empty ingredients"""
        actual_ingredients = []
        total_cost, ingredient_costs = calculate_actual_cost(actual_ingredients, self.products_df)
        
        self.assertEqual(total_cost, 0)
        self.assertEqual(len(ingredient_costs), 0)

    def test_get_variance_status(self):
        """Test variance status determination"""
        # Positive variance (over budget)
        self.assertEqual(get_variance_status(10), "positive")
        
        # Negative variance (under budget)
        self.assertEqual(get_variance_status(-5), "negative")
        
        # No variance
        self.assertEqual(get_variance_status(0), "none")

    def test_format_currency(self):
        """Test currency formatting"""
        self.assertEqual(format_currency(123.45), "$123.45")
        self.assertEqual(format_currency(0), "$0.00")
        self.assertEqual(format_currency(100), "$100.00")
        self.assertEqual(format_currency(1234.56), "$1234.56")

    def test_edge_cases(self):
        """Test edge cases and error conditions"""
        # Test with very large numbers
        variance, percentage = calculate_variance(1000000, 1000100)
        self.assertEqual(variance, 100)
        self.assertEqual(percentage, 0.01)
        
        # Test with very small numbers
        variance, percentage = calculate_variance(0.01, 0.02)
        self.assertEqual(variance, 0.01)
        self.assertEqual(percentage, 100.0)
        
        # Test with negative costs
        variance, percentage = calculate_variance(-100, -90)
        self.assertEqual(variance, 10)
        self.assertEqual(percentage, -10.0)

if __name__ == '__main__':
    unittest.main()
