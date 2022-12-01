import logging

class Trust:
    def __init__(self):
        self.trust_dict ={}

    def update_trust(self, name_other: str, val: int) -> None:
        raise NotImplementedError

    def check_trust(self, name_other : str) -> None:
        raise NotImplementedError
    
    def get_trust_value(self, name_other: str) -> int:
        raise NotImplementedError


    

# adds 1 tust when good resuts subtructs 1 when information is useless local for every agent
class NaiveTrust(Trust):
    def __init__(self):
        super().__init__()

    def update_trust(self, name_other: str, val: int) -> None:
        if not (name_other in self.trust_dict):
            self.trust_dict[name_other] = 1
        else:
            self.trust_dict[name_other] = max(1, self.trust_dict[name_other] +val)
        logging.debug(f"Updated trust {name_other} to {self.trust_dict[name_other] } ")
        return self.trust_dict[name_other] 

    def check_trust(self, name_other : str) -> None:
        if not (name_other in self.trust_dict):
            self.trust_dict[name_other] = 1
        return self.trust_dict[name_other]

    
    def get_trust_value(self, name_other: str) -> int:
        if not (name_other in self.trust_dict):
            self.trust_dict[name_other] = 1
        return  self.trust_dict[name_other]
