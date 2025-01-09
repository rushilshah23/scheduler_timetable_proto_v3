from .base import DatabaseService

class SubjectService(DatabaseService):
    """
    Service class for managing operations related to the `subjects` table.
    """

    def create_subject(self, id, subject_name):
        """
        Creates a new subject and inserts it into the `subjects` table.
        """
        # Check if the subject already exists with the same id
        check_query = """
        SELECT * FROM subjects WHERE id = :id;
        """
        existing_subject = self.execute_query(check_query, {"id": id}).fetchone()

        if existing_subject:
            raise ValueError(f"Subject with ID {id} already exists.")

        # Insert the new subject
        insert_query = """
        INSERT INTO subjects (id, subject_name) 
        VALUES (:id, :subject_name) 
        RETURNING row_to_json(subjects.*);
        """
        result = self.execute_query(insert_query, {"id": id, "subject_name": subject_name})
        return result.fetchone()[0]

    def get_subject(self, subject_id):
        """
        Fetches a subject by its ID.
        """
        query = """
        SELECT * FROM subjects WHERE id = :id;
        """
        result = self.execute_query(query, {"id": subject_id}).fetchone()
        if not result:
            raise ValueError(f"No subject found with ID {subject_id}.")
        return result

    def update_subject(self, subject_id, subject_name):
        """
        Updates the details of a subject.
        """
        # Check if the subject exists
        check_query = """
        SELECT * FROM subjects WHERE id = :id;
        """
        existing_subject = self.execute_query(check_query, {"id": subject_id}).fetchone()
        if not existing_subject:
            raise ValueError(f"No subject found with ID {subject_id} to update.")

        # Update the subject details
        update_query = """
        UPDATE subjects 
        SET subject_name = :subject_name 
        WHERE id = :id 
        RETURNING row_to_json(subjects.*);
        """
        result = self.execute_query(update_query, {
            "id": subject_id,
            "subject_name": subject_name
        })
        return result.fetchone()[0]

    def delete_subject(self, subject_id):
        """
        Deletes a subject by its ID.
        """
        # Check if the subject exists
        check_query = """
        SELECT * FROM subjects WHERE id = :id;
        """
        existing_subject = self.execute_query(check_query, {"id": subject_id}).fetchone()
        if not existing_subject:
            raise ValueError(f"No subject found with ID {subject_id} to delete.")

        # Delete the subject
        delete_query = """
        DELETE FROM subjects WHERE id = :id;
        """
        self.execute_query(delete_query, {"id": subject_id})
        return {"message": f"Subject with ID {subject_id} has been deleted."}
