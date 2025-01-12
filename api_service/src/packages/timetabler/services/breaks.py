from .base import DatabaseService



class BreakService(DatabaseService):
    def create_break(self, id, name):
        query = """
        INSERT INTO breaks (id, name) 
        VALUES (:id, :name) 
        RETURNING row_to_json(breaks.*);
        """
        result = self.execute_query(query, {"id": id, "name": name})
        return result.fetchone()[0]

    def get_break(self, break_id):
        query = "SELECT * FROM breaks WHERE id = :id;"
        result = self.execute_query(query, {"id": break_id}).fetchone()
        if not result:
            raise ValueError(f"No break found with ID {break_id}.")
        return result

    def delete_break(self, break_id):
        query = "DELETE FROM breaks WHERE id = :id RETURNING id;"
        result = self.execute_query(query, {"id": break_id}).fetchone()
        if not result:
            raise ValueError(f"No break found with ID {break_id} to delete.")
        return result[0]
