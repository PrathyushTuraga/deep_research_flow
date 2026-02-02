# Changelog

All notable changes to the Deep Research Flow project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

---

## [0.2.0] - Enhanced Edition (Current Version)

### Added

#### 1. **Configuration Management System**
   - **New file**: `config.yaml` - Centralized configuration for entire project
   - **Externalized parameters**:
     * LLM model and base URL (`ollama/granite4`, `http://localhost:11434`)
     * Embedding model settings (`nomic-embed-text`)
     * File paths (user preferences, output reports)
     * Flow settings (tracing, flow ID, testing mode)
     * Crew settings (memory, verbose, process type)
     * Research parameters (retries, timeout)
     * UI colors and behavior
   - **Location**: Project root (`config.yaml`)
   - **Benefits**: Easy model swapping, no code changes needed for configuration

#### 2. **Streamlit Web Interface** (Yet to be developed)
   - **New file**: `streamlit_app.py` in project root
   - **Features**:
     * Browser-based chatbot interface
     * Real-time output streaming
     * Interactive chat history
     * Session state management
     * Clean, modern UI with colored sections
   - **Run command**: `streamlit run streamlit_app.py`
   - **Benefits**: User-friendly alternative to CLI

#### 3. **Enhanced Requirements Management**
   - **New file**: `requirements.txt` for conda environments
   - **Includes**:
     * Core dependencies: `crewai`, `crewai_tools`, `litellm`
     * Data tools: `pandas`, `matplotlib`, `seaborn`
     * LLM integration: `langchain-ollama`, `langchain-community`
     * Web interface: `streamlit`
     * Dev tools: `ipython`, `jupyter`
   - **Benefits**: One-command dependency installation

#### 4. **Comprehensive Documentation**
   - **Enhanced README.md**:
     * Detailed project explanation with architecture diagrams
     * Agent roles and responsibilities
     * Task workflow descriptions
     * Guardrails explanation
     * Tools and capabilities
     * System requirements (hardware + software)
     * Cross-platform installation guides
     * Configuration deep dive
     * Customization examples
     * Troubleshooting section
     * Development guide
   - **Enhanced CHANGELOG.md**:
     * Semantic versioning
     * Detailed feature descriptions
     * Migration guides
     * Breaking changes documentation
     * Technical details for each change
   - **.gitignore** file:
     * Prevents PII commits (user_preference.txt)
     * Ignores generated reports
     * Excludes virtual environments
     * Blocks IDE-specific files

#### 5. **Enhanced Agent Definitions**
   - **File**: `config/agents.yaml`
   - **Improvements**:
     * More detailed backstories for each agent
     * Specific expertise areas (PhD, 10+ years experience, etc.)
     * Clear success criteria in goals
     * Edge case handling (bias detection, misinformation, etc.)
     * Professional personas with credentials
   - **Agents enhanced**:
     * Research Planner - PhD in information science
     * Topic Researcher - 10+ years investigative experience
     * Fact Checker - Journalism & peer review background
     * Report Writer - 15+ years research writing experience

#### 6. **Enhanced Task Descriptions**
   - **File**: `config/tasks.yaml`
   - **Improvements**:
     * More comprehensive research planning requirements
     * Detailed expected outputs with numbered criteria
     * Better fact-checking guidelines
     * Explicit citation requirements
     * Success criteria for each task
     * Structured output formats
   - **Tasks enhanced**:
     * `create_research_plan` - Now requires 3-5 main + 2-4 secondary topics
     * `research_main_topics` - Cross-verification across 3+ sources
     * `validate_main_topics` - Source credibility ratings
     * `write_final_report` - Mandatory sections (Summary, Insights, Citations)

#### 7. **Warnings Suppression**
   - **Implementation**: `import warnings; warnings.filterwarnings("ignore")`
   - **Locations**:
     * Top of `src/deep_research_flow/main.py`
     * Top of `src/deep_research_flow/crews/deep_research_crew/crew.py`
   - **Benefits**: Cleaner console output, better user experience

