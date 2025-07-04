import streamlit as st
import os
from dotenv import load_dotenv
from utils import render_sidebar

# Load environment variables
load_dotenv()

def main():
    # Render shared sidebar navigation
    render_sidebar()

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

# if __name__ == "__main__":
#     main()
main()