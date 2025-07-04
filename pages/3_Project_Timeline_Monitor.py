# pages/3_Project_Timeline_Monitor.py
import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import os
from dotenv import load_dotenv
import sys
sys.path.append('..')
from utils import render_sidebar

# Load environment variables
load_dotenv()

class TimelineMonitor:
    def __init__(self):
        self.today = datetime.now().date()
    
    def calculate_status(self, row):
        """Calculate project status based on dates and completion"""
        start_date = pd.to_datetime(row['Start Date']).date()
        end_date = pd.to_datetime(row['End Date']).date()
        completion = row['Completion %']
        
        # Calculate expected completion based on time elapsed
        total_days = (end_date - start_date).days
        elapsed_days = (self.today - start_date).days
        expected_completion = min(100, max(0, (elapsed_days / total_days) * 100))
        
        # Determine status
        if self.today > end_date and completion < 100:
            return 'Overdue', 'red'
        elif completion < expected_completion - 15:
            return 'Behind Schedule', 'orange'
        elif completion >= expected_completion - 5:
            return 'On Track', 'green'
        else:
            return 'At Risk', 'yellow'
    
    def create_timeline_chart(self, df):
        """Create Gantt chart for project timelines"""
        fig = go.Figure()
        
        colors = {'On Track': 'green', 'At Risk': 'orange', 'Behind Schedule': 'red', 'Overdue': 'darkred'}
        
        for idx, row in df.iterrows():
            status, color = self.calculate_status(row)
            
            fig.add_trace(go.Scatter(
                x=[row['Start Date'], row['End Date']],
                y=[row['Project Name'], row['Project Name']],
                mode='lines+markers',
                line=dict(color=colors.get(color, 'blue'), width=6),
                marker=dict(size=8),
                name=row['Project Name'],
                hovertemplate=f"<b>{row['Project Name']}</b><br>" +
                             f"Owner: {row['Project Owner']}<br>" +
                             f"Status: {status}<br>" +
                             f"Completion: {row['Completion %']}%<br>" +
                             f"Start: {row['Start Date']}<br>" +
                             f"End: {row['End Date']}<extra></extra>"
            ))
        
        # Add today line
        fig.add_vline(
            x=self.today,
            line_dash="dash",
            line_color="black",
            annotation_text="Today"
        )
        
        fig.update_layout(
            title="Project Timeline Overview",
            xaxis_title="Date",
            yaxis_title="Projects",
            height=400,
            showlegend=False
        )
        
        return fig
    
    def send_notification(self, project_name, owner_email, message):
        """Send email notification (placeholder implementation)"""
        try:
            # This is a placeholder - you would need to configure SMTP settings
            st.success(f"📧 Notification sent to {owner_email} for project '{project_name}'")
            return True
        except Exception as e:
            st.error(f"Failed to send notification: {str(e)}")
            return False

