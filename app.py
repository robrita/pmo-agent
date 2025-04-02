import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta

# Set page config
st.set_page_config(
    page_title="URC PMO - Project Planning Gantt Chart",
    page_icon="📊",
    layout="wide"
)

# Add title and description
st.title("URC PMO - Project Planning Gantt Chart")
st.markdown("""
This dashboard visualizes the resource planning and project timelines for URC PMO software projects.
Use the filters on the sidebar to customize the view.
""")

# Load data
@st.cache_data
def load_data():
    # Read CSV with explicit string parsing to avoid automatic conversion
    df = pd.read_csv('projects_chart.csv', dtype=str)
    
    # Split the dataframe into two parts
    # First part: rows before the resource availability section
    project_rows = []
    resource_rows = []
    
    resource_section_started = False
    
    # Process row by row to handle the mixed format
    for idx, row in df.iterrows():
        if "Resource Availability" in str(row["Task"]):
            resource_section_started = True
            continue
        
        if resource_section_started:
            resource_rows.append(row)
        else:
            project_rows.append(row)
    
    # Create separate dataframes
    df_projects = pd.DataFrame(project_rows)
    df_resources = pd.DataFrame(resource_rows)
    
    # Process project tasks
    if not df_projects.empty:
        # Convert date columns to datetime
        df_projects['Start Date'] = pd.to_datetime(df_projects['Start Date'])
        df_projects['End Date'] = pd.to_datetime(df_projects['End Date'])
        # Convert duration to numeric
        df_projects['Duration (days)'] = pd.to_numeric(df_projects['Duration (days)'])
    
    # Process resource availability
    if not df_resources.empty:
        # Convert date columns to datetime - using reliable column positions
        df_resources['Start Date'] = pd.to_datetime(df_resources.iloc[:, 2])  # Third column contains start dates
        df_resources['End Date'] = pd.to_datetime(df_resources.iloc[:, 3])    # Fourth column contains end dates
        # Convert duration to numeric
        df_resources['Duration (days)'] = pd.to_numeric(df_resources['Duration (days)'])
        # Make sure Project column is set correctly
        df_resources['Project'] = 'Resource'
    
    # Combine the dataframes back
    df_combined = pd.concat([df_projects, df_resources], ignore_index=True)
    
    # Add a column for task ID (for Gantt chart)
    df_combined['Task ID'] = df_combined.index
    
    return df_combined

