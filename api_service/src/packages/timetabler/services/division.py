from .base import DatabaseService

class DivisionService(DatabaseService):
    def create_division(self, id, name, standard_id):
        query = """
        INSERT INTO divisions (id, name, standard_id)
        VALUES (:id, :name, :standard_id) RETURNING row_to_json(divisions.*);
        """
        result = self.execute_query(query, {"id": id, "name": name, "standard_id": standard_id})
        return result.fetchone()[0]

    def get_division(self, division_id):
        query = "SELECT * FROM divisions WHERE id = :id;"
        result = self.execute_query(query, {"id": division_id}).fetchone()
        if not result:
            raise ValueError(f"No division found with ID {division_id}.")
        return result

    def update_division(self, division_id, **kwargs):
        update_fields = ", ".join([f"{key} = :{key}" for key in kwargs])
        query = f"""
        UPDATE divisions SET {update_fields} WHERE id = :id RETURNING row_to_json(divisions.*);
        """
        params = kwargs
        params["id"] = division_id

        result = self.execute_query(query, params).fetchone()
        if not result:
            raise ValueError(f"Failed to update division with ID {division_id}.")
        return result[0]

    def delete_division(self, division_id):
        query = "DELETE FROM divisions WHERE id = :id RETURNING id;"
        result = self.execute_query(query, {"id": division_id}).fetchone()
        if not result:
            raise ValueError(f"No division found with ID {division_id} to delete.")
        return result[0]

    def list_divisions(self, standard_id=None):
        if standard_id:
            query = "SELECT * FROM divisions WHERE standard_id = :standard_id;"
            result = self.execute_query(query, {"standard_id": standard_id})
        else:
            query = "SELECT * FROM divisions;"
            result = self.execute_query(query)
        return [row for row in result.fetchall()]
