# Data Flow Sequence Diagram

```mermaid
%% Add light shaded backgrounds using rect
sequenceDiagram
    participant User
    participant CLI as CLI/Web UI
    participant Orchestrator as LangGraph Orchestrator
    participant NewsAgent as News Agent
    participant DataAgent as Data Agent
    participant AnalystAgent as Analyst Agent
    participant ExpertAgent as Financial Expert Agent
    participant GROQ as GROQ LLM
    participant Yahoo as Yahoo Finance
    participant DDG as DuckDuckGo
    participant Output as Output Generator

    User->>CLI: Enter Stock Symbol (e.g., AAPL)
    CLI->>Orchestrator: Initialize Analysis Workflow
    
    rect rgb(245, 245, 255)
    par Parallel Data Collection
        Orchestrator->>NewsAgent: Gather Company News
        NewsAgent->>DDG: Search Company News
        DDG-->>NewsAgent: Return News Results
        NewsAgent->>GROQ: Analyze Sentiment
        GROQ-->>NewsAgent: Sentiment Analysis
        NewsAgent-->>Orchestrator: News Data + Sentiment
        
        Orchestrator->>DataAgent: Retrieve Financial Data
        DataAgent->>Yahoo: Get Market Data
        Yahoo-->>DataAgent: Financial Metrics
        DataAgent->>GROQ: Process Financial Data
        GROQ-->>DataAgent: Processed Financial Data
        DataAgent-->>Orchestrator: Financial Data + Metrics
    end
    end
    
    rect rgb(240, 255, 240)
    Orchestrator->>AnalystAgent: Synthesize Information
    AnalystAgent->>GROQ: Generate Comprehensive Analysis
    GROQ-->>AnalystAgent: Analysis Results
    AnalystAgent-->>Orchestrator: Comprehensive Analysis
    end
    
    rect rgb(255, 250, 240)
    Orchestrator->>ExpertAgent: Generate Investment Recommendation
    ExpertAgent->>GROQ: Create Investment Decision
    GROQ-->>ExpertAgent: Recommendation + Reasoning
    ExpertAgent-->>Orchestrator: Investment Recommendation
    end
    
    rect rgb(255, 245, 245)
    Orchestrator->>Output: Generate Final Reports
    Output->>Output: Create Analysis.md
    Output->>Output: Create Recommendation.md
    Output-->>Orchestrator: Report Files Generated
    end
    
    Orchestrator-->>CLI: Analysis Complete
    CLI-->>User: Display Results + File Locations

```

## Sequence Description

### 1. User Input Phase
- User provides stock symbol through CLI or Web UI
- System initializes LangGraph workflow orchestration

### 2. Parallel Data Collection
- **News Agent**: Searches DuckDuckGo for company news and analyzes sentiment using GROQ
- **Data Agent**: Retrieves financial data from Yahoo Finance and processes it using GROQ

### 3. Information Synthesis
- **Analyst Agent**: Combines news and financial data to generate comprehensive analysis
- Uses GROQ LLM for intelligent information synthesis

### 4. Recommendation Generation
- **Financial Expert Agent**: Processes analysis to create investment recommendations
- Generates confidence levels, target prices, and reasoning

### 5. Output Generation
- Creates structured Markdown reports (Analysis.md, Recommendation.md)
- Returns results to user interface

## Key Benefits

- **Parallel Processing**: News and financial data collection happen simultaneously
- **LLM Integration**: GROQ LLM used at multiple stages for intelligent processing
- **Structured Workflow**: Clear sequence of operations with defined inputs/outputs
- **Error Handling**: Each stage can handle failures gracefully
