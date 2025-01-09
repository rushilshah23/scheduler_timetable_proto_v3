from .base import DatabaseService

class AllotableEntityService(DatabaseService):
    """
    Service class for managing `allotable_entities` table operations.
    """

    def create_allotable_entity(self, id):
        """
        Inserts a new allotable entity into the `allotable_entities` table.
        """
        # Check if the allotable entity already exists with the same id
        check_query = """
        SELECT * FROM allotable_entities WHERE id = :id;
        """
        existing_entity = self.execute_query(check_query, {"id": id}).fetchone()

        if existing_entity:
            raise ValueError(f"Allotable Entity with ID {id} already exists in the database.")

        # Insert the new allotable entity
        insert_query = """
        INSERT INTO allotable_entities (id) 
        VALUES (:id) 
        RETURNING row_to_json(allotable_entities.*);
        """
        result = self.execute_query(insert_query, {
            "id": id
        })
        return result.fetchone()[0]

    def get_allotable_entity(self, entity_id):
        """
        Fetches an allotable entity by its ID.
        """
        query = """
        SELECT * FROM allotable_entities WHERE id = :id;
        """
        result = self.execute_query(query, {"id": entity_id}).fetchone()
        if not result:
            raise ValueError(f"No allotable entity found with ID {entity_id}.")
        return result

    def update_allotable_entity(self, entity_id, new_id):
        """
        Updates the details of an allotable entity given its ID.
        """
        # Check if the allotable entity exists
        check_query = """
        SELECT * FROM allotable_entities WHERE id = :id;
        """
        existing_entity = self.execute_query(check_query, {"id": entity_id}).fetchone()
        if not existing_entity:
            raise ValueError(f"No allotable entity found with ID {entity_id} to update.")
        
        # Update the allotable entity
        update_query = """
        UPDATE allotable_entities 
        SET id = :new_id 
        WHERE id = :id 
        RETURNING row_to_json(allotable_entities.*);
        """
        result = self.execute_query(update_query, {
            "id": entity_id,
            "new_id": new_id
        })
        return result.fetchone()[0]

    def delete_allotable_entity(self, entity_id):
        """
        Deletes an allotable entity by its ID.
        """
        # Check if the allotable entity exists
        check_query = """
        SELECT * FROM allotable_entities WHERE id = :id;
        """
        existing_entity = self.execute_query(check_query, {"id": entity_id}).fetchone()
        if not existing_entity:
            raise ValueError(f"No allotable entity found with ID {entity_id} to delete.")

        # Delete the allotable entity
        delete_query = """
        DELETE FROM allotable_entities WHERE id = :id;
        """
        self.execute_query(delete_query, {"id": entity_id})
        return {"message": f"Allotable Entity with ID {entity_id} has been deleted."}
