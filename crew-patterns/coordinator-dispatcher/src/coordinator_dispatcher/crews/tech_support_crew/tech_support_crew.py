from typing import List

from crewai import Agent, Crew, Process, Task
from crewai.agents.agent_builder.base_agent import BaseAgent
from crewai.project import CrewBase, agent, crew, task
from coordinator_dispatcher.tools.tools import diagnostic_tool, knowledge_base

@CrewBase
class TechSupportCrew:
    """Tech Support Crew"""

    agents: List[BaseAgent]
    tasks: List[Task]

    agents_config = "config/agents.yaml"
    tasks_config = "config/tasks.yaml"

    @agent
    def tech_support_specialist(self) -> Agent:
        return Agent(
            config=self.agents_config["tech_support_specialist"],
            verbose=True,
            tools=[diagnostic_tool, knowledge_base]

        )

    @task
    def tech_support_task(self) -> Task:
        return Task(
            config=self.tasks_config["tech_support_task"], 
        )

    @crew
    def crew(self) -> Crew:
        """Creates the Tech Support Crew"""
    
        return Crew(
            agents=self.agents,  
            tasks=self.tasks,  
            process=Process.sequential,
            verbose=True,
        )
