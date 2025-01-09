from dataclasses import dataclass
from datetime import time
from src.packages.timetabler.domain import SlotAllotable
from src.packages.timetabler.mapper import DivisionMapper, WorkingDayMapper
from .base import DomainMapper

@dataclass
class SlotAllotableMapper(DomainMapper):
    
    @staticmethod
    def serialize_dbModel(dict):
        """
        Converts a database model to a domain model.
        """
        division = DivisionMapper.serialize_dbModel(dict["division"])  # Use DivisionMapper for division
        working_day = WorkingDayMapper.serialize_dbModel(dict["working_day"]) if dict.get("working_day") else None

        return SlotAllotable(
            id=dict["id"],
            division_id=dict["division_id"],
            name=dict["name"],
            continuous_slot=dict["continuous_slot"],
            weekly_frequency=dict["weekly_frequency"],
            fixed_slot=dict["fixed_slot"],
            start_time=time.fromisoformat(dict["start_time"]) if dict.get("start_time") else None,
            end_time=time.fromisoformat(dict["end_time"]) if dict.get("end_time") else None,
            working_day_id=dict["working_day_id"],
            division=division,
            working_day=working_day
        )

    @staticmethod
    def deserialize_dbModel(object):
        """
        Converts a domain model to a dictionary to be inserted into the database.
        """
        return {
            "id": object.id,
            "division_id": object.division_id,
            "name": object.name,
            "continuous_slot": object.continuous_slot,
            "weekly_frequency": object.weekly_frequency,
            "fixed_slot": object.fixed_slot,
            "start_time": object.start_time.strftime("%H:%M:%S") if object.start_time else None,
            "end_time": object.end_time.strftime("%H:%M:%S") if object.end_time else None,
            "working_day_id": object.working_day_id
        }
