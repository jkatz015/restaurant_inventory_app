import pandas as pd
import os
from datetime import datetime
import json

# Language translations
TRANSLATIONS = {
    "en": {
        "page_title": "📊 Variance Calculator",
        "page_caption": "Calculate and analyze cost variances",
        "theoretical_cost": "Theoretical Cost",
        "actual_cost": "Actual Cost",
        "variance": "Variance",
        "variance_percentage": "Variance %",
        "recipe": "Recipe",
        "ingredients": "Ingredients",
        "theoretical_ingredients": "Theoretical Ingredients",
        "actual_ingredients": "Actual Ingredients",
        "add_ingredient": "Add Ingredient",
        "calculate_variance": "Calculate Variance",
        "variance_results": "Variance Results",
        "positive_variance": "Positive Variance (Over Budget)",
        "negative_variance": "Negative Variance (Under Budget)",
        "no_variance": "No Variance",
        "total_theoretical": "Total Theoretical Cost",
        "total_actual": "Total Actual Cost",
        "total_variance": "Total Variance",
        "variance_analysis": "Variance Analysis",
        "cost_breakdown": "Cost Breakdown"
    },
    "es": {
        "page_title": "📊 Calculadora de Varianza",
        "page_caption": "Calcula y analiza varianzas de costos",
        "theoretical_cost": "Costo Teórico",
        "actual_cost": "Costo Real",
        "variance": "Varianza",
        "variance_percentage": "Varianza %",
        "recipe": "Receta",
        "ingredients": "Ingredientes",
        "theoretical_ingredients": "Ingredientes Teóricos",
        "actual_ingredients": "Ingredientes Reales",
        "add_ingredient": "Agregar Ingrediente",
        "calculate_variance": "Calcular Varianza",
        "variance_results": "Resultados de Varianza",
        "positive_variance": "Varianza Positiva (Sobre Presupuesto)",
        "negative_variance": "Varianza Negativa (Bajo Presupuesto)",
        "no_variance": "Sin Varianza",
        "total_theoretical": "Costo Teórico Total",
        "total_actual": "Costo Real Total",
        "total_variance": "Varianza Total",
        "variance_analysis": "Análisis de Varianza",
        "cost_breakdown": "Desglose de Costos"
    }
}

def get_text(key, lang="en", **kwargs):
    """Get translated text for the given key"""
    if lang not in TRANSLATIONS:
        lang = "en"
    text = TRANSLATIONS[lang].get(key, key)
    if text is None:
        text = key
    return text.format(**kwargs) if kwargs else text

# File paths
RECIPES_FILE = "data/recipes.json"
PRODUCTS_FILE = "data/product_data.csv"

def load_recipes():
    """Load recipes from JSON file"""
    try:
        if os.path.exists(RECIPES_FILE):
            with open(RECIPES_FILE, 'r') as f:
                return json.load(f)
        else:
            return {}
    except Exception as e:
        return {}

def load_products():
    """Load products from CSV file"""
    try:
        if os.path.exists(PRODUCTS_FILE):
            return pd.read_csv(PRODUCTS_FILE)
        else:
            return pd.DataFrame()
    except Exception as e:
        return pd.DataFrame()

def calculate_theoretical_cost(recipe_name, recipes, products_df):
    """Calculate theoretical cost for a recipe"""
    if recipe_name not in recipes:
        return 0, []
    
    recipe = recipes[recipe_name]
    ingredients = recipe.get('ingredients', [])
    total_cost = 0
    ingredient_costs = []
    
    for ingredient in ingredients:
        product_name = ingredient['product_name']
        quantity = ingredient['quantity']
        unit = ingredient['unit']
        
        # Find matching product
        product_match = products_df[products_df['Product Name'] == product_name]
        
        if not product_match.empty:
            product = product_match.iloc[0]
            product_cost = product['Cost per Unit']
            cost = quantity * product_cost
            
            ingredient_costs.append({
                'product_name': product_name,
                'quantity': quantity,
                'unit': unit,
                'cost': cost
            })
            total_cost += cost
    
    return total_cost, ingredient_costs

def calculate_actual_cost(actual_ingredients, products_df):
    """Calculate actual cost based on actual ingredients used"""
    total_cost = 0
    ingredient_costs = []
    
    for ingredient in actual_ingredients:
        product_name = ingredient['product_name']
        quantity = ingredient['quantity']
        unit = ingredient['unit']
        
        # Find matching product
        product_match = products_df[products_df['Product Name'] == product_name]
        
        if not product_match.empty:
            product = product_match.iloc[0]
            product_cost = product['Cost per Unit']
            cost = quantity * product_cost
            
            ingredient_costs.append({
                'product_name': product_name,
                'quantity': quantity,
                'unit': unit,
                'cost': cost
            })
            total_cost += cost
    
    return total_cost, ingredient_costs

def calculate_variance(theoretical_cost, actual_cost):
    """Calculate variance between theoretical and actual costs"""
    variance = actual_cost - theoretical_cost
    variance_percentage = (variance / theoretical_cost * 100) if theoretical_cost != 0 else 0
    
    return variance, variance_percentage

def format_currency(amount):
    """Format amount as currency"""
    return f"${amount:.2f}"

def get_variance_status(variance):
    """Get variance status (positive, negative, or none)"""
    if variance > 0:
        return "positive"
    elif variance < 0:
        return "negative"
    else:
        return "none"
