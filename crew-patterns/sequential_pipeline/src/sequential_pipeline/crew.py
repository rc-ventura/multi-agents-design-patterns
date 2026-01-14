from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task
from crewai.agents.agent_builder.base_agent import BaseAgent
from typing import List
from .tools.tools import pdf_parser, regex_extractor, summary_engine



@CrewBase
class SequentialPipeline():
    """SequentialPipeline crew"""

    agents: List[BaseAgent]
    tasks: List[Task]

    
    @agent
    def parser_agent(self) -> Agent:
        return Agent(
            config=self.agents_config['parser_agent'],
            verbose=True,
            tools=[pdf_parser]
        )

    @agent
    def extractor_agent(self) -> Agent:
        return Agent(
            config=self.agents_config['extractor_agent'],
            verbose=True,
            tools=[regex_extractor]
        )

    @agent
    def summarizer_agent(self) -> Agent:
        return Agent(
            config=self.agents_config['summarizer_agent'],
            verbose=True,
            tools=[summary_engine]
        )

   
    @task
    def parser_task(self) -> Task:
        return Task(
            config=self.tasks_config['parser_task'],
        )

    @task
    def extractor_task(self) -> Task:
        return Task(
            config=self.tasks_config['extractor_task'],
        )

    @task
    def summarizer_task(self) -> Task:
        return Task(
            config=self.tasks_config['summarizer_task'],
        )


    @crew
    def crew(self) -> Crew:
        """Creates the SequentialPipeline crew"""

        return Crew(
            agents=self.agents,
            tasks=self.tasks,
            process=Process.sequential,
            verbose=True,
        )
