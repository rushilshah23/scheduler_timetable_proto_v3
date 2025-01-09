from dataclasses import dataclass
from src.packages.timetabler.services import DatabaseService


@dataclass
class Controller():
    service:DatabaseService