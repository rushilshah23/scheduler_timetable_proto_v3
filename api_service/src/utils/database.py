from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from flask import Flask
from sqlalchemy.orm import Session

# Declare the engine and session maker as global variables
Base = declarative_base()
engine = None
SessionLocal = None

def init_db(app: Flask):
    global engine, SessionLocal

    # Read the DATABASE_URL from the Flask config
    database_url = app.config['DATABASE_URL']
    print(f"Connecting to database at {database_url}")
    
    # Create the SQLAlchemy engine
    engine = create_engine(database_url,     pool_size=10,  # Max number of connections in the pool
    max_overflow=5,  # Additional connections beyond pool_size
    pool_timeout=30,  # Timeout for acquiring a connection
    pool_pre_ping=True)  # Check connections' validity before using them  # Added pool_pre_ping for more robust connection handling
    
    # Create a session factory (SessionLocal)
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

    # Create tables if they don't exist (but only on app startup, not every request)
    import  src.packages.timetabler.models 
    Base.metadata.create_all(bind=engine)
    print("Database tables created successfully or already exist.")


# Helper function to get the DB session
def get_db():
    """Get a database session."""
    if SessionLocal is None:
        raise RuntimeError("SessionLocal is not initialized. Ensure the database is configured before usage.")
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()