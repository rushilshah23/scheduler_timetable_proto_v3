from .base import DatabaseService


class DayService(DatabaseService):
    """
    Service class for managing `days` table operations.
    """

    def create_day(self, id, day_name):
        """
        Inserts a new day into the `days` table, ensuring no duplicate entries.
        The day name is case-insensitive and stored in lowercase.
        """
        # Normalize day_name to lowercase
        normalized_day_name = day_name.strip().lower()

        # Check if the day already exists
        check_query = """
        SELECT * FROM days WHERE id = :id OR day_name = :day_name;
        """
        existing_day = self.execute_query(check_query, {"id": id, "day_name": normalized_day_name}).fetchone()

        if existing_day:
            raise ValueError(f"Day with ID {id} or name '{day_name}' already exists in the database.")

        # Insert the new day
        insert_query = """
        INSERT INTO days (id, day_name) VALUES (:id, :day_name) 
        RETURNING row_to_json(days.*);
        """
        result = self.execute_query(insert_query, {"id": id, "day_name": normalized_day_name})
        return result.fetchone()[0]

    def get_day(self, day_id):
        """
        Fetches a day by its ID.
        """
        query = """
        SELECT * FROM days WHERE id = :id;
        """
        result = self.execute_query(query, {"id": day_id}).fetchone()
        if not result:
            raise ValueError(f"No day found with ID {day_id}.")
        return result

    def update_day(self, day_id, new_day_name):
        """
        Updates the name of a day given its ID.
        The day name is case-insensitive and stored in lowercase.
        """
        # Check if the day exists
        check_query = """
        SELECT * FROM days WHERE id = :id;
        """
        existing_day = self.execute_query(check_query, {"id": day_id}).fetchone()
        if not existing_day:
            raise ValueError(f"No day found with ID {day_id} to update.")

        # Normalize new_day_name to lowercase
        normalized_new_day_name = new_day_name.strip().lower()

        # Check for duplicate day name (excluding the current day)
        duplicate_query = """
        SELECT * FROM days WHERE day_name = :day_name AND id != :id;
        """
        duplicate_day = self.execute_query(duplicate_query, {"day_name": normalized_new_day_name, "id": day_id}).fetchone()
        if duplicate_day:
            raise ValueError(f"Day name '{new_day_name}' already exists in the database.")

        # Update the day
        query = """
        UPDATE days SET day_name = :new_day_name WHERE id = :id RETURNING row_to_json(days.*);
        """
        result = self.execute_query(query, {"id": day_id, "new_day_name": normalized_new_day_name})
        return result.fetchone()[0]

    def delete_day(self, day_id):
        """
        Deletes a day by its ID.
        """
        # Check if the day exists
        check_query = """
        SELECT * FROM days WHERE id = :id;
        """
        existing_day = self.execute_query(check_query, {"id": day_id}).fetchone()
        if not existing_day:
            raise ValueError(f"No day found with ID {day_id} to delete.")

        # Delete the day
        query = """
        DELETE FROM days WHERE id = :id;
        """
        self.execute_query(query, {"id": day_id})
        return {"message": f"Day with ID {day_id} has been deleted."}
