from flask import Flask
from src.utils.database import init_db, SessionLocal
from src.configs.base import Config
from src.utils.celery import celery_init_app

from src.packages.timetabler.routers import DayRouter
from src.packages.timetabler.services import DayService
from src.packages.timetabler.controllers import DayController


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    # Initialize the database
    init_db(app)
    celery_init_app(app)
    from src.packages.timetabler.routes import timetable_router
    from src.utils.database import engine
    day_router = DayRouter(
        router_name="day_api",
        controller=DayController(service=DayService(engine=engine)),
        service=DayService(engine=engine)
    )
    app.register_blueprint(day_router.api)

    # Register blueprints
    app.register_blueprint(timetable_router, url_prefix="/timetable")

    # Register lifecycle events
    # register_lifecycle_events(app)

    return app

def register_lifecycle_events(app):
    @app.before_first_request
    def startup():
        """
        Lifecycle event: Establish a database connection at startup.
        """
        # The database connection setup is usually handled by SQLAlchemy.
        # If you need specific logic, implement it here.

    @app.teardown_appcontext
    def shutdown(exception=None):
        """
        Lifecycle event: Disconnect the database when app context ends.
        """
        # If using scoped sessions, remove them here
        # SessionLocal().close()
