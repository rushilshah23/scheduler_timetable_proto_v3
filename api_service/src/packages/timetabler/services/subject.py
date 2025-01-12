from .base import DatabaseService

class SubjectService(DatabaseService):
    def create_subject(self, id, name, university_id):
        query = """
        INSERT INTO subjects (id, name, university_id)
        VALUES (:id, :name, :university_id) RETURNING row_to_json(subjects.*);
        """
        result = self.execute_query(query, {"id": id, "name": name, "university_id": university_id})
        return result.fetchone()[0]

    def get_subject(self, subject_id):
        query = "SELECT * FROM subjects WHERE id = :id;"
        result = self.execute_query(query, {"id": subject_id}).fetchone()
        if not result:
            raise ValueError(f"No subject found with ID {subject_id}.")
        return result

    def update_subject(self, subject_id, **kwargs):
        update_fields = ", ".join([f"{key} = :{key}" for key in kwargs])
        query = f"""
        UPDATE subjects SET {update_fields} WHERE id = :id RETURNING row_to_json(subjects.*);
        """
        params = kwargs
        params["id"] = subject_id

        result = self.execute_query(query, params).fetchone()
        if not result:
            raise ValueError(f"Failed to update subject with ID {subject_id}.")
        return result[0]

    def delete_subject(self, subject_id):
        query = "DELETE FROM subjects WHERE id = :id RETURNING id;"
        result = self.execute_query(query, {"id": subject_id}).fetchone()
        if not result:
            raise ValueError(f"No subject found with ID {subject_id} to delete.")
        return result[0]
