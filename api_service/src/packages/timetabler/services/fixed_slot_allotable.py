from .base import DatabaseService

class FixedSlotAllotableService(DatabaseService):
    """
    Service class for managing `fixed_slot_allotables` table operations.
    """

    def create_fixed_slot(self, id, start_time, end_time, working_day_id):
        """
        Inserts a new fixed slot allotable into the `fixed_slot_allotables` table.
        """
        # Check if the fixed slot already exists with the same id
        check_query = """
        SELECT * FROM fixed_slot_allotables WHERE id = :id;
        """
        existing_slot = self.execute_query(check_query, {"id": id}).fetchone()

        if existing_slot:
            raise ValueError(f"Fixed Slot with ID {id} already exists in the database.")

        # Insert the new fixed slot
        insert_query = """
        INSERT INTO fixed_slot_allotables (id, start_time, end_time, working_day_id) 
        VALUES (:id, :start_time, :end_time, :working_day_id) 
        RETURNING row_to_json(fixed_slot_allotables.*);
        """
        result = self.execute_query(insert_query, {
            "id": id,
            "start_time": start_time,
            "end_time": end_time,
            "working_day_id": working_day_id
        })
        return result.fetchone()[0]

    def get_fixed_slot(self, slot_id):
        """
        Fetches a fixed slot by its ID.
        """
        query = """
        SELECT * FROM fixed_slot_allotables WHERE id = :id;
        """
        result = self.execute_query(query, {"id": slot_id}).fetchone()
        if not result:
            raise ValueError(f"No fixed slot found with ID {slot_id}.")
        return result

    def update_fixed_slot(self, slot_id, new_start_time, new_end_time, new_working_day_id):
        """
        Updates the details of a fixed slot given its ID.
        """
        # Check if the fixed slot exists
        check_query = """
        SELECT * FROM fixed_slot_allotables WHERE id = :id;
        """
        existing_slot = self.execute_query(check_query, {"id": slot_id}).fetchone()
        if not existing_slot:
            raise ValueError(f"No fixed slot found with ID {slot_id} to update.")

        # Update the fixed slot
        query = """
        UPDATE fixed_slot_allotables 
        SET start_time = :new_start_time, end_time = :new_end_time, working_day_id = :new_working_day_id 
        WHERE id = :id RETURNING row_to_json(fixed_slot_allotables.*);
        """
        result = self.execute_query(query, {
            "id": slot_id,
            "new_start_time": new_start_time,
            "new_end_time": new_end_time,
            "new_working_day_id": new_working_day_id
        })
        return result.fetchone()[0]

    def delete_fixed_slot(self, slot_id):
        """
        Deletes a fixed slot by its ID.
        """
        # Check if the fixed slot exists
        check_query = """
        SELECT * FROM fixed_slot_allotables WHERE id = :id;
        """
        existing_slot = self.execute_query(check_query, {"id": slot_id}).fetchone()
        if not existing_slot:
            raise ValueError(f"No fixed slot found with ID {slot_id} to delete.")

        # Delete the fixed slot
        query = """
        DELETE FROM fixed_slot_allotables WHERE id = :id;
        """
        self.execute_query(query, {"id": slot_id})
        return {"message": f"Fixed Slot with ID {slot_id} has been deleted."}
