# LangGraph Workflow Orchestration Diagram

```mermaid
flowchart TD
    Start([Start Analysis]) --> Input[Input: Stock Symbol<br/>+ Company Name]
    
    Input --> NewsAgent[News Agent<br/>Gather Company News<br/>Market Sentiment]
    Input --> DataAgent[Data Agent<br/>Retrieve Financial Data<br/>Market Metrics]
    
    NewsAgent --> NewsData[News Data<br/>+ Sentiment Analysis]
    DataAgent --> FinancialData[Financial Data<br/>+ Market Metrics]
    
    NewsData --> AnalystAgent[Analyst Agent<br/>Synthesize Information<br/>Generate Analysis]
    FinancialData --> AnalystAgent
    
    AnalystAgent --> Analysis[Comprehensive Analysis<br/>Financial Health<br/>Growth Trends<br/>Risk Factors]
    
    Analysis --> ExpertAgent[Financial Expert Agent<br/>Generate Recommendations<br/>Confidence Levels<br/>Target Prices]
    
    ExpertAgent --> Recommendation[Investment Recommendation<br/>BUY/SELL/HOLD<br/>+ Reasoning]
    
    Analysis --> Output1[Analysis.md<br/>Detailed Financial Analysis]
    Recommendation --> Output2[Recommendation.md<br/>Investment Decision]
    
    Output1 --> End([Analysis Complete])
    Output2 --> End
    
    style Start fill:#e1f5fe
    style End fill:#c8e6c9
    style NewsAgent fill:#fff3e0
    style DataAgent fill:#fff3e0
    style AnalystAgent fill:#f3e5f5
    style ExpertAgent fill:#e8f5e8
    style NewsData fill:#e8faf5
    style FinancialData fill:#e8faf5
    style Analysis fill:#fce4ec
    style Recommendation fill:#e0f2f1
```

## Workflow Description

### Phase 1: Data Collection
- **News Agent**: Searches for company-related news, press releases, and market updates
- **Data Agent**: Retrieves financial statements, market data, and performance metrics

### Phase 2: Information Synthesis
- **Analyst Agent**: Combines news and financial data to create comprehensive analysis
- **Output**: Financial health assessment, growth trends, and risk factors

### Phase 3: Recommendation Generation
- **Financial Expert Agent**: Processes analysis to generate investment recommendations
- **Output**: BUY/SELL/HOLD decision with confidence levels and target prices

### Phase 4: Report Generation
- **Analysis.md**: Detailed financial and contextual analysis report
- **Recommendation.md**: Investment recommendation with reasoning and strategy

## Key Features

- **Parallel Processing**: News and Data agents work simultaneously
- **Sequential Analysis**: Analyst and Expert agents process in sequence
- **Structured Output**: Consistent Markdown report generation
- **Data Flow**: Clear information passing between agents
