from .base import DatabaseService

class BreakService(DatabaseService):
    """
    Service class for managing `breaks` table operations.
    """

    def create_break(self, id):
        """
        Inserts a new break into the `breaks` table, inheriting from AllotableEntity.
        """
        # Check if the break already exists with the same id
        check_query = """
        SELECT * FROM breaks WHERE id = :id;
        """
        existing_break = self.execute_query(check_query, {"id": id}).fetchone()

        if existing_break:
            raise ValueError(f"Break with ID {id} already exists in the database.")

        # Insert the new break into AllotableEntity first (as Break inherits from it)
        insert_query = """
        INSERT INTO allotable_entities (id) 
        VALUES (:id) 
        RETURNING id;
        """
        result = self.execute_query(insert_query, {"id": id})
        allotable_entity_id = result.fetchone()[0]

        # Now insert the break into the `breaks` table
        insert_break_query = """
        INSERT INTO breaks (id) 
        VALUES (:id) 
        RETURNING row_to_json(breaks.*);
        """
        break_result = self.execute_query(insert_break_query, {"id": allotable_entity_id})
        return break_result.fetchone()[0]

    def get_break(self, break_id):
        """
        Fetches a break by its ID.
        """
        query = """
        SELECT * FROM breaks WHERE id = :id;
        """
        result = self.execute_query(query, {"id": break_id}).fetchone()
        if not result:
            raise ValueError(f"No break found with ID {break_id}.")
        return result

    def update_break(self, break_id, new_id):
        """
        Updates the details of a break given its ID.
        """
        # Check if the break exists
        check_query = """
        SELECT * FROM breaks WHERE id = :id;
        """
        existing_break = self.execute_query(check_query, {"id": break_id}).fetchone()
        if not existing_break:
            raise ValueError(f"No break found with ID {break_id} to update.")

        # Update the break's ID
        update_query = """
        UPDATE breaks 
        SET id = :new_id 
        WHERE id = :id 
        RETURNING row_to_json(breaks.*);
        """
        result = self.execute_query(update_query, {
            "id": break_id,
            "new_id": new_id
        })
        return result.fetchone()[0]

    def delete_break(self, break_id):
        """
        Deletes a break by its ID.
        """
        # Check if the break exists
        check_query = """
        SELECT * FROM breaks WHERE id = :id;
        """
        existing_break = self.execute_query(check_query, {"id": break_id}).fetchone()
        if not existing_break:
            raise ValueError(f"No break found with ID {break_id} to delete.")

        # Delete the break
        delete_query = """
        DELETE FROM breaks WHERE id = :id;
        """
        self.execute_query(delete_query, {"id": break_id})
        return {"message": f"Break with ID {break_id} has been deleted."}
