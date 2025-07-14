"""
Product Manager Module

This module handles all product-related operations including:
- Product CRUD operations (Create, Read, Update, Delete)
- Price calculations and unit conversions
- Data validation and file I/O operations
- Bulk operations for supplier data updates

Dependencies:
- pandas: For data manipulation
- os: For file operations
- locale: For currency formatting
- utils.validator: For data validation
- utils.file_loader: For file operations
- config: For configuration settings

Classes:
    None

Functions:
    get_text: Get translated text for UI
    initialize_product_data: Initialize product data file
    load_products: Load products from CSV file
    save_product: Save new product to file
    delete_product: Delete product from file
    update_product: Update existing product
    bulk_update_prices: Update prices from supplier data
    format_currency: Format amount as currency
    format_currency_small: Format small amounts as currency
    convert_to_oz: Convert quantity to ounces
    calculate_cost_per_oz: Calculate cost per ounce
    migrate_existing_data: Migrate existing data to new format
"""

import pandas as pd
import os
import locale
from datetime import datetime
from typing import Dict, List, Tuple, Optional, Union, Any
from pathlib import Path

# Import utilities
from utils.validator import validate_product_data, validate_sku, validate_price

# File operations - using pandas directly since utils.file_loader was removed
def load_csv_file(file_path: str) -> pd.DataFrame:
    """Load CSV file using pandas"""
    try:
        return pd.read_csv(file_path)
    except Exception as e:
        raise FileNotFoundError(f"Could not load file {file_path}: {e}")

def save_csv_file(df: pd.DataFrame, file_path: Union[str, Path]) -> None:
    """Save DataFrame to CSV file"""
    try:
        df.to_csv(str(file_path), index=False)
    except Exception as e:
        raise IOError(f"Could not save file {file_path}: {e}")

class FileLoadError(Exception):
    """Custom exception for file loading errors"""
    pass

from config import config

# Set locale for currency formatting
try:
    locale.setlocale(locale.LC_ALL, 'en_US.UTF-8')
except:
    try:
        locale.setlocale(locale.LC_ALL, 'en_US')
    except:
        pass  # Use default formatting if locale not available

