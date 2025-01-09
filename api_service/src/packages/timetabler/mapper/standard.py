from .base import DatabaseService

class StandardService(DatabaseService):
    """
    Service class for managing operations related to the `standards` table.
    """

    def create_standard(self, id, standard_name, department_id):
        """
        Creates a new standard and inserts it into the `standards` table.
        """
        # Check if the standard already exists with the same id
        check_query = """
        SELECT * FROM standards WHERE id = :id;
        """
        existing_standard = self.execute_query(check_query, {"id": id}).fetchone()

        if existing_standard:
            raise ValueError(f"Standard with ID {id} already exists.")

        # Check if the department exists
        check_department_query = """
        SELECT * FROM departments WHERE id = :department_id;
        """
        department = self.execute_query(check_department_query, {"department_id": department_id}).fetchone()
        if not department:
            raise ValueError(f"No department found with ID {department_id}.")

        # Insert the new standard
        insert_query = """
        INSERT INTO standards (id, standard_name, department_id) 
        VALUES (:id, :standard_name, :department_id) 
        RETURNING row_to_json(standards.*);
        """
        result = self.execute_query(insert_query, {
            "id": id,
            "standard_name": standard_name,
            "department_id": department_id
        })
        return result.fetchone()[0]

    def get_standard(self, standard_id):
        """
        Fetches a standard by its ID.
        """
        query = """
        SELECT * FROM standards WHERE id = :id;
        """
        result = self.execute_query(query, {"id": standard_id}).fetchone()
        if not result:
            raise ValueError(f"No standard found with ID {standard_id}.")
        return result

    def update_standard(self, standard_id, standard_name, department_id):
        """
        Updates the details of a standard.
        """
        # Check if the standard exists
        check_query = """
        SELECT * FROM standards WHERE id = :id;
        """
        existing_standard = self.execute_query(check_query, {"id": standard_id}).fetchone()
        if not existing_standard:
            raise ValueError(f"No standard found with ID {standard_id} to update.")

        # Check if the department exists
        check_department_query = """
        SELECT * FROM departments WHERE id = :department_id;
        """
        department = self.execute_query(check_department_query, {"department_id": department_id}).fetchone()
        if not department:
            raise ValueError(f"No department found with ID {department_id}.")

        # Update the standard details
        update_query = """
        UPDATE standards 
        SET standard_name = :standard_name, department_id = :department_id
        WHERE id = :id
        RETURNING row_to_json(standards.*);
        """
        result = self.execute_query(update_query, {
            "id": standard_id,
            "standard_name": standard_name,
            "department_id": department_id
        })
        return result.fetchone()[0]

    def delete_standard(self, standard_id):
        """
        Deletes a standard by its ID.
        """
        # Check if the standard exists
        check_query = """
        SELECT * FROM standards WHERE id = :id;
        """
        existing_standard = self.execute_query(check_query, {"id": standard_id}).fetchone()
        if not existing_standard:
            raise ValueError(f"No standard found with ID {standard_id} to delete.")

        # Delete the standard
        delete_query = """
        DELETE FROM standards WHERE id = :id;
        """
        self.execute_query(delete_query, {"id": standard_id})
        return {"message": f"Standard with ID {standard_id} has been deleted."}