#### 8. **Flow Visualization Support**
   - **Command**: `crewai flow plot`
   - **Functionality**: Generates interactive flow diagram
   - **Shows**:
     * All flow states and transitions
     * Decision points and routing logic
     * Agent interactions
     * Task dependencies
     * Parallel execution paths
   - **Benefits**: Visual debugging, architecture understanding

---

### Fixed

#### 1. **User Input Visibility Issue**
   - **Problem**: User prompts were not visible before input
   - **Root cause**: Inline prompts in `input()` function
   - **Solution**: Separated `print()` statements before `input()`
   - **Affected methods**:
     * `start_conversation()` - Initial query input
     * `clarify_query()` - Clarification input
   - **Code changes**:
     ```python
     # Before (broken):
     self.state.user_query = input("What would you like to know?\n>> ")
     
     # After (fixed):
     print("What would you like to know?")
     self.state.user_query = input(">> ")
     ```

#### 2. **PII Removal from Repository**
   - **Files cleaned**:
     * `knowledge/user_preference.txt`
       - Changed from: "User name is John Dev" (PII)
       - Changed to: "User name is [Your Name]" (placeholder)
       - Updated all fields to placeholders
     * `pyproject.toml`
       - Changed from: Real author info
       - Changed to: "Deep Research Flow Team" / "contact@example.com"
   - **Benefits**: Safe for public GitHub repositories

#### 3. **Configuration Loading Robustness**
   - **Enhancement**: Added fallback config.yaml search paths
   - **Implementation**:
     ```python
     config_path = Path(__file__).resolve().parent.parent.parent / "config.yaml"
     if not config_path.exists():
         config_path = Path.cwd() / "config.yaml"
     ```
   - **Benefits**: Works from any execution directory

---

### Changed

#### 1. **Hardcoded Parameters → Configuration-Driven**

All hardcoded values moved to `config.yaml`:

| Parameter | Before (Hardcoded) | After (Config) |
|-----------|-------------------|----------------|
| LLM Model | `ollama/granite4` | `config["llm"]["model"]` |
| LLM Base URL | `http://localhost:11434` | `config["llm"]["base_url"]` |
| Embedding Model | `nomic-embed-text` | `config["embeddings"]["model"]` |
| Output File | `../research_report.md` | `config["paths"]["output_report"]` |
| User Preferences | Hardcoded path | `config["paths"]["user_preference"]` |
| Flow Tracing | `True` | `config["flow"]["tracing"]` |
| Flow ID | `our-deep-research_flow` | `config["flow"]["flow_id"]` |

#### 2. **Code Organization Improvements**
   - **Configuration loading**: Centralized at module import time
   - **Consistency**: All files use same config loading pattern
   - **Separation of concerns**: Configuration vs. logic cleanly separated
   - **Error handling**: Improved error messages with config paths

#### 3. **Documentation Structure**
   - **README.md**: Reorganized into logical sections
   - **CHANGELOG.md**: Adopted Keep a Changelog format
   - **Code comments**: Enhanced inline documentation

---

### Technical Details

#### Files Modified

1. **`src/deep_research_flow/main.py`**
   - Added: `warnings.filterwarnings("ignore")`
   - Added: Config loading with fallback paths
   - Fixed: User input prompt visibility
   - Updated: All LLM initializations to use `config["llm"]["model"]`
   - Updated: File paths to use `config["paths"]["output_report"]`
   - Updated: Flow tracing to use `config["flow"]["tracing"]`
   - Improved: Error messages with more context

2. **`src/deep_research_flow/crews/deep_research_crew/crew.py`**
   - Added: `warnings.filterwarnings("ignore")`
   - Added: Config loading with project root detection
   - Updated: LLM initialization to `LLM(model=config["llm"]["model"], base_url=config["llm"]["base_url"])`
   - Updated: Embedding configuration to use `config["embeddings"]["model"]`
   - Updated: Crew configuration to use config values
   - Added: Environment variable for embeddings model name
   - Improved: Config path error handling

3. **`src/deep_research_flow/crews/deep_research_crew/config/agents.yaml`**
   - Enhanced: All 4 agent definitions
   - Added: Detailed backstories with credentials
   - Improved: Goal descriptions with specific criteria
   - Added: Edge case handling in responsibilities
   - Expanded: Coverage of research scenarios

