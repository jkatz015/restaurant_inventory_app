import pandas as pd
import os
from datetime import datetime

# Language translations
TRANSLATIONS = {
    "en": {
        "page_title": "📦 Inventory Management",
        "page_caption": "Track inventory levels and manage stock",
        "current_inventory": "Current Inventory",
        "add_inventory": "Add Inventory",
        "update_inventory": "Update Inventory",
        "product": "Product",
        "quantity": "Quantity",
        "unit": "Unit",
        "date": "Date",
        "notes": "Notes",
        "add_button": "Add to Inventory",
        "update_button": "Update Inventory",
        "inventory_added": "Inventory added successfully!",
        "inventory_updated": "Inventory updated successfully!",
        "no_products": "No products found. Add products first.",
        "select_product": "Select a product:",
        "enter_quantity": "Enter quantity:",
        "enter_notes": "Enter notes (optional):",
        "inventory_summary": "Inventory Summary",
        "total_items": "Total Items",
        "total_value": "Total Value",
        "low_stock": "Low Stock Items",
        "out_of_stock": "Out of Stock"
    },
    "es": {
        "page_title": "📦 Gestión de Inventario",
        "page_caption": "Rastrea niveles de inventario y gestiona stock",
        "current_inventory": "Inventario Actual",
        "add_inventory": "Agregar Inventario",
        "update_inventory": "Actualizar Inventario",
        "product": "Producto",
        "quantity": "Cantidad",
        "unit": "Unidad",
        "date": "Fecha",
        "notes": "Notas",
        "add_button": "Agregar al Inventario",
        "update_button": "Actualizar Inventario",
        "inventory_added": "¡Inventario agregado exitosamente!",
        "inventory_updated": "¡Inventario actualizado exitosamente!",
        "no_products": "No se encontraron productos. Agrega productos primero.",
        "select_product": "Selecciona un producto:",
        "enter_quantity": "Ingresa cantidad:",
        "enter_notes": "Ingresa notas (opcional):",
        "inventory_summary": "Resumen de Inventario",
        "total_items": "Total de Artículos",
        "total_value": "Valor Total",
        "low_stock": "Artículos con Poco Stock",
        "out_of_stock": "Sin Stock"
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
INVENTORY_FILE = "data/inventory.csv"
PRODUCTS_FILE = "data/product_data.csv"

def load_inventory():
    """Load inventory data from CSV file"""
    try:
        if os.path.exists(INVENTORY_FILE):
            return pd.read_csv(INVENTORY_FILE)
        else:
            return pd.DataFrame()
    except Exception as e:
        return pd.DataFrame()

def save_inventory(inventory_df):
    """Save inventory data to CSV file"""
    try:
        os.makedirs("data", exist_ok=True)
        inventory_df.to_csv(INVENTORY_FILE, index=False)
        return True
    except Exception as e:
        return False

def add_inventory_item(product_name, quantity, unit, notes=""):
    """Add a new inventory item"""
    try:
        inventory_df = load_inventory()
        
        new_item = {
            'Product Name': product_name,
            'Quantity': quantity,
            'Unit': unit,
            'Date': datetime.now().strftime('%Y-%m-%d'),
            'Notes': notes
        }
        
        inventory_df = pd.concat([inventory_df, pd.DataFrame([new_item])], ignore_index=True)
        
        if save_inventory(inventory_df):
            return True, "Inventory added successfully!"
        else:
            return False, "Error saving inventory."
    except Exception as e:
        return False, f"Error adding inventory: {e}"

def update_inventory_item(product_name, new_quantity, notes=""):
    """Update existing inventory item"""
    try:
        inventory_df = load_inventory()
        
        # Find the item to update
        mask = inventory_df['Product Name'] == product_name
        if not mask.any():
            return False, f"Product '{product_name}' not found in inventory!"
        
        # Update quantity and notes
        inventory_df.loc[mask, 'Quantity'] = new_quantity
        if notes:
            inventory_df.loc[mask, 'Notes'] = notes
        inventory_df.loc[mask, 'Date'] = datetime.now().strftime('%Y-%m-%d')
        
        if save_inventory(inventory_df):
            return True, "Inventory updated successfully!"
        else:
            return False, "Error saving inventory."
    except Exception as e:
        return False, f"Error updating inventory: {e}"

def calculate_inventory_value(inventory_df, products_df):
    """Calculate total inventory value"""
    total_value = 0
    
    for _, inventory_item in inventory_df.iterrows():
        product_name = inventory_item['Product Name']
        quantity = inventory_item['Quantity']
        
        # Find matching product
        product_match = products_df[products_df['Product Name'] == product_name]
        
        if not product_match.empty:
            product = product_match.iloc[0]
            unit_cost = product['Cost per Unit']
            total_value += quantity * unit_cost
    
    return total_value

def get_low_stock_items(inventory_df, threshold=10):
    """Get items with low stock"""
    low_stock = inventory_df[inventory_df['Quantity'] <= threshold]
    return low_stock

def get_out_of_stock_items(inventory_df):
    """Get items that are out of stock"""
    out_of_stock = inventory_df[inventory_df['Quantity'] <= 0]
    return out_of_stock
