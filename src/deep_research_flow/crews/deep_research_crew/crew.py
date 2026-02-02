import warnings
warnings.filterwarnings("ignore")

import os
import yaml
from crewai import LLM
from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task, after_kickoff

# Load configuration
import sys
from pathlib import Path

# Find project root (where config.yaml is located)
current_file = Path(__file__).resolve()
project_root = current_file.parent.parent.parent.parent.parent
config_path = project_root / "config.yaml"

if not config_path.exists():
    # Fallback: try to find config.yaml in current working directory
    config_path = Path.cwd() / "config.yaml"
    if not config_path.exists():
        raise FileNotFoundError(f"config.yaml not found. Expected at: {project_root / 'config.yaml'}")

with open(config_path, "r") as f:
    config = yaml.safe_load(f)

llm = LLM(model=config["llm"]["model"], base_url=config["llm"]["base_url"])

# for embedder
os.environ["EMBEDDINGS_OLLAMA_MODEL_NAME"] = config["embeddings"]["model"]

# import the guardrail
#from deep_research_flow.crews.deep_research_crew.guardrails.guardrails import write_report_guardrail

try:
    from deep_research_flow.crews.deep_research_crew.guardrails.guardrails import write_report_guardrail
except ModuleNotFoundError:
    from .guardrails.guardrails import write_report_guardrail

from crewai.knowledge.source.text_file_knowledge_source import TextFileKnowledgeSource

from crewai_tools import WebsiteSearchTool, ScrapeWebsiteTool
os.environ["OPENAI_API_KEY"] = "dummy"

exa_search_tool = WebsiteSearchTool(
    config=dict(
        llm=dict(
            provider="ollama",
            config=dict(
                model=config["llm"]["model"].split("/")[-1],
                api_key=""
            ),
        ),
        embedder=dict(
            provider="ollama",
            config=dict(
                model_name=config["embeddings"]["model"],
                api_key="",
                task_type="RETRIEVAL_DOCUMENT",
            ),
        ),
    )
)

scrape_website_tool = ScrapeWebsiteTool()

@CrewBase
class ParallelDeepResearchCrew:
    """ParallelDeepResearchCrew crew"""
    # Define the agents
    @agent
    def research_planner(self) -> Agent:
        return Agent(
            config=self.agents_config["research_planner"],
            llm=llm,
            verbose=True
        )

    @agent
    def topic_researcher(self) -> Agent:
        return Agent(
            config=self.agents_config["topic_researcher"],
            # Define the tools
            tools=[exa_search_tool, scrape_website_tool],
            llm=llm,
            verbose=True
        )
    
    @agent
    def fact_checker(self) -> Agent:
        return Agent(
            config=self.agents_config["fact_checker"],
            tools=[exa_search_tool, scrape_website_tool],
            llm=llm,
            verbose=True
        )
    
    @agent
    def report_writer(self) -> Agent:
        return Agent(
            config=self.agents_config["report_writer"],
            llm=llm,
            verbose=True
        )

    @task
    def create_research_plan(self) -> Task:
        return Task(
            config=self.tasks_config["create_research_plan"],
            llm=llm,
        )

    # Define the tasks
    @task
    def research_main_topics(self) -> Task:
        return Task(
            config=self.tasks_config["research_main_topics"],
            async_execution=True,
        )
    
    @task
    def research_secondary_topics(self) -> Task:
        return Task(
            config=self.tasks_config["research_secondary_topics"],
            async_execution=True,
        )
    
    @task
    def validate_main_topics(self) -> Task:
        return Task(
            config=self.tasks_config["validate_main_topics"],
        )
    
    @task
    def validate_secondary_topics(self) -> Task:
        return Task(
            config=self.tasks_config["validate_secondary_topics"],
        )
    
    @task
    def write_final_report(self) -> Task:
        return Task(
            config=self.tasks_config["write_final_report"],
            # add the guardrail
            guardrails=[write_report_guardrail],
            markdown=True,
            output_file='report.md'
        )

    # Define the crew
    @crew
    def crew(self) -> Crew:
        """Creates the ParallelDeepResearchCrew crew"""
        return Crew(
            agents=self.agents,  # Automatically created by the @agent decorator
            tasks=self.tasks,  # Automatically created by the @task decorator
            # Set the memory to True so the crew remembers previous interactions
            memory=config["crew"]["memory"],  
            embedder={
                "provider": "ollama",
                "config": {
                    "model": config["embeddings"]["model"],
                    "api_key": ""
                }
            },
            # Define the sequential process
            process=Process.sequential,
            tracing=config["flow"]["tracing"],
            verbose=config["crew"]["verbose"],
            skip_task_evaluation=config["crew"].get("skip_task_evaluation", False),
            knowledge_sources=[TextFileKnowledgeSource(
                file_paths=["user_preference.txt"]
            )]
        )
