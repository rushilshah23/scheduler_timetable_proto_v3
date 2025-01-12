from .base import DomainMapper
from dataclasses import dataclass
from src.packages.timetabler.domain import Day

@dataclass
class DayMapper(DomainMapper):

    def serialzie_dbModel(dict):
        return Day(
            id=dict["id"],
            name=dict["name"]
        )
    
    def deserialzie_dbModel(object ):
        return {
            "id":object.id,
            "name":object.name
        }

        
