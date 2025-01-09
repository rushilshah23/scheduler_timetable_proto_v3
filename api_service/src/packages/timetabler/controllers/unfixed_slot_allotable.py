from .base import DatabaseService

class UnFixedSlotAllotableService(DatabaseService):
    """
    Service class for managing `unfixed_slot_allotables` table operations.
    """

    def create_unfixed_slot(self, id):
        """
        Inserts a new unfixed slot allotable into the `unfixed_slot_allotables` table.
        """
        # Check if the unfixed slot already exists with the same id
        check_query = """
        SELECT * FROM unfixed_slot_allotables WHERE id = :id;
        """
        existing_slot = self.execute_query(check_query, {"id": id}).fetchone()

        if existing_slot:
            raise ValueError(f"Unfixed Slot with ID {id} already exists in the database.")

        # Insert the new unfixed slot
        insert_query = """
        INSERT INTO unfixed_slot_allotables (id) 
        VALUES (:id) 
        RETURNING row_to_json(unfixed_slot_allotables.*);
        """
        result = self.execute_query(insert_query, {
            "id": id
        })
        return result.fetchone()[0]

    def get_unfixed_slot(self, slot_id):
        """
        Fetches an unfixed slot by its ID.
        """
        query = """
        SELECT * FROM unfixed_slot_allotables WHERE id = :id;
        """
        result = self.execute_query(query, {"id": slot_id}).fetchone()
        if not result:
            raise ValueError(f"No unfixed slot found with ID {slot_id}.")
        return result

    def update_unfixed_slot(self, slot_id):
        """
        Updates the details of an unfixed slot given its ID.
        """
        # Since `UnFixedSlotAllotable` doesn't have additional fields to update,
        # this method can be used to re-validate the slot's existence or trigger any necessary actions.
        check_query = """
        SELECT * FROM unfixed_slot_allotables WHERE id = :id;
        """
        existing_slot = self.execute_query(check_query, {"id": slot_id}).fetchone()
        if not existing_slot:
            raise ValueError(f"No unfixed slot found with ID {slot_id} to update.")
        
        # Here, we just return the existing data as no specific fields are available for update
        return existing_slot

    def delete_unfixed_slot(self, slot_id):
        """
        Deletes an unfixed slot by its ID.
        """
        # Check if the unfixed slot exists
        check_query = """
        SELECT * FROM unfixed_slot_allotables WHERE id = :id;
        """
        existing_slot = self.execute_query(check_query, {"id": slot_id}).fetchone()
        if not existing_slot:
            raise ValueError(f"No unfixed slot found with ID {slot_id} to delete.")

        # Delete the unfixed slot
        query = """
        DELETE FROM unfixed_slot_allotables WHERE id = :id;
        """
        self.execute_query(query, {"id": slot_id})
        return {"message": f"Unfixed Slot with ID {slot_id} has been deleted."}
