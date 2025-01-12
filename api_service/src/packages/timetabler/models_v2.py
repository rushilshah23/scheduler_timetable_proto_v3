from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from datetime import time
from enum import Enum
from typing import List, Optional
from src.utils.database import Base, engine

db = SQLAlchemy()

# Day model
class Day(Base):
    __tablename__ = 'days'
    id = db.Column(db.String, primary_key=True)
    name = db.Column(db.String, unique=True)

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name
        }

# WorkingDay model
class WorkingDay(Base):
    __tablename__ = 'working_days'

    id = db.Column(db.String, primary_key=True)
    day_id = db.Column(db.String, db.ForeignKey('days.id'))
    start_time = db.Column(db.Time)
    end_time = db.Column(db.Time)
    slot_duration = db.Column(db.Integer)
    division_id = db.Column(db.String, db.ForeignKey('divisions.id'))


    def to_dict(self):
        return {
            "id": self.id,
            "day_id": self.day_id,
            "start_time": self.start_time.strftime("%H:%M:%S"),
            "end_time": self.end_time.strftime("%H:%M:%S"),
            "slot_duration": self.slot_duration,
            "division_id": self.division_id
        }

# Slot model
class Slot(Base):
    __tablename__ = 'slots'

    id = db.Column(db.String, primary_key=True)
    start_time = db.Column(db.Time)
    end_time = db.Column(db.Time)
    working_day_id = db.Column(db.String, db.ForeignKey('working_days.id'))
    daily_slot_number = db.Column(db.Integer)
    weekly_slot_number = db.Column(db.Integer)
    slot_alloted_to_allotable_entity_mapper_id = db.Column(db.String, db.ForeignKey('slot_allotables_entities_mapper.id'),nullable=True)

    def to_dict(self):
        return {
            "id": self.id,
            "start_time": self.start_time.strftime("%H:%M:%S"),
            "end_time": self.end_time.strftime("%H:%M:%S"),
            "working_day_id": self.working_day_id,
            "daily_slot_number": self.daily_slot_number,
            "weekly_slot_number": self.weekly_slot_number,
            "slot_alloted_to_allotable_entity_mapper_id":self.slot_alloted_to_allotable_entity_mapper_id if self.slot_alloted_to_allotable_entity_mapper_id else None
        }


# SlotAllotable model
class SlotAllotable(Base):
    __tablename__ = 'slot_allotables'

    id = db.Column(db.String, primary_key=True)
    division_id = db.Column(db.String, db.ForeignKey('divisions.id'))
    continuous_slot = db.Column(db.Integer)
    weekly_frequency = db.Column(db.Integer)
    fixed_slot = db.Column(db.Boolean, default=False)
    next_slot_allotable_id = db.Column(db.String, db.ForeignKey('slot_allotables.id'), nullable=True)

    def to_dict(self):
        return {
            "id": self.id,
            "division_id": self.division_id,
            "fixed_slot": self.fixed_slot,
            "continuous_slot": self.continuous_slot,
            "weekly_frequency": self.weekly_frequency,
            "next_slot_allotable_id": self.next_slot_allotable_id,

        }

class FixedSlotAllotable(SlotAllotable):
    __tablename__ = 'fixed_slot_allotables'
    id = db.Column(db.String, db.ForeignKey('slot_allotables.id'), primary_key=True)
    start_time = db.Column(db.Time)
    end_time = db.Column(db.Time)
    working_day_id = db.Column(db.String, db.ForeignKey('working_days.id'))
    def to_dict(self):
        base_dict = super().to_dict()
        base_dict.update({
            'start_time': self.start_time.strftime("%H:%M:%S"),
            'end_time': self.end_time.strftime("%H:%M:%S"),
            "working_day_id": self.working_day_id
        })
        return base_dict

class UnFixedSlotAllotable(SlotAllotable):
    __tablename__ = 'unfixed_slot_allotables'
    id = db.Column(db.String, db.ForeignKey('slot_allotables.id'), primary_key=True)

    def to_dict(self):
        base_dict = super().to_dict()
        return base_dict
    

# Break model (inherits SlotAllotable)
class AllotableEntity(Base):
    __tablename__ = 'allotable_entities'
    id = db.Column(db.String,  primary_key=True)
    name = db.Column(db.String)

    def to_dict(self):
        return {
            "id":self.id,
            "name":self.name
        }
    

class Break(AllotableEntity):
    __tablename__ = 'breaks'

    id = db.Column(db.String, db.ForeignKey('allotable_entities.id'), primary_key=True)

    def to_dict(self):
        base_dict = super().to_dict()
        return base_dict

# Faculty model
class Faculty(Base):
    __tablename__ = 'faculties'

    id = db.Column(db.String, primary_key=True)
    name = db.Column(db.String)
    university_id = db.Column(db.String, db.ForeignKey('universities.id'))

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "university_id": self.university_id

        }

# Subject model
class Subject(Base):
    __tablename__ = 'subjects'

    id = db.Column(db.String, primary_key=True)
    name = db.Column(db.String)
    university_id = db.Column(db.String, db.ForeignKey('universities.id'))

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "university_id": self.university_id

        }

# Division model
class Division(Base):
    __tablename__ = 'divisions'

    id = db.Column(db.String, primary_key=True)
    name = db.Column(db.String)
    standard_id = db.Column(db.String, db.ForeignKey('standards.id'))


    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "standard_id": self.standard_id,
        }

# Standard model
class Standard(Base):
    __tablename__ = 'standards'

    id = db.Column(db.String, primary_key=True)
    name = db.Column(db.String)
    department_id = db.Column(db.String, db.ForeignKey('departments.id'))


    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "department_id": self.department_id,
        }

# Department model
class Department(Base):
    __tablename__ = 'departments'

    id = db.Column(db.String, primary_key=True)
    name = db.Column(db.String)
    university_id = db.Column(db.String, db.ForeignKey('universities.id'))
    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "university_id": self.university_id,
        }

# University model
class University(Base):
    __tablename__ = 'universities'

    id = db.Column(db.String, primary_key=True)
    name = db.Column(db.String)
    logo=db.Column(db.String)

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "logo":self.logo
        }

# FacultySubjectDivision model
class FacultySubjectDivision(AllotableEntity):
    __tablename__ = 'faculty_subject_division_allotables'
    id = db.Column(db.String, db.ForeignKey('allotable_entities.id'), primary_key=True)

    faculty_id = db.Column(db.String, db.ForeignKey('faculties.id'))
    subject_id = db.Column(db.String, db.ForeignKey('subjects.id'))
    division_id = db.Column(db.String, db.ForeignKey('divisions.id'))  

    def to_dict(self):
        base_dict = super().to_dict()
        base_dict.update({
            "faculty_id": self.faculty_id,
            "subject_id": self.subject_id,
            "division_id": self.division_id,

        })
        return base_dict
    

class SlotAllotableEntityMapper(Base):
    __tablename__ = 'slot_allotables_entities_mapper'
    id = db.Column(db.String, primary_key=True)
    slot_allotable_id = db.Column(db.String, db.ForeignKey('slot_allotables.id'), primary_key=True)
    allotable_entity_id = db.Column(db.String, db.ForeignKey('allotable_entities.id'), primary_key=True)

    def to_dict(self):
        return {
            "id":self.id,
            "slot_alllotable_id":self.slot_allotable_id,
            "allotable_entity_id":self.allotable_entity_id
        }

