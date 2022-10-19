import logging

from jmetal.problem.singleobjective.unconstrained import Rastrigin
from runners.single import MultiAgentRunner
from runners.statistic import StatisticRunner
from communication.types import CommunicationWithMutation
from communication.operators import average_operator
import inicialization as init
from settings import Settings

with open("config.json","r") as f:
    settings = Settings(f)

logging.basicConfig(level=settings.log_level)
logging.info(settings.json_settings)
print(settings.decodeAgentsData())


# Agents, Agent_Reference = init.create_agents_float_solution(10, problem, CommuncationWithMutation(operator=average_operator))

# runner = MultiAgentRunner(agents= Agents, agent_single= Agent_Reference)

# Statistic_runner = StatisticRunner(runner)


# Statistic_runner.run_an_collect_data(no_runs = 15, cycles=150, cycle_iter=40, num_of_comm=5  )
# Statistic_runner.plot()

