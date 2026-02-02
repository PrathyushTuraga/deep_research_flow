#!/usr/bin/env python
import warnings
warnings.filterwarnings("ignore")

from pydantic import BaseModel
from crewai import LLM
from crewai.flow import Flow, listen, start, router, or_
from crewai.flow.persistence import persist
from deep_research_flow.crews.deep_research_crew.crew import ParallelDeepResearchCrew
import os
import yaml

# Load configuration
from pathlib import Path

config_path = Path(__file__).resolve().parent.parent.parent / "config.yaml"
if not config_path.exists():
    config_path = Path.cwd() / "config.yaml"
    
with open(config_path, "r", encoding="utf-8") as f:
    config = yaml.safe_load(f)

os.environ["CREWAI_TESTING"] = str(config["flow"]["testing_mode"]).lower()



# define the flow state
class ResearchState(BaseModel):
    user_query: str = ""
    ### START CODE HERE ###
    needs_research: bool = False
    research_report: str = ""
    final_answer: str = ""
    ### END CODE HERE ###

### START CODE HERE ###
# add persistence to the flow
@persist()
### END CODE HERE ###

class DeepResearchFlow(Flow[ResearchState]):
    # define the entrypoint
    ### START CODE HERE ###
    @start()
    ### END CODE HERE ###
    def start_conversation(self):
        """Entry point for the flow"""
        print("\n" + "="*80)
        print("🔍 Deep Research Flow Started")
        print("="*80)
        if self.state.user_query != "":
            print(f"\nI remember last time you wanted to know about:\n{self.state.user_query}\n")
        print("What would you like to know?")
        self.state.user_query = input(">> ")
        print("="*80)
        print(f"\nQuery received: \"{self.state.user_query}\"\n")

    # define the router
    ### START CODE HERE ###
    @router(start_conversation)
    ### END CODE HERE ###
    def analyze_query(self):
        """Router: Should trigger research?"""
        print("🤔 Analyzing query complexity...")
        
        ### START CODE HERE ###
        prompt = (# Write the prompt for the LLM to decide if the query is simple or requires research
                  ""
                  "Analyze this query and respond with exactly one word: SIMPLE or RESEARCH\n\n"
                  "SIMPLE: greetings, basic questions, well-known facts, context-based queries\n"
                  "RESEARCH: complex topics requiring comprehensive investigation, current events, detailed analysis, multi-faceted questions\n\n"
                  f"Query: \"{self.state.user_query}\"\n\n"
                  "Response (one word only):")
        ### END CODE HERE ###

        # define the llm for the decision 
        llm = LLM(model=config["llm"]["model"], base_url=config["llm"]["base_url"])
        # call the llm and save the result
        decision = llm.call(messages=prompt)

        if "RESEARCH" in decision.upper():
            self.state.needs_research = True
            print("📚 Complex query detected - initiating research process\n")
            return "RESEARCH"
        else:
            print("💬 Simple query detected - providing direct answer\n")
            return "SIMPLE"
    
    # define the simple answer task (no research needed)
    @listen("SIMPLE")
    def simple_answer(self):
        """LLM: Direct answer for simple queries"""
        print("✨ Generating direct answer...\n")
        
        ### START CODE HERE ###
        prompt = (# Write the missing part of the query for the LLM
                 ""
                 "Provide a direct, helpful, and comprehensive answer to this query. "
                 "Be informative but concise.\n\n"
                 f"Query: \"{self.state.user_query}\"\n\n"
                 "Answer:"
                 )
        # set up the LLM
        llm = LLM(model=config["llm"]["model"], base_url=config["llm"]["base_url"])
        # call the llm with the prompt and save the result to the final_answer state variable
        self.state.final_answer = llm.call(messages=prompt)
        ### END CODE HERE ###

    # define the clarification task (if research is needed)
    ### START CODE HERE ###
    @listen("RESEARCH")
    #### END CODE HERE ###
    def clarify_query(self):
        """LLM: Clarification before research"""
        print("🔍 Reviewing query for research clarity...\n")
        
        # write the prompt to decide if the query is clear enough
        prompt = ("Review this research query and determine if it's clear enough "
                 "for comprehensive research.\n\n"
                 "Respond in one of these formats:\n"
                 "- If clear and specific: \"PROCEED\"\n"
                 "- If needs clarification: \"CLARIFY: [specific questions to ask the user]\"\n\n"
                 f"Query: \"{self.state.user_query}\"\n\n"
                 "Response:"
                 )
        # define the llm and call it with the prompt
        llm = LLM(model=config["llm"]["model"], base_url=config["llm"]["base_url"])
        response = llm.call(messages=prompt)

        # if the query is not clear, ask the user for clarification
        if "PROCEED" not in response:
            clarification_needed = response.replace("CLARIFY:", "").strip()
            print("\n" + "="*80)
            print("❓ CLARIFICATION NEEDED")
            print("="*80)
            print(clarification_needed)
            print("="*80)
            print("\nPlease provide more details:")
            additional_info = input(">> ")
            print("="*80 + "\n")
            # update the user_query state variable with the additional information
            self.state.user_query += f"\n\nAdditional context: {additional_info}"
    
    # define the research execution task
    ### START CODE HERE ###
    @listen("clarify_query")
    ### END CODE HERE ###
    def execute_research(self):
        """Execute the Deep Research Crew"""
        print("🚀 Executing deep research crew...")
        print(f"🔍 Researching: \"{self.state.user_query}\"\n")

        # define the crew
        research_crew = ParallelDeepResearchCrew()

        ### START CODE HERE ###

        # kickoff the crew with the user query as input
        result = research_crew.crew().kickoff(
            # use the value in the user_query state variable as the input
            inputs={"user_query": self.state.user_query}
        )

        # update the research_report state variable with the crew's output (use the `raw` attribute)
        self.state.research_report = result.raw
        ### END CODE HERE ###
        
        print("\n✅ Research completed successfully!\n")

        
    # define the task to save and summarize the report
    ### START CODE HERE ###
    @listen(execute_research)
    ### END CODE HERE ###
    def save_report_and_summarize(self):
        """
        Save the final research report to a local markdown file
        """
        print("📄 Saving research report...")
        # save the report
        try:
            with open(config["paths"]["output_report"], "w", encoding="utf-8") as f:
                ### START CODE HERE ###
                # write the content of the research_report state variable to the file
                f.write(self.state.research_report)
                ### END CODE HERE ###
            print(f"✅ Report saved to: {config['paths']['output_report']}\n")
        except Exception as e:
            print(f"❌ Failed to save report: {str(e)}\n")
        
        # summarize the report
        # define the LLM and and write the prompt
        print("📝 Creating summary...")
        llm = LLM(model=config["llm"]["model"], base_url=config["llm"]["base_url"])
        prompt = ("Summarize the following research report into a one paragraph, informative answer:\n\n"
                  f"Report: \"{self.state.research_report}\"\n\n"
                 )
        # update the final_answer state variable with the summary from the LLM call
        summary = llm.call(messages=prompt)
        self.state.final_answer = ("This is a summary of the final answer:\n\n" 
                                    f"{summary}\n\n"
                                    f"A full report has been saved to {config['paths']['output_report']}."
                                    )
        print("✅ Summary created\n")
    
    # define the final answer task
    @listen(or_("simple_answer", "save_report_and_summarize"))
    def return_final_answer(self):
        """Return the final answer to the user"""
        print("\n" + "="*80)
        print("📝 FINAL ANSWER")
        print("="*80)
        print(f"Query: \"{self.state.user_query}\"")
        print("="*80)
        print(self.state.final_answer)
        print("="*80)
        print("\n✨ Deep Research Flow completed!")
        print("="*80 + "\n")

    

def kickoff():
    ### START CODE HERE ###
    # instantiate the DeepResearchFlow with tracing enabled
    deep_research_flow = DeepResearchFlow(tracing=config["flow"]["tracing"])
    ### END CODE HERE ###
    
    # kickoff the flow with a custom id, so you can persist the state
    deep_research_flow.kickoff(inputs={"id": config["flow"]["flow_id"]})
    

def plot():
    deep_research_flow = DeepResearchFlow()
    deep_research_flow.plot()


if __name__ == "__main__":
    kickoff()