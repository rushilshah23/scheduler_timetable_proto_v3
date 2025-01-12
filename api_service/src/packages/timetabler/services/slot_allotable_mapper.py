from .base import DatabaseService

class SlotAllotableEntityMapperService(DatabaseService):
    def create_mapping(self, slot_allotable_id, allotable_entity_id):
        query = """
        INSERT INTO slot_allotables_entities_mapper (slot_allotable_id, allotable_entity_id)
        VALUES (:slot_allotable_id, :allotable_entity_id);
        """
        self.execute_query(query, {
            "slot_allotable_id": slot_allotable_id,
            "allotable_entity_id": allotable_entity_id
        })

    def get_mapping(self, slot_allotable_id, allotable_entity_id):
        query = """
        SELECT * FROM slot_allotables_entities_mapper
        WHERE slot_allotable_id = :slot_allotable_id AND allotable_entity_id = :allotable_entity_id;
        """
        return self.execute_query(query, {
            "slot_allotable_id": slot_allotable_id,
            "allotable_entity_id": allotable_entity_id
        }).fetchone()

    def delete_mapping(self, slot_allotable_id, allotable_entity_id):
        query = """
        DELETE FROM slot_allotables_entities_mapper
        WHERE slot_allotable_id = :slot_allotable_id AND allotable_entity_id = :allotable_entity_id;
        """
        self.execute_query(query, {
            "slot_allotable_id": slot_allotable_id,
            "allotable_entity_id": allotable_entity_id
        })
