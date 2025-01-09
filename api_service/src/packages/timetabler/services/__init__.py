from .base import DatabaseService
from .day import DayService
from .allotable_entity import AllotableEntityService
from .breaks import BreakService
from .department import DepartmentService
from .division import DivisionService
from .faculty import FacultyService
from .faculty_subject_division import FacultySubjectDivisionService
from .fixed_slot_allotable import FixedSlotAllotableService
from .slot import SlotService
from .slot_allotable import SlotAllotableService
from .slot_allotable_mapper import SlotAllotableEntityMapperService
from .standard import StandardService
from .subject import SubjectService
from .unfixed_slot_allotable import UnFixedSlotAllotableService
from .university import UniversityService
from .working_day import WorkingDayService


__all__ = (
    DatabaseService,
    DayService,
    AllotableEntityService,
    BreakService,
    DepartmentService,
    DivisionService,
    FacultyService,
    FacultySubjectDivisionService,
    FixedSlotAllotableService,
    SlotService,
    SlotAllotableService,
    SlotAllotableEntityMapperService,
    StandardService,
    SubjectService,
    UnFixedSlotAllotableService,
    UniversityService,
    WorkingDayService

    
)
