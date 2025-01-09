from dataclasses import dataclass
from .base import Controller
from src.utils.misc import get_new_id

from src.packages.timetabler.mapper import DayMapper
@dataclass
class DayController(Controller):

    def create_day(self, day_name):
        """
        Handles the creation of a new day.
        Returns a business response with data and status code.
        """
        try:
            # Perform business logic
            result = self.service.create_day(id=get_new_id(), day_name=day_name)
            result = DayMapper.serialzie_dbModel(result)
            print(result)
            return {"data": result, "status_code": 201}
        except Exception as e:
            return {"error": str(e), "status_code": 500}

    def get_day(self, day_id):
        """
        Handles fetching a day by ID.
        Returns a business response with data and status code.
        """
        try:
            # Perform business logic
            day = self.service.get_day(day_id)
            if not day:
                return {"error": "Day not found", "status_code": 404}
            return {"data": day[1], "status_code": 200}
        except Exception as e:
            return {"error": str(e), "status_code": 500}

    def update_day(self, day_id, new_day_name):
        """
        Handles updating a day by ID.
        Returns a business response with data and status code.
        """
        try:
            result = self.service.update_day(day_id, new_day_name)
            return {"data": result, "status_code": 200}
        except Exception as e:
            return {"error": str(e), "status_code": 500}

    def delete_day(self, day_id):
        """
        Handles deleting a day by ID.
        Returns a business response with data and status code.
        """
        try:
            result = self.service.delete_day(day_id)
            return {"data": result, "status_code": 200}
        except Exception as e:
            return {"error": str(e), "status_code": 500}
