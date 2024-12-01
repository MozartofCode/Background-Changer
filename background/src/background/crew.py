from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task
from background.tools.custom_tool import DownloadingTool, ChangingTool
from crewai_tools import SerperDevTool

@CrewBase
class BackgroundCrew():
	"""Background crew"""

	@agent
	def researcher(self) -> Agent:
		return Agent(
			config=self.agents_config['researcher'],
			tools=[SerperDevTool()],
			verbose=True
		)
	
	@agent
	def downloader(self) -> Agent:
		return Agent(
			config=self.agents_config['downloader'],
			tools=[DownloadingTool(), SerperDevTool()],
			verbose=True
		)

	@agent
	def changer(self) -> Agent:
		return Agent(
			config=self.agents_config['changer'],
			tools=[ChangingTool()],
			verbose=True
		)
	
	@task
	def research_task(self) -> Task:
		return Task(
			config=self.tasks_config['research_task'],
		)

	@task
	def downloader_task(self) -> Task:
		return Task(
			config=self.tasks_config['downloader_task'],
		)

	@task
	def changer_task(self) -> Task:
		return Task(
			config=self.tasks_config['changer_task'],
		)

	@crew
	def crew(self) -> Crew:
		return Crew(
			agents=self.agents,
			tasks=self.tasks,
			verbose=True,
		)