from sqlalchemy.sql import text
from sqlalchemy.exc import IntegrityError

class CRUDUtilities:
    def __init__(self, db_session):
        self.db_session = db_session

    def create_day(self, day_data: dict):
        try:
            query = text("""
                INSERT INTO days (id, day_name)
                VALUES (:id, :day_name)
            """)
            self.db_session.execute(query, {"id": day_data['id'], "day_name": day_data['day_name']})
            self.db_session.commit()
        except IntegrityError:
            self.db_session.rollback()
            raise ValueError(f"Day with id {day_data['id']} already exists.")

    def get_day(self, day_id: str):
        query = text("""
            SELECT * FROM days WHERE id = :id
        """)
        result = self.db_session.execute(query, {"id": day_id}).fetchone()
        return result

    def update_day(self, day_id: str, day_data: dict):
        query = text("""
            UPDATE days
            SET day_name = :day_name
            WHERE id = :id
        """)
        result = self.db_session.execute(query, {"id": day_id, "day_name": day_data['day_name']})
        self.db_session.commit()
        return result

    def delete_day(self, day_id: str):
        query = text("""
            DELETE FROM days WHERE id = :id
        """)
        result = self.db_session.execute(query, {"id": day_id})
        self.db_session.commit()
        return result

    def create_university(self, university_data: dict):
        try:
            query = text("""
                INSERT INTO universities (id, university_name)
                VALUES (:id, :university_name)
            """)
            self.db_session.execute(query, {"id": university_data['id'], "university_name": university_data['university_name']})
            self.db_session.commit()
        except IntegrityError:
            self.db_session.rollback()
            raise ValueError(f"University with id {university_data['id']} already exists.")

    def get_university(self, university_id: str):
        query = text("""
            SELECT * FROM universities WHERE id = :id
        """)
        result = self.db_session.execute(query, {"id": university_id}).fetchone()
        return result

    def update_university(self, university_id: str, university_data: dict):
        query = text("""
            UPDATE universities
            SET university_name = :university_name
            WHERE id = :id
        """)
        result = self.db_session.execute(query, {"id": university_id, "university_name": university_data['university_name']})
        self.db_session.commit()
        return result

    def delete_university(self, university_id: str):
        query = text("""
            DELETE FROM universities WHERE id = :id
        """)
        result = self.db_session.execute(query, {"id": university_id})
        self.db_session.commit()
        return result

    def create_department(self, department_data: dict):
        try:
            query = text("""
                INSERT INTO departments (id, department_name, university_id)
                VALUES (:id, :department_name, :university_id)
            """)
            self.db_session.execute(query, {
                "id": department_data['id'],
                "department_name": department_data['department_name'],
                "university_id": department_data['university_id']
            })
            self.db_session.commit()
        except IntegrityError:
            self.db_session.rollback()
            raise ValueError(f"Department with id {department_data['id']} already exists.")

    def get_department(self, department_id: str):
        query = text("""
            SELECT * FROM departments WHERE id = :id
        """)
        result = self.db_session.execute(query, {"id": department_id}).fetchone()
        return result

    def update_department(self, department_id: str, department_data: dict):
        query = text("""
            UPDATE departments
            SET department_name = :department_name, university_id = :university_id
            WHERE id = :id
        """)
        result = self.db_session.execute(query, {
            "id": department_id,
            "department_name": department_data['department_name'],
            "university_id": department_data['university_id']
        })
        self.db_session.commit()
        return result

    def delete_department(self, department_id: str):
        query = text("""
            DELETE FROM departments WHERE id = :id
        """)
        result = self.db_session.execute(query, {"id": department_id})
        self.db_session.commit()
        return result

    # Similar changes are applied for all the other CRUD methods like `create_standard`, `get_standard`, `update_standard`, etc.

    def create_standard(self, standard_data: dict):
        try:
            query = text("""
                INSERT INTO standards (id, standard_name, department_id)
                VALUES (:id, :standard_name, :department_id)
            """)
            self.db_session.execute(query, {
                "id": standard_data['id'],
                "standard_name": standard_data['standard_name'],
                "department_id": standard_data['department_id']
            })
            self.db_session.commit()
        except IntegrityError:
            self.db_session.rollback()
            raise ValueError(f"Standard with id {standard_data['id']} already exists.")

    def get_standard(self, standard_id: str):
        query = text("""
            SELECT * FROM standards WHERE id = :id
        """)
        result = self.db_session.execute(query, {"id": standard_id}).fetchone()
        return result

    def update_standard(self, standard_id: str, standard_data: dict):
        query = text("""
            UPDATE standards
            SET standard_name = :standard_name, department_id = :department_id
            WHERE id = :id
        """)
        result = self.db_session.execute(query, {
            "id": standard_id,
            "standard_name": standard_data['standard_name'],
            "department_id": standard_data['department_id']
        })
        self.db_session.commit()
        return result

    def delete_standard(self, standard_id: str):
        query = text("""
            DELETE FROM standards WHERE id = :id
        """)
        result = self.db_session.execute(query, {"id": standard_id})
        self.db_session.commit()
        return result
