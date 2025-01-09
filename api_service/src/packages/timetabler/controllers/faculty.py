from .base import DatabaseService

class FacultyService(DatabaseService):
    """
    Service class for managing operations related to the `faculties` table.
    """

    def create_faculty(self, id, faculty_name):
        """
        Creates a new faculty and inserts it into the `faculties` table.
        """
        # Check if the faculty already exists with the same id
        check_query = """
        SELECT * FROM faculties WHERE id = :id;
        """
        existing_faculty = self.execute_query(check_query, {"id": id}).fetchone()

        if existing_faculty:
            raise ValueError(f"Faculty with ID {id} already exists.")

        # Insert the new faculty
        insert_query = """
        INSERT INTO faculties (id, faculty_name) 
        VALUES (:id, :faculty_name) 
        RETURNING row_to_json(faculties.*);
        """
        result = self.execute_query(insert_query, {"id": id, "faculty_name": faculty_name})
        return result.fetchone()[0]

    def get_faculty(self, faculty_id):
        """
        Fetches a faculty by its ID.
        """
        query = """
        SELECT * FROM faculties WHERE id = :id;
        """
        result = self.execute_query(query, {"id": faculty_id}).fetchone()
        if not result:
            raise ValueError(f"No faculty found with ID {faculty_id}.")
        return result

    def update_faculty(self, faculty_id, faculty_name):
        """
        Updates the details of a faculty.
        """
        # Check if the faculty exists
        check_query = """
        SELECT * FROM faculties WHERE id = :id;
        """
        existing_faculty = self.execute_query(check_query, {"id": faculty_id}).fetchone()
        if not existing_faculty:
            raise ValueError(f"No faculty found with ID {faculty_id} to update.")

        # Update the faculty details
        update_query = """
        UPDATE faculties 
        SET faculty_name = :faculty_name 
        WHERE id = :id 
        RETURNING row_to_json(faculties.*);
        """
        result = self.execute_query(update_query, {
            "id": faculty_id,
            "faculty_name": faculty_name
        })
        return result.fetchone()[0]

    def delete_faculty(self, faculty_id):
        """
        Deletes a faculty by its ID.
        """
        # Check if the faculty exists
        check_query = """
        SELECT * FROM faculties WHERE id = :id;
        """
        existing_faculty = self.execute_query(check_query, {"id": faculty_id}).fetchone()
        if not existing_faculty:
            raise ValueError(f"No faculty found with ID {faculty_id} to delete.")

        # Delete the faculty
        delete_query = """
        DELETE FROM faculties WHERE id = :id;
        """
        self.execute_query(delete_query, {"id": faculty_id})
        return {"message": f"Faculty with ID {faculty_id} has been deleted."}