# Language translations
TRANSLATIONS: Dict[str, Dict[str, str]] = {
    "en": {
        "page_title": "🧺 Product Database",
        "page_caption": "Manage your product catalog and inventory items",
        "add_new_product": "Add New Product",
        "product_name": "Product Name",
        "sku": "SKU",
        "pack_size": "Pack Size",
        "category": "Category",
        "unit_of_measure": "Unit of Measure",
        "cost_per_unit": "Cost per Unit",
        "cost_per_unit_help": "Enter the cost in dollars",
        "location": "Location",
        "location_help": "Select where this product is stored",
        "add_product_button": "Add Product",
        "cost_per_ounce_preview": "💡 Cost per ounce: {cost} (1 {unit} = {conversion} oz)",
        "please_enter_name": "Please enter a product name.",
        "product_exists": "Product '{name}' already exists!",
        "product_added": "{name} added to the product list!",
        "product_list": "Product List",
        "search_products": "🔍 Search products by name or SKU:",
        "filter_by_category": "Filter by category:",
        "all_categories": "All Categories",
        "showing_products": "Showing {filtered} of {total} products",
        "no_products_match": "No products match your search criteria.",
        "manage_products": "Manage Products",
        "delete_product": "Delete Product",
        "edit_product": "Edit Product",
        "delete_a_product": "Delete a Product",
        "select_product_delete": "Select product to delete:",
        "delete_button": "🗑️ Delete Product",
        "deleted_successfully": "Deleted '{name}' successfully!",
        "select_product_delete_warning": "Please select a product to delete.",
        "edit_a_product": "Edit a Product",
        "select_product_edit": "Select product to edit:",
        "editing": "Editing: **{name}**",
        "update_product_button": "💾 Update Product",
        "product_updated": "Updated '{name}' successfully!",
        "summary": "📊 Summary",
        "total_products": "Total Products",
        "most_expensive": "Most Expensive",
        "total_inventory_value": "Total Inventory Value",
        "top_category": "Top Category",
        "items": "items",
        "no_products_found": "No products found. Add a product to get started.",
        "na": "N/A",
        "bulk_update_title": "📊 Bulk Update from Supplier CSV",
        "upload_supplier_csv": "Upload supplier CSV file",
        "supplier_csv_preview": "Supplier CSV Preview:",
        "column_mapping": "Column Mapping:",
        "select_sku_column": "Select SKU column:",
        "select_price_column": "Select price column:",
        "update_prices_button": "Update Prices",
        "updated_products_count": "Updated {count} products with new pricing!"
    },
    "es": {
        "page_title": "🧺 Base de Datos de Productos",
        "page_caption": "Gestiona tu catálogo de productos e inventario",
        "add_new_product": "Agregar Nuevo Producto",
        "product_name": "Nombre del Producto",
        "sku": "SKU",
        "pack_size": "Tamaño del Paquete",
        "category": "Categoría",
        "unit_of_measure": "Unidad de Medida",
        "cost_per_unit": "Costo por Unidad",
        "cost_per_unit_help": "Ingresa el costo en dólares",
        "location": "Ubicación",
        "location_help": "Selecciona dónde se almacena este producto",
        "add_product_button": "Agregar Producto",
        "cost_per_ounce_preview": "💡 Costo por onza: {cost} (1 {unit} = {conversion} oz)",
        "please_enter_name": "Por favor ingresa un nombre de producto.",
        "product_exists": "¡El producto '{name}' ya existe!",
        "product_added": "¡{name} agregado a la lista de productos!",
        "product_list": "Lista de Productos",
        "search_products": "🔍 Buscar productos por nombre o SKU:",
        "filter_by_category": "Filtrar por categoría:",
        "all_categories": "Todas las Categorías",
        "showing_products": "Mostrando {filtered} de {total} productos",
        "no_products_match": "Ningún producto coincide con tu búsqueda.",
        "manage_products": "Gestionar Productos",
        "delete_product": "Eliminar Producto",
        "edit_product": "Editar Producto",
        "delete_a_product": "Eliminar un Producto",
        "select_product_delete": "Selecciona el producto a eliminar:",
        "delete_button": "🗑️ Eliminar Producto",
        "deleted_successfully": "¡'{name}' eliminado exitosamente!",
        "select_product_delete_warning": "Por favor selecciona un producto para eliminar.",
        "edit_a_product": "Editar un Producto",
        "select_product_edit": "Selecciona el producto a editar:",
        "editing": "Editando: **{name}**",
        "update_product_button": "💾 Actualizar Producto",
        "product_updated": "¡'{name}' actualizado exitosamente!",
        "summary": "📊 Resumen",
        "total_products": "Total de Productos",
        "most_expensive": "Más Caro",
        "total_inventory_value": "Valor Total del Inventario",
        "top_category": "Categoría Principal",
        "items": "artículos",
        "no_products_found": "No se encontraron productos. Agrega un producto para comenzar.",
        "na": "N/A",
        "bulk_update_title": "📊 Actualización Masiva desde CSV del Proveedor",
        "upload_supplier_csv": "Subir archivo CSV del proveedor",
        "supplier_csv_preview": "Vista Previa del CSV del Proveedor:",
        "column_mapping": "Mapeo de Columnas:",
        "select_sku_column": "Selecciona columna SKU:",
        "select_price_column": "Selecciona columna de precio:",
        "update_prices_button": "Actualizar Precios",
        "updated_products_count": "¡{count} productos actualizados con nuevos precios!"
    }
}

# File path for storing products
DATA_FILE = config.PRODUCTS_FILE

# Unit conversion factors to ounces
UNIT_CONVERSIONS: Dict[str, float] = config.UNIT_CONVERSIONS

def get_text(key: str, lang: str = "en", **kwargs) -> str:
    """
    Get translated text for the given key
    
    Args:
        key: Translation key to look up
        lang: Language code ('en' or 'es')
        **kwargs: Format parameters for the text
    
    Returns:
        str: Translated text with parameters substituted
        
    Example:
        >>> get_text("product_added", "en", name="Apple")
        "Apple added to the product list!"
    """
    if lang not in TRANSLATIONS:
        lang = "en"
    text = TRANSLATIONS[lang].get(key, key)
    if text is None:
        text = key
    return text.format(**kwargs) if kwargs else text

