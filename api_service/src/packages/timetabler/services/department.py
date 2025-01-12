from .base import DatabaseService

class DepartmentService(DatabaseService):
    def create_department(self, id, name, university_id):
        query = """
        INSERT INTO departments (id, name, university_id)
        VALUES (:id, :name, :university_id) RETURNING row_to_json(departments.*);
        """
        result = self.execute_query(query, {"id": id, "name": name, "university_id": university_id})
        return result.fetchone()[0]

    def get_department(self, department_id):
        query = "SELECT * FROM departments WHERE id = :id;"
        result = self.execute_query(query, {"id": department_id}).fetchone()
        if not result:
            raise ValueError(f"No department found with ID {department_id}.")
        return result

    def update_department(self, department_id, **kwargs):
        update_fields = ", ".join([f"{key} = :{key}" for key in kwargs])
        query = f"""
        UPDATE departments SET {update_fields} WHERE id = :id RETURNING row_to_json(departments.*);
        """
        params = kwargs
        params["id"] = department_id

        result = self.execute_query(query, params).fetchone()
        if not result:
            raise ValueError(f"Failed to update department with ID {department_id}.")
        return result[0]

    def delete_department(self, department_id):
        query = "DELETE FROM departments WHERE id = :id RETURNING id;"
        result = self.execute_query(query, {"id": department_id}).fetchone()
        if not result:
            raise ValueError(f"No department found with ID {department_id} to delete.")
        return result[0]

    def list_departments(self, university_id=None):
        if university_id:
            query = "SELECT * FROM departments WHERE university_id = :university_id;"
            result = self.execute_query(query, {"university_id": university_id})
        else:
            query = "SELECT * FROM departments;"
            result = self.execute_query(query)
        return [row for row in result.fetchall()]