4. **`src/deep_research_flow/crews/deep_research_crew/config/tasks.yaml`**
   - Enhanced: All 6 task definitions
   - Added: Numbered expected outputs
   - Improved: Research planning requirements
   - Added: Explicit citation requirements
   - Expanded: Quality assessment criteria

5. **`knowledge/user_preference.txt`**
   - Removed: Personal information (PII)
   - Changed to: Placeholder format
   - Updated: All fields to `[Your ...]` format

6. **`pyproject.toml`**
   - Updated: Author name to "Deep Research Flow Team"
   - Updated: Email to "contact@example.com"
   - Maintained: Version and dependency structure

#### Files Added

1. **`config.yaml`**
   - Purpose: Centralized configuration
   - Sections: LLM, Embeddings, Paths, Flow, Crew, Research, UI
   - Benefits: One-stop configuration management

2. **`requirements.txt`**
   - Purpose: Conda environment dependencies
   - Contents: All required packages with comments
   - Benefits: Easy environment setup

3. **`README.md`** (Enhanced)
   - Purpose: Comprehensive project documentation
   - Sections: 20+ sections covering all aspects
   - Benefits: Professional onboarding experience

4. **`.gitignore`**
   - Purpose: Prevent unwanted files in git
   - Covers: Python, virtual envs, IDEs, reports, logs, user data
   - Benefits: Clean repository

5. **`CHANGELOG.md`** (This file)
   - Purpose: Version history tracking
   - Format: Keep a Changelog standard
   - Benefits: Clear upgrade paths

---

## Migration Guide

### For Existing Users (v0.1.0 → v0.2.0)

#### 1. Update Your Conda Environment

```bash
# Activate your environment
conda activate venv

# Install new dependencies
pip install -r requirements.txt

# Verify installation
python -c "import crewai, streamlit, yaml; print('✓ All dependencies installed')"
```

#### 2. Update User Preferences

**IMPORTANT**: Replace placeholder data with your information

```bash
# Edit the file
nano knowledge/user_preference.txt  # or vim, code, etc.

# Change from placeholders:
# User name is [Your Name].
# User is a [Your Profession/Role].

# To your actual data:
# User name is Jane Smith.
# User is a Data Scientist.
```

#### 3. Review and Customize Configuration

```bash
# Open config file
nano config.yaml

# Key settings to check:
# - llm.model: Change if using different Ollama model
# - embeddings.model: Must match your Ollama installation
# - flow.tracing: Set to false for production
# - crew.verbose: Set to false for quieter output
```

#### 4. Test Both Interfaces

```bash
# Test CLI
crewai run

# Test Web UI (if streamlit_app.py exists)
streamlit run streamlit_app.py

# Test visualization
crewai flow plot
```

#### 5. Verify PII Removal

```bash
# Check no personal info in tracked files
git status
git diff knowledge/user_preference.txt

# Should show placeholder format, not real data
```

### Breaking Changes

**None** - All changes are backward compatible. The system works the same way, just with:
- Better configuration options
- Improved documentation
- Enhanced agent capabilities
- Fixed user experience issues

### Rollback Instructions (If Needed)

```bash
# If you need to revert to v0.1.0
git checkout v0.1.0

# Or manually:
# 1. Remove config.yaml
# 2. Revert main.py and crew.py to hardcoded values
# 3. Update user_preference.txt with your data
```

---

## [0.1.0] - Initial Release

### Added
- Initial project structure with CrewAI Flow
- 4 specialized AI agents:
  * Research Planner
  * Topic Researcher
  * Fact Checker
  * Report Writer
- 6 coordinated tasks:
  * create_research_plan
  * research_main_topics (async)
  * research_secondary_topics (async)
  * validate_main_topics
  * validate_secondary_topics
  * write_final_report
- Basic flow logic:
  * Query analysis router
  * Simple answer path
  * Research path with crew execution
- Guardrails for report quality
- Memory and knowledge management
- Web search and scraping tools
- Basic documentation

### Features
- Intelligent query routing (SIMPLE vs RESEARCH)
- Parallel research execution
- Fact-checking and validation
- Automated report generation
- State persistence across sessions
- Local LLM support (Ollama)

