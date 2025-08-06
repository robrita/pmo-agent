import streamlit as st
from dotenv import load_dotenv
from utils import render_sidebar

# Load environment variables
load_dotenv()

def main():
    # Render shared sidebar navigation
    render_sidebar()

    # Loading the CSS
    with open('style.css') as f:
        st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

    st.title("🚀 PMO Agent Dashboard")
    st.markdown("Welcome to the PMO Agent Dashboard - your comprehensive project management operations tool.")

    # Main Container
    container = st.container()
    container.empty()
    col1, col2, col3, col4 = st.columns(4, gap = 'large')

    with col1.container(key = 'container1'):
        img = "https://cdn-icons-png.flaticon.com/512/7277/7277044.png"
        st.markdown(f"""<div style="text-align: center;"><img src="{img}" width="125" style="border-radius: 5px;" /><br><br></div>""",unsafe_allow_html=True)
        st.empty()
        if st.button("Employee Skills Generator", use_container_width=True):
            st.switch_page("pages/1_Employee_Skills_Generator.py")

    with col2.container(key = 'container2'):
        img = "https://cdn-icons-png.freepik.com/512/8366/8366999.png"
        st.markdown(f"""<div style="text-align: center;"><img src="{img}" width="125" style="border-radius: 5px;" /><br><br></div>""",unsafe_allow_html=True)
        if st.button("Scoping Document Evaluator", use_container_width=True):
            st.switch_page("pages/2_Project_Scoping_Document_Evaluator.py")

    with col3.container(key = 'container3'):
        img = "https://cdn-icons-png.flaticon.com/512/5656/5656665.png"
        st.markdown(f"""<div style="text-align: center;"><img src="{img}" width="125" style="border-radius: 5px;" /><br><br></div>""",unsafe_allow_html=True)
        if st.button("Project Timeline Monitor", use_container_width=True):
            st.switch_page("pages/3_Project_Timeline_Monitor.py")

    with col4.container(key = 'container4'):
        img = "https://cdn-icons-png.freepik.com/256/13558/13558989.png"
        st.markdown(f"""<div style="text-align: center;"><img src="{img}" width="125" style="border-radius: 5px;" /><br><br></div>""",unsafe_allow_html=True)
        if st.button("Unstructured Document Parser", use_container_width=True):
            st.switch_page("pages/4_Unstructured_Document_Parser.py")

if __name__ == "__main__":
    main()