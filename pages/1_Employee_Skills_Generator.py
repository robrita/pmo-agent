# pages/1_Employee_Skills_Generator.py
import streamlit as st
import pandas as pd
import os
from openai import AzureOpenAI
from dotenv import load_dotenv
import re

# Load environment variables
load_dotenv()

st.set_page_config(page_title="Employee Skills Generator", page_icon="👥")

class SkillsGenerator:
    def __init__(self):
        self.client = AzureOpenAI(
            api_key=os.getenv("AZURE_OPENAI_KEY"),
            api_version=os.getenv("AZURE_OPENAI_API_VERSION"),
            azure_endpoint=os.getenv("AZURE_OPENAI_ENDPOINT")
        )
        
    def parse_employees(self, input_text):
        """Parse the input text to extract employee names and roles"""
        employees = []
        lines = input_text.strip().split('\n')
        
        for line in lines:
            line = line.strip()
            if line and ',' in line:
                parts = line.split(',', 1)
                if len(parts) == 2:
                    name = parts[0].strip()
                    role = parts[1].strip()
                    employees.append({'name': name, 'role': role})
        
        return employees
    
    def generate_skills(self, role):
        """Generate skills for a given role using Azure OpenAI"""
        try:
            prompt = f"""
            Generate a list of 8-12 relevant technical and soft skills for a {role}.
            Focus on current industry standards and practical skills.
            Return the skills as a comma-separated list.
            Example format: Python, JavaScript, Problem Solving, Team Collaboration, etc.
            """
            
            response = self.client.chat.completions.create(
                model="gpt-4",  # Replace with your deployed model name
                messages=[
                    {"role": "system", "content": "You are an HR expert specializing in skill assessment and career development."},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=200,
                temperature=0.7
            )
            
            skills = response.choices[0].message.content.strip()
            return skills
            
        except Exception as e:
            st.error(f"Error generating skills: {str(e)}")
            return "Error generating skills"

def main():
    st.title("👥 Employee Skills Generator")
    st.markdown("Generate relevant skills for employees based on their job roles using AI.")
    
    # Initialize the skills generator
    skills_gen = SkillsGenerator()
    
    # Input section
    st.subheader("📝 Input Employee Data")
    st.markdown("Enter employees in the format: **Name, Job Role** (one per line)")
    
    # Example data
    example_data = """John Regala, Frontend Developer
Sarah Johnson, Data Scientist
Mike Chen, DevOps Engineer
Lisa Brown, UX Designer"""
    
    input_text = st.text_area(
        "Employee List:",
        placeholder="John Regala, Frontend Developer\nSarah Johnson, Data Scientist",
        height=150,
        value=example_data if st.checkbox("Use example data") else ""
    )
    
    # Generate button
    if st.button("🚀 Generate Skills", type="primary"):
        if input_text.strip():
            # Parse employees
            employees = skills_gen.parse_employees(input_text)
            
            if employees:
                st.subheader("⚡ Generating Skills...")
                
                # Progress bar
                progress_bar = st.progress(0)
                status_text = st.empty()
                
                results = []
                
                for i, employee in enumerate(employees):
                    status_text.text(f"Generating skills for {employee['name']}...")
                    
                    # Generate skills
                    skills = skills_gen.generate_skills(employee['role'])
                    
                    results.append({
                        'Name': employee['name'],
                        'Role': employee['role'],
                        'Suggested Skills': skills
                    })
                    
                    # Update progress
                    progress_bar.progress((i + 1) / len(employees))
                
                status_text.text("✅ Skills generation complete!")
                
                # Display results
                st.subheader("📊 Results")
                
                # Create DataFrame
                df = pd.DataFrame(results)
                
                # Display as table
                st.dataframe(
                    df,
                    use_container_width=True,
                    hide_index=True
                )
                
                # Download option
                csv = df.to_csv(index=False)
                st.download_button(
                    label="📥 Download as CSV",
                    data=csv,
                    file_name="employee_skills.csv",
                    mime="text/csv"
                )
                
            else:
                st.error("❌ No valid employee entries found. Please check the format.")
        else:
            st.warning("⚠️ Please enter employee data first.")

if __name__ == "__main__":
    main()