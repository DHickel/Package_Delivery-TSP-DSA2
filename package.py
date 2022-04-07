from enum import Enum, auto

from hashtable import HashTable


class Status(Enum):
    DELIVERED = auto()
    ENROUTE = auto()
    HUB = auto()
    HOLD = auto()


class Package:

    def __init__(self):
        self.id = None
        self.address = None
        self.city = None
        self.state = None
        self.zipcode = None
        self.deadline = None
        self.weight = None
        self.notes = None
        self.truck = None
        self.status = Status.HUB
        self.time_delivered = None



