# PMO Agent Dashboard - Product Requirements Document (PRD)

## 1. Executive Summary

### 1.1 Product Overview
The PMO Agent Dashboard is a comprehensive **Project Management Operations (PMO) platform** built with **Streamlit** that leverages **Azure AI Foundry** and **Azure Cosmos DB** to automate and enhance project management workflows. The platform provides four specialized AI-powered modules designed to streamline PMO operations, from skills management to document analysis and project monitoring.

### 1.2 Business Value Proposition
- **Automated Skill Assessment**: AI-powered generation of role-specific skills for workforce development
- **Document Intelligence**: Automated evaluation of project scoping documents against industry standards
- **Project Health Monitoring**: Real-time timeline analysis with deviation tracking and risk identification
- **Intelligent Document Processing**: Advanced parsing and structuring of unstructured documents

### 1.3 Key Stakeholders
- **Primary Users**: Project Managers, PMO Directors, HR Managers, Business Analysts
- **Secondary Users**: Project Team Members, Executives, Document Authors
- **Technical Users**: System Administrators, IT Operations Teams

---

## 2. Product Architecture

### 2.1 Technology Stack

#### Core Framework
- **Frontend**: Streamlit (Python-based web application framework)
- **Backend Language**: Python 3.9+
- **UI Styling**: Custom CSS with Google Fonts (Gasoek One, Oswald)
- **Data Processing**: Pandas, Plotly (for visualizations)

#### Azure Integration
- **AI Services**: Azure AI Foundry (Agents Client)
- **Database**: Azure Cosmos DB (NoSQL document database)
- **Authentication**: Azure Identity with DefaultAzureCredential
- **Content Analysis**: Azure Content Understanding API

#### Key Dependencies
```
streamlit, plotly, openai, python-docx, pandas, python-dotenv,
email-validator, datetime, openpyxl, tabulate, azure-ai-projects,
azure-identity, azure-ai-ml, azure-cosmos, markitdown[pdf, docx, pptx, xlsx, xls]
```

### 2.2 Application Structure
```
pmo-agent/
├── app.py                          # Main dashboard entry point
├── config.py                       # Configuration management
├── utils.py                        # Shared utilities and Azure integration
├── style.css                       # Custom styling
├── requirements.txt                # Python dependencies
├── pages/                          # Module pages
│   ├── 1_Employee_Skills_Generator.py
│   ├── 2_Project_Scoping_Document_Evaluator.py
│   ├── 3_Project_Timeline_Monitor.py
│   └── 4_Unstructured_Document_Parser.py
├── prompts/                        # AI agent prompts
│   ├── 1_Employee_Skills_Generator.md
│   ├── 2_Project_Scoping_Document_Evaluator.md
│   ├── 3_Project_Timeline_Monitor.md
│   └── 4_Unstructured_Document_Parser.md
└── data/                          # Reference data and samples
    ├── project_scoping_guidelines.md
    ├── chatapp_scoping_doc.md
    ├── project1_data.csv
    └── project2_data.csv
```

### 2.3 Core Components

#### Shared Infrastructure (`utils.py`)
- **Navigation System**: Consistent sidebar navigation across all modules
- **Session State Management**: Persistent state management for file uploads and processing
- **Cosmos DB Integration**: Centralized database connectivity with managed identity support
- **UI/UX Framework**: Standardized styling and layout components

#### Configuration Management (`config.py`)
- **Environment Variables**: Secure management of API keys and endpoints
- **Azure OpenAI Settings**: Endpoint, API key, and API version configuration
- **Email Integration**: SMTP configuration for notifications
- **Validation Framework**: Required configuration validation

---

## 3. Module Specifications

### 3.1 Employee Skills Generator

#### Purpose
AI-powered generation of role-specific skills with appropriate proficiency levels for workforce development and competency mapping.

