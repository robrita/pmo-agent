# pages/2_Project_Scoping_Document_Evaluator.py
import streamlit as st
import pandas as pd
import os
from openai import AzureOpenAI
from dotenv import load_dotenv
from docx import Document
import tempfile
import sys
sys.path.append('..')
from utils import render_sidebar

# Load environment variables
load_dotenv()

class DocumentEvaluator:
    def __init__(self):
        self.client = AzureOpenAI(
            api_key=os.getenv("AZURE_OPENAI_KEY"),
            api_version=os.getenv("AZURE_OPENAI_API_VERSION"),
            azure_endpoint=os.getenv("AZURE_OPENAI_ENDPOINT")
        )
    
    def extract_text_from_docx(self, file):
        """Extract text from uploaded .docx file"""
        try:
            # Save uploaded file temporarily
            with tempfile.NamedTemporaryFile(delete=False, suffix='.docx') as tmp_file:
                tmp_file.write(file.getvalue())
                tmp_file_path = tmp_file.name
            
            # Read the document
            doc = Document(tmp_file_path)
            text = []
            
            for paragraph in doc.paragraphs:
                if paragraph.text.strip():
                    text.append(paragraph.text.strip())
            
            # Clean up temporary file
            os.unlink(tmp_file_path)
            
            return '\n'.join(text)
            
        except Exception as e:
            st.error(f"Error reading document: {str(e)}")
            return None
    
    def evaluate_document(self, scoping_doc_text, guidelines_text):
        """Evaluate scoping document against guidelines"""
        try:
            prompt = f"""
            You are a project management expert. Please evaluate the following project scoping document against the provided guidelines.

            GUIDELINES DOCUMENT:
            {guidelines_text}

            PROJECT SCOPING DOCUMENT:
            {scoping_doc_text}

            Please provide a comprehensive evaluation report that includes:

            1. MISSING SECTIONS: List any sections from the guidelines that are completely missing from the scoping document.

            2. INCOMPLETE DETAILS: Identify sections that exist but lack sufficient detail or clarity.

            3. MISALIGNMENTS: Point out any content that doesn't align with the guidelines or contradicts them.

            4. RECOMMENDATIONS: Provide specific suggestions for improvement.

            5. OVERALL SCORE: Rate the document completeness on a scale of 1-10.

            Format your response in clear sections with headers and bullet points.
            """
            
            response = self.client.chat.completions.create(
                model="gpt-4",  # Replace with your deployed model name
                messages=[
                    {"role": "system", "content": "You are a senior project management consultant with expertise in document analysis and project scoping."},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=1500,
                temperature=0.3
            )
            
            return response.choices[0].message.content.strip()
            
        except Exception as e:
            st.error(f"Error evaluating document: {str(e)}")
            return None

def main():
    # Render shared sidebar navigation
    render_sidebar()
    
    st.title("📄 Project Scoping Document Evaluator")
    st.markdown("Analyze project scoping documents against guidelines to identify gaps and improvements.")
    
    # Initialize evaluator
    evaluator = DocumentEvaluator()
    
    # File upload section
    st.subheader("📁 Upload Documents")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("**Project Scoping Document**")
        scoping_file = st.file_uploader(
            "Upload Project Scoping Document",
            type=['docx'],
            key="scoping_doc",
            help="Upload the project scoping document to be evaluated"
        )
    
    with col2:
        st.markdown("**Project Guidelines Document**")
        guidelines_file = st.file_uploader(
            "Upload Project Guidelines Document",
            type=['docx'],
            key="guidelines_doc",
            help="Upload the guidelines document for comparison"
        )
    
    # Process documents
    if scoping_file and guidelines_file:
        st.subheader("📋 Document Information")
        
        col1, col2 = st.columns(2)
        with col1:
            st.info(f"**Scoping Document:** {scoping_file.name}")
        with col2:
            st.info(f"**Guidelines Document:** {guidelines_file.name}")
        
        # Analyze button
        if st.button("🔍 Analyze Documents", type="primary"):
            with st.spinner("Extracting text from documents..."):
                # Extract text from both documents
                scoping_text = evaluator.extract_text_from_docx(scoping_file)
                guidelines_text = evaluator.extract_text_from_docx(guidelines_file)
                
                if scoping_text and guidelines_text:
                    st.success("✅ Documents processed successfully!")
                    
                    with st.spinner("Analyzing document compliance..."):
                        # Evaluate the document
                        evaluation = evaluator.evaluate_document(scoping_text, guidelines_text)
                        
                        if evaluation:
                            st.subheader("📊 Evaluation Report")
                            
                            # Display the evaluation in an expandable format
                            with st.expander("📋 Full Evaluation Report", expanded=True):
                                st.markdown(evaluation)
                            
                            # Additional features
                            st.subheader("📥 Export Options")
                            
                            col1, col2 = st.columns(2)
                            
                            with col1:
                                # Download evaluation as text
                                st.download_button(
                                    label="📄 Download Report as Text",
                                    data=evaluation,
                                    file_name="evaluation_report.txt",
                                    mime="text/plain"
                                )
                            
                            with col2:
                                # Create summary metrics
                                lines = evaluation.split('\n')
                                word_count = len(evaluation.split())
                                st.metric("Report Length", f"{word_count} words")
                        
                        else:
                            st.error("❌ Failed to generate evaluation report.")
                else:
                    st.error("❌ Failed to extract text from one or both documents.")
    
    else:
        st.info("👆 Please upload both documents to begin the analysis.")
        
        # Show example or help
        with st.expander("ℹ️ How to use this tool"):
            st.markdown("""
            ### How to Use the Document Evaluator:
            
            1. **Upload Project Scoping Document**: Upload the .docx file containing your project scope
            2. **Upload Guidelines Document**: Upload the .docx file with your organization's project guidelines
            3. **Click Analyze**: The AI will compare both documents and provide a detailed evaluation
            
            ### What You'll Get:
            - **Missing Sections**: Identify what's missing from your scoping document
            - **Incomplete Details**: Find areas that need more information
            - **Misalignments**: Spot content that doesn't follow guidelines
            - **Recommendations**: Get specific suggestions for improvement
            - **Overall Score**: Receive a completeness rating
            
            ### Supported Formats:
            - Microsoft Word documents (.docx)
            """)

if __name__ == "__main__":
    main()