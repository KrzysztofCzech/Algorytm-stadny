from runners.statistic import StatisticRunner
from runners.bulilders.agents_inicialization import create_agents_all_equal, create_agents_different_probability
from runners.single import MultiAgentRunner
from communication.types import CommunicationMigration
from copy import deepcopy


class StatisticRunnerBuilder:
    def __init__(self):
        self.migration_comparion = None
        self.no_runs = None
        self.statistic_runner = None
        self.communication_freq = None
        self.communication_num = None
        self.iterations = None
        self.agent_reference = None
        self.agents = None
        self.max_iterations = 100000000

    def set_agents_all_the_same(self, config):
        agents, reference, migration = create_agents_all_equal(config)
        self.agents = agents
        self.agent_reference = reference
        self.migration_comparion = migration

    def set_agents_different_probability(self, config, factor):
        agents, reference, migration = create_agents_different_probability(config, factor)
        self.agents = agents
        self.agent_reference = reference
        self.migration_comparion = migration

    def set_run_config(self, no_runs, communication_num, iterations, communication_freq):
        self.iterations = iterations
        self.communication_num = communication_num
        self.communication_freq = communication_freq
        self.no_runs = no_runs

    def build(self):
        runner = MultiAgentRunner(agents=self.agents)
        island_comparison = MultiAgentRunner(agents=self.migration_comparion)
        single_comparison = MultiAgentRunner(agents=[self.agent_reference])
        statistic_runner = StatisticRunner(runner)
        statistic_runner.set_single_agent(single_comparison)
        statistic_runner.set_island_comparion(island_comparison)
        statistic_runner.all_iterations = self.iterations
        statistic_runner.communication_frequency = self.communication_freq
        statistic_runner.communication_number = self.communication_num
        statistic_runner.no_runs = self.no_runs
        return statistic_runner