#### Core Functionality
- **Input Processing**: Accepts employee data in format "Name, Job Role, Seniority Level"
- **AI Analysis**: Uses Azure AI Agent (`AGENT_SKILLS_GENERATOR_ID`) to generate relevant skills
- **Skill Classification**: Returns skills with proficiency levels (Beginner, Intermediate, Advanced)
- **Export Capabilities**: CSV download for further processing

#### Technical Implementation
```python
class SkillsGenerator:
    - Azure Foundry Agent integration
    - Thread-based conversation management
    - JSON response parsing with structured output
    - Streamlit session state for persistence
```

#### Input Format
```
Sarah Johnson, Data Scientist, Mid-level
Mike Chen, DevOps Engineer, Mid-level
Lisa Brown, UX Designer, Junior
```

#### Output Format
```json
{
    "results": [
        {
            "name": "Sarah Johnson",
            "role": "Data Scientist", 
            "level": "Mid-level",
            "skills": "Python (Advanced), SQL (Intermediate), Machine Learning (Intermediate)..."
        }
    ]
}
```

#### Business Value
- **Workforce Planning**: Identify skill gaps and training needs
- **Competency Mapping**: Standardize skill assessment across roles
- **Career Development**: Provide clear skill progression paths
- **Resource Allocation**: Match skills to project requirements

### 3.2 Project Scoping Document Evaluator

#### Purpose
Automated analysis of project scoping documents against comprehensive industry guidelines to identify gaps, improvements, and compliance issues.

#### Core Functionality
- **Document Upload**: Supports PDF, DOCX, and Markdown files
- **Text Extraction**: Uses MarkItDown library for multi-format document parsing
- **AI Evaluation**: Compares uploaded documents against reference guidelines
- **Compliance Analysis**: Identifies missing sections, incomplete details, and misalignments
- **Scoring System**: Provides overall completeness rating (1-10 scale)

#### Technical Implementation
```python
class DocumentEvaluator:
    - MarkItDown integration for document parsing
    - Azure AI Agent processing with guidelines comparison
    - File validation and error handling
    - Real-time processing feedback
```

#### Evaluation Criteria
1. **Missing Sections**: Identifies sections from guidelines not present in document
2. **Incomplete Details**: Flags sections lacking sufficient detail
3. **Misalignments**: Detects content contradicting guidelines
4. **Recommendations**: Provides specific improvement suggestions
5. **Overall Score**: Numerical completeness rating

#### Reference Guidelines Include
- Project Overview and Business Case
- Scope Definition and Boundaries
- Stakeholder Analysis and Communication Plan
- Technical Requirements (Functional/Non-functional)
- Risk Assessment and Mitigation Strategies
- Success Criteria and KPIs
- Implementation Approach and Timeline
- Resource Requirements and Budget
- Quality Assurance and Testing Strategy
- Deployment and Support Planning

#### Business Value
- **Quality Assurance**: Ensure project documents meet industry standards
- **Risk Mitigation**: Identify potential project risks early
- **Process Standardization**: Consistent document quality across projects
- **Compliance**: Meet organizational and regulatory requirements

### 3.3 Project Timeline Monitor

#### Purpose
Comprehensive project timeline analysis with Gantt chart visualization, deviation tracking, and performance monitoring across multiple projects.

#### Core Functionality
- **Multi-file Upload**: Supports CSV and Excel files for project data
- **Timeline Analysis**: Calculates planned vs actual durations and deviations
- **Gantt Visualization**: Interactive Gantt charts with baseline overlay using Plotly
- **Deviation Analysis**: Color-coded charts showing delays, early completions, and on-time tasks
- **Project Statistics**: Summary metrics for multiple projects simultaneously

#### Technical Implementation
```python
class ProjectTimelineMonitor:
    - Pandas for data processing and analysis
    - Plotly for interactive visualizations
    - Multi-project data management
    - Statistical analysis and reporting
```

