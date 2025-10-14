import streamlit as st
import streamlit.components.v1 as components
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
    css = """
    <style>
      /* Hide Streamlit chrome */
      #MainMenu, footer, header { visibility: hidden; }

      /* Hide the default Streamlit sidebar navigation entries only */
      [data-testid="stSidebarNav"] { display: none !important; }

      /* Our controlled sidebar collapse state */
      [data-testid="stSidebar"].collapsed-sidebar {
        transform: translateX(-100%);
        min-width: 0 !important;
        max-width: 0 !important;
        width: 0 !important;
        opacity: 0;
        pointer-events: none;
        transition: transform 0.3s ease, opacity 0.3s ease;
      }

      /* When collapsed, remove left margin from app view (prevents dead space) */
      body.sidebar-collapsed [data-testid="stAppViewContainer"] {
        margin-left: 0 !important;
      }

      /* Floating Hamburger Button (always visible) */
      .hamburger-menu {
        position: fixed;
        top: 1rem;
        left: 1rem;
        z-index: 1000000; /* above Streamlit chrome */
        background-color: #ff4b4b;
        color: #fff;
        border: none;
        border-radius: 8px;
        width: 50px;
        height: 50px;
        font-size: 28px;
        cursor: pointer;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        display: flex !important;
        align-items: center;
        justify-content: center;
        transition: transform .2s ease, box-shadow .2s ease, background-color .2s ease;
        line-height: 1;
        padding: 0;
      }
      .hamburger-menu:hover { background-color: #ff6b6b; transform: scale(1.05); }
      .hamburger-menu:active { transform: scale(0.95); }
    </style>
    """
    st.markdown(css, unsafe_allow_html=True)

    html = """
    <script>
      (function () {
        if (window.sidebarInitialized) return;
        window.sidebarInitialized = true;

        const STORAGE_KEY = "customSidebarCollapsed";
        const BUTTON_ID = "custom-sidebar-toggle";

        function selectSidebar() {
          return window.parent.document.querySelector('[data-testid="stSidebar"]');
        }

        function applyState(collapsed) {
          const sidebar = selectSidebar();
          if (!sidebar) return;

          if (collapsed) {
            sidebar.classList.add('collapsed-sidebar');
            sidebar.setAttribute('aria-expanded', 'false');
            window.parent.document.body.classList.add('sidebar-collapsed');
          } else {
            sidebar.classList.remove('collapsed-sidebar');
            sidebar.setAttribute('aria-expanded', 'true');
            window.parent.document.body.classList.remove('sidebar-collapsed');
          }
        }

        function toggle() {
          const sidebar = selectSidebar();
          if (!sidebar) return;
          const willCollapse = !sidebar.classList.contains('collapsed-sidebar');
          applyState(willCollapse);
          try {
            sessionStorage.setItem(STORAGE_KEY, willCollapse ? 'true' : 'false');
          } catch(e) {}
        }

        function ensureButton() {
          const doc = window.parent.document;
          let button = doc.getElementById(BUTTON_ID);
          if (!button) {
            button = doc.createElement("button");
            button.id = BUTTON_ID;
            button.className = "hamburger-menu";
            button.setAttribute("aria-label", "Toggle sidebar");
            button.setAttribute("title", "Toggle Navigation Menu");
            button.innerHTML = "&#9776;";
            button.onclick = function(e) {
              e.preventDefault();
              e.stopPropagation();
              toggle();
            };
            doc.body.appendChild(button);
          }
          return button;
        }

        function init() {
          ensureButton();
          let collapsed = false;
          try {
            collapsed = sessionStorage.getItem(STORAGE_KEY) === 'true';
          } catch(e) {}
          applyState(collapsed);
        }

        window.parent.__toggleSidebar = toggle;

        // Watch for DOM changes and ensure button persists
        const observer = new MutationObserver(function() {
          ensureButton();
        });

        // Start observing
        if (window.parent.document.body) {
          observer.observe(window.parent.document.body, { childList: true, subtree: false });
        }

        // Initialize
        setTimeout(init, 100);
        setTimeout(init, 500);

        // Keep checking for button
        setInterval(ensureButton, 1000);
      })();
    </script>
    """
    components.html(html, height=0, width=0)

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
