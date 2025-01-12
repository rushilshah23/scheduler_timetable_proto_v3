from .base import DatabaseService

class FixedSlotAllotableService(DatabaseService):
    def create_fixed_slot_allotable(self, id, division_id, continuous_slot, weekly_frequency, fixed_slot,
                                    next_slot_id, start_time, end_time, working_day_id):
        # First, insert into the `slot_allotables` table
        query_slot_allotable = """
        INSERT INTO slot_allotables (id, division_id, continuous_slot, weekly_frequency, fixed_slot, next_slot_id)
        VALUES (:id, :division_id, :continuous_slot, :weekly_frequency, :fixed_slot, :next_slot_id);
        """
        self.execute_query(query_slot_allotable, {
            "id": id,
            "division_id": division_id,
            "continuous_slot": continuous_slot,
            "weekly_frequency": weekly_frequency,
            "fixed_slot": fixed_slot,
            "next_slot_id": next_slot_id
        })

        # Then, insert into the `fixed_slot_allotables` table
        query_fixed_slot_allotable = """
        INSERT INTO fixed_slot_allotables (id, start_time, end_time, working_day_id)
        VALUES (:id, :start_time, :end_time, :working_day_id)
        RETURNING row_to_json(fixed_slot_allotables.*);
        """
        result = self.execute_query(query_fixed_slot_allotable, {
            "id": id,
            "start_time": start_time,
            "end_time": end_time,
            "working_day_id": working_day_id
        })

        return result.fetchone()[0]

    def get_fixed_slot_allotable(self, allotable_id):
        query = """
        SELECT fs.*, sa.division_id, sa.continuous_slot, sa.weekly_frequency, sa.fixed_slot, sa.next_slot_id
        FROM fixed_slot_allotables fs
        JOIN slot_allotables sa ON fs.id = sa.id
        WHERE fs.id = :id;
        """
        result = self.execute_query(query, {"id": allotable_id}).fetchone()
        if not result:
            raise ValueError(f"No fixed slot allotable found with ID {allotable_id}.")
        return result

    def update_fixed_slot_allotable(self, allotable_id, **kwargs):
        # Split fields for `slot_allotables` and `fixed_slot_allotables`
        slot_allotable_fields = {key: kwargs.pop(key) for key in kwargs.copy() if key in [
            "division_id", "continuous_slot", "weekly_frequency", "fixed_slot", "next_slot_id"
        ]}
        fixed_slot_allotable_fields = kwargs

        if slot_allotable_fields:
            update_fields = ", ".join([f"{key} = :{key}" for key in slot_allotable_fields])
            query_slot_allotable = f"""
            UPDATE slot_allotables SET {update_fields} WHERE id = :id;
            """
            slot_allotable_fields["id"] = allotable_id
            self.execute_query(query_slot_allotable, slot_allotable_fields)

        if fixed_slot_allotable_fields:
            update_fields = ", ".join([f"{key} = :{key}" for key in fixed_slot_allotable_fields])
            query_fixed_slot_allotable = f"""
            UPDATE fixed_slot_allotables SET {update_fields} WHERE id = :id
            RETURNING row_to_json(fixed_slot_allotables.*);
            """
            fixed_slot_allotable_fields["id"] = allotable_id
            result = self.execute_query(query_fixed_slot_allotable, fixed_slot_allotable_fields).fetchone()
            if not result:
                raise ValueError(f"Failed to update fixed slot allotable with ID {allotable_id}.")
            return result[0]

    def delete_fixed_slot_allotable(self, allotable_id):
        # Delete from `fixed_slot_allotables` first due to FK constraint
        query_fixed_slot_allotable = "DELETE FROM fixed_slot_allotables WHERE id = :id RETURNING id;"
        result = self.execute_query(query_fixed_slot_allotable, {"id": allotable_id}).fetchone()
        if not result:
            raise ValueError(f"No fixed slot allotable found with ID {allotable_id} to delete.")

        # Then delete from `slot_allotables`
        query_slot_allotable = "DELETE FROM slot_allotables WHERE id = :id RETURNING id;"
        result = self.execute_query(query_slot_allotable, {"id": allotable_id}).fetchone()
        if not result:
            raise ValueError(f"No slot allotable found with ID {allotable_id} to delete.")
        return result[0]