def format_currency(amount: Union[float, int, None]) -> str:
    """
    Format amount as currency with dollar sign and commas
    
    Args:
        amount: Amount to format
        
    Returns:
        str: Formatted currency string
        
    Example:
        >>> format_currency(1234.56)
        "$1,234.56"
    """
    try:
        if amount is None:
            return "$None"
        return f"${amount:,.2f}"
    except (ValueError, TypeError):
        return f"${amount:.2f}"

def format_currency_small(amount: Union[float, int, None]) -> str:
    """
    Format amount as currency for small values (2 decimal places)
    
    Args:
        amount: Amount to format
        
    Returns:
        str: Formatted currency string
        
    Example:
        >>> format_currency_small(2.5)
        "$2.50"
    """
    try:
        if amount is None:
            return "$None"
        return f"${amount:,.2f}"
    except (ValueError, TypeError):
        return f"${amount:.2f}"

def migrate_existing_data() -> Optional[str]:
    """
    Migrate existing data to include SKU, Location, and Pack Size columns if they don't exist
    
    Returns:
        Optional[str]: Success message or None if no migration needed
        
    Raises:
        FileLoadError: If file operations fail
    """
    try:
        if os.path.exists(DATA_FILE):
            df = load_csv_file(str(DATA_FILE))
            migration_messages = []
            
            if "SKU" not in df.columns:
                # Add SKU column with empty values
                df.insert(1, "SKU", "")
                migration_messages.append("SKU column")
            
            if "Location" not in df.columns:
                # Add Location column with default value (after SKU column)
                df.insert(2, "Location", "Dry Goods Storage")
                migration_messages.append("Location column")
            
            if "Pack Size" not in df.columns:
                # Add Pack Size column with empty values (after Category column)
                df.insert(4, "Pack Size", "")
                migration_messages.append("Pack Size column")
            
            if "Current Price per Unit" not in df.columns:
                # Rename "Cost per Unit" to "Current Price per Unit" and add new columns
                if "Cost per Unit" in df.columns:
                    df = df.rename(columns={"Cost per Unit": "Current Price per Unit"})
                else:
                    df.insert(6, "Current Price per Unit", "")
                migration_messages.append("Current Price per Unit column")
            
            if "Last Price per Unit" not in df.columns:
                # Add Last Price per Unit column
                df.insert(7, "Last Price per Unit", "")
                migration_messages.append("Last Price per Unit column")
            
            if "Last Updated Date" not in df.columns:
                # Add Last Updated Date column
                df.insert(8, "Last Updated Date", "")
                migration_messages.append("Last Updated Date column")
            
            if migration_messages:
                save_csv_file(df, DATA_FILE)
                return f"Data migrated to include {', '.join(migration_messages)}!"
    except Exception as e:
        raise FileLoadError(f"Error migrating data: {e}")
    
    return None

def initialize_product_data() -> Optional[str]:
    """
    Initialize the product data file if it doesn't exist
    
    Returns:
        Optional[str]: Migration message or None if no initialization needed
        
    Raises:
        FileLoadError: If file operations fail
    """
    try:
        if not os.path.exists("data"):
            os.makedirs("data")
        if not os.path.exists(DATA_FILE):
            df = pd.DataFrame({
                "Product Name": pd.Series(dtype="str"),
                "SKU": pd.Series(dtype="str"),
                "Location": pd.Series(dtype="str"),
                "Category": pd.Series(dtype="str"),
                "Pack Size": pd.Series(dtype="str"),
                "Unit": pd.Series(dtype="str"),
                "Current Price per Unit": pd.Series(dtype="float"),
                "Last Price per Unit": pd.Series(dtype="float"),
                "Last Updated Date": pd.Series(dtype="str"),
                "Cost per Oz": pd.Series(dtype="float")  # New column for cost per ounce
            })
            df.to_csv(DATA_FILE, index=False)
        else:
            # Migrate existing data to include new columns
            return migrate_existing_data()
    except Exception as e:
        raise FileLoadError(f"Error initializing product data: {e}")
    
    return None

def convert_to_oz(quantity: Union[float, int], unit: str) -> float:
    """
    Convert quantity to ounces based on unit
    
    Args:
        quantity: Quantity to convert
        unit: Unit of measurement
        
    Returns:
        float: Quantity in ounces
        
    Example:
        >>> convert_to_oz(1, "lb")
        16.0
    """
    conversion = UNIT_CONVERSIONS.get(unit.lower(), 1)
    return quantity * conversion

