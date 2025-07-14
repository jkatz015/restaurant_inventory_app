import pandas as pd
import os
import json
from datetime import datetime

# Language translations
TRANSLATIONS = {
    "en": {
        "page_title": "👨‍🍳 Recipe Builder",
        "page_caption": "Create and manage recipes with detailed ingredient lists and cost calculations",
        "create_recipe": "📝 Create Recipe",
        "view_recipes": "📋 View Recipes",
        "edit_recipe": "✏️ Edit Recipe",
        "create_new_recipe": "Create New Recipe",
        "recipe_name": "Recipe Name",
        "description": "Description",
        "servings": "Servings",
        "prep_time": "Prep Time (minutes)",
        "cook_time": "Cook Time (minutes)",
        "category": "Category",
        "ingredients": "Ingredients",
        "instructions": "Instructions",
        "cooking_instructions": "Cooking Instructions",
        "add_ingredient": "➕ Add Ingredient",
        "remove": "Remove",
        "save_recipe": "💾 Save Recipe",
        "please_enter_name": "Please enter a recipe name.",
        "recipe_saved": "Recipe '{name}' saved successfully!",
        "view_all_recipes": "View All Recipes",
        "no_recipes_found": "No recipes found. Create your first recipe!",
        "total_recipes": "Total Recipes",
        "total_recipe_cost": "Total Recipe Cost",
        "average_recipe_cost": "Average Recipe Cost",
        "showing_recipes": "Showing {count} recipe(s) in '{category}'",
        "no_recipes_category": "No recipes found in category '{category}'.",
        "filter_by_category": "Filter by category:",
        "all_categories": "All Categories",
        "edit_recipe_title": "Edit Recipe",
        "no_recipes_edit": "No recipes to edit.",
        "search_recipe": "🔍 Search recipe by name:",
        "select_recipe_edit": "Select recipe to edit:",
        "editing_recipe": "Editing: {name}",
        "update_recipe": "💾 Update Recipe",
        "delete_recipe": "🗑️ Delete Recipe",
        "recipe_updated": "Recipe updated successfully!",
        "recipe_deleted": "Recipe '{name}' deleted successfully!",
        "no_recipes_match": "No recipes match your search criteria.",
        "product": "Product",
        "quantity": "Qty",
        "unit": "Unit"
    },
    "es": {
        "page_title": "👨‍🍳 Constructor de Recetas",
        "page_caption": "Crea y gestiona recetas con listas detalladas de ingredientes y cálculos de costos",
        "create_recipe": "📝 Crear Receta",
        "view_recipes": "📋 Ver Recetas",
        "edit_recipe": "✏️ Editar Receta",
        "create_new_recipe": "Crear Nueva Receta",
        "recipe_name": "Nombre de la Receta",
        "description": "Descripción",
        "servings": "Porciones",
        "prep_time": "Tiempo de Preparación (minutos)",
        "cook_time": "Tiempo de Cocción (minutos)",
        "category": "Categoría",
        "ingredients": "Ingredientes",
        "instructions": "Instrucciones",
        "cooking_instructions": "Instrucciones de Cocción",
        "add_ingredient": "➕ Agregar Ingrediente",
        "remove": "Eliminar",
        "save_recipe": "💾 Guardar Receta",
        "please_enter_name": "Por favor ingresa un nombre de receta.",
        "recipe_saved": "¡Receta '{name}' guardada exitosamente!",
        "view_all_recipes": "Ver Todas las Recetas",
        "no_recipes_found": "No se encontraron recetas. ¡Crea tu primera receta!",
        "total_recipes": "Total de Recetas",
        "total_recipe_cost": "Costo Total de Recetas",
        "average_recipe_cost": "Costo Promedio de Receta",
        "showing_recipes": "Mostrando {count} receta(s) en '{category}'",
        "no_recipes_category": "No se encontraron recetas en la categoría '{category}'.",
        "filter_by_category": "Filtrar por categoría:",
        "all_categories": "Todas las Categorías",
        "edit_recipe_title": "Editar Receta",
        "no_recipes_edit": "No hay recetas para editar.",
        "search_recipe": "🔍 Buscar receta por nombre:",
        "select_recipe_edit": "Selecciona receta para editar:",
        "editing_recipe": "Editando: {name}",
        "update_recipe": "💾 Actualizar Receta",
        "delete_recipe": "🗑️ Eliminar Receta",
        "recipe_updated": "¡Receta actualizada exitosamente!",
        "recipe_deleted": "¡Receta '{name}' eliminada exitosamente!",
        "no_recipes_match": "Ninguna receta coincide con tu búsqueda.",
        "product": "Producto",
        "quantity": "Cantidad",
        "unit": "Unidad"
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

def load_products() -> pd.DataFrame:
    """Load products from the Product Database"""
    try:
        if os.path.exists(PRODUCTS_FILE):
            return pd.read_csv(PRODUCTS_FILE)
        else:
            return pd.DataFrame()
    except Exception as e:
        return pd.DataFrame()

def load_recipes() -> dict:
    """Load recipes from JSON file"""
    try:
        if os.path.exists(RECIPES_FILE):
            with open(RECIPES_FILE, 'r') as f:
                return json.load(f)
        else:
            return {}
    except Exception as e:
        return {}

def save_recipes(recipes: dict) -> bool:
    """Save recipes to JSON file"""
    try:
        # Ensure data directory exists
        os.makedirs("data", exist_ok=True)
        with open(RECIPES_FILE, 'w') as f:
            json.dump(recipes, f, indent=2)
        return True
    except Exception as e:
        return False

def calculate_recipe_cost(ingredients: list[dict], products_df: pd.DataFrame) -> tuple[float, list[dict]]:
    """Calculate total cost of recipe ingredients"""
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
            product_unit = product['Unit']
            product_cost = product['Cost per Unit']
            
            # Simple cost calculation (can be enhanced with unit conversions)
            if unit == product_unit:
                cost = (quantity * product_cost)
            else:
                # For now, use product cost as is
                cost = (quantity * product_cost)
            
            ingredient_costs.append({
                'product_name': product_name,
                'quantity': quantity,
                'unit': unit,
                'cost': cost,
                'unit_cost': product_cost
            })
            total_cost += cost
    
    return total_cost, ingredient_costs

def format_currency(amount: float) -> str:
    """Format amount as currency"""
    return f"${amount:.2f}"

def save_recipe(recipe_data: dict) -> tuple[bool, str]:
    """Save a new recipe to the JSON file"""
    try:
        recipes = load_recipes()
        
        # Check if recipe already exists
        if recipe_data['name'] in recipes:
            return False, f"Recipe '{recipe_data['name']}' already exists!"
        
        # Calculate recipe cost
        products_df = load_products()
        total_cost, ingredient_costs = calculate_recipe_cost(recipe_data['ingredients'], products_df)
        
        # Add cost information to recipe
        recipe_data['total_cost'] = total_cost
        recipe_data['ingredient_costs'] = ingredient_costs
        recipe_data['created_at'] = datetime.now().isoformat()
        recipe_data['updated_at'] = datetime.now().isoformat()
        
        # Save recipe
        recipes[recipe_data['name']] = recipe_data
        
        if save_recipes(recipes):
            return True, f"Recipe '{recipe_data['name']}' saved successfully!"
        else:
            return False, "Error saving recipe."
    except Exception as e:
        return False, f"Error saving recipe: {e}"

def update_recipe(old_name: str, recipe_data: dict) -> tuple[bool, str]:
    """Update an existing recipe"""
    try:
        recipes = load_recipes()
        
        if old_name not in recipes:
            return False, f"Recipe '{old_name}' not found!"
        
        # Calculate recipe cost
        products_df = load_products()
        total_cost, ingredient_costs = calculate_recipe_cost(recipe_data['ingredients'], products_df)
        
        # Add cost information to recipe
        recipe_data['total_cost'] = total_cost
        recipe_data['ingredient_costs'] = ingredient_costs
        recipe_data['updated_at'] = datetime.now().isoformat()
        
        # Remove old recipe and add updated one
        if old_name != recipe_data['name']:
            del recipes[old_name]
        
        recipes[recipe_data['name']] = recipe_data
        
        if save_recipes(recipes):
            return True, "Recipe updated successfully!"
        else:
            return False, "Error updating recipe."
    except Exception as e:
        return False, f"Error updating recipe: {e}"

def delete_recipe(recipe_name: str) -> tuple[bool, str]:
    """Delete a recipe from the JSON file"""
    try:
        recipes = load_recipes()
        
        if recipe_name not in recipes:
            return False, f"Recipe '{recipe_name}' not found!"
        
        del recipes[recipe_name]
        
        if save_recipes(recipes):
            return True, f"Recipe '{recipe_name}' deleted successfully!"
        else:
            return False, "Error deleting recipe."
    except Exception as e:
        return False, f"Error deleting recipe: {e}"

def get_recipe_categories(recipes: dict) -> list[str]:
    """Get list of unique recipe categories"""
    categories = set()
    for recipe in recipes.values():
        if 'category' in recipe and recipe['category']:
            categories.add(recipe['category'])
    return sorted(list(categories))

def filter_recipes_by_category(recipes: dict, category: str) -> dict:
    """Filter recipes by category"""
    if category == "All Categories":
        return recipes
    
    filtered = {}
    for name, recipe in recipes.items():
        if recipe.get('category') == category:
            filtered[name] = recipe
    return filtered

def search_recipes(recipes: dict, search_term: str) -> dict:
    """Search recipes by name"""
    if not search_term:
        return recipes
    
    filtered = {}
    search_lower = search_term.lower()
    for name, recipe in recipes.items():
        if search_lower in name.lower():
            filtered[name] = recipe
    return filtered
