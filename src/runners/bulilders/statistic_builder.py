from typing import List
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
        self.max_iterations = 100000000
        self.executors : List[MultiAgentRunner]= []

    def set_agents_all_the_same(self, config, name):
        name = "Identical "+ name
        agents, reference, migration = create_agents_all_equal(config)
        runner  = MultiAgentRunner(agents, name)
        runner.set_config(config)
        self.executors.append(runner)
        self.agent_reference = reference
        self.migration_comparion = migration

    def set_agents_different_probability(self, config, factor, name):
        name = "Different "+ name
        agents, reference, migration = create_agents_different_probability(config, factor)
        runner  = MultiAgentRunner(agents, name)
        runner.set_config(config)
        self.executors.append(runner)        
        self.agent_reference = reference
        self.migration_comparion = migration

    def set_run_config(self, no_runs, communication_num, iterations, communication_freq):
        self.iterations = iterations
        self.communication_num = communication_num
        self.communication_freq = communication_freq
        self.no_runs = no_runs

    def build(self):
        island_comparison = MultiAgentRunner(self.migration_comparion, "Island")
        single_comparison = MultiAgentRunner([self.agent_reference], "Single")
        statistic_runner = StatisticRunner()
        for executor in self.executors:
            statistic_runner.add_Executor(executor)
        statistic_runner.set_single_agent(single_comparison)
        statistic_runner.set_island_comparion(island_comparison)
        statistic_runner.all_iterations = self.iterations
        statistic_runner.communication_frequency = self.communication_freq
        statistic_runner.communication_number = self.communication_num
        statistic_runner.no_runs = self.no_runs
        return statistic_runner
