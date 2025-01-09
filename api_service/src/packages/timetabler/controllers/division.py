from .base import DatabaseService

class DivisionService(DatabaseService):
    """
    Service class for managing operations related to the `divisions` table.
    """

    def create_division(self, id, division_name, standard_id):
        """
        Creates a new division and inserts it into the `divisions` table.
        """
        # Check if the division already exists with the same id
        check_query = """
        SELECT * FROM divisions WHERE id = :id;
        """
        existing_division = self.execute_query(check_query, {"id": id}).fetchone()

        if existing_division:
            raise ValueError(f"Division with ID {id} already exists.")

        # Check if the standard exists
        check_standard_query = """
        SELECT * FROM standards WHERE id = :standard_id;
        """
        standard = self.execute_query(check_standard_query, {"standard_id": standard_id}).fetchone()
        if not standard:
            raise ValueError(f"No standard found with ID {standard_id}.")

        # Insert the new division
        insert_query = """
        INSERT INTO divisions (id, division_name, standard_id) 
        VALUES (:id, :division_name, :standard_id) 
        RETURNING row_to_json(divisions.*);
        """
        result = self.execute_query(insert_query, {
            "id": id,
            "division_name": division_name,
            "standard_id": standard_id
        })
        return result.fetchone()[0]

    def get_division(self, division_id):
        """
        Fetches a division by its ID.
        """
        query = """
        SELECT * FROM divisions WHERE id = :id;
        """
        result = self.execute_query(query, {"id": division_id}).fetchone()
        if not result:
            raise ValueError(f"No division found with ID {division_id}.")
        return result

    def update_division(self, division_id, division_name, standard_id):
        """
        Updates the details of a division.
        """
        # Check if the division exists
        check_query = """
        SELECT * FROM divisions WHERE id = :id;
        """
        existing_division = self.execute_query(check_query, {"id": division_id}).fetchone()
        if not existing_division:
            raise ValueError(f"No division found with ID {division_id} to update.")

        # Check if the standard exists
        check_standard_query = """
        SELECT * FROM standards WHERE id = :standard_id;
        """
        standard = self.execute_query(check_standard_query, {"standard_id": standard_id}).fetchone()
        if not standard:
            raise ValueError(f"No standard found with ID {standard_id}.")

        # Update the division details
        update_query = """
        UPDATE divisions 
        SET division_name = :division_name, standard_id = :standard_id
        WHERE id = :id
        RETURNING row_to_json(divisions.*);
        """
        result = self.execute_query(update_query, {
            "id": division_id,
            "division_name": division_name,
            "standard_id": standard_id
        })
        return result.fetchone()[0]

    def delete_division(self, division_id):
        """
        Deletes a division by its ID.
        """
        # Check if the division exists
        check_query = """
        SELECT * FROM divisions WHERE id = :id;
        """
        existing_division = self.execute_query(check_query, {"id": division_id}).fetchone()
        if not existing_division:
            raise ValueError(f"No division found with ID {division_id} to delete.")

        # Delete the division
        delete_query = """
        DELETE FROM divisions WHERE id = :id;
        """
        self.execute_query(delete_query, {"id": division_id})
        return {"message": f"Division with ID {division_id} has been deleted."}
