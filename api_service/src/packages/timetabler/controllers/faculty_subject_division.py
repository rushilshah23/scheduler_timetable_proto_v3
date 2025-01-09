from .base import DatabaseService

class FacultySubjectDivisionService(DatabaseService):
    """
    Service class for managing operations related to the `faculty_subject_division_allotables` table.
    """

    def create_faculty_subject_division(self, id, faculty_id, subject_id, division_id):
        """
        Creates a new faculty-subject-division allotment and inserts it into the `faculty_subject_division_allotables` table.
        """
        # Insert the new faculty-subject-division allotment
        insert_query = """
        INSERT INTO faculty_subject_division_allotables (id, faculty_id, subject_id, division_id) 
        VALUES (:id, :faculty_id, :subject_id, :division_id)
        RETURNING row_to_json(faculty_subject_division_allotables.*);
        """
        result = self.execute_query(insert_query, {
            "id": id,
            "faculty_id": faculty_id,
            "subject_id": subject_id,
            "division_id": division_id
        })
        return result.fetchone()[0]

    def get_faculty_subject_division(self, allotable_id):
        """
        Fetches a faculty-subject-division allotment by its ID.
        """
        query = """
        SELECT * FROM faculty_subject_division_allotables WHERE id = :id;
        """
        result = self.execute_query(query, {"id": allotable_id}).fetchone()
        if not result:
            raise ValueError(f"No allotment found with ID {allotable_id}.")
        return result

    def delete_faculty_subject_division(self, allotable_id):
        """
        Deletes a faculty-subject-division allotment by its ID.
        """
        delete_query = """
        DELETE FROM faculty_subject_division_allotables WHERE id = :id;
        """
        self.execute_query(delete_query, {"id": allotable_id})
        return {"message": f"Allotment with ID {allotable_id} has been deleted."}