try:
    data = load_data()
    
    # Get unique projects and resources for filtering
    projects = ['All Projects'] + sorted([p for p in data['Project'].unique() if p != 'Resource'])
    resources = ['All Resources'] + sorted([r for r in data['Resource'].unique() if r != 'Project'])
    
    # Sidebar filters
    st.sidebar.header("Filters")
    selected_view = st.sidebar.radio(
        "Select View:",
        ["Projects View", "Resources View"]
    )
    
    selected_project = st.sidebar.selectbox(
        "Select Project:",
        projects
    )
    
    selected_resource = st.sidebar.selectbox(
        "Select Resource:",
        resources
    )
    
    # Date range filter
    min_date = data['Start Date'].min().date()
    max_date = data['End Date'].max().date()
    
    date_range = st.sidebar.date_input(
        "Date Range:",
        value=[min_date, max_date],
        min_value=min_date,
        max_value=max_date
    )
    
    if len(date_range) == 2:
        start_date, end_date = date_range
    else:
        start_date, end_date = min_date, max_date
    
    # Filter data based on selections
    filtered_data = data.copy()
    
    if selected_project != 'All Projects':
        filtered_data = filtered_data[filtered_data['Project'] == selected_project]
    else:
        # When "All Projects" is selected, exclude the resource availability rows in the main view
        if selected_view == "Projects View":
            filtered_data = filtered_data[filtered_data['Project'] != 'Resource']
    
    if selected_resource != 'All Resources':
        filtered_data = filtered_data[filtered_data['Resource'] == selected_resource]
    
    # Filter by date range
    filtered_data = filtered_data[
        (filtered_data['Start Date'].dt.date >= start_date) & 
        (filtered_data['End Date'].dt.date <= end_date)
    ]
    
    # Create different views based on selection
    if selected_view == "Projects View":
        # Only show tasks (remove resource availability rows)
        project_data = filtered_data[filtered_data['Project'] != 'Resource']
        
        if not project_data.empty:
            # Create Gantt chart
            fig = px.timeline(
                project_data, 
                x_start="Start Date", 
                x_end="End Date", 
                y="Task",
                color="Project",
                hover_name="Resource",
                hover_data={"Task": True, "Start Date": True, "End Date": True, "Duration (days)": True},
                height=800
            )
            
            # Customize layout
            fig.update_layout(
                title="Project Tasks Timeline",
                xaxis_title="Timeline",
                yaxis_title="Tasks",
                yaxis={'categoryorder':'total ascending'},
                legend_title="Projects",
                xaxis_rangeslider_visible=True
            )
            
            # Display the chart
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.warning("No data matches your filter criteria.")
    
    else:  # Resources View
        # Only show resources assignments, not the project rows
        resource_view_data = filtered_data[filtered_data['Resource'] != 'Project'].copy()
        
        if not resource_view_data.empty:
            # For resources view, use resource as y-axis
            try:
                # Create resource Gantt chart
                fig = px.timeline(
                    resource_view_data, 
                    x_start="Start Date", 
                    x_end="End Date", 
                    y="Resource",
                    color="Project",
                    hover_name="Task",
                    hover_data={"Start Date": True, "End Date": True, "Duration (days)": True},
                    height=800
                )
                
                # Customize layout
                fig.update_layout(
                    title="Resources Allocation Timeline",
                    xaxis_title="Timeline",
                    yaxis_title="Resources",
                    yaxis={'categoryorder':'total ascending'},
                    legend_title="Projects",
                    xaxis_rangeslider_visible=True
                )
                
                # Only add resource availability as background when looking at all resources or a specific one
                if selected_resource == 'All Resources' or selected_resource != 'All Resources':
                    # Get resource availability data (those with Project='Resource')
                    resource_availability = data[data['Project'] == 'Resource'].copy()
                    
                    # Filter resource availability to only those in the current view
                    if selected_resource != 'All Resources':
                        resource_availability = resource_availability[resource_availability['Resource'] == selected_resource]
                    
                    # Get list of resources currently displayed in the chart
                    visible_resources = resource_view_data['Resource'].unique()
                    
                    # Only add shapes for resources that are visible in the current view
                    if not resource_availability.empty:
                        for _, row in resource_availability.iterrows():
                            # Only add availability background if the resource is in the current view
                            if row['Resource'] in visible_resources:
                                try:
                                    # Safely add the shape for resource availability
                                    fig.add_shape(
                                        type="rect",
                                        x0=row['Start Date'],
                                        x1=row['End Date'],
                                        y0=row['Resource'],  # Use resource name directly
                                        y1=row['Resource'],  # Use resource name directly
                                        fillcolor="lightgreen",
                                        opacity=0.3,
                                        layer="below",
                                        line_width=0,
                                        yref="y",
                                        ysizemode="scaled"
                                    )
                                except Exception as shape_error:
                                    # Don't let shape errors break the whole app
                                    st.warning(f"Could not display availability for {row['Resource']}. This won't affect functionality.")
                
                # Display the chart
                st.plotly_chart(fig, use_container_width=True)
            
            except Exception as chart_error:
                st.error(f"Error creating the resource chart: {chart_error}")
                st.warning("Try selecting specific projects or resources to narrow down the view.")
        else:
            st.warning("No data matches your filter criteria.")
    
    # Resource allocation metrics
    if not filtered_data.empty:
        st.header("Resource Allocation Metrics")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            # Resource utilization
            resource_counts = filtered_data['Resource'].value_counts()
            resource_counts = resource_counts[resource_counts.index != 'Project']  # Exclude Project rows
            st.metric("Total Resources Used", len(resource_counts))
        
        with col2:
            # Project count
            project_counts = filtered_data[filtered_data['Project'] != 'Resource']['Project'].nunique()
            st.metric("Number of Projects", project_counts)
        
        with col3:
            # Total timeline - handle safely
            try:
                if 'Project' in filtered_data['Resource'].values or 'Resource' in filtered_data['Project'].values:
                    # Get only actual tasks for timeline calculation
                    task_data = filtered_data[(filtered_data['Resource'] != 'Project') & (filtered_data['Project'] != 'Resource')]
                    timeline_days = (task_data['End Date'].max() - task_data['Start Date'].min()).days
                else:
                    timeline_days = (filtered_data['End Date'].max() - filtered_data['Start Date'].min()).days
                
                st.metric("Total Timeline (Days)", timeline_days)
            except Exception:
                st.metric("Total Timeline (Days)", "N/A")
        
        # Resource allocation table
        st.subheader("Resource Allocation Details")
        
        # Prepare a cleaned table for display
        display_columns = ['Resource', 'Task', 'Project', 'Start Date', 'End Date', 'Duration (days)']
        display_data = filtered_data[filtered_data['Resource'] != 'Project'][display_columns].copy()
        
        # Format dates for display
        display_data['Start Date'] = display_data['Start Date'].dt.strftime('%Y-%m-%d')
        display_data['End Date'] = display_data['End Date'].dt.strftime('%Y-%m-%d')
        
        # Show resource allocation table
        st.dataframe(display_data, use_container_width=True)
    
    # Add information about new hires
    st.header("New Hires Required")
    new_hires_data = data[data['Resource'].str.contains('New Hire', na=False)]
    
    if not new_hires_data.empty:
        new_hires_df = new_hires_data[['Resource', 'Task', 'Start Date', 'End Date', 'Duration (days)']].copy()
        new_hires_df['Start Date'] = new_hires_df['Start Date'].dt.strftime('%Y-%m-%d')
        new_hires_df['End Date'] = new_hires_df['End Date'].dt.strftime('%Y-%m-%d')
        
        st.dataframe(new_hires_df, use_container_width=True)
        
        st.info("""
        **Budget Impact for New Hires:**
        - UI/UX Designers (2): $30,000-$40,000 total
        - Security Specialist (1): $25,000-$35,000
        - Total estimated budget impact: $55,000-$75,000
        """)
    else:
        st.write("No new hires information available.")

except Exception as e:
    st.error(f"An error occurred while loading the data: {e}")
    st.info("Please check the format of the CSV file and ensure that date columns are in the correct format (YYYY-MM-DD).")
    
# Footer
st.markdown("---")
st.caption("URC Project Management Office (PMO) - Resource Planning Dashboard | Generated on March 26, 2025")