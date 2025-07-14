import streamlit as st
import importlib
import os
from PIL import Image
import sys

# Add pages directory to path for dynamic imports
sys.path.append('pages')

# Language translations for main app
MAIN_TRANSLATIONS = {
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
        "app_title": "🍽️ Restaurant Kitchen Inventory",
        "company_name": "Curated Restaurant Consulting"
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
        "app_title": "🍽️ Inventario de Cocina de Restaurante",
        "company_name": "Curated Restaurant Consulting"
    }
}

def get_main_text(key, lang="en"):
    """Get translated text for main app"""
    if lang not in MAIN_TRANSLATIONS:
        lang = "en"
    return MAIN_TRANSLATIONS[lang].get(key, key)

# ===============================================================================
# PAGE CONFIGURATION
# ===============================================================================

st.set_page_config(
    page_title="Restaurant Kitchen Inventory",
    page_icon="🍽️",
    layout="wide",
    initial_sidebar_state="expanded",
    menu_items={
        'Get Help': None,
        'Report a bug': None,
        'About': None
    }
)

# Hide Streamlit's default menu and footer
hide_streamlit_style = """
    <style>
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    
    /* Hide the default Streamlit sidebar navigation */
    [data-testid="stSidebarNav"] {display: none;}
    [data-testid="stSidebar"] [data-testid="stSidebarNav"] {display: none;}
    
    /* Alternative selectors for different Streamlit versions */
    .css-1d391kg {display: none;}
    .css-1lcbmhc {display: none;}
    </style>
"""
st.markdown(hide_streamlit_style, unsafe_allow_html=True)

# ===============================================================================
# SESSION STATE INITIALIZATION
# ===============================================================================

if 'current_page' not in st.session_state:
    st.session_state.current_page = "1_ProductDatabase"

# ===============================================================================
# UTILITY FUNCTIONS
# ===============================================================================

def load_logo():
    """Load and display the company logo"""
    try:
        logo_path = "data/Curated Restaurant Consulting Logo for Business Card.png"
        if os.path.exists(logo_path):
            # Check if file is not empty
            if os.path.getsize(logo_path) > 0:
                logo = Image.open(logo_path)
                # Don't resize - use original quality
                return logo
            else:
                st.warning("Logo file is empty. Please add your actual logo image.")
                return None
        else:
            st.warning("Logo file not found at data/Curated Restaurant Consulting Logo for Business Card.png")
            return None
    except Exception as e:
        st.warning(f"Could not load logo: {e}")
        return None

def load_page_module(page_name):
    """Dynamically load page modules using importlib"""
    try:
        # Remove .py extension if present
        page_name = page_name.replace('.py', '')
        
        # Import the module
        module = importlib.import_module(page_name)
        
        # Check if the module has a main function
        if hasattr(module, 'main'):
            return module.main
        else:
            st.error(f"Page {page_name} does not have a main() function")
            return None
    except ImportError as e:
        st.error(f"Could not import page {page_name}: {e}")
        return None
    except Exception as e:
        st.error(f"Error loading page {page_name}: {e}")
        return None

# ===============================================================================
# SIDEBAR NAVIGATION
# ===============================================================================

def setup_sidebar():
    """Setup sidebar with logo and navigation"""
    
    # Language toggle in sidebar
    lang = st.sidebar.radio("Language", ["English", "Spanish"], horizontal=True)
    current_lang = "es" if lang == "Spanish" else "en"
    
    # Navigation title
    st.sidebar.markdown(f"### {get_main_text('navigation_title', current_lang)}")
    
    # Define pages with icons and descriptions
    pages = [
        {
            "name": "1_ProductDatabase",
            "display": get_main_text("product_database", current_lang),
            "description": get_main_text("product_database_desc", current_lang)
        },
        {
            "name": "2_RecipeBuilder", 
            "display": get_main_text("recipe_builder", current_lang),
            "description": get_main_text("recipe_builder_desc", current_lang)
        },
        {
            "name": "3_VarianceCalculator",
            "display": get_main_text("variance_calculator", current_lang), 
            "description": get_main_text("variance_calculator_desc", current_lang)
        },
        {
            "name": "4_SheetToShelfInventory",
            "display": get_main_text("sheet_to_shelf", current_lang),
            "description": get_main_text("sheet_to_shelf_desc", current_lang)
        }
    ]
    
    # Create navigation buttons
    selected_page = None
    for page in pages:
        if st.sidebar.button(
            page["display"],
            key=f"nav_{page['name']}",
            help=page["description"]
        ):
            selected_page = page["name"]
            st.session_state.current_page = page["name"]
    
    # If no button was clicked, use current page from session state
    if selected_page is None:
        selected_page = st.session_state.current_page
    
    # Show current page info
    current_page_info = next((p for p in pages if p["name"] == selected_page), None)
    if current_page_info:
        st.sidebar.markdown("---")
        st.sidebar.markdown(f"**{get_main_text('current_page', current_lang)}** {current_page_info['display']}")
        st.sidebar.markdown(f"*{current_page_info['description']}*")
    
    return selected_page, current_lang

# ===============================================================================
# MAIN APPLICATION
# ===============================================================================

def main():
    """Main application entry point"""
    
    # Setup sidebar and get selected page
    selected_page, current_lang = setup_sidebar()
    
    # Display logo in main content area (above title)
    logo = load_logo()
    if logo:
        # Center the logo and make it larger for main content
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            st.image(logo, width=400, use_container_width=False)
        st.markdown("---")
    
    # Main content area
    st.title(get_main_text("app_title", current_lang))
    st.markdown(f"**{get_main_text('company_name', current_lang)}**")
    st.markdown("---")
    
    # Load and execute the selected page
    if selected_page:
        page_function = load_page_module(selected_page)
        if page_function:
            try:
                page_function()
            except Exception as e:
                st.error(f"Error executing page {selected_page}: {e}")
                st.info("Please check that the page module is properly implemented.")
        else:
            # Show placeholder content if page module not found
            st.info(f"Page {selected_page} is not yet implemented.")
            st.markdown("### TODO: Implement page functionality")
            st.markdown(f"Create the `{selected_page}.py` file in the `pages/` directory with a `main()` function.")
    else:
        st.warning("No page selected. Please choose a page from the sidebar.")

# ===============================================================================
# APPLICATION ENTRY POINT
# ===============================================================================

if __name__ == "__main__":
    main()
