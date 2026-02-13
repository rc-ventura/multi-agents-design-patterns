from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task
from crewai.agents.agent_builder.base_agent import BaseAgent
from typing import List
from .tools.tools import code_security_scanner, style_checker, complexity_analyzer


@CrewBase
class ParallelFanOut():
    """ParallelFanOut crew implementing the Fan-Out/Fan-In pattern for code review"""

    agents: List[BaseAgent]
    tasks: List[Task]

    
    @agent
    def security_auditor(self) -> Agent:
        return Agent(
            config=self.agents_config['security_auditor'],
            verbose=True,
            tools=[code_security_scanner]
        )

    @agent
    def style_enforcer(self) -> Agent:
        return Agent(
            config=self.agents_config['style_enforcer'],
            verbose=True,
            tools=[style_checker]
        )

    @agent
    def performance_analyst(self) -> Agent:
        return Agent(
            config=self.agents_config['performance_analyst'],
            verbose=True,
            tools=[complexity_analyzer]
        )

    @agent
    def pr_summarizer(self) -> Agent:
        return Agent(
            config=self.agents_config['pr_summarizer'],
            verbose=True
        )

   
    @task
    def security_audit_task(self) -> Task:
        return Task(
            config=self.tasks_config['security_audit_task'],
        )

    @task
    def style_check_task(self) -> Task:
        return Task(
            config=self.tasks_config['style_check_task'],
        )

    @task
    def performance_analysis_task(self) -> Task:
        return Task(
            config=self.tasks_config['performance_analysis_task'],
        )

    @task
    def pr_summary_task(self) -> Task:
        return Task(
            config=self.tasks_config['pr_summary_task'],
        )


    @crew
    def crew(self) -> Crew:
        """Creates the ParallelFanOut crew with sequential process and context-based synthesis"""

        return Crew(
            agents=self.agents,
            tasks=self.tasks,
            process=Process.sequential,
            verbose=True,
        )