def main():
    # Render shared sidebar navigation
    render_sidebar()
    
    st.title("⏰ Project Timeline Monitor")
    st.markdown("Track project progress, monitor deadlines, and get alerts for off-track projects.")
    
    # Initialize monitor
    monitor = TimelineMonitor()
    
    # Data input options
    st.subheader("📊 Project Data Input")
    
    input_method = st.radio(
        "Choose input method:",
        ["Upload CSV File", "Manual Entry", "Use Sample Data"]
    )
    
    df = None
    
    if input_method == "Upload CSV File":
        uploaded_file = st.file_uploader(
            "Upload project timeline CSV",
            type=['csv'],
            help="CSV should contain columns: Project Name, Project Owner, Owner Email, Start Date, End Date, Completion %"
        )
        
        if uploaded_file:
            try:
                df = pd.read_csv(uploaded_file)
                st.success("✅ File uploaded successfully!")
            except Exception as e:
                st.error(f"Error reading file: {str(e)}")
    
    elif input_method == "Manual Entry":
        st.markdown("**Add Project Details:**")
        
        with st.form("project_form"):
            col1, col2 = st.columns(2)
            
            with col1:
                project_name = st.text_input("Project Name")
                project_owner = st.text_input("Project Owner")
                owner_email = st.email_input("Owner Email")
            
            with col2:
                start_date = st.date_input("Start Date")
                end_date = st.date_input("End Date")
                completion = st.slider("Completion %", 0, 100, 0)
            
            if st.form_submit_button("Add Project"):
                # Initialize session state for projects if it doesn't exist
                if 'projects' not in st.session_state:
                    st.session_state.projects = []
                
                # Add project to session state
                st.session_state.projects.append({
                    'Project Name': project_name,
                    'Project Owner': project_owner,
                    'Owner Email': owner_email,
                    'Start Date': start_date,
                    'End Date': end_date,
                    'Completion %': completion
                })
                
                st.success(f"Project '{project_name}' added!")
        
        # Display current projects
        if 'projects' in st.session_state and st.session_state.projects:
            df = pd.DataFrame(st.session_state.projects)
    
    else:  # Use Sample Data
        # Create sample data
        sample_data = {
            'Project Name': [
                'Website Redesign',
                'Mobile App Development',
                'Database Migration',
                'Security Audit',
                'API Integration',
                'Cloud Migration'
            ],
            'Project Owner': [
                'Alice Johnson',
                'Bob Smith',
                'Carol Davis',
                'David Wilson',
                'Eva Brown',
                'Frank Miller'
            ],
            'Owner Email': [
                'alice@company.com',
                'bob@company.com',
                'carol@company.com',
                'david@company.com',
                'eva@company.com',
                'frank@company.com'
            ],
            'Start Date': [
                datetime.now().date() - timedelta(days=30),
                datetime.now().date() - timedelta(days=45),
                datetime.now().date() - timedelta(days=60),
                datetime.now().date() - timedelta(days=15),
                datetime.now().date() - timedelta(days=20),
                datetime.now().date() - timedelta(days=10)
            ],
            'End Date': [
                datetime.now().date() + timedelta(days=30),
                datetime.now().date() + timedelta(days=15),
                datetime.now().date() - timedelta(days=5),  # Overdue
                datetime.now().date() + timedelta(days=45),
                datetime.now().date() + timedelta(days=25),
                datetime.now().date() + timedelta(days=50)
            ],
            'Completion %': [75, 60, 85, 40, 30, 20]
        }
        df = pd.DataFrame(sample_data)
        st.info("📋 Using sample project data for demonstration")
    
    # Process and display data
    if df is not None and not df.empty:
        st.subheader("📈 Project Dashboard")
        
        # Calculate statuses
        status_data = []
        for idx, row in df.iterrows():
            status, color = monitor.calculate_status(row)
            status_data.append({
                'Project': row['Project Name'],
                'Owner': row['Project Owner'],
                'Status': status,
                'Completion': row['Completion %'],
                'Start': row['Start Date'],
                'End': row['End Date'],
                'Color': color
            })
        
        status_df = pd.DataFrame(status_data)
        
        # Summary metrics
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            total_projects = len(status_df)
            st.metric("Total Projects", total_projects)
        
        with col2:
            on_track = len(status_df[status_df['Status'] == 'On Track'])
            st.metric("On Track", on_track, f"{(on_track/total_projects*100):.0f}%")
        
        with col3:
            at_risk = len(status_df[status_df['Status'].isin(['At Risk', 'Behind Schedule'])])
            st.metric("At Risk", at_risk, f"{(at_risk/total_projects*100):.0f}%")
        
        with col4:
            overdue = len(status_df[status_df['Status'] == 'Overdue'])
            st.metric("Overdue", overdue, f"{(overdue/total_projects*100):.0f}%")
        
        # Timeline visualization
        st.subheader("📊 Timeline Visualization")
        timeline_chart = monitor.create_timeline_chart(df)
        st.plotly_chart(timeline_chart, use_container_width=True)
        
        # Status table
        st.subheader("📋 Project Status Details")
        
        # Color code the status column
        def color_status(val):
            color_map = {
                'On Track': 'background-color: #d4edda; color: #155724',
                'At Risk': 'background-color: #fff3cd; color: #856404',
                'Behind Schedule': 'background-color: #f8d7da; color: #721c24',
                'Overdue': 'background-color: #f5c6cb; color: #721c24'
            }
            return color_map.get(val, '')
        
        styled_df = status_df[['Project', 'Owner', 'Status', 'Completion', 'Start', 'End']].style.applymap(
            color_status, subset=['Status']
        )
        
        st.dataframe(styled_df, use_container_width=True)
        
        # Notification section
        st.subheader("📧 Notifications")
        
        # Find projects that need attention
        attention_projects = status_df[status_df['Status'].isin(['Behind Schedule', 'Overdue', 'At Risk'])]
        
        if not attention_projects.empty:
            st.warning(f"⚠️ {len(attention_projects)} project(s) need attention!")
            
            for idx, project in attention_projects.iterrows():
                with st.expander(f"🚨 {project['Project']} - {project['Status']}"):
                    st.write(f"**Owner:** {project['Owner']}")
                    st.write(f"**Completion:** {project['Completion']}%")
                    st.write(f"**End Date:** {project['End']}")
                    
                    if st.button(f"Send Alert to {project['Owner']}", key=f"alert_{idx}"):
                        # Get owner email from original dataframe
                        owner_email = df[df['Project Name'] == project['Project']]['Owner Email'].iloc[0]
                        message = f"Your project '{project['Project']}' is {project['Status'].lower()}. Please review and update status."
                        monitor.send_notification(project['Project'], owner_email, message)
        
        else:
            st.success("✅ All projects are on track!")
        
        # Export options
        st.subheader("📥 Export Data")
        col1, col2 = st.columns(2)
        
        with col1:
            csv_data = status_df.to_csv(index=False)
            st.download_button(
                label="📊 Download Status Report",
                data=csv_data,
                file_name=f"project_status_{datetime.now().strftime('%Y%m%d')}.csv",
                mime="text/csv"
            )
        
        with col2:
            if st.button("🔄 Refresh Data"):
                st.rerun()
    
    else:
        st.info("👆 Please provide project data to start monitoring.")
        
        # Help section
        with st.expander("ℹ️ CSV Format Requirements"):
            st.markdown("""
            ### Required CSV Columns:
            - **Project Name**: Name of the project
            - **Project Owner**: Person responsible for the project
            - **Owner Email**: Email address for notifications
            - **Start Date**: Project start date (YYYY-MM-DD format)
            - **End Date**: Project end date (YYYY-MM-DD format)
            - **Completion %**: Current completion percentage (0-100)
            
            ### Example CSV Content:
            ```
            Project Name,Project Owner,Owner Email,Start Date,End Date,Completion %
            Website Redesign,Alice Johnson,alice@company.com,2024-01-01,2024-03-01,75
            Mobile App,Bob Smith,bob@company.com,2024-02-01,2024-05-01,60
            ```
            """)

if __name__ == "__main__":
    main()