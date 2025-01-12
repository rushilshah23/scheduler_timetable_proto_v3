from .base import DatabaseService

class UnFixedSlotAllotableService(DatabaseService):
    def create_unfixed_slot_allotable(self, id):
        query = """
        INSERT INTO unfixed_slot_allotables (id)
        VALUES (:id);
        """
        self.execute_query(query, {"id": id})

    def get_unfixed_slot_allotable(self, id):
        query = """
        SELECT * FROM unfixed_slot_allotables WHERE id = :id;
        """
        return self.execute_query(query, {"id": id}).fetchone()

    def delete_unfixed_slot_allotable(self, id):
        query = """
        DELETE FROM unfixed_slot_allotables WHERE id = :id;
        """
        self.execute_query(query, {"id": id})
 