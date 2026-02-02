# Deep Research Flow
## Multi-Agent AI Research System Powered by CrewAI

A **completely open-source**, **locally-runnable** multi-agent AI research workflow that conducts comprehensive research on user queries using **free LLM models** and **free web search APIs**. Built with CrewAI's agentic framework, this system orchestrates multiple AI agents working in parallel to deliver high-quality research reports.

---

## 🌟 What This Project Does

Deep Research Flow is an intelligent research assistant that automatically:

1. **Analyzes user queries** to determine complexity (simple answer vs. deep research needed)
2. **Plans research strategy** by breaking down complex queries into main and secondary topics
3. **Conducts parallel research** using multiple specialized AI agents
4. **Validates information** through fact-checking and cross-referencing
5. **Generates comprehensive reports** with citations, insights, and recommendations

The system uses a **CrewAI Flow** architecture with intelligent routing, parallel execution, and quality guardrails to ensure accurate, well-structured research outputs.

---

## 🎯 Why This Project Is Useful

If you're wondering:

- *How can I build autonomous AI agents that work together?*
- *What does a real-world multi-agent system look like?*
- *How do I implement research workflows with LLMs?*
- *Can I run advanced AI agents locally without expensive API costs?*

**This project answers those questions** with a fully functional, production-ready example.

### Key Benefits

✅ **100% Open Source** - Use any Ollama model (Llama, Mistral, Granite, etc.)  
✅ **Free Web Search** - No paid API keys required for research capabilities  
✅ **Cross-Platform** - Runs on Windows, macOS, and Linux  
✅ **Local Execution** - Works on regular home PCs (no cloud required)  
✅ **Educational** - Learn CrewAI flows, agent orchestration, and RAG patterns  
✅ **Production-Ready** - Includes guardrails, error handling, and quality checks

---

## 🏗️ Project Architecture

### CrewAI Flow Structure

The project implements a sophisticated **CrewAI Flow** with conditional routing and parallel execution:

```
User Query
    │
    ├─→ Analyze Query (Router)
    │       ├─→ SIMPLE → Direct LLM Answer → Final Answer
    │       └─→ RESEARCH → Clarify Query
    │                          │
    │                          ├─→ Execute Research (Crew Kickoff)
    │                          │       │
    │                          │       ├─→ Research Planner (Sequential)
    │                          │       │       │
    │                          │       │       ├─→ Research Main Topics (Async) ──┐
    │                          │       │       │                                   │
    │                          │       │       └─→ Research Secondary Topics (Async)│
    │                          │       │                                            │
    │                          │       └─→ Validate Main Topics ←──────────────────┘
    │                          │                  │
    │                          │                  ├─→ Validate Secondary Topics
    │                          │                  │
    │                          │                  └─→ Write Final Report (Guardrails)
    │                          │
    │                          └─→ Save Report & Summarize → Final Answer
    │
    └─→ Return Final Answer (Display)
```

### Visualize the Flow

You can generate a visual diagram of the entire flow:

```bash
crewai flow plot
```

This creates an interactive visualization showing all flow paths, decision points, and agent interactions.

---

## 🤖 Agents & Their Roles

The system employs **4 specialized AI agents**, each with distinct expertise:

### 1. **Research Planner**
- **Role**: Strategic research planning
- **Expertise**: Information science, research methodology
- **Responsibilities**:
  - Analyze user query complexity
  - Break down into MAIN (core) and SECONDARY (supporting) topics
  - Identify key questions and research priorities
  - Create comprehensive research roadmap

### 2. **Topic Researcher** (Used for both Main & Secondary topics)
- **Role**: Information gathering and investigation
- **Expertise**: Online research, source evaluation, fact verification
- **Tools**: Web search, website scraping
- **Responsibilities**:
  - Search multiple credible sources
  - Gather comprehensive, up-to-date information
  - Cross-verify facts across 3+ independent sources
  - Properly cite all sources with URLs and dates

