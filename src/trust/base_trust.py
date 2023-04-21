import logging


class Trust:
    def __init__(self):
        self.trust_dict = {}

    def update_trust(self, name_self: str, name_other: str, val: int) -> None:
        raise NotImplementedError

    def check_trust(self, name_other: str) -> int:
        raise NotImplementedError

    def get_trust_value(self, name_other: str) -> int:
        raise NotImplementedError

    def initialize(self):
        raise NotImplementedError


# adds 1 trust when good results subtracts 1 when information is useless local for every agent
class NaiveTrust(Trust):
    def __init__(self, start_trust, max_trust):
        super().__init__()
        self.start_trust = start_trust
        self.max_trust = max_trust

    def update_trust(self, name_self, name_other: str, val: int) -> None:
        if not (name_other in self.trust_dict):
            self.trust_dict[name_other] = self.start_trust
        else:
            self.trust_dict[name_other] = max(1, self.trust_dict[name_other] + val)
        logging.debug(f"Updated trust {name_other} to {self.trust_dict[name_other]} ")
        return self.trust_dict[name_other]

    def check_trust(self, name_other: str) -> int:
        if not (name_other in self.trust_dict):
            self.trust_dict[name_other] = self.start_trust
        return self.trust_dict[name_other]

    def get_trust_value(self, name_other: str) -> int:
        if not (name_other in self.trust_dict):
            self.trust_dict[name_other] = self.start_trust
        return self.trust_dict[name_other]

    def initialize(self):
        self.trust_dict = {}


class Singleton(type):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]


class GlobalTrust(Trust, metaclass=Singleton):
    def __init__(self, start_trust=10, max_trust=30):
        super().__init__()
        self.max_trust = max_trust
        self.start_trust = start_trust

    def update_trust(self, name_self, name_other: str, val: int) -> None:
        if not (name_other in self.trust_dict):
            self.trust_dict[name_other] = self.start_trust
        elif not (name_self in self.trust_dict):
            self.trust_dict[name_self] = self.start_trust
        else:
            my_trust_new = self.trust_dict[name_self] - val
            other_trust_new = self.trust_dict[name_other] + val
            if (self.max_trust >= my_trust_new >= 1) and (
                    self.max_trust >= other_trust_new >= 1) and name_other != name_self:
                self.trust_dict[name_self] = my_trust_new
                self.trust_dict[name_other] = other_trust_new
        return self.trust_dict[name_other]

    def check_trust(self, name_other: str) -> None:
        if not (name_other in self.trust_dict):
            self.trust_dict[name_other] = self.start_trust
        return int(self.trust_dict[name_other])

    def get_trust_value(self, name_other: str) -> int:
        if not (name_other in self.trust_dict):
            self.trust_dict[name_other] = self.start_trust
        return int(self.trust_dict[name_other])

    def initialize(self):
        self.trust_dict = {}
