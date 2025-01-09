from .base import DatabaseService

class WorkingDayService(DatabaseService):
    """
    Service class for managing `working_days` table operations.
    """

    def create_working_day(self, id, day_id, start_time, end_time, slot_duration, division_id):
        """
        Inserts a new working day into the `working_days` table, ensuring no duplicate entries.
        """
        # Check if the working day already exists with the same id
        check_query = """
        SELECT * FROM working_days WHERE id = :id;
        """
        existing_working_day = self.execute_query(check_query, {"id": id}).fetchone()

        if existing_working_day:
            raise ValueError(f"Working day with ID {id} already exists in the database.")

        # Insert the new working day
        insert_query = """
        INSERT INTO working_days (id, day_id, start_time, end_time, slot_duration, division_id) 
        VALUES (:id, :day_id, :start_time, :end_time, :slot_duration, :division_id) 
        RETURNING row_to_json(working_days.*);
        """
        result = self.execute_query(insert_query, {
            "id": id,
            "day_id": day_id,
            "start_time": start_time,
            "end_time": end_time,
            "slot_duration": slot_duration,
            "division_id": division_id
        })
        return result.fetchone()[0]

    def get_working_day(self, working_day_id):
        """
        Fetches a working day by its ID.
        """
        query = """
        SELECT * FROM working_days WHERE id = :id;
        """
        result = self.execute_query(query, {"id": working_day_id}).fetchone()
        if not result:
            raise ValueError(f"No working day found with ID {working_day_id}.")
        return result

    def update_working_day(self, working_day_id, new_start_time, new_end_time, new_slot_duration):
        """
        Updates the details of a working day given its ID.
        """
        # Check if the working day exists
        check_query = """
        SELECT * FROM working_days WHERE id = :id;
        """
        existing_working_day = self.execute_query(check_query, {"id": working_day_id}).fetchone()
        if not existing_working_day:
            raise ValueError(f"No working day found with ID {working_day_id} to update.")

        # Update the working day
        query = """
        UPDATE working_days 
        SET start_time = :new_start_time, end_time = :new_end_time, slot_duration = :new_slot_duration 
        WHERE id = :id RETURNING row_to_json(working_days.*);
        """
        result = self.execute_query(query, {
            "id": working_day_id,
            "new_start_time": new_start_time,
            "new_end_time": new_end_time,
            "new_slot_duration": new_slot_duration
        })
        return result.fetchone()[0]

    def delete_working_day(self, working_day_id):
        """
        Deletes a working day by its ID.
        """
        # Check if the working day exists
        check_query = """
        SELECT * FROM working_days WHERE id = :id;
        """
        existing_working_day = self.execute_query(check_query, {"id": working_day_id}).fetchone()
        if not existing_working_day:
            raise ValueError(f"No working day found with ID {working_day_id} to delete.")

        # Delete the working day
        query = """
        DELETE FROM working_days WHERE id = :id;
        """
        self.execute_query(query, {"id": working_day_id})
        return {"message": f"Working day with ID {working_day_id} has been deleted."}