---

## Future Enhancements

### Planned for v0.3.0
- [ ] **Docker Containerization**
  - Dockerfile for easy deployment
  - Docker Compose for multi-service setup
  - Pre-configured Ollama container

- [ ] **API Endpoint**
  - FastAPI REST endpoint
  - WebSocket for streaming responses
  - API documentation with Swagger/OpenAPI

- [ ] **Multiple Export Formats**
  - PDF export with formatting
  - DOCX export with styles
  - HTML export with CSS
  - JSON structured output

- [ ] **Research History & Analytics**
  - SQLite database for query history
  - Analytics dashboard
  - Research trends visualization
  - Performance metrics tracking

### Planned for v0.4.0
- [ ] **Custom Agent Configuration UI**
  - Web-based agent editor
  - Live agent testing
  - Prompt template library
  - Agent performance metrics

- [ ] **Cloud Storage Integration**
  - AWS S3 connector
  - Google Cloud Storage connector
  - Azure Blob Storage connector
  - Automatic backup/sync

- [ ] **Advanced Visualization Tools**
  - Research tree visualization
  - Knowledge graph display
  - Topic clustering maps
  - Citation network graphs

### Future Ideas (No Version Assigned)
- [ ] Multi-language support (Spanish, French, Chinese, etc.)
- [ ] Voice input/output integration
- [ ] Mobile app (React Native)
- [ ] Collaborative research features (multi-user)
- [ ] Custom LLM fine-tuning pipeline
- [ ] Benchmarking suite for model comparison
- [ ] Plugin system for community extensions
- [ ] Integration with research databases (PubMed, arXiv, etc.)
- [ ] Automated citation formatting (APA, MLA, Chicago, etc.)
- [ ] Research project templates
- [ ] Cost tracking for cloud API usage
- [ ] A/B testing framework for prompts
- [ ] Automated agent performance optimization

---

## Known Issues

### Current Limitations
1. **Streamlit App**: May not be included in all distributions
2. **Memory Usage**: Large research tasks can consume significant RAM
3. **Execution Time**: Complex queries may take 5-10 minutes
4. **Model Compatibility**: Some Ollama models may produce inconsistent outputs
5. **Web Search Rate Limits**: Free API may have usage restrictions

### Workarounds
1. **Streamlit**: Use CLI if web interface unavailable
2. **Memory**: Use smaller models or reduce research scope
3. **Time**: Enable `skip_task_evaluation` for faster execution
4. **Models**: Use recommended models (granite4, llama3.3)
5. **Rate Limits**: Add delays between requests if needed

---

## Version History Summary

| Version | Release Date | Key Features |
|---------|--------------|--------------|
| 0.2.0 | 2026-02-02 | Configuration system, enhanced docs, PII cleanup |
| 0.1.0 | 2026-01-25 | Initial release with multi-agent flow |

---

## Upgrade Notes

### From v0.1.0 to v0.2.0
- **Required**: Install new dependencies (`pip install -r requirements.txt`)
- **Required**: Update `knowledge/user_preference.txt` with your data
- **Recommended**: Review and customize `config.yaml`
- **Optional**: Test new visualization with `crewai flow plot`

### Database Migrations
None required for this version.

### API Changes
None - all changes are internal improvements.

---

## Contributing to Changelog

When contributing, please:
1. Add entries under "Unreleased" section
2. Categorize changes: Added, Changed, Deprecated, Removed, Fixed, Security
3. Include file paths for code changes
4. Add migration notes if needed
5. Update version numbers following Semantic Versioning

### Changelog Entry Template

```markdown
### Added
- **Feature Name**
  - Description of what was added
  - Location: `path/to/file.py`
  - Benefits: Why this helps users

### Fixed
- **Issue Name**
  - Problem: What was broken
  - Solution: How it was fixed
  - Affected: Which users/features
```

---

**Last Updated**: February 2, 2026  
**Maintained By**: Deep Research Flow Team  
**Changelog Format**: [Keep a Changelog](https://keepachangelog.com/)  
**Versioning**: [Semantic Versioning](https://semver.org/)
