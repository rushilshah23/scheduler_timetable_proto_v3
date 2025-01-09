from .base import DatabaseService

class SlotAllotableService(DatabaseService):
    """
    Service class for managing `slot_allotables` table operations.
    """

    def create_slot_allotable(self, id, division_id, name, continuous_slot, weekly_frequency, fixed_slot=False):
        """
        Inserts a new slot allotable into the `slot_allotables` table.
        Ensures no duplicate entries.
        """
        # Check if the slot allotable already exists with the same ID
        check_query = """
        SELECT * FROM slot_allotables WHERE id = :id;
        """
        existing_slot_allotable = self.execute_query(check_query, {"id": id}).fetchone()

        if existing_slot_allotable:
            raise ValueError(f"Slot allotable with ID {id} already exists in the database.")

        # Insert the new slot allotable
        insert_query = """
        INSERT INTO slot_allotables (id, division_id, name, continuous_slot, weekly_frequency, fixed_slot) 
        VALUES (:id, :division_id, :name, :continuous_slot, :weekly_frequency, :fixed_slot) 
        RETURNING row_to_json(slot_allotables.*);
        """
        result = self.execute_query(insert_query, {
            "id": id,
            "division_id": division_id,
            "name": name,
            "continuous_slot": continuous_slot,
            "weekly_frequency": weekly_frequency,
            "fixed_slot": fixed_slot
        })
        return result.fetchone()[0]

    def get_slot_allotable(self, slot_allotable_id):
        """
        Fetches a slot allotable by its ID.
        """
        query = """
        SELECT * FROM slot_allotables WHERE id = :id;
        """
        result = self.execute_query(query, {"id": slot_allotable_id}).fetchone()
        if not result:
            raise ValueError(f"No slot allotable found with ID {slot_allotable_id}.")
        return result

    def update_slot_allotable(self, slot_allotable_id, **kwargs):
        """
        Updates the details of a slot allotable given its ID. Accepts dynamic fields for update.
        """
        # Check if the slot allotable exists
        check_query = """
        SELECT * FROM slot_allotables WHERE id = :id;
        """
        existing_slot_allotable = self.execute_query(check_query, {"id": slot_allotable_id}).fetchone()
        if not existing_slot_allotable:
            raise ValueError(f"No slot allotable found with ID {slot_allotable_id} to update.")

        # Construct dynamic SET clause for SQL
        set_clause = ", ".join([f"{key} = :{key}" for key in kwargs])
        
        # Update the slot allotable
        query = f"""
        UPDATE slot_allotables 
        SET {set_clause}
        WHERE id = :id RETURNING row_to_json(slot_allotables.*);
        """
        kwargs["id"] = slot_allotable_id
        result = self.execute_query(query, kwargs)
        return result.fetchone()[0]

    def delete_slot_allotable(self, slot_allotable_id):
        """
        Deletes a slot allotable by its ID.
        """
        # Check if the slot allotable exists
        check_query = """
        SELECT * FROM slot_allotables WHERE id = :id;
        """
        existing_slot_allotable = self.execute_query(check_query, {"id": slot_allotable_id}).fetchone()
        if not existing_slot_allotable:
            raise ValueError(f"No slot allotable found with ID {slot_allotable_id} to delete.")

        # Delete the slot allotable
        query = """
        DELETE FROM slot_allotables WHERE id = :id;
        """
        self.execute_query(query, {"id": slot_allotable_id})
        return {"message": f"Slot allotable with ID {slot_allotable_id} has been deleted."}