#### Required Data Format
```csv
TaskID,TaskName,PlannedStart,PlannedEnd,ActualStart,ActualEnd,StoryPoints,Sprint
T001,Requirements Gathering,2024-01-01,2024-01-15,2024-01-01,2024-01-18,8,Sprint 1
T002,Design Phase,2024-01-16,2024-01-30,2024-01-19,2024-02-02,13,Sprint 1
```

#### Analytics Capabilities
- **Deviation Calculation**: `Actual Duration - Planned Duration`
- **Performance Metrics**: 
  - Total/Delayed/Early/On-time task counts
  - Average deviation analysis
  - Story point tracking
- **Visual Analytics**:
  - Gantt charts with planned vs actual overlays
  - Deviation bar charts with color coding (Red: Delayed, Green: Early, Gray: On-time)
  - Project comparison across multiple timelines

#### Business Value
- **Project Health Monitoring**: Real-time visibility into project performance
- **Risk Identification**: Early detection of potential delays and bottlenecks
- **Resource Planning**: Data-driven resource allocation decisions
- **Performance Optimization**: Historical analysis for process improvement

### 3.4 Unstructured Document Parser

#### Purpose
Advanced document parsing and structuring system that converts unstructured documents into organized, searchable JSON format with optional Azure Content Understanding integration.

#### Core Functionality
- **Multi-format Support**: PDF, DOCX, and Markdown document processing
- **Dual Processing Methods**:
  - **Standard Parsing**: MarkItDown + AI agent structuring
  - **Content Understanding**: Azure Content Understanding API + AI structuring
- **Cosmos DB Integration**: Automatic saving to 'scoping' container
- **Structured Output**: JSON format with sections, tables, and lists
- **Export Options**: Text, Markdown, and JSON download formats

#### Technical Implementation
```python
class DocumentParser:
    - MarkItDown for standard document extraction
    - Azure Content Understanding API integration
    - Cosmos DB connectivity for persistence
    - Polling mechanism for async processing
    - Error handling and progress tracking
```

#### Processing Flow
1. **Document Upload**: File validation and type detection
2. **Text Extraction**: 
   - Standard: MarkItDown conversion to markdown
   - Advanced: Azure Content Understanding API analysis
3. **AI Structuring**: Azure AI Agent processes extracted text
4. **JSON Output**: Structured data in standardized format
5. **Storage**: Optional Cosmos DB persistence in 'scoping' container

#### Output Format
```json
{
  "sections": [
    {
      "heading": "Project Overview",
      "content": "Detailed project description...",
      "tables": [
        {
          "caption": "Project Timeline",
          "rows": [["Phase", "Duration", "Resources"]]
        }
      ],
      "lists": [
        {
          "type": "ordered",
          "items": ["Requirement analysis", "Design phase", "Development"]
        }
      ]
    }
  ]
}
```

#### Cosmos DB Integration
- **Container**: 'scoping' container for document storage
- **Document Structure**: 
  - Unique ID generation with timestamp and hash
  - Original filename preservation
  - Sections array from parsed JSON
  - Processing timestamp
- **Configuration**: Environment variables for endpoint and database settings

#### Business Value
- **Document Intelligence**: Convert unstructured content into actionable data
- **Knowledge Management**: Centralized document storage and retrieval
- **Content Analysis**: Extract key insights from various document types
- **Process Automation**: Reduce manual document processing effort

---

## 4. User Experience Design

### 4.1 Navigation System
- **Centralized Sidebar**: Consistent navigation across all modules
- **Corporate Branding**: Universal Robina Corporation logo and branding
- **Module Icons**: Visual indicators for each functionality
- **Azure Attribution**: "Powered by Azure AI Foundry" branding

### 4.2 Visual Design
- **Color Scheme**: Dark theme with cyan accents (`rgba(60, 255, 208, 1)`)
- **Typography**: Custom fonts (Gasoek One, Oswald) for modern appearance
- **Layout**: Grid-based design with rounded containers
- **Responsive Design**: Optimized for desktop and tablet usage

