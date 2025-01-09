from .base import DatabaseService

class DepartmentService(DatabaseService):
    """
    Service class for managing operations related to the `departments` table.
    """

    def create_department(self, id, department_name, university_id):
        """
        Creates a new department and inserts it into the `departments` table.
        """
        # Check if the department already exists with the same id
        check_query = """
        SELECT * FROM departments WHERE id = :id;
        """
        existing_department = self.execute_query(check_query, {"id": id}).fetchone()

        if existing_department:
            raise ValueError(f"Department with ID {id} already exists.")

        # Check if the university exists
        check_university_query = """
        SELECT * FROM universities WHERE id = :university_id;
        """
        university = self.execute_query(check_university_query, {"university_id": university_id}).fetchone()
        if not university:
            raise ValueError(f"No university found with ID {university_id}.")

        # Insert the new department
        insert_query = """
        INSERT INTO departments (id, department_name, university_id) 
        VALUES (:id, :department_name, :university_id) 
        RETURNING row_to_json(departments.*);
        """
        result = self.execute_query(insert_query, {
            "id": id,
            "department_name": department_name,
            "university_id": university_id
        })
        return result.fetchone()[0]

    def get_department(self, department_id):
        """
        Fetches a department by its ID.
        """
        query = """
        SELECT * FROM departments WHERE id = :id;
        """
        result = self.execute_query(query, {"id": department_id}).fetchone()
        if not result:
            raise ValueError(f"No department found with ID {department_id}.")
        return result

    def update_department(self, department_id, department_name, university_id):
        """
        Updates the details of a department.
        """
        # Check if the department exists
        check_query = """
        SELECT * FROM departments WHERE id = :id;
        """
        existing_department = self.execute_query(check_query, {"id": department_id}).fetchone()
        if not existing_department:
            raise ValueError(f"No department found with ID {department_id} to update.")

        # Check if the university exists
        check_university_query = """
        SELECT * FROM universities WHERE id = :university_id;
        """
        university = self.execute_query(check_university_query, {"university_id": university_id}).fetchone()
        if not university:
            raise ValueError(f"No university found with ID {university_id}.")

        # Update the department details
        update_query = """
        UPDATE departments 
        SET department_name = :department_name, university_id = :university_id
        WHERE id = :id
        RETURNING row_to_json(departments.*);
        """
        result = self.execute_query(update_query, {
            "id": department_id,
            "department_name": department_name,
            "university_id": university_id
        })
        return result.fetchone()[0]

    def delete_department(self, department_id):
        """
        Deletes a department by its ID.
        """
        # Check if the department exists
        check_query = """
        SELECT * FROM departments WHERE id = :id;
        """
        existing_department = self.execute_query(check_query, {"id": department_id}).fetchone()
        if not existing_department:
            raise ValueError(f"No department found with ID {department_id} to delete.")

        # Delete the department
        delete_query = """
        DELETE FROM departments WHERE id = :id;
        """
        self.execute_query(delete_query, {"id": department_id})
        return {"message": f"Department with ID {department_id} has been deleted."}
