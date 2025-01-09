from .base import DatabaseService

class UniversityService(DatabaseService):
    """
    Service class for managing operations related to the `universities` table.
    """

    def create_university(self, id, university_name, logo):
        """
        Creates a new university and inserts it into the `universities` table.
        """
        # Check if the university already exists with the same id
        check_query = """
        SELECT * FROM universities WHERE id = :id;
        """
        existing_university = self.execute_query(check_query, {"id": id}).fetchone()

        if existing_university:
            raise ValueError(f"University with ID {id} already exists.")

        # Insert the new university
        insert_query = """
        INSERT INTO universities (id, university_name, logo) 
        VALUES (:id, :university_name, :logo) 
        RETURNING row_to_json(universities.*);
        """
        result = self.execute_query(insert_query, {
            "id": id,
            "university_name": university_name,
            "logo": logo
        })
        return result.fetchone()[0]

    def get_university(self, university_id):
        """
        Fetches a university by its ID.
        """
        query = """
        SELECT * FROM universities WHERE id = :id;
        """
        result = self.execute_query(query, {"id": university_id}).fetchone()
        if not result:
            raise ValueError(f"No university found with ID {university_id}.")
        return result

    def update_university(self, university_id, university_name, logo):
        """
        Updates the details of a university.
        """
        # Check if the university exists
        check_query = """
        SELECT * FROM universities WHERE id = :id;
        """
        existing_university = self.execute_query(check_query, {"id": university_id}).fetchone()
        if not existing_university:
            raise ValueError(f"No university found with ID {university_id} to update.")

        # Update the university details
        update_query = """
        UPDATE universities 
        SET university_name = :university_name, logo = :logo
        WHERE id = :id
        RETURNING row_to_json(universities.*);
        """
        result = self.execute_query(update_query, {
            "id": university_id,
            "university_name": university_name,
            "logo": logo
        })
        return result.fetchone()[0]

    def delete_university(self, university_id):
        """
        Deletes a university by its ID.
        """
        # Check if the university exists
        check_query = """
        SELECT * FROM universities WHERE id = :id;
        """
        existing_university = self.execute_query(check_query, {"id": university_id}).fetchone()
        if not existing_university:
            raise ValueError(f"No university found with ID {university_id} to delete.")

        # Delete the university
        delete_query = """
        DELETE FROM universities WHERE id = :id;
        """
        self.execute_query(delete_query, {"id": university_id})
        return {"message": f"University with ID {university_id} has been deleted."}
