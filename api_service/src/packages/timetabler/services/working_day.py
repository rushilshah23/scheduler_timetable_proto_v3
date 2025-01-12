from .base import DatabaseService

class WorkingDayService(DatabaseService):
    def create_working_day(self, id, day_id, start_time, end_time, slot_duration, division_id):
        query = """
        INSERT INTO working_days (id, day_id, start_time, end_time, slot_duration, division_id) 
        VALUES (:id, :day_id, :start_time, :end_time, :slot_duration, :division_id)
        RETURNING row_to_json(working_days.*);
        """
        result = self.execute_query(query, {
            "id": id, 
            "day_id": day_id, 
            "start_time": start_time,
            "end_time": end_time,
            "slot_duration": slot_duration,
            "division_id": division_id
        })
        return result.fetchone()[0]

    def get_working_day(self, working_day_id):
        query = "SELECT * FROM working_days WHERE id = :id;"
        result = self.execute_query(query, {"id": working_day_id}).fetchone()
        if not result:
            raise ValueError(f"No working day found with ID {working_day_id}.")
        return result

    def update_working_day(self, working_day_id, **kwargs):
        update_fields = ", ".join([f"{key} = :{key}" for key in kwargs])
        query = f"""
        UPDATE working_days SET {update_fields} WHERE id = :id RETURNING row_to_json(working_days.*);
        """
        params = kwargs
        params["id"] = working_day_id

        result = self.execute_query(query, params).fetchone()
        if not result:
            raise ValueError(f"Failed to update working day with ID {working_day_id}.")
        return result[0]

    def delete_working_day(self, working_day_id):
        query = "DELETE FROM working_days WHERE id = :id RETURNING id;"
        result = self.execute_query(query, {"id": working_day_id}).fetchone()
        if not result:
            raise ValueError(f"No working day found with ID {working_day_id} to delete.")
        return result[0]
