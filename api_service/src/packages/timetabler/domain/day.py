from .base import BaseDomain
from enum import Enum
from dataclasses import dataclass


class DayEnum(Enum):
    MONDAY="MONDAY"
    TUESDAY="TUESDAY"
    WEDNESDAY="WEDNESDAY"
    THURSDAY="THURSDAY"
    FRIDAY="FRIDAY"
    SATURDAY="SATURDAY"
    SUNDAY="SUNDAY"



@dataclass
class Day:
    id: str
    name: str


    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name
        }