### 3. **Fact Checker & Quality Assurance Specialist**
- **Role**: Information validation and quality control
- **Expertise**: Fact-checking, bias detection, peer review
- **Tools**: Web search, source verification
- **Responsibilities**:
  - Verify accuracy and consistency
  - Identify contradictions or misinformation
  - Rate source credibility
  - Flag gaps in research coverage
  - Detect hallucinated content

### 4. **Report Writer**
- **Role**: Synthesis and communication
- **Expertise**: Technical writing, information synthesis
- **Responsibilities**:
  - Create well-structured final report
  - Synthesize findings from all validated research
  - Include proper citations and multiple perspectives
  - Provide actionable insights and recommendations
  - Ensure clarity for target audience

---

## 📋 Tasks & Workflow

The crew executes **6 coordinated tasks**:

### Sequential Phase
1. **create_research_plan** (Research Planner)
   - Analyzes query and creates research strategy
   - Outputs: Main topics, secondary topics, key questions, priorities

### Parallel Phase (Async Execution)
2. **research_main_topics** (Topic Researcher)
   - Gathers comprehensive data for core topics
   - Runs in parallel with secondary research

3. **research_secondary_topics** (Topic Researcher)
   - Collects supporting information
   - Runs in parallel with main research

### Validation Phase (Sequential)
4. **validate_main_topics** (Fact Checker)
   - Verifies main topic data accuracy
   - Outputs: Quality assessment, verified facts, source ratings

5. **validate_secondary_topics** (Fact Checker)
   - Validates secondary topic data
   - Ensures consistency with main research

### Report Generation Phase
6. **write_final_report** (Report Writer)
   - Creates comprehensive markdown report
   - **Guardrails Applied**: Must include Summary, Insights, and Citations sections
   - Auto-saves to `research_report.md`

---

## 🛡️ Guardrails & Quality Assurance

The system implements **strict quality guardrails** to ensure report completeness:

```python
# Guardrail Checks (guardrails.py)
✓ Summary section must be present
✓ Insights or Recommendations section required
✓ Citations or References section mandatory
✗ Report rejected if any section missing → Agent retries
```

These guardrails prevent incomplete or low-quality outputs, ensuring every report meets professional standards.

---

## 🧠 Memory & Knowledge Management

### Agent Memory
- **Short-term memory**: Remembers context within current session
- **Long-term memory**: Stores insights across sessions using embeddings
- **Entity memory**: Tracks entities and relationships mentioned in queries

### Knowledge Sources
- **User Preferences**: Personalized context from `knowledge/user_preference.txt`
- **RAG Integration**: Embeds user preferences into agent context
- **Embeddings**: Uses `nomic-embed-text` for semantic search

---

## 🔧 Tools & Capabilities

### Built-in Tools
1. **WebsiteSearchTool** (Exa/Free API)
   - Searches the web for relevant information
   - No API key required
   - Configurable LLM and embedder

2. **ScrapeWebsiteTool**
   - Extracts full content from websites
   - Used for deep-dive research

### Tool Configuration
Tools are configured to use local Ollama models:
```yaml
llm:
  provider: ollama
  model: granite4
  
embedder:
  provider: ollama
  model: nomic-embed-text
```

---

## 💻 System Requirements

### Hardware
- **RAM**: 8GB minimum (16GB recommended)
- **Storage**: 10GB free space for models
- **CPU**: Multi-core processor (for parallel processing)
- **GPU**: Optional (speeds up inference)

### Software
- **Python**: 3.10 to 3.13 (3.11 recommended)
- **Conda** or **Miniconda**
- **Ollama**: For running local LLMs

### Operating Systems
✅ **Windows** (10/11)  
✅ **macOS** (Intel & Apple Silicon)  
✅ **Linux** (Ubuntu 20.04+, Debian, Fedora, etc.)

---

## 🚀 Installation & Setup

### 1. Install Ollama and Models

