import logging
import os

from runners.bulilders.statistic_builder import StatisticRunnerBuilder
from settings.settings import Settings

Statistic_runner_list = []
prefix = os.path.join("run_configs", "problem")
for agent_no in [10]:
    for idx, config in enumerate(["config_R.json"]):
        with open(os.path.join(prefix, config), "r") as f:
            settings = Settings(f)
            # logging.basicConfig(level=settings.log_level)
        logging.basicConfig(level=logging.INFO)
        config = settings.decodeAgentsData()
        config.noAgents = agent_no
        logging.info(settings.json_settings)
        from jmetal.problem.singleobjective.unconstrained import Rastrigin
        iterations = config.problem.number_of_variables **2 * 10
        statisticRunnerBuilder = StatisticRunnerBuilder()
        statisticRunnerBuilder.set_agents_different_probability(config, 1.3)
        statisticRunnerBuilder.set_run_config(no_runs=3, communication_num=1, iterations=iterations,
                                              communication_freq=10)
        Statistic_runner_list.append(statisticRunnerBuilder.build())
for statistic in Statistic_runner_list:
    statistic.run_an_collect_data()
    if settings.enable_plots:
        statistic.plot()


def average_data(data):
    return sum(data) / len(data)
