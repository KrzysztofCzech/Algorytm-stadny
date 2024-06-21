import json
import logging
from dataclasses import dataclass
from jmetal.core.problem import Problem
from communication.types import CommunicationType
from settings.decoder import decode_problem, decode_communication, decode_trust
from trust.base_trust import Trust
import dataclasses
from settings.enumStrings import *


@dataclass
class AgentConfigData:
    noAgents: int
    problem: Problem
    communicationType: CommunicationType
    trust_type: Trust
    population_size: int
    offspring_population: int
    start_trust: int

    def as_dict(self):
        return dataclasses.asdict(self)
    
    def __str__(self):
        return f"agents: {self.noAgents}, problem {self.problem.get_name()} {self.problem.number_of_variables}, trust {self.trust_type.start_trust}"


def decodeLogLevel():
    return logging.INFO


class Settings:
    def __init__(self, json_settings):
        self.delete_agents = None
        self.enable_plots = None
        self.agents_data = None
        self.max_time = None
        self.log_level = None
        self.json_settings = json_settings
        self.decodeJson()

    def decodeJson(self):
        self.log_level = decodeLogLevel()
        self.max_time = self.json_settings["max_time"]
        self.agents_data = self.decodeAgentsData()
        self.enable_plots = self.json_settings["enable_plots"]
        #self.delete_agents = self.json_settings["delete agents"]

    def decodeAgentsData(self):
        noAgents = self.json_settings["number_of_agents"]
        problem = decode_problem(self.json_settings["problem"], self.json_settings["problem_size"])
        communication = decode_communication(self.json_settings["communication_type"],
                                             self.json_settings["communication_operator"])
        trust_type = decode_trust(self.json_settings[trustMembers.TRUST])
        population_size = self.json_settings["population size"]
        offspring_size = self.json_settings["offspring size"]
        return AgentConfigData(noAgents, problem, communication, trust_type, population_size, offspring_size, start_trust = self.json_settings[trustMembers.TRUST][trustMembers.START])
