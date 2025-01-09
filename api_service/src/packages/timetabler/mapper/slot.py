from dataclasses import dataclass
from datetime import time
from src.packages.timetabler.domain import Slot
from src.packages.timetabler.mapper import WorkingDayMapper, SlotAllotableMapper
from .base import DomainMapper

@dataclass
class SlotMapper(DomainMapper):

    @staticmethod
    def serialize_dbModel(dict):
        """
        Converts a database model to a domain model.
        """
        working_day = WorkingDayMapper.serialize_dbModel(dict["working_day"])  # Use WorkingDayMapper for working_day
        slot_alloted_to = SlotAllotableMapper.serialize_dbModel(dict["slot_alloted_to"]) if dict.get("slot_alloted_to") else None

        return Slot(
            id=dict["id"],
            start_time=time.fromisoformat(dict["start_time"]),
            end_time=time.fromisoformat(dict["end_time"]),
            working_day_id=dict["working_day_id"],
            daily_slot_number=dict["daily_slot_number"],
            weekly_slot_number=dict["weekly_slot_number"],
            slot_alloted_to_id=dict["slot_alloted_to_id"],
            working_day=working_day,
            slot_alloted_to=slot_alloted_to
        )

    @staticmethod
    def deserialize_dbModel(object):
        """
        Converts a domain model to a dictionary to be inserted into the database.
        """
        return {
            "id": object.id,
            "start_time": object.start_time.strftime("%H:%M:%S"),
            "end_time": object.end_time.strftime("%H:%M:%S"),
            "working_day_id": object.working_day_id,
            "daily_slot_number": object.daily_slot_number,
            "weekly_slot_number": object.weekly_slot_number,
            "slot_alloted_to_id": object.slot_alloted_to_id
        }