### 4.3 User Workflow
1. **Dashboard Landing**: Overview of all available modules
2. **Module Selection**: Click-based navigation to specific functionality
3. **Data Input**: File upload or text input depending on module
4. **Processing**: Real-time feedback with progress indicators
5. **Results Display**: Interactive visualizations and structured output
6. **Export/Save**: Multiple export formats and optional persistence

---

## 5. Integration Architecture

### 5.1 Azure AI Foundry Integration
- **Agent Management**: Four specialized agents for different functionalities
- **Thread-based Processing**: Conversation threads for context management
- **Message Handling**: Structured communication with AI agents
- **Error Handling**: Comprehensive error management and user feedback

### 5.2 Azure Cosmos DB Integration
- **Connection Management**: Centralized client management with caching
- **Authentication**: Managed identity support for secure connectivity
- **Container Operations**: Document CRUD operations for 'scoping' container
- **Error Recovery**: Graceful handling of connectivity issues

### 5.3 Environment Configuration
```python
# Required Environment Variables
AZURE_OPENAI_ENDPOINT = "Your Azure OpenAI endpoint"
AZURE_OPENAI_KEY = "Your Azure OpenAI API key"
FOUNDRY_API_ENDPOINT = "Your Azure AI Foundry endpoint"
AGENT_SKILLS_GENERATOR_ID = "Skills generator agent ID"
AGENT_DOCUMENT_EVALUATOR_ID = "Document evaluator agent ID" 
AGENT_DOCUMENT_PARSER_ID = "Document parser agent ID"
CONTENT_UNDERSTANDING_ENDPOINT = "Azure Content Understanding endpoint"
CONTENT_UNDERSTANDING_API_KEY = "Content Understanding API key"
AZURE_COSMOS_ENDPOINT = "Cosmos DB endpoint"
AZURE_COSMOS_DATABASE = "Database name"
```

---

## 6. Security and Compliance

### 6.1 Authentication and Authorization
- **Azure Identity**: DefaultAzureCredential for secure Azure service access
- **Environment Variables**: Secure configuration management via .env files
- **API Key Management**: Centralized credential handling through config.py

### 6.2 Data Security
- **In-transit Encryption**: HTTPS/TLS for all communications
- **At-rest Security**: Azure Cosmos DB encryption and security
- **Access Control**: Role-based access through Azure Identity
- **Session Management**: Streamlit session state for temporary data handling

### 6.3 Compliance Considerations
- **Data Privacy**: User data isolation and session-based processing
- **Audit Trail**: Processing logs and user activity tracking
- **Data Retention**: Configurable storage policies in Cosmos DB
- **Corporate Compliance**: Universal Robina Corporation standards adherence

---

## 7. Performance and Scalability

### 7.1 Performance Characteristics
- **Document Processing**: Optimized for files up to 10MB
- **Concurrent Users**: Streamlit's built-in session management
- **Response Times**: 
  - Skills Generation: 10-30 seconds depending on input size
  - Document Evaluation: 30-60 seconds for comprehensive analysis
  - Timeline Analysis: Near real-time for standard datasets
  - Document Parsing: 30-120 seconds based on complexity and method

### 7.2 Scalability Considerations
- **Azure Service Scaling**: Leverages Azure's auto-scaling capabilities
- **Database Performance**: Cosmos DB's global distribution and performance tiers
- **Caching Strategy**: `@st.cache_resource` decorators for expensive operations
- **Session State Management**: Efficient state persistence across page navigation

### 7.3 Resource Optimization
- **Memory Management**: Efficient file handling with BytesIO streams
- **API Rate Limiting**: Built-in handling for Azure service limits
- **Progress Indicators**: User feedback during long-running operations
- **Error Recovery**: Graceful degradation and retry mechanisms

---

## 8. Deployment and Operations

### 8.1 Deployment Architecture
- **Application Hosting**: Streamlit application deployment
- **Azure Dependencies**: Multi-service Azure integration
- **Environment Management**: Development, staging, and production configurations
- **Configuration Management**: Environment-specific variable handling

