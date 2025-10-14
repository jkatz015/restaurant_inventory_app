import streamlit as st
from PIL import Image
import os

def setup_page_config():
    """Configure the main page settings"""
    st.set_page_config(
        page_title="Restaurant Kitchen Inventory",
        page_icon="dY???,?",
        layout="wide",
        initial_sidebar_state="expanded",
        menu_items={
            'Get Help': None,
            'Report a bug': None,
            'About': None
        }
    )

def apply_custom_styles():
    # Initialize session state for sidebar collapse
    if "sidebar_collapsed" not in st.session_state:
        st.session_state.sidebar_collapsed = False

    # Create floating hamburger button using Streamlit (always visible)
    col1, col2, col3 = st.columns([0.1, 8, 0.1])
    with col1:
        # Use a container with a specific test ID for styling
        button_container = st.container()
        with button_container:
            if st.button("☰", key="sidebar_toggle_btn", help="Toggle Navigation Menu"):
                st.session_state.sidebar_collapsed = not st.session_state.sidebar_collapsed
                st.rerun()

    collapsed = st.session_state.sidebar_collapsed

    # Apply CSS styles
    css = f"""
    <style>
      /* Hide Streamlit chrome */
      #MainMenu, footer, header {{ visibility: hidden; }}

      /* Hide the default Streamlit sidebar navigation entries only */
      [data-testid="stSidebarNav"] {{ display: none !important; }}

      /* Style the hamburger button to be floating */
      div[data-testid="column"]:has(button[key="sidebar_toggle_btn"]) {{
        position: fixed !important;
        top: 1rem;
        left: 1rem;
        z-index: 1000000;
        width: auto !important;
        flex: none !important;
      }}

      button[kind="secondary"][key="sidebar_toggle_btn"] {{
        position: fixed;
        top: 1rem;
        left: 1rem;
        z-index: 1000000;
        background-color: #ff4b4b !important;
        color: white !important;
        border: none !important;
        border-radius: 8px !important;
        width: 50px !important;
        height: 50px !important;
        font-size: 28px !important;
        cursor: pointer;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        padding: 0 !important;
        display: flex !important;
        align-items: center !important;
        justify-content: center !important;
        transition: transform 0.2s ease, background-color 0.2s ease;
      }}

      button[kind="secondary"][key="sidebar_toggle_btn"]:hover {{
        background-color: #ff6b6b !important;
        transform: scale(1.05);
        border: none !important;
      }}

      button[kind="secondary"][key="sidebar_toggle_btn"]:active {{
        transform: scale(0.95);
      }}

      /* Sidebar collapse state */
      {'[data-testid="stSidebar"] { transform: translateX(-100%); min-width: 0 !important; max-width: 0 !important; width: 0 !important; opacity: 0; pointer-events: none; transition: transform 0.3s ease, opacity 0.3s ease; }' if collapsed else ''}

      /* When collapsed, remove left margin from app view */
      {'[data-testid="stAppViewContainer"] { margin-left: 0 !important; }' if collapsed else ''}
    </style>
    """
    st.markdown(css, unsafe_allow_html=True)

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
