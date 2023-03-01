import logging

from inicialization.agents_inicialization import create_agents_float_solution
from settings import Settings
from runners.single import MultiAgentRunner
from runners.statistic import StatisticRunner
from time import time

time1 =  time()
with open("config.json","r") as f:
    settings = Settings(f)

# logging.basicConfig(level=settings.log_level)
logging.basicConfig(level=logging.INFO)
logging.info(settings.json_settings)
config = settings.decodeAgentsData()


Agents, Agent_Reference = create_agents_float_solution(config)
Agents[0].get_trust_memory().starting_trust = 8
runner = MultiAgentRunner(agents= Agents, agent_single= Agent_Reference)



Statistic_runner = StatisticRunner(runner)
 


Statistic_runner.run_an_collect_data(no_runs = 8, cycles=250 , cycle_iter=50, num_of_comm=3)
if settings.enable_plots:
    Statistic_runner.plot()

