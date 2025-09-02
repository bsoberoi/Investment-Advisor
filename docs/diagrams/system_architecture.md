# System Architecture Diagram

```mermaid
graph TB
    subgraph "User Interface Layer"
        CLI[Command Line Interface<br/>main.py]
        WebUI[Streamlit Web UI<br/>ui/app.py]
    end
    
    subgraph "Application Layer"
        Orchestrator[LangGraph Workflow<br/>graphs/investment_graph.py]
        Executor[Workflow Execution<br/>graphs/execution.py]
        Setup[Environment Setup<br/>setup.py]
    end
    
    subgraph "Agent Layer"
        NewsAgent[News Agent<br/>agents/news_agent.py]
        DataAgent[Data Agent<br/>agents/data_agent.py]
        AnalystAgent[Analyst Agent<br/>agents/analyst_agent.py]
        ExpertAgent[Financial Expert Agent<br/>agents/financial_expert_agent.py]
    end
    
    subgraph "External Services"
        GROQ[GROQ LLM API]
        Yahoo[Yahoo Finance API]
        DDG[DuckDuckGo Search]
    end
    
    subgraph "Data Storage"
        Analysis[Analysis Outputs<br/>outputs/analysis/]
        Recs[Recommendations<br/>outputs/recommendations/]
        Logs[Log Files<br/>outputs/logs/]
        Config[Configuration<br/>config/]
    end
    
    CLI --> Orchestrator
    WebUI --> Orchestrator
    Orchestrator --> Executor
    Executor --> NewsAgent
    Executor --> DataAgent
    Executor --> AnalystAgent
    Executor --> ExpertAgent
    
    NewsAgent --> DDG
    DataAgent --> Yahoo
    NewsAgent --> GROQ
    DataAgent --> GROQ
    AnalystAgent --> GROQ
    ExpertAgent --> GROQ
    
    Executor --> Analysis
    Executor --> Recs
    Executor --> Logs
    
    Setup --> Config
    Setup --> Analysis
    Setup --> Recs
    Setup --> Logs
```

## Layer Descriptions

### User Interface Layer
- **CLI**: Command-line interface for direct system interaction
- **Web UI**: Streamlit-based web interface for browser access

### Application Layer
- **Orchestrator**: LangGraph workflow management and agent coordination
- **Executor**: Workflow execution engine and output generation
- **Setup**: Environment initialization and dependency management

### Agent Layer
- **News Agent**: News gathering and sentiment analysis
- **Data Agent**: Financial data retrieval and processing
- **Analyst Agent**: Information synthesis and analysis
- **Financial Expert Agent**: Investment recommendations

### External Services
- **GROQ**: Large Language Model API for AI processing
- **Yahoo Finance**: Financial data and market information
- **DuckDuckGo**: News search and company information

### Data Storage
- **Analysis**: Generated analysis reports in Markdown format
- **Recommendations**: Investment recommendation reports
- **Logs**: System execution logs and debugging information
- **Config**: System configuration and settings
