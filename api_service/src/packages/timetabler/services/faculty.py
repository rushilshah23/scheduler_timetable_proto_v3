from .base import DatabaseService

class FacultyService(DatabaseService):
    def create_faculty(self, id, name, university_id):
        query = """
        INSERT INTO faculties (id, name, university_id)
        VALUES (:id, :name, :university_id);
        """
        self.execute_query(query, {"id": id, "name": name, "university_id": university_id})

    def get_faculty(self, id):
        query = """
        SELECT * FROM faculties WHERE id = :id;
        """
        return self.execute_query(query, {"id": id}).fetchone()

    def update_faculty(self, id, **kwargs):
        fields = ", ".join([f"{key} = :{key}" for key in kwargs])
        query = f"""
        UPDATE faculties SET {fields} WHERE id = :id;
        """
        kwargs["id"] = id
        self.execute_query(query, kwargs)

    def delete_faculty(self, id):
        query = """
        DELETE FROM faculties WHERE id = :id;
        """
        self.execute_query(query, {"id": id})
