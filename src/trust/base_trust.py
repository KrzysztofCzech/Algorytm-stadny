import logging

class Trust:
    def __init__(self):
        self.trust_dict ={}

    def update_trust(self, name_self:str, name_other: str, val: int) -> None:
        raise NotImplementedError

    def check_trust(self, name_other : str) -> None:
        raise NotImplementedError
    
    def get_trust_value(self, name_other: str) -> int:
        raise NotImplementedError

    def initalize(self):
        raise NotImplementedError


    

# adds 1 tust when good resuts subtructs 1 when information is useless local for every agent
class NaiveTrust(Trust):
    def __init__(self):
        super().__init__()

    def update_trust(self,name_self, name_other: str, val: int) -> None:
        if not (name_other in self.trust_dict):
            self.trust_dict[name_other] = 1
        else:
            self.trust_dict[name_other] = max(1, self.trust_dict[name_other] +val)
        logging.debug(f"Updated trust {name_other} to {self.trust_dict[name_other] } ")
        return self.trust_dict[name_other] 

    def check_trust(self,name_other : str) -> None:
        if not (name_other in self.trust_dict):
            self.trust_dict[name_other] = 1
        return self.trust_dict[name_other]

    
    def get_trust_value(self, name_other: str) -> int:
        if not (name_other in self.trust_dict):
            self.trust_dict[name_other] = 1
        return  self.trust_dict[name_other]

    def initalize(self):
        self.trust_dict = {}

class Singleton(type):
    _instances = {}
    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]
        
class GlobalTrust(Trust, metaclass=Singleton):
    def __init__(self):
        super().__init__()
        self.max_trust = 30
        self.starting_trust = 10

    def update_trust(self,name_self, name_other: str, val: int) -> None:
        if not (name_other in self.trust_dict):
            self.trust_dict[name_other] = self.starting_trust
            logging.debug(f"Initalised4 {name_other}  to {self.trust_dict[name_other]}")
        elif not (name_self in self.trust_dict):
            self.trust_dict[name_self] = self.starting_trust
            logging.debug(f"Initalised3 {name_self}  to {self.trust_dict[name_self]}")
        else:
            my_trust_new = self.trust_dict[name_self] - val
            other_trust_new = self.trust_dict[name_other] + val

            if (self.max_trust >= my_trust_new >= 1) and (self.max_trust >= other_trust_new >= 1) and name_other != name_self:
                logging.debug(f"{self.trust_dict}")
                self.trust_dict[name_self] = my_trust_new
                self.trust_dict[name_other] = other_trust_new
                logging.debug(f"Updated trust {name_other} to {self.trust_dict[name_other]} by {name_self} mydiff{ my_trust_new} {other_trust_new} val{val} ")
                logging.debug(f"{self.trust_dict}")
        return self.trust_dict[name_other] 

    def check_trust(self, name_other : str) -> None:
        if not (name_other in self.trust_dict):
            self.trust_dict[name_other] = self.starting_trust
            logging.debug(f"Initalised 2{name_other}  to {self.trust_dict[name_other]}")

        return int(self.trust_dict[name_other])

    
    def get_trust_value(self, name_other: str) -> int:
        if not (name_other in self.trust_dict):
            self.trust_dict[name_other] = self.starting_trust
            logging.debug(f"Initalised1 {name_other}  to {self.trust_dict[name_other]}")
        return  int(self.trust_dict[name_other])

    def initalize(self):
        self.trust_dict = {}