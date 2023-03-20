from agent.agent import Agent
import numpy as np
def restart_agent(agent_to_modify :Agent, agent2:Agent):
    agent_to_modify.random_restart()
    return False

def kill_agent(agent_to_modify: Agent, agent2: Agent):
    return True

def modify_agent(agent_to_modify: Agent, agent2: Agent):
    mutation_probablity, crossover_probability = agent2.get_algorithm_stats()
    agent_to_modify.change_probability(mutation_probablity, crossover_probability)
    return False