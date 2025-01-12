from .base import DatabaseService

class SlotAllotableService(DatabaseService):
    def create_slot_allotable(self, id, division_id, continuous_slot, weekly_frequency, fixed_slot, next_slot_id):
        query = """
        INSERT INTO slot_allotables (id, division_id, continuous_slot, weekly_frequency, fixed_slot, next_slot_id) 
        VALUES (:id, :division_id, :continuous_slot, :weekly_frequency, :fixed_slot, :next_slot_id)
        RETURNING row_to_json(slot_allotables.*);
        """
        result = self.execute_query(query, {
            "id": id,
            "division_id": division_id,
            "continuous_slot": continuous_slot,
            "weekly_frequency": weekly_frequency,
            "fixed_slot": fixed_slot,
            "next_slot_id": next_slot_id
        })
        return result.fetchone()[0]

    def get_slot_allotable(self, allotable_id):
        query = "SELECT * FROM slot_allotables WHERE id = :id;"
        result = self.execute_query(query, {"id": allotable_id}).fetchone()
        if not result:
            raise ValueError(f"No slot allotable found with ID {allotable_id}.")
        return result

    def update_slot_allotable(self, allotable_id, **kwargs):
        update_fields = ", ".join([f"{key} = :{key}" for key in kwargs])
        query = f"""
        UPDATE slot_allotables SET {update_fields} WHERE id = :id RETURNING row_to_json(slot_allotables.*);
        """
        params = kwargs
        params["id"] = allotable_id

        result = self.execute_query(query, params).fetchone()
        if not result:
            raise ValueError(f"Failed to update slot allotable with ID {allotable_id}.")
        return result[0]

    def delete_slot_allotable(self, allotable_id):
        query = "DELETE FROM slot_allotables WHERE id = :id RETURNING id;"
        result = self.execute_query(query, {"id": allotable_id}).fetchone()
        if not result:
            raise ValueError(f"No slot allotable found with ID {allotable_id} to delete.")
        return result[0]
