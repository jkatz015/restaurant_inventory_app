import streamlit as st

# Language translations for sidebar
SIDEBAR_TRANSLATIONS = {
    "en": {
        "navigation_title": "📋 Navigation",
        "product_database": "📦 Product Database",
        "product_database_desc": "Manage product catalog and inventory items",
        "recipe_builder": "👨‍🍳 Recipe Builder", 
        "recipe_builder_desc": "Create and manage recipes with ingredient lists",
        "variance_calculator": "📊 Variance Calculator",
        "variance_calculator_desc": "Calculate and analyze inventory variances",
        "sheet_to_shelf": "📋 Sheet-to-Shelf Inventory",
        "sheet_to_shelf_desc": "Conduct physical inventory counts",
        "current_page": "Current Page:",
        "language_label": "Language"
    },
    "es": {
        "navigation_title": "📋 Navegación",
        "product_database": "📦 Base de Datos de Productos",
        "product_database_desc": "Gestiona el catálogo de productos e inventario",
        "recipe_builder": "👨‍🍳 Constructor de Recetas",
        "recipe_builder_desc": "Crea y gestiona recetas con listas de ingredientes",
        "variance_calculator": "📊 Calculadora de Variación",
        "variance_calculator_desc": "Calcula y analiza variaciones de inventario",
        "sheet_to_shelf": "📋 Inventario de Hoja a Estante",
        "sheet_to_shelf_desc": "Realiza conteos físicos de inventario",
        "current_page": "Página Actual:",
        "language_label": "Idioma"
    }
}

def get_sidebar_text(key, lang="en"):
    """Get translated text for sidebar"""
    if lang not in SIDEBAR_TRANSLATIONS:
        lang = "en"
    return SIDEBAR_TRANSLATIONS[lang].get(key, key)

def create_language_selector():
    """Create language selection radio buttons"""
    lang = st.sidebar.radio(
        "Language", 
        ["English", "Spanish"], 
        horizontal=True
    )
    return "es" if lang == "Spanish" else "en"

def get_navigation_pages(current_lang):
    """Get the list of navigation pages with translations"""
    return [
        {
            "name": "1_ProductDatabase",
            "display": get_sidebar_text("product_database", current_lang),
            "description": get_sidebar_text("product_database_desc", current_lang)
        },
        {
            "name": "2_RecipeBuilder", 
            "display": get_sidebar_text("recipe_builder", current_lang),
            "description": get_sidebar_text("recipe_builder_desc", current_lang)
        },
        {
            "name": "3_VarianceCalculator",
            "display": get_sidebar_text("variance_calculator", current_lang), 
            "description": get_sidebar_text("variance_calculator_desc", current_lang)
        },
        {
            "name": "4_SheetToShelfInventory",
            "display": get_sidebar_text("sheet_to_shelf", current_lang),
            "description": get_sidebar_text("sheet_to_shelf_desc", current_lang)
        }
    ]

def create_navigation_buttons(pages, current_lang):
    """Create navigation buttons in the sidebar"""
    st.sidebar.markdown(f"### {get_sidebar_text('navigation_title', current_lang)}")
    
    selected_page = None
    for page in pages:
        if st.sidebar.button(
            page["display"],
            key=f"nav_{page['name']}",
            help=page["description"]
        ):
            selected_page = page["name"]
            st.session_state.current_page = page["name"]
    
    return selected_page

def display_current_page_info(selected_page, pages, current_lang):
    """Display information about the current page"""
    # If no button was clicked, use current page from session state
    if selected_page is None:
        selected_page = st.session_state.current_page
    
    # Show current page info
    current_page_info = next((p for p in pages if p["name"] == selected_page), None)
    if current_page_info:
        st.sidebar.markdown("---")
        st.sidebar.markdown(f"**{get_sidebar_text('current_page', current_lang)}** {current_page_info['display']}")
        st.sidebar.markdown(f"*{current_page_info['description']}*")
    
    return selected_page

def setup_sidebar():
    """Setup sidebar with language selector and navigation"""
    # Language toggle in sidebar
    current_lang = create_language_selector()
    
    # Get navigation pages
    pages = get_navigation_pages(current_lang)
    
    # Create navigation buttons
    selected_page = create_navigation_buttons(pages, current_lang)
    
    # Display current page info
    final_selected_page = display_current_page_info(selected_page, pages, current_lang)
    
    return final_selected_page, current_lang
