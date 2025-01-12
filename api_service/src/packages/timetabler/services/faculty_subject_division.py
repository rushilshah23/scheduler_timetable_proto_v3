from .base import DatabaseService

class FacultySubjectDivisionService(DatabaseService):
    def create_faculty_subject_division(self, id, faculty_id, subject_id, division_id):
        query = """
        INSERT INTO faculty_subject_division_allotables (id, faculty_id, subject_id, division_id)
        VALUES (:id, :faculty_id, :subject_id, :division_id);
        """
        self.execute_query(query, {
            "id": id,
            "faculty_id": faculty_id,
            "subject_id": subject_id,
            "division_id": division_id
        })

    def get_faculty_subject_division(self, id):
        query = """
        SELECT * FROM faculty_subject_division_allotables WHERE id = :id;
        """
        return self.execute_query(query, {"id": id}).fetchone()

    def update_faculty_subject_division(self, id, **kwargs):
        fields = ", ".join([f"{key} = :{key}" for key in kwargs])
        query = f"""
        UPDATE faculty_subject_division_allotables SET {fields} WHERE id = :id;
        """
        kwargs["id"] = id
        self.execute_query(query, kwargs)

    def delete_faculty_subject_division(self, id):
        query = """
        DELETE FROM faculty_subject_division_allotables WHERE id = :id;
        """
        self.execute_query(query, {"id": id})

