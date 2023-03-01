import json
import logging
from dataclasses import dataclass
from jmetal.core.problem import Problem
from communication.types import CommunicationType
from decoder import decode_problem, decode_communication,decode_trust
from trust.base_trust import Trust
import dataclasses

@dataclass
class ConfigData:
    noAgents : int
    problem : Problem
    commuincationType: CommunicationType
    trust_type: Trust
    population_size: int
    offspring_population: int

    def as_dict(self):
        return dataclasses.asdict(self)


class Settings:
    def __init__(self, json_settings):
        self.json_settings= json.load(json_settings)
        self.decodeJson()

    def decodeJson(self):
        self.log_level = self.decodeLogLevel()
        self.maxtime = self.json_settings["max_time"]
        self.agents_data = self.decodeAgentsData()
        self.enable_plots = self.json_settings["enable_plots"]

    def decodeLogLevel(self):
        return logging.INFO

    def decodeAgentsData(self):
        noAgents = self.json_settings["number_of_agents"]
        problem =  decode_problem(self.json_settings["problem"], self.json_settings["problem_size"])
        communication = decode_communication(self.json_settings["communication_type"], self.json_settings["communication_operator"])
        trust_type =  decode_trust(self.json_settings["trust"])
        population_size = self.json_settings["population size"]
        offspring_size = self.json_settings["offspring size"]
        return ConfigData(noAgents, problem, communication, trust_type , population_size, offspring_size)