### 8.2 Monitoring and Logging
- **Application Monitoring**: Streamlit built-in metrics and logging
- **Azure Service Monitoring**: Native Azure monitoring for integrated services
- **Error Tracking**: Comprehensive error handling and user feedback
- **Performance Metrics**: Response time and usage analytics

### 8.3 Maintenance Procedures
- **Dependency Updates**: Regular package and service updates
- **Agent Management**: AI agent prompt updates and version management
- **Database Maintenance**: Cosmos DB optimization and cleanup
- **Backup Strategy**: Azure service backup and recovery procedures

---

## 9. Success Metrics and KPIs

### 9.1 User Adoption Metrics
- **Module Usage**: Tracking usage across all four modules
- **Session Duration**: Average time spent per module
- **Document Processing Volume**: Number of documents processed daily/weekly
- **User Retention**: Return usage patterns and frequency

### 9.2 Performance Metrics
- **Processing Accuracy**: AI-generated content quality and relevance
- **Response Times**: Meeting target performance benchmarks
- **Error Rates**: System reliability and error frequency
- **User Satisfaction**: Feedback scores and usability metrics

### 9.3 Business Value Metrics
- **Time Savings**: Reduction in manual PMO tasks
- **Document Quality**: Improvement in scoping document completeness
- **Project Success Rate**: Correlation with timeline monitoring usage
- **Skills Development**: Effectiveness of generated skill assessments

---

## 10. Future Roadmap

### 10.1 Short-term Enhancements (Next 3 months)
- **Multi-user Support**: User authentication and role-based access
- **Enhanced Visualizations**: Additional chart types and interactive features
- **Notification System**: Email alerts for completed processing
- **Template Library**: Pre-built templates for common PMO tasks

### 10.2 Medium-term Features (3-6 months)
- **API Development**: RESTful API for integration with other systems
- **Advanced Analytics**: Predictive analytics and trend analysis
- **Collaborative Features**: Shared workspaces and team functionality
- **Mobile Optimization**: Responsive design for mobile devices

### 10.3 Long-term Vision (6+ months)
- **Enterprise Integration**: SAML/SSO integration for enterprise environments
- **Advanced AI Features**: Custom model training and fine-tuning
- **Workflow Automation**: End-to-end PMO process automation
- **Multi-language Support**: Internationalization and localization

---

## 11. Risk Assessment and Mitigation

### 11.1 Technical Risks
- **Azure Service Dependencies**: Mitigation through fallback mechanisms and error handling
- **AI Model Limitations**: Managing token limits and response quality
- **Data Processing Complexity**: Robust testing across diverse document types
- **Performance Scalability**: Monitoring and optimization strategies

### 11.2 Business Risks
- **User Adoption**: Comprehensive training and change management
- **Data Quality**: Input validation and user guidance
- **Integration Challenges**: Thorough testing and documentation
- **Cost Management**: Azure service optimization and monitoring

### 11.3 Security Risks
- **Data Privacy**: Secure handling of sensitive project information
- **Access Control**: Proper authentication and authorization implementation
- **API Security**: Secure credential management and transmission
- **Compliance**: Adherence to corporate and regulatory requirements

---

## 12. Conclusion

The PMO Agent Dashboard represents a comprehensive, AI-powered solution for modern project management operations. By leveraging Azure's advanced AI capabilities and providing an intuitive Streamlit interface, the platform addresses critical PMO challenges while demonstrating the potential of intelligent automation in project management.

The modular architecture ensures scalability and maintainability, while the Azure integration provides enterprise-grade security and performance. With its four specialized modules covering skills management, document evaluation, timeline monitoring, and intelligent parsing, the platform offers a complete toolkit for PMO professionals.

The success of this platform will be measured not only by its technical capabilities but by its ability to transform PMO operations, reduce manual effort, and improve project outcomes across the organization.