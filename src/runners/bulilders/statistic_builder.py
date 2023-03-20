from runners.statistic import StatisticRunner
from runners.bulilders.agents_inicialization import create_agents_all_equal, create_agents_different_probability
from runners.single import MultiAgentRunner
class StatisticRunnerBuilder:
    def __init__(self):
        self.max_iterations  = 100000000

    def set_agents_all_the_same(self, config):
        agents, reference = create_agents_all_equal(config) 
        self.agents = agents
        self.agent_reference =  reference

    def set_agents_diffrent_porbability(self, config, factor):
        agents, reference = create_agents_different_probability(config, factor) 
        self.agents = agents
        self.agent_reference =  reference

    def set_run_config(self, no_runs, communication_num, iterations, communication_freq):
        self.iterations = iterations
        self.communication_num = communication_num
        self.communication_freq = communication_freq
        self.no_runs = no_runs
        

    def build(self):
        runner = MultiAgentRunner(agents= self.agents, agent_single= self.agent_reference)
        statisitic_runner =  StatisticRunner(runner)
        statisitic_runner.all_iterations = self.iterations
        statisitic_runner.communication_frequency = self.communication_freq
        statisitic_runner.communication_number = self.communication_num
        statisitic_runner.no_runs = self.no_runs
        return statisitic_runner