def calculate_cost_per_oz(cost_per_unit: Union[float, int], unit: str) -> float:
    """
    Calculate cost per ounce for a given unit and cost
    
    Args:
        cost_per_unit: Cost per unit
        unit: Unit of measurement
        
    Returns:
        float: Cost per ounce
        
    Example:
        >>> calculate_cost_per_oz(16, "lb")
        1.0
    """
    conversion = UNIT_CONVERSIONS.get(unit.lower(), 1)
    return cost_per_unit / conversion if conversion > 0 else 0

def save_product(product: Dict[str, Any]) -> Tuple[bool, str]:
    """
    Save a new product to the data file
    
    Args:
        product: Product dictionary with required fields
        
    Returns:
        Tuple[bool, str]: (success, message)
        
    Raises:
        FileLoadError: If file operations fail
        ValidationError: If product data is invalid
    """
    try:
        # Validate product data
        is_valid, errors = validate_product_data(product)
        if not is_valid:
            return False, f"Validation errors: {', '.join(errors)}"
        
        # Load existing products
        products_df = load_products()
        
        # Check if product already exists
        if not products_df.empty and product['name'] in products_df['Product Name'].values:
            return False, get_text("product_exists", "en", name=product['name'])
        
        # Calculate cost per ounce
        cost_per_oz = calculate_cost_per_oz(product['cost'], product['unit'])
        
        # Create new product row
        new_product = {
            'Product Name': product['name'],
            'SKU': product.get('sku', ''),
            'Location': product.get('location', 'Dry Goods Storage'),
            'Category': product.get('category', ''),
            'Pack Size': product.get('pack_size', ''),
            'Unit': product['unit'],
            'Current Price per Unit': product['cost'],
            'Last Price per Unit': None,  # No previous price for new products
            'Last Updated Date': None,    # No previous update for new products
            'Cost per Oz': cost_per_oz
        }
        
        # Add to DataFrame
        new_df = pd.DataFrame([new_product])
        if products_df.empty:
            products_df = new_df
        else:
            products_df = pd.concat([products_df, new_df], ignore_index=True)
        
        # Save to file
        if save_csv_file is None:
            raise FileLoadError("save_csv_file function is not defined")
        save_csv_file(products_df, str(DATA_FILE))
        
        return True, get_text("product_added", "en", name=product['name'])
        
    except Exception as e:
        raise FileLoadError(f"Error saving product: {e}")

def load_products() -> pd.DataFrame:
    """
    Load products from the data file
    
    Returns:
        pd.DataFrame: Products data
        
    Raises:
        FileLoadError: If file operations fail
    """
    try:
        if not os.path.exists(DATA_FILE):
            # Initialize if file doesn't exist
            initialize_product_data()
            return pd.DataFrame({col: pd.Series(dtype='object') for col in ['Product Name', 'SKU', 'Location', 'Category', 'Pack Size', 'Unit', 'Current Price per Unit', 'Last Price per Unit', 'Last Updated Date', 'Cost per Oz']})
        
        df = load_csv_file(str(DATA_FILE))
        return df if isinstance(df, pd.DataFrame) else pd.DataFrame()
    except Exception as e:
        raise FileLoadError(f"Error loading products: {e}")

def delete_product(product_name: str) -> Tuple[bool, str]:
    """
    Delete a product from the data file
    
    Args:
        product_name: Name of the product to delete
        
    Returns:
        Tuple[bool, str]: (success, message)
        
    Raises:
        FileLoadError: If file operations fail
    """
    try:
        products_df = load_products()
        
        if product_name not in products_df['Product Name'].values:
            return False, f"Product '{product_name}' not found."
        
        # Remove the product
        products_df = products_df[products_df['Product Name'] != product_name]
        products_df = pd.DataFrame(products_df)  # Ensure it's a DataFrame
        
        # Save updated data
        if save_csv_file is None:
            raise FileLoadError("save_csv_file function is not defined")
        save_csv_file(products_df, str(DATA_FILE))
        
        return True, get_text("deleted_successfully", "en", name=product_name)
        
    except Exception as e:
        raise FileLoadError(f"Error deleting product: {e}")

