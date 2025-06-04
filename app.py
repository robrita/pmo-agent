import streamlit as st
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Configure page
st.set_page_config(
    page_title="PMO Agent Dashboard",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

def main():
    st.title("🚀 PMO Agent Dashboard")
    st.markdown("""
    Welcome to the PMO Agent Dashboard - your comprehensive project management operations tool.
    
    ## Available Tools:
    
    ### 📋 Employee Skills Generator
    Generate relevant skills for employees based on their job roles using AI-powered analysis.
    
    ### 📄 Project Scoping Document Evaluator
    Analyze project scoping documents against guidelines to identify gaps and improvements.
    
    ### ⏰ Project Timeline Monitor
    Track project progress, monitor deadlines, and get alerts for off-track projects.
    
    **Select a page from the sidebar to get started!**
    """)
    
    # Display some stats or overview
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric("Active Projects", "12", "2")
    
    with col2:
        st.metric("Team Members", "45", "3")
    
    with col3:
        st.metric("Completion Rate", "87%", "5%")
    
    # Quick links
    st.markdown("---")
    st.subheader("🔗 Quick Actions")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button("👥 Generate Skills", use_container_width=True):
            st.switch_page("pages/1_Employee_Skills_Generator.py")
    
    with col2:
        if st.button("📄 Evaluate Document", use_container_width=True):
            st.switch_page("pages/2_Project_Scoping_Document_Evaluator.py")
    
    with col3:
        if st.button("⏰ Monitor Timeline", use_container_width=True):
            st.switch_page("pages/3_Project_Timeline_Monitor.py")
    
    # Configuration status
    st.markdown("---")
    st.subheader("⚙️ Configuration Status")
    
    # Check if Azure OpenAI is configured
    if os.getenv("AZURE_OPENAI_KEY") and os.getenv("AZURE_OPENAI_ENDPOINT"):
        st.success("✅ Azure OpenAI configured")
    else:
        st.error("❌ Azure OpenAI not configured. Please check your .env file.")
        with st.expander("Configuration Help"):
            st.markdown("""
            To configure Azure OpenAI:
            1. Copy `.env_sample` to `.env`
            2. Fill in your Azure OpenAI credentials:
               - `AZURE_OPENAI_ENDPOINT`
               - `AZURE_OPENAI_KEY`
               - `AZURE_OPENAI_API_VERSION`
            """)

if __name__ == "__main__":
    main()