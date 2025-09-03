from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task
from dotenv import load_dotenv
from tools.file_write_tool import CustomFileWriteTool

load_dotenv()


@CrewBase
class Interview():
    """Interview crew"""

    agents_config = 'config/agents.yaml'
    tasks_config = 'config/tasks.yaml'

    @agent
    def interview_agent(self) -> Agent:
        return Agent(
            config=self.agents_config['interview_agent'],
            verbose=True
        )

    @agent
    def summary_agent(self) -> Agent:
        return Agent(
            config=self.agents_config['summary_agent'],
            tools=[CustomFileWriteTool()],
            verbose=True
        )

    @task
    def interview_task(self) -> Task:
        return Task(
            config=self.tasks_config['interview_task'],
        )

    @task
    def summary_task(self) -> Task:
        return Task(
            config=self.tasks_config['summary_task'],
        )

    @crew
    def crew(self) -> Crew:
        """Creates the Interview crew"""
        return Crew(
            agents=self.agents,
            tasks=self.tasks,
            process=Process.sequential,
            verbose=True,
        )
