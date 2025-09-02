# Component Relationships and Dependencies Diagram

```mermaid
graph TB
    subgraph "Entry Points"
        Main[main.py<br/>CLI Entry Point]
        App[ui/app.py<br/>Streamlit Web UI]
        Setup[setup.py<br/>Environment Setup]
    end
    
    subgraph "Core Orchestration"
        Graph[graphs/investment_graph.py<br/>LangGraph Definition]
        Exec[graphs/execution.py<br/>Workflow Execution]
    end
    
    subgraph "Agent System"
        News[agents/news_agent.py<br/>News Agent]
        Data[agents/data_agent.py<br/>Data Agent]
        Analyst[agents/analyst_agent.py<br/>Analyst Agent]
        Expert[agents/financial_expert_agent.py<br/>Financial Expert]
    end
    
    subgraph "Tools & Utilities"
        Search[tools/search_tool.py<br/>Search Tool]
        Config[config/settings.py<br/>Configuration]
        Logging[config/logging_config.py<br/>Logging]
    end
    
    subgraph "External Dependencies"
        GROQ[GROQ API<br/>LLM Service]
        Yahoo[Yahoo Finance<br/>Financial Data]
        DDG[DuckDuckGo<br/>News Search]
    end
    
    subgraph "Output & Storage"
        Analysis[outputs/analysis/<br/>Analysis Reports]
        Recs[outputs/recommendations/<br/>Recommendations]
        Logs[outputs/logs/<br/>System Logs]
    end
    
    %% Entry Point Dependencies
    Main --> Graph
    Main --> Exec
    App --> Graph
    App --> Exec
    Setup --> Config
    Setup --> Analysis
    Setup --> Recs
    Setup --> Logs
    
    %% Core Orchestration Dependencies
    Graph --> News
    Graph --> Data
    Graph --> Analyst
    Graph --> Expert
    Exec --> Graph
    Exec --> Analysis
    Exec --> Recs
    Exec --> Logs
    
    %% Agent Dependencies
    News --> Search
    News --> GROQ
    Data --> Yahoo
    Data --> GROQ
    Analyst --> GROQ
    Expert --> GROQ
    
    %% Tool Dependencies
    Search --> DDG
    News --> Config
    Data --> Config
    Analyst --> Config
    Expert --> Config
    
    %% Logging Dependencies
    Main --> Logging
    App --> Logging
    Setup --> Logging
    News --> Logging
    Data --> Logging
    Analyst --> Logging
    Expert --> Logging
    
    %% Configuration Dependencies
    News --> Config
    Data --> Config
    Analyst --> Config
    Expert --> Config
    Logging --> Config
    
    style Main fill:#e3f2fd
    style App fill:#e3f2fd
    style Setup fill:#e3f2fd
    style Graph fill:#f3e5f5
    style Exec fill:#f3e5f5
    style News fill:#fff3e0
    style Data fill:#fff3e0
    style Analyst fill:#fff3e0
    style Expert fill:#fff3e0
    style Config fill:#e8f5e8
    style Logging fill:#e8f5e8
```

## Component Dependencies

### Entry Points
- **main.py**: Primary CLI interface, depends on orchestration and execution modules
- **ui/app.py**: Web interface, depends on orchestration and execution modules
- **setup.py**: Environment setup, depends on configuration and output directories

### Core Orchestration
- **investment_graph.py**: Defines LangGraph workflow and agent interactions
- **execution.py**: Executes workflow and manages output generation

### Agent System
- **news_agent.py**: News gathering and sentiment analysis
- **data_agent.py**: Financial data retrieval and processing
- **analyst_agent.py**: Information synthesis and analysis
- **financial_expert_agent.py**: Investment recommendations

### Tools & Utilities
- **search_tool.py**: DuckDuckGo search integration
- **settings.py**: Centralized configuration management
- **logging_config.py**: Logging setup and management

### External Dependencies
- **GROQ API**: Large Language Model service
- **Yahoo Finance**: Financial data provider
- **DuckDuckGo**: News search service

### Output & Storage
- **analysis/**: Generated analysis reports
- **recommendations/**: Investment recommendations
- **logs/**: System execution logs

## Key Relationships

- **Configuration Centralization**: All agents depend on centralized settings
- **Logging Integration**: All components use centralized logging system
- **LLM Integration**: Multiple agents use GROQ for AI processing
- **Data Flow**: Clear dependency chain from input to output generation