def update_product(old_name: str, updated_product: Dict[str, Any]) -> Tuple[bool, str]:
    """
    Update an existing product in the data file
    
    Args:
        old_name: Original product name
        updated_product: Updated product data
        
    Returns:
        Tuple[bool, str]: (success, message)
        
    Raises:
        FileLoadError: If file operations fail
        ValidationError: If product data is invalid
    """
    try:
        # Validate updated product data
        is_valid, errors = validate_product_data(updated_product)
        if not is_valid:
            return False, f"Validation errors: {', '.join(errors)}"
        
        products_df = load_products()
        
        if old_name not in products_df['Product Name'].values:
            return False, f"Product '{old_name}' not found."
        
        # Calculate new cost per ounce
        cost_per_oz = calculate_cost_per_oz(updated_product['cost'], updated_product['unit'])
        
        # Check if price has changed
        mask = products_df['Product Name'] == old_name
        current_price = products_df.loc[mask, 'Current Price per Unit'].iloc[0]
        new_price = updated_product['cost']
        
        # Update the product
        products_df.loc[mask, 'Product Name'] = updated_product['name']
        products_df.loc[mask, 'SKU'] = updated_product.get('sku', '')
        products_df.loc[mask, 'Location'] = updated_product.get('location', 'Dry Goods Storage')
        products_df.loc[mask, 'Category'] = updated_product.get('category', '')
        products_df.loc[mask, 'Pack Size'] = updated_product.get('pack_size', '')
        products_df.loc[mask, 'Unit'] = updated_product['unit']
        
        # Handle price history
        if current_price != new_price:
            # Price changed - update history
            products_df.loc[mask, 'Last Price per Unit'] = current_price
            products_df.loc[mask, 'Last Updated Date'] = datetime.now().strftime('%Y-%m-%d')
        
        products_df.loc[mask, 'Current Price per Unit'] = new_price
        products_df.loc[mask, 'Cost per Oz'] = cost_per_oz
        
        # Save updated data
        save_csv_file(products_df, DATA_FILE)
        
        return True, get_text("product_updated", "en", name=updated_product['name'])
        
    except Exception as e:
        raise FileLoadError(f"Error updating product: {e}")

def bulk_update_prices(supplier_df: pd.DataFrame, sku_column: str, price_column: str) -> Tuple[bool, str]:
    """
    Update product prices from supplier CSV data
    
    Args:
        supplier_df: Supplier data DataFrame
        sku_column: Name of the SKU column in supplier data
        price_column: Name of the price column in supplier data
        
    Returns:
        Tuple[bool, str]: (success, message)
        
    Raises:
        FileLoadError: If file operations fail
    """
    try:
        products_df = load_products()
        updated_count = 0
        
        for _, supplier_row in supplier_df.iterrows():
            sku = supplier_row[sku_column]
            new_price = float(supplier_row[price_column])
            
            # Convert SKU to int to handle float/int comparison
            sku_int = int(float(sku))
            
            # Find matching product by SKU - handle both string and int types
            mask = products_df['SKU'] == sku_int
            if mask.any():
                current_price = products_df.loc[mask, 'Current Price per Unit'].iloc[0]
                
                # Always update the price (even if same) to ensure cost per oz recalculation
                # Update price history if price changed
                if current_price != new_price:
                    products_df.loc[mask, 'Last Price per Unit'] = current_price
                    products_df.loc[mask, 'Last Updated Date'] = datetime.now().strftime('%Y-%m-%d')
                
                # Update price and recalculate cost per ounce
                products_df.loc[mask, 'Current Price per Unit'] = new_price
                # Get the unit for all matching rows (should be the same for all)
                unit_series = products_df.loc[mask, 'Unit']
                # Use the first unit if available, else skip cost per oz update
                if not unit_series.empty:
                    unit = unit_series.iloc[0]
                    cost_per_oz = calculate_cost_per_oz(new_price, unit)
                    products_df.loc[mask, 'Cost per Oz'] = cost_per_oz
                updated_count += 1

        if updated_count > 0:
            save_csv_file(products_df, DATA_FILE)
            return True, get_text("updated_products_count", "en", count=updated_count)
        else:
            return False, "No products were updated. Check SKU matching."
        
    except Exception as e:
        raise FileLoadError(f"Error updating prices: {e}")
