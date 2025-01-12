from .base import DatabaseService

class DayService(DatabaseService):
    def create_day(self, id, name):
        query = """
        INSERT INTO days (id, name) 
        VALUES (:id, :name) RETURNING row_to_json(days.*);
        """
        result = self.execute_query(query, {"id": id, "name": name})
        return result.fetchone()[0]

    def get_day(self, day_id):
        query = "SELECT * FROM days WHERE id = :id;"
        result = self.execute_query(query, {"id": day_id}).fetchone()
        if not result:
            raise ValueError(f"No day found with ID {day_id}.")
        return result

    def update_day(self, day_id, **kwargs):
        update_fields = ", ".join([f"{key} = :{key}" for key in kwargs])
        query = f"""
        UPDATE days SET {update_fields} WHERE id = :id RETURNING row_to_json(days.*);
        """
        params = kwargs
        params["id"] = day_id

        result = self.execute_query(query, params).fetchone()
        if not result:
            raise ValueError(f"Failed to update day with ID {day_id}.")
        return result[0]

    def delete_day(self, day_id):
        query = "DELETE FROM days WHERE id = :id RETURNING id;"
        result = self.execute_query(query, {"id": day_id}).fetchone()
        if not result:
            raise ValueError(f"No day found with ID {day_id} to delete.")
        return result[0]
