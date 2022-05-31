from enum import Enum

class AttiduteType(Enum):
    GOOD = 0
    MEDIUM = 1
    BAD = 2



def get_selector(attidute :  AttiduteType):
    return {AttiduteType.GOOD : lambda num, list : list[0: num], 
            AttiduteType.MEDIUM : lambda num, list : list[(len(list) - num)//2 : (len(list) + num)//2], 
            AttiduteType.BAD : lambda num, list : list[-num :]
    }[attidute]