#### Install Ollama
Visit [ollama.com](https://ollama.com/) and download for your OS.

#### Pull Required Models
```bash
# LLM model (choose one or use multiple)
ollama pull granite4    # (IBM's open model). Or you can use any other model like gpt-oss

# Embedding model (required)
ollama pull nomic-embed-text
```

### 2. Create Conda Environment

```bash
# Create environment with Python 3.11
conda create -n venv python=3.11

# Activate environment
conda activate venv
```

### 3. Clone Repository & Install Dependencies

```bash
# Clone the repository
git clone <your-repo-url>
cd deep_research_flow

# Install all dependencies
pip install -r requirements.txt
```

### 4. Configure User Preferences

Edit `knowledge/user_preference.txt` to personalize agent responses:

```text
User name is [Your Name].
User is a [Your Profession/Role].
User is interested in [Your Interests].
User is based in [Your Location].
```

**Example:**
```text
User name is John Dev.
User is a AI Engineer.
User is interested in AI agents.
User is based in Los Angeles, California.
```

### 5. Customize Configuration (Optional)

Edit `config.yaml` to change models, paths, or behavior:

```yaml
llm:
  model: ollama/granite4    # Change to llama3.3, mistral, etc.
  base_url: http://localhost:11434
  
embeddings:
  model: nomic-embed-text   # Or use other embedding models
  
paths:
  output_report: research_report.md
  
flow:
  tracing: true             # Enable/disable flow tracing
  testing_mode: true        # Set to false for production
```

---

## 📖 Usage

### Option 1: Terminal Interface (CLI)

```bash
# Activate conda environment
conda activate venv

# Generate interactive flow diagram
crewai flow plot

# Run the flow
crewai run
```

**Example Session:**
```
================================================================================
🔍 Deep Research Flow Started
================================================================================
What would you like to know?
>> What are the latest developments in quantum computing?

🤔 Analyzing query complexity...
📚 Complex query detected - initiating research process

🔍 Reviewing query for research clarity...
✅ Query is clear and ready for research

🚀 Executing deep research crew...
[Agent outputs...]
✅ Research completed successfully!

📄 Saving research report...
✅ Report saved to: research_report.md
```

### Option 2: Streamlit Web Interface

**Note**: If `streamlit_app.py` exists in your version:

```bash
# Activate conda environment
conda activate venv

# Run the Streamlit app
streamlit run streamlit_app.py
```

Web interface opens at `http://localhost:8501` with chat-style interactions. (streamlit uses 8501 as default port if open)


This creates a visual representation showing:
- All flow states and transitions
- Decision points and routing logic
- Agent interactions and task dependencies
- Parallel execution paths

**Why Use This**: Helps understand the system architecture and debug complex flows.

---

## 📁 Project Structure

```
deep_research_flow/
│
├── config.yaml                       # Central configuration file
├── requirements.txt                   # Python dependencies
├── pyproject.toml                     # Project metadata & scripts
├── README.md                          # This file
├── CHANGELOG.md                       # Version history
├── .gitignore                         # Git ignore rules
│
├── knowledge/
│   └── user_preference.txt           # User personalization data
│
├── src/deep_research_flow/
│   ├── __init__.py
│   ├── main.py                       # Flow logic & orchestration
│   ├── utils.py                      # Utility functions
│   │
│   ├── crews/deep_research_crew/
│   │   ├── __init__.py
│   │   ├── crew.py                   # Crew definition & agent setup
│   │   │
│   │   ├── config/
│   │   │   ├── agents.yaml           # Agent configurations
│   │   │   └── tasks.yaml            # Task definitions
│   │   │
│   │   └── guardrails/
│   │       ├── __init__.py
│   │       └── guardrails.py         # Quality validation rules
│   │
│   └── tools/
│       └── __init__.py               # Custom tools (if any)
│
├── research_report.md                 # Generated reports (gitignored)
└── report.md                          # Alternative report output
```

---

## ⚙️ Configuration Deep Dive

### config.yaml Breakdown

```yaml
# LLM Configuration - Change models here
llm:
  model: ollama/granite4              # Format: provider/model
  base_url: http://localhost:11434    # Ollama server URL
  temperature: 0.7                     # Creativity level (0-1)

# Embeddings for Memory & RAG
embeddings:
  model: nomic-embed-text             # Embedding model
  provider: ollama

# File Paths
paths:
  user_preference: knowledge/user_preference.txt
  output_report: research_report.md

# Flow Behavior
flow:
  tracing: true                       # Log flow execution
  flow_id: our-deep-research-flow     # Unique flow identifier
  testing_mode: true                  # Skip strict evaluations

# Crew Settings
crew:
  memory: true                        # Enable agent memory
  verbose: true                       # Show detailed logs
  process: sequential                 # Task execution mode
  skip_task_evaluation: true          # Speed up for local models

# Research Parameters
research:
  max_retries: 3                      # Retry failed tasks
  timeout_seconds: 300                # 5-minute timeout
```

---

## 🎨 Customization Guide

### Change LLM Models

#### Use Different Ollama Models
```yaml
# In config.yaml
llm:
  model: ollama/llama3.3     # Meta's Llama 3.3
  # OR
  model: ollama/mistral      # Mistral 7B
  # OR
  model: ollama/qpt-oss      # OpenAI's gpt-oss:20B
```

#### Use Cloud APIs (OpenAI, Anthropic, etc.)
```yaml
llm:
  model: gpt-4o              # OpenAI GPT-4
  # OR
  model: claude-3-opus       # Anthropic Claude
```

Then set API keys:
```bash
export OPENAI_API_KEY="your-key"
export ANTHROPIC_API_KEY="your-key"
```

### Modify Agent Behavior

#### Edit Agent Personas
File: `src/deep_research_flow/crews/deep_research_crew/config/agents.yaml`

```yaml
research_planner:
  role: Research Planner
  goal: >
    [Customize the goal - what should this agent achieve?]
  backstory: >
    [Customize expertise - what makes this agent qualified?]
```

#### Adjust Task Requirements
File: `src/deep_research_flow/crews/deep_research_crew/config/tasks.yaml`

```yaml
create_research_plan:
  description: >
    [Customize what the task should do]
  expected_output: >
    [Customize what output format/content is required]
```

### Add Custom Tools

Create new tools in `src/deep_research_flow/tools/`:

```python
# custom_tool.py
from crewai_tools import BaseTool

class MyCustomTool(BaseTool):
    name: str = "My Custom Tool"
    description: str = "What this tool does"
    
    def _run(self, argument: str) -> str:
        # Tool logic here
        return result
```

Then add to agents in `crew.py`:
```python
@agent
def topic_researcher(self) -> Agent:
    return Agent(
        config=self.agents_config["topic_researcher"],
        tools=[exa_search_tool, scrape_website_tool, my_custom_tool],
        llm=llm,
    )
```

### Customize Guardrails

Edit `src/deep_research_flow/crews/deep_research_crew/guardrails/guardrails.py`:

```python
def write_report_guardrail(output):
    # Add custom checks
    if "my_required_section" not in output.lower():
        return (False, "Report must include my custom section")
    
    # Add length requirements
    if len(output) < 1000:
        return (False, "Report must be at least 1000 characters")
    
    return (True, output)
```

---

## 🔍 How It Works: Technical Details

### Flow Execution Lifecycle

1. **State Initialization**
   ```python
   class ResearchState(BaseModel):
       user_query: str = ""
       needs_research: bool = False
       research_report: str = ""
       final_answer: str = ""
   ```

2. **Entry Point**
   ```python
   @start()
   def start_conversation(self):
       # Captures user input
       self.state.user_query = input(">> ")
   ```

3. **Decision Router**
   ```python
   @router(start_conversation)
   def analyze_query(self):
       # LLM decides: SIMPLE or RESEARCH
       decision = llm.call(messages=prompt)
       return "SIMPLE" if "SIMPLE" in decision else "RESEARCH"
   ```

4. **Conditional Paths**
   - **SIMPLE Path**: Direct LLM answer → Final output
   - **RESEARCH Path**: Multi-agent crew → Validation → Report

5. **Crew Kickoff**
   ```python
   @listen("clarify_query")
   def execute_research(self):
       research_crew = ParallelDeepResearchCrew()
       result = research_crew.crew().kickoff(
           inputs={"user_query": self.state.user_query}
       )
       self.state.research_report = result.raw
   ```

6. **State Persistence**
   ```python
   @persist()
   class DeepResearchFlow(Flow[ResearchState]):
       # Flow remembers state across sessions
   ```

### Parallel Execution with CrewAI

Tasks marked with `async_execution=True` run in parallel:

```python
@task
def research_main_topics(self) -> Task:
    return Task(
        config=self.tasks_config["research_main_topics"],
        async_execution=True,  # Runs in parallel
    )

@task
def research_secondary_topics(self) -> Task:
    return Task(
        config=self.tasks_config["research_secondary_topics"],
        async_execution=True,  # Runs in parallel
    )
```

### Memory & RAG Integration

```python
# In crew.py
knowledge_sources=[TextFileKnowledgeSource(
    file_paths=["user_preference.txt"]
)]

# Embeddings configuration
embedder={
    "provider": "ollama",
    "config": {
        "model": "nomic-embed-text",
        "api_key": ""
    }
}
```

---

## 🐛 Troubleshooting

### Common Issues & Solutions

#### 1. "User input not visible" / Prompt doesn't show
**Fixed in v0.2.0** - Ensure you have the latest code with separate `print()` statements.

#### 2. "Ollama connection error"
```bash
# Solution: Start Ollama server
ollama serve

# Verify it's running
curl http://localhost:11434/api/tags
```

#### 3. "Config file not found"
```bash
# Solution: Run from project root
cd deep_research_flow
crewai run

# Or set config path explicitly
export CONFIG_PATH=/path/to/config.yaml
```

#### 4. "Import errors" / "ModuleNotFoundError"
```bash
# Solution: Reinstall dependencies
conda activate deep_research
pip install -r requirements.txt

# Or install crewai tools explicitly
pip install 'crewai[tools]'
```

#### 5. "Models not found" in Ollama
```bash
# Solution: Pull required models
ollama pull granite4
ollama pull nomic-embed-text

# List installed models
ollama list
```

#### 6. "Out of memory" errors
```bash
# Solution: Use smaller models
# In config.yaml:
llm:
  model: ollama/llama3.2:1b  # Smaller than granite4/llama3.3
```

#### 7. Slow execution / Long wait times
```bash
# Solutions:
# 1. Enable skip_task_evaluation in config.yaml
crew:
  skip_task_evaluation: true

# 2. Use faster models
llm:
  model: ollama/msitral:7b  # Fast 7B model

# 3. Reduce research scope in tasks.yaml
```

#### 8. "Guardrail failed" / Report rejected
Check your report includes:
- ✓ Summary section (## Summary or # Summary)
- ✓ Insights OR Recommendations section
- ✓ Citations OR References section

---

## 🧪 Development & Testing

### Run in Development Mode

```bash
# Enable verbose logging
# In config.yaml:
flow:
  tracing: true
crew:
  verbose: true
```

### Test Flow Paths

```bash
# Test simple query path
crewai run
>> Hello, how are you?

# Test research path
crewai run
>> What is causal inference?
```

### View Flow Diagram

```bash
crewai flow plot
```

### Debug Agent Behavior

Add print statements in `main.py`:
```python
def execute_research(self):
    print(f"DEBUG: Query = {self.state.user_query}")
    result = research_crew.crew().kickoff(...)
    print(f"DEBUG: Result length = {len(result.raw)}")
```

---

## 🌐 Deployment Options

### Local Deployment (Development)
```bash
crewai run  # CLI
streamlit run streamlit_app.py  # Web UI
```

### Docker Deployment (Recommended for Production)
```dockerfile
# Future enhancement - Docker support coming soon
# See CHANGELOG.md for planned features
```

### Cloud Deployment
- **AWS**: Lambda + API Gateway
- **Google Cloud**: Cloud Run
- **Azure**: Container Instances

**Note**: Requires cloud LLM APIs (OpenAI, Anthropic) for cloud deployment.

---

## 📊 Evaluation Metrics

The system tracks:
- **Query Classification Accuracy**: SIMPLE vs RESEARCH routing
- **Research Coverage**: Main + Secondary topics addressed
- **Fact-Checking Results**: Verified vs. Questionable information
- **Guardrail Pass Rate**: Reports meeting quality standards
- **Execution Time**: Per task and total flow

View metrics in verbose logs when `tracing: true`.

---

## 🤝 Contributing

We welcome contributions! Here's how:

1. **Fork the repository**
2. **Create a feature branch**
   ```bash
   git checkout -b feature/amazing-feature
   ```
3. **Make your changes**
   - Add new agents in `config/agents.yaml`
   - Add new tasks in `config/tasks.yaml`
   - Add new tools in `tools/`
4. **Test thoroughly**
   ```bash
   pytest  # When tests are added
   ```
5. **Commit and push**
   ```bash
   git commit -m "Add amazing feature"
   git push origin feature/amazing-feature
   ```
6. **Submit a pull request**

### Contribution Ideas
- [ ] New specialized agents (Data Analyst, Code Reviewer, etc.)
- [ ] Additional tools (Database search, API integration, etc.)
- [ ] Export formats (PDF, DOCX, HTML)
- [ ] Web UI enhancements
- [ ] Docker containerization
- [ ] Test coverage
- [ ] Documentation improvements

---

## 📄 License

**MIT License** - Free to use, modify, and distribute.

See `LICENSE` file for full details.

---

## 🙏 Acknowledgments

### Built With
- **[CrewAI](https://www.crewai.com/)** - Multi-agent framework
- **[Ollama](https://ollama.com/)** - Local LLM runtime
- **[Streamlit](https://streamlit.io/)** - Web interface (if included)
- **[Langchain](https://www.langchain.com/)** - LLM tooling

### Inspired By
- **DeepLearning.AI Course**: [Design, Develop and Deploy Multi-Agent Systems with CrewAI](https://learn.deeplearning.ai/courses/design-develop-and-deploy-multi-agent-systems-with-crewai/)
  - Course covers: Multi-agent design patterns, CrewAI flows, RAG integration, and production deployment

### Special Thanks
- CrewAI team for the amazing framework
- Ollama team for making local LLMs accessible
- DeepLearning.AI for educational resources
- Open-source community for tools and models

---

## 📞 Support & Resources

### Get Help
- **Issues**: Open a [GitHub Issue](your-repo-issues-url)
- **Discussions**: Join [GitHub Discussions](your-repo-discussions-url)
- **Documentation**: 
  - [CrewAI Docs](https://docs.crewai.com)
  - [Ollama Docs](https://docs.ollama.com)
  - [DeepLearning.AI Course](https://learn.deeplearning.ai/)

### Stay Updated
- **Star this repo** to get notified of updates
- **Watch releases** for new features
- **Follow the roadmap** in CHANGELOG.md

---

## 🗺️ Roadmap

See `CHANGELOG.md` for planned features and recent updates.

**Upcoming Features:**
- [ ] Docker containerization
- [ ] API endpoint for programmatic access
- [ ] Multiple export formats (PDF, DOCX)
- [ ] Research history and analytics
- [ ] Custom agent configuration UI
- [ ] Cloud storage integration (S3, GCS)
- [ ] Advanced visualization tools
- [ ] Benchmarking suite

---

## 📚 Learn More

### Recommended Reading
1. **CrewAI Flows**: [Official Guide](https://docs.crewai.com/en/concepts/flows)
2. **Multi-Agent Systems**: Research papers on agent collaboration
3. **RAG Architecture**: Retrieval-Augmented Generation patterns
4. **Prompt Engineering**: Effective LLM prompting techniques

### Related Projects
- [LangGraph](https://github.com/langchain-ai/langgraph) - Alternative agent framework
- [AutoGen](https://github.com/microsoft/autogen) - Microsoft's multi-agent system
- [Agency Swarm](https://github.com/VRSEN/agency-swarm) - OpenAI-based agent framework

---

**Happy Researching! 🚀**

*If you find this project useful, please give it a ⭐ on GitHub!*
