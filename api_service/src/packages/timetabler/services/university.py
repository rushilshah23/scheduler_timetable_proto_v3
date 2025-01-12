from .base import DatabaseService

class UniversityService(DatabaseService):
    def create_university(self, id, name, logo):
        query = """
        INSERT INTO universities (id, name, logo)
        VALUES (:id, :name, :logo) RETURNING row_to_json(universities.*);
        """
        result = self.execute_query(query, {"id": id, "name": name, "logo": logo})
        return result.fetchone()[0]

    def get_university(self, university_id):
        query = "SELECT * FROM universities WHERE id = :id;"
        result = self.execute_query(query, {"id": university_id}).fetchone()
        if not result:
            raise ValueError(f"No university found with ID {university_id}.")
        return result

    def update_university(self, university_id, **kwargs):
        update_fields = ", ".join([f"{key} = :{key}" for key in kwargs])
        query = f"""
        UPDATE universities SET {update_fields} WHERE id = :id RETURNING row_to_json(universities.*);
        """
        params = kwargs
        params["id"] = university_id

        result = self.execute_query(query, params).fetchone()
        if not result:
            raise ValueError(f"Failed to update university with ID {university_id}.")
        return result[0]

    def delete_university(self, university_id):
        query = "DELETE FROM universities WHERE id = :id RETURNING id;"
        result = self.execute_query(query, {"id": university_id}).fetchone()
        if not result:
            raise ValueError(f"No university found with ID {university_id} to delete.")
        return result[0]

    def list_universities(self):
        query = "SELECT * FROM universities;"
        result = self.execute_query(query)
        return [row for row in result.fetchall()]
