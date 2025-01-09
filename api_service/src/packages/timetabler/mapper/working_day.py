from dataclasses import dataclass
from src.packages.timetabler.domain import WorkingDay
from src.packages.timetabler.mapper import DayMapper
from src.packages.timetabler.mapper import DivisionMapper
from datetime import time
from .base import DomainMapper

@dataclass
class WorkingDayMapper(DomainMapper):

    @staticmethod
    def serialize_dbModel(dict):
        """
        Converts a database model to a domain model.
        """
        day = DayMapper.serialzie_dbModel(dict["day"])  # Use DayMapper to convert day data
        division = DivisionMapper.serialize_dbModel(dict["division"])  # Convert division data

        return WorkingDay(
            id=dict["id"],
            day_id=dict["day_id"],
            start_time=time.fromisoformat(dict["start_time"]),
            end_time=time.fromisoformat(dict["end_time"]),
            slot_duration=dict["slot_duration"],
            day=day,
            division_id=dict["division_id"],
            division=division
        )
    
    @staticmethod
    def deserialize_dbModel(object):
        """
        Converts a domain model to a dictionary to be inserted into the database.
        """
        return {
            "id": object.id,
            "day_id": object.day_id,
            "start_time": object.start_time.strftime("%H:%M:%S"),
            "end_time": object.end_time.strftime("%H:%M:%S"),
            "slot_duration": object.slot_duration,
            "division_id": object.division_id,
            "division": DivisionMapper.deserialize_dbModel(object.division) if object.division else None
        }
