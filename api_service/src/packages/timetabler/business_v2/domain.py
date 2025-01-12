from dataclasses import dataclass, field
from typing import List, Optional
from datetime import time
from enum import Enum
from abc import  ABC, abstractmethod
from src.packages.ga import Gene, Chromosome

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
    start_time: time  # You can use datetime if you need more control
    end_time: time
    slot_duration: int
    division_id:str


    day: Day
    division:'Division'
    

    def to_dict(self):
        return {
            "id": self.id,
            "day_id": self.day_id,
            "start_time": self.start_time.strftime("%H:%M:%S"),
            "end_time": self.end_time.strftime("%H:%M:%S"),
            "slot_duration": self.slot_duration,
            "division_id":self.division_id,
            "day": self.day.to_dict(),
            "division":self.division.to_dict()
        }

@dataclass
class Slot(Gene):
    id: str
    start_time: time
    end_time: time
    working_day_id: str
    daily_slot_number:int
    weekly_slot_number:int
    slot_alloted_to_allotable_entity_mapper_id:str

    working_day: WorkingDay
    slot_alloted_to_allotable_entity_mapper: "SlotAllotableEntityMapper" = None



    def to_dict(self):
        return {
            "id": self.id,
            "start_time": self.start_time.strftime("%H:%M:%S"),
            "end_time": self.end_time.strftime("%H:%M:%S"),
            "working_day_id": self.working_day_id,
            "daily_slot_number":self.daily_slot_number,
            "weekly_slot_number":self.weekly_slot_number,
            "slot_alloted_to_allotable_entity_mapper_id":self.slot_alloted_to_allotable_entity_mapper,
            "working_day": self.working_day.to_dict() if self.working_day else None,
            "slot_alloted_to_allotable_entity_mapper": self.slot_alloted_to_allotable_entity_mapper.to_dict() if self.slot_alloted_to_allotable_entity_mapper else None,
        }

@dataclass
class SlotAllotable:
    id: str
    division_id:str
    continuous_slot:int
    weekly_frequency:int
    fixed_slot: bool
    next_slot_allotable_id:str
    
    division: 'Division'
    next_slot_allotable:'SlotAllotable'



    def to_dict(self):
        return {
            "id": self.id,
            "division_id": self.division_id,
            "continuous_slot": self.continuous_slot,
            "weekly_frequency": self.weekly_frequency,
            "fixed_slot": self.fixed_slot,
            "next_slot_allotable_id": self.next_slot_allotable_id,
            "division": self.division.to_dict() if self.division else None,
            "next_slot_allotable": self.next_slot_allotable.to_dict() if self.next_slot_allotable else None,
        }
        

@dataclass
class FixedSlotAllotable(SlotAllotable):
    start_time: time
    end_time: time
    working_day_id: str
    working_day: 'WorkingDay'

    def to_dict(self):
        base_dict = super().to_dict()
        base_dict.update({
            "start_time": self.start_time.strftime("%H:%M:%S") if self.start_time else None,
            "end_time": self.end_time.strftime("%H:%M:%S") if self.end_time else None,
            "working_day_id": self.working_day_id,
            "working_day": self.working_day.to_dict() if self.working_day else None,
        })
        return base_dict


@dataclass
class UnFixedSlotAllotable(SlotAllotable):
    def to_dict(self):
        return super().to_dict()


@dataclass
class AllotableEntity(SlotAllotable):
    id:str
    name:str

    def to_dict(self):
        return {
            'id':self.id,
            'name':self.name
        }

@dataclass
class Break(AllotableEntity):

    def to_dict(self):
        base_dict = super().to_dict()
        return base_dict



@dataclass
class Faculty:
    id: str
    name: str
    university_id:str
 
    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "university_id":self.university_id
        }
    


@dataclass
class Subject:
    id: str
    name: str
    university_id:str

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "university_id":self.university_id

        }

@dataclass
class Division:
    id: str
    name: str
    standard_id: str
    standard: "Standard"
    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "standard_id": self.standard_id,
            "standard": self.standard.to_dict() if self.standard else None
        }



@dataclass
class Standard:
    id: str
    name: str
    department_id: str
    department: "Department"
    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "department_id": self.department_id,
            "department": self.department.to_dict() if self.department else None
        }


@dataclass
class Department:
    id: str
    name: str
    university_id: str
    university: "University"

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "university_id": self.university_id,
            "university": self.university.to_dict() if self.university else None
        }
@dataclass
class University:
    id: str
    name: str
    logo:str

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "logo":self.logo
        }


@dataclass
class FacultySubjectDivision(AllotableEntity):
    faculty_id: str
    subject_id: str
    division_id: str

    faculty:Faculty
    subject:Subject
    division:Division



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

