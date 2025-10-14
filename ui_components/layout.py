import streamlit as st
from PIL import Image
import os

def setup_page_config():
    """Configure the main page settings"""
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

def apply_custom_styles():
    """Apply custom CSS styles to hide default Streamlit elements"""
    hide_streamlit_style = """
        <style>
        #MainMenu {visibility: hidden;}
        footer {visibility: hidden;}
        header {visibility: hidden;}

        /* Hide the default Streamlit sidebar navigation but keep our custom sidebar */
        [data-testid="stSidebarNav"] {display: none;}
        [data-testid="stSidebar"] [data-testid="stSidebarNav"] {display: none;}

        /* Alternative selectors for different Streamlit versions */
        .css-1d391kg {display: none;}
        .css-1lcbmhc {display: none;}

        /* Ensure our custom sidebar is visible */
        [data-testid="stSidebar"] {
            display: block !important;
        }

        /* Make sure sidebar content is visible */
        .css-1d391kg .css-1lcbmhc {
            display: block !important;
        }
        </style>
    """
    st.markdown(hide_streamlit_style, unsafe_allow_html=True)

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

def display_header(logo, title, company_name):
    """Display the main header with logo, title, and company name"""
    # Display logo in main content area (above title)
    if logo:
        # Center the logo and make it larger for main content
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            st.image(logo, width=400, use_container_width=False)
        st.markdown("---")

    # Main content area
    st.title(title)
    st.markdown(f"**{company_name}**")
    st.markdown("---")

def create_main_layout():
    """Create the main layout structure"""
    # Setup page configuration
    setup_page_config()

    # Apply custom styles
    apply_custom_styles()

    # Load logo
    logo = load_logo()

    return logo
