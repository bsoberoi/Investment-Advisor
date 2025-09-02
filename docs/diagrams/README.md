# Investment Advisor System Diagrams

This directory contains comprehensive diagrams that illustrate the architecture, workflows, and deployment options for the Investment Advisor Multi-Agent System.

## Available Diagrams

### 1. System Architecture Diagram
**File**: `system_architecture.md`
**Description**: High-level system architecture showing the five main architectural layers and their relationships.
**Key Elements**:
- User Interface Layer (CLI & Web UI)
- Application Layer (LangGraph orchestration)
- Agent Layer (specialized AI agents)
- External Services (GROQ, Yahoo Finance, DuckDuckGo)
- Data Storage (outputs, logs, configuration)

### 2. LangGraph Workflow Orchestration
**File**: `langgraph_workflow.md`
**Description**: Detailed workflow showing how agents interact and process data through the LangGraph orchestration engine.
**Key Elements**:
- Parallel data collection (News & Data agents)
- Sequential information synthesis (Analyst & Expert agents)
- Clear data flow between agents
- Output generation process

### 3. Data Flow Sequence Diagram
**File**: `data_flow_sequence.md`
**Description**: Sequence diagram showing the end-to-end process from user input to final output generation.
**Key Elements**:
- User interaction flow
- Parallel vs. sequential processing
- External API interactions
- Error handling and recovery

### 4. Component Relationships and Dependencies
**File**: `component_relationships.md`
**Description**: Detailed view of how different modules interact and their dependencies.
**Key Elements**:
- Module dependencies and relationships
- Configuration and logging integration
- External service connections
- Data flow patterns

### 5. Extensibility and Customization Architecture
**File**: `extensibility_architecture.md`
**Description**: Shows how the system can be extended with new agents, data sources, and workflows.
**Key Elements**:
- Pluggable agent architecture
- Extensible data sources
- Customizable workflows
- LLM provider flexibility

### 6. Deployment Architecture and Options
**File**: `deployment_architecture.md`
**Description**: Comprehensive deployment options from local development to enterprise-scale deployments.
**Key Elements**:
- Local development setup
- Streamlit Cloud deployment
- Cloud VM deployment
- PaaS and container orchestration

## How to Use These Diagrams

### For Developers
- **System Architecture**: Understand the overall system structure
- **Component Relationships**: Plan new features and modifications
- **Data Flow**: Debug issues and optimize performance

### For Architects
- **LangGraph Workflow**: Design new agent workflows
- **Extensibility**: Plan system extensions and customizations
- **Deployment**: Choose appropriate deployment strategies

### For Stakeholders
- **System Overview**: Understand system capabilities and scope
- **Deployment Options**: Evaluate hosting and scaling requirements
- **Future Planning**: Assess extensibility and growth potential

## Diagram Formats

All diagrams are created using **Mermaid** syntax, which provides:
- **Version Control**: Diagrams are stored as text and can be versioned
- **Rendering**: Automatic rendering in GitHub, GitLab, and other platforms
- **Maintenance**: Easy updates and modifications
- **Collaboration**: Team members can suggest changes through pull requests

## Rendering the Diagrams

### GitHub/GitLab
- Diagrams render automatically in markdown files
- No additional setup required

### Local Development
- Use Mermaid Live Editor: https://mermaid.live/
- Copy diagram code and paste for visualization
- Export as PNG, SVG, or PDF

### Documentation Tools
- Many documentation platforms support Mermaid
- Can be integrated into automated documentation pipelines

## Contributing

When adding new diagrams:
1. Use clear, descriptive filenames
2. Include comprehensive descriptions
3. Follow the existing naming conventions
4. Update this README with new diagram information
5. Ensure diagrams are accessible and well-documented

## Related Documentation

- **Technical Design Document**: `../Technical_Design_Investment_Advisor.md`
- **System README**: `../../README.md`
- **Setup Guide**: `../../setup.py`
- **Streamlit Hosting Guide**: `../streamlit_hosting.md`
