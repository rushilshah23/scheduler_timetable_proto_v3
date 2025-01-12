from dataclasses import dataclass, field
from typing import List, Optional
from datetime import time
from src.packages.ga import Gene, Chromosome
from src.packages.timetabler.models_v2 import Day, WorkingDay, Slot, SlotAllotable, FixedSlotAllotable, UnFixedSlotAllotable, Break, AllotableEntity


@dataclass
class Day:
    id: str
    name: str

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name
        }


@dataclass
class WorkingDay:
    id: str
    day_id: str
    start_time: time
    end_time: time
    slot_duration: int
    division_id: str
    division: "Division"

    def to_dict(self):
        return {
            "id": self.id,
            "day_id": self.day_id,
            "start_time": self.start_time.strftime("%H:%M:%S"),
            "end_time": self.end_time.strftime("%H:%M:%S"),
            "slot_duration": self.slot_duration,
            "division_id": self.division_id,
            "division": self.division.to_dict() if self.division else None
        }


@dataclass
class Slot(Gene):
    id: str
    start_time: time
    end_time: time
    working_day_id: str
    daily_slot_number: int
    weekly_slot_number: int
    slot_alloted_to_id:str=None

    slot_alloted_to: "SlotAllotable" = None
    working_day: WorkingDay

    def to_dict(self):
        return {
            "id": self.id,
            "start_time": self.start_time.strftime("%H:%M:%S"),
            "end_time": self.end_time.strftime("%H:%M:%S"),
            "working_day_id": self.working_day_id,
            "daily_slot_number": self.daily_slot_number,
            "weekly_slot_number": self.weekly_slot_number,
            "slot_alloted_to_id":self.slot_alloted_to_id if self.slot_alloted_to_id else None,
            "slot_alloted_to": self.slot_alloted_to.to_dict() if self.slot_alloted_to else None,
            "working_day":self.working_day.to_dict() if self.working_day else None
        }


@dataclass
class SlotAllotable:
    id: str
    division_id: str
    name: str
    continuous_slot: int
    weekly_frequency: int
    fixed_slot: bool
    division: 'Division'
    

    def to_dict(self):
        return {
            "id": self.id,
            "division_id": self.division_id,
            "name": self.name,
            "fixed_slot": self.fixed_slot,
            "continuous_slot": self.continuous_slot,
            "weekly_frequency": self.weekly_frequency,
            "division": self.division.to_dict() if self.division else None
        }


@dataclass
class Break(SlotAllotable):
    start_time: time
    end_time: time
    working_day_id: str
    working_day: 'WorkingDay'
    fixed_slot: bool = field(default=True, init=False)
    continuous_slot: int = 1
    weekly_frequency: int = 1

    def to_dict(self):
        base_dict = super().to_dict()
        base_dict.update({
            'start_time': self.start_time.strftime("%H:%M:%S"),
            'end_time': self.end_time.strftime("%H:%M:%S"),
            'working_day_id': self.working_day_id,
            'working_day': self.working_day.to_dict() if self.working_day else None
        })
        return base_dict


@dataclass
class Faculty:
    id: str
    faculty_name: str

    def to_dict(self):
        return {
            "id": self.id,
            "faculty_name": self.faculty_name
        }


@dataclass
class Subject:
    id: str
    subject_name: str

    def to_dict(self):
        return {
            "id": self.id,
            "subject_name": self.subject_name
        }


@dataclass
class Division:
    id: str
    division_name: str
    standard_id: str
    standard: "Standard"

    def to_dict(self):
        return {
            "id": self.id,
            "division_name": self.division_name,
            "standard_id": self.standard_id,
            "standard": self.standard.to_dict() if self.standard else None
        }


@dataclass
class Standard:
    id: str
    standard_name: str
    department_id: str
    department: "Department"

    def to_dict(self):
        return {
            "id": self.id,
            "standard_name": self.standard_name,
            "department_id": self.department_id,
            "department": self.department.to_dict() if self.department else None
        }


@dataclass
class Department:
    id: str
    department_name: str
    university_id: str
    university: "University"

    def to_dict(self):
        return {
            "id": self.id,
            "department_name": self.department_name,
            "university_id": self.university_id,
            "university": self.university.to_dict() if self.university else None
        }


@dataclass
class University:
    id: str
    university_name: str

    def to_dict(self):
        return {
            "id": self.id,
            "university_name": self.university_name
        }


@dataclass
class FacultySubjectDivision(SlotAllotable):
    faculty_id: str
    subject_id: str
    division_id: str
    faculty: Faculty
    subject: Subject
    division: Division
    fixed_slot: bool = field(default=False, init=False)
    start_time: Optional[time] = None
    end_time: Optional[time] = None
    working_day_id: Optional[str] = None
    working_day: Optional['WorkingDay'] = None
    continuous_slot: int = 1
    weekly_frequency: int = 1

    def to_dict(self):
        base_dict = super().to_dict()
        base_dict.update({
            "faculty_id": self.faculty_id,
            "subject_id": self.subject_id,
            "division_id": self.division_id,
            "faculty": self.faculty.to_dict() if self.faculty else None,
            "subject": self.subject.to_dict() if self.subject else None,
            "division": self.division.to_dict() if self.division else None
        })
        return base_dict

