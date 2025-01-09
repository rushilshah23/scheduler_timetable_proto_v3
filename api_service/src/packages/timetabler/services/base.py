from sqlalchemy import text
from sqlalchemy.orm import scoped_session
from sqlalchemy.exc import SQLAlchemyError

class DatabaseService:
    def __init__(self, engine, autocommit=False):
        self.engine = engine
        self.autocommit = autocommit

    def execute_query(self, query, params=None):
        try:
            with self.engine.connect() as connection:
                if self.autocommit:
                    result = connection.execute(text(query), params or {})
                    return result
                else:
                    transaction = connection.begin()
                    try:
                        result = connection.execute(text(query), params or {})
                        transaction.commit()
                        return result
                    except SQLAlchemyError as e:
                        transaction.rollback()
                        raise e
        except SQLAlchemyError as e:
            print(f"Database error: {e}")
            raise