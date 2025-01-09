from .base import DatabaseService

class SlotService(DatabaseService):
    """
    Service class for managing `slots` table operations.
    """

    def create_slot(self, id, start_time, end_time, working_day_id, daily_slot_number, weekly_slot_number, slot_alloted_to_id=None):
        """
        Inserts a new slot into the `slots` table, ensuring no duplicate entries.
        """
        # Check if the slot already exists with the same id
        check_query = """
        SELECT * FROM slots WHERE id = :id;
        """
        existing_slot = self.execute_query(check_query, {"id": id}).fetchone()

        if existing_slot:
            raise ValueError(f"Slot with ID {id} already exists in the database.")

        # Insert the new slot
        insert_query = """
        INSERT INTO slots (id, start_time, end_time, working_day_id, daily_slot_number, weekly_slot_number, slot_alloted_to_id) 
        VALUES (:id, :start_time, :end_time, :working_day_id, :daily_slot_number, :weekly_slot_number, :slot_alloted_to_id) 
        RETURNING row_to_json(slots.*);
        """
        result = self.execute_query(insert_query, {
            "id": id,
            "start_time": start_time,
            "end_time": end_time,
            "working_day_id": working_day_id,
            "daily_slot_number": daily_slot_number,
            "weekly_slot_number": weekly_slot_number,
            "slot_alloted_to_id": slot_alloted_to_id
        })
        return result.fetchone()[0]

    def get_slot(self, slot_id):
        """
        Fetches a slot by its ID.
        """
        query = """
        SELECT * FROM slots WHERE id = :id;
        """
        result = self.execute_query(query, {"id": slot_id}).fetchone()
        if not result:
            raise ValueError(f"No slot found with ID {slot_id}.")
        return result

    def update_slot(self, slot_id, **kwargs):
        """
        Updates the details of a slot given its ID. Accepts dynamic fields for update.
        """
        # Check if the slot exists
        check_query = """
        SELECT * FROM slots WHERE id = :id;
        """
        existing_slot = self.execute_query(check_query, {"id": slot_id}).fetchone()
        if not existing_slot:
            raise ValueError(f"No slot found with ID {slot_id} to update.")

        # Construct dynamic SET clause for SQL
        set_clause = ", ".join([f"{key} = :{key}" for key in kwargs])
        
        # Update the slot
        query = f"""
        UPDATE slots 
        SET {set_clause}
        WHERE id = :id RETURNING row_to_json(slots.*);
        """
        kwargs["id"] = slot_id
        result = self.execute_query(query, kwargs)
        return result.fetchone()[0]

    def delete_slot(self, slot_id):
        """
        Deletes a slot by its ID.
        """
        # Check if the slot exists
        check_query = """
        SELECT * FROM slots WHERE id = :id;
        """
        existing_slot = self.execute_query(check_query, {"id": slot_id}).fetchone()
        if not existing_slot:
            raise ValueError(f"No slot found with ID {slot_id} to delete.")

        # Delete the slot
        query = """
        DELETE FROM slots WHERE id = :id;
        """
        self.execute_query(query, {"id": slot_id})
        return {"message": f"Slot with ID {slot_id} has been deleted."}
