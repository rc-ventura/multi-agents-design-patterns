from typing import List

from crewai import Agent, Crew, Process, Task
from crewai.agents.agent_builder.base_agent import BaseAgent
from crewai.project import CrewBase, agent, crew, task
from coordinator_dispatcher.tools.tools import billing_system_db, invoice_generator

@CrewBase
class BillingCrew:
    """Billing Crew"""

    agents: List[BaseAgent]
    tasks: List[Task]

    agents_config = "config/agents.yaml"
    tasks_config = "config/tasks.yaml"

    @agent
    def billing_specialist(self) -> Agent:
        return Agent(
            config=self.agents_config["billing_specialist"],
            tools=[billing_system_db, invoice_generator],
            verbose=True
        )

    @task
    def billing_task(self) -> Task:
        return Task(
            config=self.tasks_config["billing_task"],  
        )

    @crew
    def crew(self) -> Crew:
        return Crew(
            agents=self.agents,  
            tasks=self.tasks,  
            process=Process.sequential,
            verbose=True,
        )
