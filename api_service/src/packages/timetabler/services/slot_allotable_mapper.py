from .base import DatabaseService

class SlotAllotableEntityMapperService(DatabaseService):
    """
    Service class for managing operations related to the `slot_allotables_entities_mapper` table.
    """

    def create_mapping(self, slot_allotable_id, allotable_entity_id):
        """
        Creates a new slot-allotable entity mapping and inserts it into the `slot_allotables_entities_mapper` table.
        """
        insert_query = """
        INSERT INTO slot_allotables_entities_mapper (slot_allotable_id, allotable_entity_id) 
        VALUES (:slot_allotable_id, :allotable_entity_id)
        RETURNING row_to_json(slot_allotables_entities_mapper.*);
        """
        result = self.execute_query(insert_query, {
            "slot_allotable_id": slot_allotable_id,
            "allotable_entity_id": allotable_entity_id
        })
        return result.fetchone()[0]

    def get_mapping(self, slot_allotable_id, allotable_entity_id):
        """
        Fetches a slot-allotable entity mapping by its IDs.
        """
        query = """
        SELECT * FROM slot_allotables_entities_mapper 
        WHERE slot_allotable_id = :slot_allotable_id 
        AND allotable_entity_id = :allotable_entity_id;
        """
        result = self.execute_query(query, {
            "slot_allotable_id": slot_allotable_id,
            "allotable_entity_id": allotable_entity_id
        }).fetchone()
        if not result:
            raise ValueError(f"No mapping found for these IDs.")
        return result

    def delete_mapping(self, slot_allotable_id, allotable_entity_id):
        """
        Deletes a slot-allotable entity mapping.
        """
        delete_query = """
        DELETE FROM slot_allotables_entities_mapper 
        WHERE slot_allotable_id = :slot_allotable_id 
        AND allotable_entity_id = :allotable_entity_id;
        """
        self.execute_query(delete_query, {
            "slot_allotable_id": slot_allotable_id,
            "allotable_entity_id": allotable_entity_id
        })
        return {"message": f"Mapping between Slot Allotable ID {slot_allotable_id} and Entity ID {allotable_entity_id} has been deleted."}
