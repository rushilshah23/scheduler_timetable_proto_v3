from .routers import DayRouter
from .services import DayService
from .controllers import DayController
from src.utils.database import engine


day_router = DayRouter(
    router_name="day_api",
    controller=DayController(service=DayService(engine=engine)),
    service=DayService(engine=engine)
)