from .base import DatabaseService

class SlotService(DatabaseService):
    def create_slot(self, id, start_time, end_time, working_day_id, daily_slot_number, weekly_slot_number, slot_alloted_to_allotable_entity_mapper_id):
        query = """
        INSERT INTO slots (id, start_time, end_time, working_day_id, daily_slot_number, weekly_slot_number, slot_alloted_to_id) 
        VALUES (:id, :start_time, :end_time, :working_day_id, :daily_slot_number, :weekly_slot_number, :slot_alloted_to_allotable_entity_mapper_id)
        RETURNING row_to_json(slots.*);
        """
        result = self.execute_query(query, {
            "id": id,
            "start_time": start_time,
            "end_time": end_time,
            "working_day_id": working_day_id,
            "daily_slot_number": daily_slot_number,
            "weekly_slot_number": weekly_slot_number,
            "slot_alloted_to_allotable_entity_mapper_id": slot_alloted_to_allotable_entity_mapper_id
        })
        return result.fetchone()[0]

    def get_slot(self, slot_id):
        query = "SELECT * FROM slots WHERE id = :id;"
        result = self.execute_query(query, {"id": slot_id}).fetchone()
        if not result:
            raise ValueError(f"No slot found with ID {slot_id}.")
        return result

    def update_slot(self, slot_id, **kwargs):
        update_fields = ", ".join([f"{key} = :{key}" for key in kwargs])
        query = f"""
        UPDATE slots SET {update_fields} WHERE id = :id RETURNING row_to_json(slots.*);
        """
        params = kwargs
        params["id"] = slot_id

        result = self.execute_query(query, params).fetchone()
        if not result:
            raise ValueError(f"Failed to update slot with ID {slot_id}.")
        return result[0]

    def delete_slot(self, slot_id):
        query = "DELETE FROM slots WHERE id = :id RETURNING id;"
        result = self.execute_query(query, {"id": slot_id}).fetchone()
        if not result:
            raise ValueError(f"No slot found with ID {slot_id} to delete.")
        return result[0]
