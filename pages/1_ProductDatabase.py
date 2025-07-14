import streamlit as st
import pandas as pd
import os
import locale

# Set locale for currency formatting
try:
    locale.setlocale(locale.LC_ALL, 'en_US.UTF-8')
except:
    try:
        locale.setlocale(locale.LC_ALL, 'en_US')
    except:
        pass  # Use default formatting if locale not available

# Language translations
TRANSLATIONS = {
    "en": {
        "page_title": "🧺 Product Database",
        "page_caption": "Manage your product catalog and inventory items",
        "add_new_product": "Add New Product",
        "product_name": "Product Name",
        "category": "Category",
        "unit_of_measure": "Unit of Measure",
        "cost_per_unit": "Cost per Unit",
        "cost_per_unit_help": "Enter the cost in dollars",
        "add_product_button": "Add Product",
        "cost_per_ounce_preview": "💡 Cost per ounce: {cost} (1 {unit} = {conversion} oz)",
        "please_enter_name": "Please enter a product name.",
        "product_exists": "Product '{name}' already exists!",
        "product_added": "{name} added to the product list!",
        "product_list": "Product List",
        "search_products": "🔍 Search products by name:",
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
        "na": "N/A"
    },
    "es": {
        "page_title": "🧺 Base de Datos de Productos",
        "page_caption": "Gestiona tu catálogo de productos e inventario",
        "add_new_product": "Agregar Nuevo Producto",
        "product_name": "Nombre del Producto",
        "category": "Categoría",
        "unit_of_measure": "Unidad de Medida",
        "cost_per_unit": "Costo por Unidad",
        "cost_per_unit_help": "Ingresa el costo en dólares",
        "add_product_button": "Agregar Producto",
        "cost_per_ounce_preview": "💡 Costo por onza: {cost} (1 {unit} = {conversion} oz)",
        "please_enter_name": "Por favor ingresa un nombre de producto.",
        "product_exists": "¡El producto '{name}' ya existe!",
        "product_added": "¡{name} agregado a la lista de productos!",
        "product_list": "Lista de Productos",
        "search_products": "🔍 Buscar productos por nombre:",
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
        "na": "N/A"
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

# File path for storing products
DATA_FILE = "data/product_data.csv"

# Unit conversion factors to ounces
UNIT_CONVERSIONS = {
    "oz": 1,           # 1 oz = 1 oz
    "lb": 16,          # 1 lb = 16 oz
    "case": 192,       # 1 case = 12 lb = 192 oz (typical case)
    "each": 8,         # 1 each = 8 oz (typical individual item)
    "gallon": 128,     # 1 gallon = 128 oz
    "liter": 33.814    # 1 liter = 33.814 oz
}

def format_currency(amount):
    """Format amount as currency with dollar sign and commas"""
    try:
        return f"${amount:,.2f}"
    except:
        return f"${amount:.2f}"

def format_currency_small(amount):
    """Format amount as currency for small values (2 decimal places)"""
    try:
        return f"${amount:,.2f}"
    except:
        return f"${amount:.2f}"

# Ensure data folder and file exist
def initialize_product_data():
    """Initialize the product data file if it doesn't exist"""
    try:
        if not os.path.exists("data"):
            os.makedirs("data")
        if not os.path.exists(DATA_FILE):
            df = pd.DataFrame({
                "Product Name": pd.Series(dtype="str"),
                "Category": pd.Series(dtype="str"),
                "Unit": pd.Series(dtype="str"),
                "Cost per Unit": pd.Series(dtype="float"),
                "Cost per Oz": pd.Series(dtype="float")  # New column for cost per ounce
            })
            df.to_csv(DATA_FILE, index=False)
    except Exception as e:
        st.error(f"Error initializing product data: {e}")

def convert_to_oz(quantity, unit):
    """Convert any quantity to ounces"""
    if unit in UNIT_CONVERSIONS:
        return quantity * UNIT_CONVERSIONS[unit]
    else:
        return quantity  # Default to 1:1 if unit not found

def calculate_cost_per_oz(cost_per_unit, unit):
    """Calculate cost per ounce"""
    if unit in UNIT_CONVERSIONS:
        return cost_per_unit / UNIT_CONVERSIONS[unit]
    else:
        return cost_per_unit  # Default if unit not found

def save_product(product):
    """Save a new product to the CSV file"""
    try:
        df = pd.read_csv(DATA_FILE)
        
        # Calculate cost per ounce
        cost_per_oz = calculate_cost_per_oz(product["Cost per Unit"], product["Unit"])
        product["Cost per Oz"] = round(cost_per_oz, 2)
        
        df = pd.concat([df, pd.DataFrame([product])], ignore_index=True)
        df.to_csv(DATA_FILE, index=False)
        return True
    except Exception as e:
        st.error(f"Error saving product: {e}")
        return False

def load_products():
    """Load all products from the CSV file"""
    try:
        df = pd.read_csv(DATA_FILE)
        # Ensure proper data types
        if not df.empty:
            df["Cost per Unit"] = pd.to_numeric(df["Cost per Unit"], errors='coerce')
            df["Cost per Oz"] = pd.to_numeric(df["Cost per Oz"], errors='coerce')
        return df
    except Exception as e:
        st.error(f"Error loading products: {e}")
        return pd.DataFrame({
            "Product Name": pd.Series(dtype="str"),
            "Category": pd.Series(dtype="str"),
            "Unit": pd.Series(dtype="str"),
            "Cost per Unit": pd.Series(dtype="float"),
            "Cost per Oz": pd.Series(dtype="float")
        })

def delete_product(product_name):
    """Delete a product from the CSV file"""
    try:
        df = pd.read_csv(DATA_FILE)
        df = df[df["Product Name"] != product_name]
        df.to_csv(DATA_FILE, index=False)
        return True
    except Exception as e:
        st.error(f"Error deleting product: {e}")
        return False

def update_product(old_name, updated_product):
    """Update an existing product in the CSV file"""
    try:
        df = pd.read_csv(DATA_FILE)
        # Find the index of the product to update
        idx = df[df["Product Name"] == old_name].index
        if len(idx) > 0:
            # Calculate new cost per ounce
            cost_per_oz = calculate_cost_per_oz(updated_product["Cost per Unit"], updated_product["Unit"])
            updated_product["Cost per Oz"] = round(cost_per_oz, 2)
            
            # Update the row
            for key, value in updated_product.items():
                df.loc[idx[0], key] = value
            df.to_csv(DATA_FILE, index=False)
            return True
        return False
    except Exception as e:
        st.error(f"Error updating product: {e}")
        return False

def main():
    """Main function for the Product Database page"""
    
    # Define restaurant categories for dropdown
    RESTAURANT_CATEGORIES_EN = [
        "Produce",
        "Beef", 
        "Pork",
        "Chicken",
        "Shellfish",
        "Fish",
        "Dairy",
        "Dry Goods",
        "Breads",
        "Grains",
        "Frozen",
        "Beer",
        "Wine",
        "Cleaning",
        "Paper Goods",
        "Packaging",
        "To-Go Supplies"
    ]
    
    RESTAURANT_CATEGORIES_ES = [
        "Productos Frescos",
        "Res", 
        "Cerdo",
        "Pollo",
        "Mariscos",
        "Pescado",
        "Lácteos",
        "Productos Secos",
        "Panes",
        "Granos",
        "Congelados",
        "Cerveza",
        "Vino",
        "Limpieza",
        "Productos de Papel",
        "Empaques",
        "Suministros Para Llevar"
    ]
    
    # Unit of measure options
    UNITS_EN = ["oz", "lb", "case", "each", "gallon", "liter"]
    UNITS_ES = ["oz", "lb", "caja", "unidad", "galón", "litro"]
    
    # Initialize CSV file if needed
    initialize_product_data()
    
    # Language toggle
    lang = st.radio("Language", ["English", "Spanish"], horizontal=True)
    current_lang = "es" if lang == "Spanish" else "en"
    
    # Page Title
    st.markdown(f"## {get_text('page_title', current_lang)}")
    st.caption(get_text("page_caption", current_lang))
    
    # --- FORM FOR NEW PRODUCT ---
    st.subheader(get_text("add_new_product", current_lang))
    
    with st.form("add_product_form", clear_on_submit=True):
        product_name = st.text_input(get_text("product_name", current_lang))
        
        # Use language-specific categories
        categories = RESTAURANT_CATEGORIES_ES if current_lang == "es" else RESTAURANT_CATEGORIES_EN
        category = st.selectbox(get_text("category", current_lang), categories)
        
        # Use language-specific units
        units = UNITS_ES if current_lang == "es" else UNITS_EN
        unit = st.selectbox(get_text("unit_of_measure", current_lang), units)
        
        cost_per_unit = st.number_input(get_text("cost_per_unit", current_lang), min_value=0.0, format="%.2f", help=get_text("cost_per_unit_help", current_lang))
        
        # Show conversion preview
        if cost_per_unit > 0 and unit in UNIT_CONVERSIONS:
            cost_per_oz = calculate_cost_per_oz(cost_per_unit, unit)
            st.info(get_text("cost_per_ounce_preview", current_lang, cost=format_currency_small(cost_per_oz), unit=unit, conversion=UNIT_CONVERSIONS[unit]))
        
        submitted = st.form_submit_button(get_text("add_product_button", current_lang))
        
        if submitted:
            if product_name.strip() == "":
                st.warning(get_text("please_enter_name", current_lang))
            else:
                # Check for duplicates
                existing_products = load_products()
                if not existing_products.empty and product_name in existing_products["Product Name"].values:
                    st.warning(get_text("product_exists", current_lang, name=product_name))
                else:
                    new_product = {
                        "Product Name": product_name,
                        "Category": category,
                        "Unit": unit,
                        "Cost per Unit": cost_per_unit
                    }
                    if save_product(new_product):
                        st.success(get_text("product_added", current_lang, name=product_name))
    
    # --- SEARCH AND FILTER ---
    st.subheader(get_text("product_list", current_lang))
    products_df = load_products()
    
    if not products_df.empty:
        # Search functionality
        col1, col2 = st.columns([2, 1])
        with col1:
            search_term = st.text_input(get_text("search_products", current_lang))
        with col2:
            category_filter = st.selectbox(get_text("filter_by_category", current_lang), 
                                         [get_text("all_categories", current_lang)] + sorted(products_df["Category"].unique().tolist()))
        
        # Apply filters
        filtered_df = products_df.copy()
        
        if search_term:
            filtered_df = filtered_df[filtered_df["Product Name"].str.contains(search_term, case=False, na=False)]
        
        if category_filter != get_text("all_categories", current_lang):
            filtered_df = filtered_df[filtered_df["Category"] == category_filter]
        
        # Display filtered results
        if isinstance(filtered_df, pd.DataFrame) and not filtered_df.empty:
            # Create a formatted display dataframe
            display_df = filtered_df.copy()
            if 'Cost per Unit' in display_df.columns:
                display_df['Cost per Unit'] = display_df['Cost per Unit'].apply(format_currency)
            if 'Cost per Oz' in display_df.columns:
                display_df['Cost per Oz'] = display_df['Cost per Oz'].apply(format_currency_small)
            
            st.dataframe(display_df, use_container_width=True)
            st.caption(get_text("showing_products", current_lang, filtered=len(filtered_df), total=len(products_df)))
        else:
            st.info(get_text("no_products_match", current_lang))
        
        # --- PRODUCT MANAGEMENT ---
        st.subheader(get_text("manage_products", current_lang))
        
        if not products_df.empty:
            # Create tabs for different management options
            tab1, tab2 = st.tabs([get_text("delete_product", current_lang), get_text("edit_product", current_lang)])
            
            with tab1:
                st.write(f"**{get_text('delete_a_product', current_lang)}**")
                product_to_delete = st.selectbox(get_text("select_product_delete", current_lang), 
                                               [""] + products_df["Product Name"].tolist(),
                                               key="delete_select")
                
                if st.button(get_text("delete_button", current_lang), type="secondary"):
                    if product_to_delete:
                        if delete_product(product_to_delete):
                            st.success(get_text("deleted_successfully", current_lang, name=product_to_delete))
                            st.rerun()
                    else:
                        st.warning(get_text("select_product_delete_warning", current_lang))
            
            with tab2:
                st.write(f"**{get_text('edit_a_product', current_lang)}**")
                product_to_edit = st.selectbox(get_text("select_product_edit", current_lang), 
                                             [""] + products_df["Product Name"].tolist(),
                                             key="edit_select")
                
                if product_to_edit:
                    # Get current product data
                    current_product = products_df[products_df["Product Name"] == product_to_edit].iloc[0]
                    
                    # Edit form
                    with st.form("edit_product_form"):
                        st.write(get_text("editing", current_lang, name=product_to_edit))
                        
                        new_name = st.text_input(get_text("product_name", current_lang), value=current_product["Product Name"])
                        
                        # Use language-specific categories for edit form
                        categories = RESTAURANT_CATEGORIES_ES if current_lang == "es" else RESTAURANT_CATEGORIES_EN
                        new_category = st.selectbox(get_text("category", current_lang), 
                                                  categories,
                                                  index=categories.index(current_product["Category"]) if current_product["Category"] in categories else 0)
                        
                        # Use language-specific units for edit form
                        units = UNITS_ES if current_lang == "es" else UNITS_EN
                        new_unit = st.selectbox(get_text("unit_of_measure", current_lang), 
                                              units,
                                              index=units.index(current_product["Unit"]) if current_product["Unit"] in units else 0)
                        new_cost = st.number_input(get_text("cost_per_unit", current_lang), 
                                                 value=float(current_product["Cost per Unit"]), 
                                                 min_value=0.0, format="%.2f", help=get_text("cost_per_unit_help", current_lang))
                        
                        # Show conversion preview for edit
                        if new_cost > 0 and new_unit in UNIT_CONVERSIONS:
                            cost_per_oz = calculate_cost_per_oz(new_cost, new_unit)
                            st.info(get_text("cost_per_ounce_preview", current_lang, cost=format_currency_small(cost_per_oz), unit=new_unit, conversion=UNIT_CONVERSIONS[new_unit]))
                        
                        edit_submitted = st.form_submit_button(get_text("update_product_button", current_lang))
                        
                        if edit_submitted:
                            if not new_name or str(new_name).strip() == "":
                                st.warning(get_text("please_enter_name", current_lang))
                            else:
                                # Check if new name already exists (but not the current product)
                                existing_products = load_products()
                                name_exists = (new_name in existing_products["Product Name"].values and 
                                             new_name != product_to_edit)
                                
                                if name_exists:
                                    st.warning(get_text("product_exists", current_lang, name=new_name))
                                else:
                                    updated_product = {
                                        "Product Name": new_name,
                                        "Category": new_category,
                                        "Unit": new_unit,
                                        "Cost per Unit": new_cost
                                    }
                                    
                                    if update_product(product_to_edit, updated_product):
                                        st.success(get_text("product_updated", current_lang, name=product_to_edit))
                                        st.rerun()
        
        # --- SUMMARY STATISTICS ---
        st.subheader(get_text("summary", current_lang))
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric(get_text("total_products", current_lang), len(products_df))
        
        with col2:
            # Most expensive product
            if not products_df.empty:
                most_expensive = products_df.loc[products_df["Cost per Unit"].idxmax()]
                st.metric(get_text("most_expensive", current_lang), f"{most_expensive['Product Name'][:15]}...", 
                         f"{format_currency(most_expensive['Cost per Unit'])}")
            else:
                st.metric(get_text("most_expensive", current_lang), get_text("na", current_lang))
        
        with col3:
            # Total inventory value (estimated)
            if not products_df.empty:
                total_value = products_df["Cost per Unit"].sum()
                st.metric(get_text("total_inventory_value", current_lang), f"{format_currency(total_value)}")
            else:
                st.metric(get_text("total_inventory_value", current_lang), format_currency(0))
        
        with col4:
            # Most common category
            if not products_df.empty:
                most_common_category = products_df["Category"].mode().iloc[0] if not products_df["Category"].mode().empty else get_text("na", current_lang)
                category_count = len(products_df[products_df["Category"] == most_common_category])
                st.metric(get_text("top_category", current_lang), most_common_category, f"{category_count} {get_text('items', current_lang)}")
            else:
                st.metric(get_text("top_category", current_lang), get_text("na", current_lang))
    
    else:
        st.info(get_text("no_products_found", current_lang))