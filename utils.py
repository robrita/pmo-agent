import streamlit as st

def render_sidebar():
    """
    Render the common sidebar navigation for all pages in the PMO Agent application.
    This function should be called on every page to maintain consistent navigation.
    """
    # Configure page
    st.set_page_config(
        page_title="PMO Agent Dashboard",
        page_icon="📊",
        layout="wide",
        initial_sidebar_state="expanded"
    )

    st.logo(
        "https://upload.wikimedia.org/wikipedia/commons/9/9a/Universal_Robina_logo_2016.svg",
        link="https://www.urc.com.ph/",
    )

    # Custom CSS to adjust padding and hide certain elements
    # This is useful to ensure the layout looks good across different pages
    st.markdown(
        """
        <style>
        .block-container {
            padding-top: 3rem;
            # padding-bottom: 1rem;
            # padding-left: 1rem;
            # padding-right: 1rem;
        }
        .stAppDeployButton {
            display: none;
        }
        .st-emotion-cache-15ecox0 {
            display: none;
        }
        .viewerBadge_container__r5tak {
            display: none;
        }
        .styles_viewerBadge__CvC9N {
            display: none;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )

    with st.sidebar:
        with st.container(border=True):
            st.page_link("app.py", label="PMO Dashboard", icon="🚀")
            st.page_link("pages/1_Employee_Skills_Generator.py", label="Skills Generator", icon="👥")
            st.page_link("pages/2_Project_Scoping_Document_Evaluator.py", label="Document Evaluator", icon="📄")
            st.page_link("pages/3_Project_Timeline_Monitor.py", label="Timeline Monitor", icon="⏰")
            st.page_link("pages/4_Unstructured_Document_Parser.py", label="Document Parser", icon="📋")

        st.image(
            "https://cdn.manilastandard.net/wp-content/uploads/2024/02/URC-Universal-Robina-Corp.jpg",
        )
        st.write("Powered by Azure AI Foundry.")

def keep_state(state_object, state_name):
    """
    Keep the Streamlit session state alive across page navigations.
    This is useful to maintain stateful data like uploaded files or user inputs.
    """
    if state_object:
        st.session_state[state_name] = state_object
    elif state_name in st.session_state:
        return True
    return False
