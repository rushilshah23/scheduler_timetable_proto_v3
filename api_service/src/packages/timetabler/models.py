# from flask import Flask
# from flask_sqlalchemy import SQLAlchemy
# from datetime import time
# from enum import Enum
# from typing import List, Optional
# from src.utils.database import Base
# db = SQLAlchemy()

# # DayEnum for enumeration
# class DayEnum(Enum):
#     MONDAY = "MONDAY"
#     TUESDAY = "TUESDAY"
#     WEDNESDAY = "WEDNESDAY"
#     THURSDAY = "THURSDAY"
#     FRIDAY = "FRIDAY"
#     SATURDAY = "SATURDAY"
#     SUNDAY = "SUNDAY"

# # Day model
# class Day(Base):
#     __tablename__ = 'days'
#     id = db.Column(db.String, primary_key=True)
#     day_name = db.Column(db.String)

#     def to_dict(self):
#         return {
#             "id": self.id,
#             "day_name": self.day_name
#         }

# # WorkingDay model
# class WorkingDay(Base):
#     __tablename__ = 'working_days'

#     id = db.Column(db.String, primary_key=True)
#     day_id = db.Column(db.String, db.ForeignKey('days.id'))
#     start_time = db.Column(db.Time)
#     end_time = db.Column(db.Time)
#     slot_duration = db.Column(db.Integer)
#     division_id = db.Column(db.String, db.ForeignKey('divisions.id'))

#     day = db.relationship('Day', backref=db.backref('working_days', lazy=True))
#     division = db.relationship('Division', backref=db.backref('working_days', lazy=True))

#     def to_dict(self):
#         return {
#             "id": self.id,
#             "day_id": self.day_id,
#             "start_time": self.start_time.strftime("%H:%M:%S"),
#             "end_time": self.end_time.strftime("%H:%M:%S"),
#             "slot_duration": self.slot_duration,
#             "day": self.day.to_dict(),
#             "division_id": self.division_id,
#             "division": self.division.to_dict() if self.division else None
#         }

# # Slot model
# class Slot(Base):
#     __tablename__ = 'slots'

#     id = db.Column(db.String, primary_key=True)
#     start_time = db.Column(db.Time)
#     end_time = db.Column(db.Time)
#     working_day_id = db.Column(db.String, db.ForeignKey('working_days.id'))
#     daily_slot_number = db.Column(db.Integer)
#     weekly_slot_number = db.Column(db.Integer)
#     timetable_id = db.Column(db.String, db.ForeignKey('timetables.id'))  # Add foreign key reference

#     working_day = db.relationship('WorkingDay', backref=db.backref('slots', lazy=True))
#     slot_alloted_to_id = db.Column(db.String, db.ForeignKey('slot_allotables.id'))
#     slot_alloted_to = db.relationship('SlotAllotable', backref=db.backref('slots', lazy=True), uselist=False)
    
#     # Change the backref name from 'slots' to avoid conflict
#     timetable = db.relationship('Timetable', backref=db.backref('slot_entries', lazy=True))  # Define the relationship with a unique backref name

#     def to_dict(self):
#         return {
#             "id": self.id,
#             "start_time": self.start_time.strftime("%H:%M:%S"),
#             "end_time": self.end_time.strftime("%H:%M:%S"),
#             "working_day_id": self.working_day_id,
#             "working_day": self.working_day.to_dict() if self.working_day else None,
#             "slot_alloted_to": self.slot_alloted_to.to_dict() if self.slot_alloted_to else None,
#             "daily_slot_number": self.daily_slot_number,
#             "weekly_slot_number": self.weekly_slot_number,
#             "timetable_id": self.timetable_id,
#             "timetable": self.timetable.to_dict() if self.timetable else None
#         }


# # SlotAllotable model
# class SlotAllotable(Base):
#     __tablename__ = 'slot_allotables'

#     id = db.Column(db.String, primary_key=True)
#     division_id = db.Column(db.String, db.ForeignKey('divisions.id'))
#     name = db.Column(db.String)
#     continuous_slot = db.Column(db.Integer)
#     weekly_frequency = db.Column(db.Integer)
#     fixed_slot = db.Column(db.Boolean, default=False)
#     type = db.Column(db.String)  # Discriminator column for polymorphism

#     division = db.relationship('Division', backref=db.backref('slot_allotables', lazy=True))

#     __mapper_args__ = {
#         'polymorphic_identity': 'slot_allotable',
#         'polymorphic_on': type
#     }

#     def to_dict(self):
#         return {
#             "id": self.id,
#             "division_id": self.division_id,
#             "name": self.name,
#             "division": self.division.to_dict() if self.division else None,
#             "fixed_slot": self.fixed_slot,
#             "continuous_slot": self.continuous_slot,
#             "weekly_frequency": self.weekly_frequency
#         }

# class FixedSlotAllotable(SlotAllotable):
#     __tablename__ = 'fixed_slot_allotables'
#     id = db.Column(db.String, db.ForeignKey('slot_allotables.id'), primary_key=True)
#     start_time = db.Column(db.Time)
#     end_time = db.Column(db.Time)
#     working_day_id = db.Column(db.String, db.ForeignKey('working_days.id'))
#     working_day = db.relationship('WorkingDay', backref=db.backref('breaks', lazy=True))

#     __mapper_args__ = {
#         'polymorphic_identity': 'fixed_slot_allotable',
#     }

#     def to_dict(self):
#         base_dict = super().to_dict()
#         base_dict.update({
#             'start_time': self.start_time.strftime("%H:%M:%S"),
#             'end_time': self.end_time.strftime("%H:%M:%S"),
#             "working_day_id": self.working_day_id,
#             "working_day": self.working_day.to_dict() if self.working_day else None
#         })
#         return base_dict
    

# # Break model (inherits SlotAllotable)

# class Break(FixedSlotAllotable):
#     __tablename__ = 'breaks'
#     __mapper_args__ = {
#         'polymorphic_identity': 'break',
#     }

#     id = db.Column(db.String, db.ForeignKey('fixed_slot_allotables.id'), primary_key=True)

#     def to_dict(self):
#         base_dict = super().to_dict()
#         return base_dict

# # Faculty model
# class Faculty(Base):
#     __tablename__ = 'faculties'

#     id = db.Column(db.String, primary_key=True)
#     faculty_name = db.Column(db.String)

#     def to_dict(self):
#         return {
#             "id": self.id,
#             "faculty_name": self.faculty_name
#         }

# # Subject model
# class Subject(Base):
#     __tablename__ = 'subjects'

#     id = db.Column(db.String, primary_key=True)
#     subject_name = db.Column(db.String)

#     def to_dict(self):
#         return {
#             "id": self.id,
#             "subject_name": self.subject_name
#         }

# # Division model
# class Division(Base):
#     __tablename__ = 'divisions'

#     id = db.Column(db.String, primary_key=True)
#     division_name = db.Column(db.String)
#     standard_id = db.Column(db.String, db.ForeignKey('standards.id'))

#     standard = db.relationship('Standard', backref=db.backref('divisions', lazy=True))

#     def to_dict(self):
#         return {
#             "id": self.id,
#             "division_name": self.division_name,
#             "standard_id": self.standard_id,
#             "standard": self.standard.to_dict() if self.standard else None
#         }

# # Standard model
# class Standard(Base):
#     __tablename__ = 'standards'

#     id = db.Column(db.String, primary_key=True)
#     standard_name = db.Column(db.String)
#     department_id = db.Column(db.String, db.ForeignKey('departments.id'))

#     department = db.relationship('Department', backref=db.backref('standards', lazy=True))

#     def to_dict(self):
#         return {
#             "id": self.id,
#             "standard_name": self.standard_name,
#             "department_id": self.department_id,
#             "department": self.department.to_dict() if self.department else None
#         }

# # Department model
# class Department(Base):
#     __tablename__ = 'departments'

#     id = db.Column(db.String, primary_key=True)
#     department_name = db.Column(db.String)
#     university_id = db.Column(db.String, db.ForeignKey('universities.id'))

#     university = db.relationship('University', backref=db.backref('departments', lazy=True))

#     def to_dict(self):
#         return {
#             "id": self.id,
#             "department_name": self.department_name,
#             "university_id": self.university_id,
#             "university": self.university.to_dict() if self.university else None
#         }

# # University model
# class University(Base):
#     __tablename__ = 'universities'

#     id = db.Column(db.String, primary_key=True)
#     university_name = db.Column(db.String)
#     logo=db.Column(db.String)

#     def to_dict(self):
#         return {
#             "id": self.id,
#             "university_name": self.university_name,
#             "logo":self.logo
#         }

# # FacultySubjectDivision model
# class FacultySubjectDivision(SlotAllotable):
#     __tablename__ = 'faculty_subject_division_allotables'
#     id = db.Column(db.String, db.ForeignKey('slot_allotables.id'), primary_key=True)

#     faculty_id = db.Column(db.String, db.ForeignKey('faculties.id'))
#     subject_id = db.Column(db.String, db.ForeignKey('subjects.id'))
#     division_id = db.Column(db.String, db.ForeignKey('divisions.id'))  

#     faculty = db.relationship('Faculty', backref=db.backref('subject_divisions', lazy=True))
#     subject = db.relationship('Subject', backref=db.backref('subject_divisions', lazy=True))
#     division = db.relationship('Division', backref=db.backref('subject_divisions', lazy=True))

#     __mapper_args__ = {
#         'polymorphic_identity': 'faculty_subject_division',
#     }

#     def to_dict(self):
#         base_dict = super().to_dict()
#         base_dict.update({
#             "faculty_id": self.faculty_id,
#             "subject_id": self.subject_id,
#             "division_id": self.division_id,
#             "faculty": self.faculty.to_dict() if self.faculty else None,
#             "subject": self.subject.to_dict() if self.subject else None,
#             "division": self.division.to_dict() if self.division else None
#         })
#         return base_dict
# # # Timetable model
# # class Timetable(Base):
# #     __tablename__ = 'timetables'

# #     id = db.Column(db.String, primary_key=True)
# #     division_id = db.Column(db.String, db.ForeignKey('divisions.id'))

# #     division = db.relationship('Division', backref=db.backref('timetables', lazy=True))
# #     slots = db.relationship('Slot', backref=db.backref('timetable_entries', lazy=True))  # Changed backref here

# #     def to_dict(self):
# #         return {
# #             "division": self.division.to_dict() if self.division else None,
# #             "slots": [slot.to_dict() for slot in self.slots]
# #         }



# ------------------------------------------------------


from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from datetime import time
from enum import Enum
from typing import List, Optional
from src.utils.database import Base, engine
db = SQLAlchemy()


# DayEnum for enumeration
class DayEnum(Enum):
    monday = "monday"
    tuesday = "tuesday"
    wednesday = "wednesday"
    thursday = "thursday"
    friday = "friday"
    saturday = "saturday"
    sunday = "sunday"

# Day model
class Day(Base):
    __tablename__ = 'days'
    id = db.Column(db.String, primary_key=True)
    day_name = db.Column(db.String)
    # day_name = db.Column(db.Enum(DayEnum.name))

    def to_dict(self):
        return {
            "id": self.id,
            "day_name": self.day_name
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

    day = db.relationship('Day', backref=db.backref('working_days', lazy=True))
    division = db.relationship('Division', backref=db.backref('working_days', lazy=True))
    slots = db.relationship('Slot', backref=db.backref('working_day', lazy=True), cascade='all, delete')

    def to_dict(self):
        return {
            "id": self.id,
            "day_id": self.day_id,
            "start_time": self.start_time.strftime("%H:%M:%S"),
            "end_time": self.end_time.strftime("%H:%M:%S"),
            "slot_duration": self.slot_duration,
            "day": self.day.to_dict(),
            "division_id": self.division_id,
            "division": self.division.to_dict() if self.division else None
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
    slot_alloted_to_id = db.Column(db.String, db.ForeignKey('slot_allotables.id'))

    working_day = db.relationship('WorkingDay', backref=db.backref('slots', lazy=True))
    slot_alloted_to = db.relationship('SlotAllotable', backref=db.backref('slots', lazy=True), uselist=False)
    

    def to_dict(self):
        return {
            "id": self.id,
            "start_time": self.start_time.strftime("%H:%M:%S"),
            "end_time": self.end_time.strftime("%H:%M:%S"),
            "working_day_id": self.working_day_id,
            "working_day": self.working_day.to_dict() if self.working_day else None,
            "slot_alloted_to": self.slot_alloted_to.to_dict() if self.slot_alloted_to else None,
            "daily_slot_number": self.daily_slot_number,
            "weekly_slot_number": self.weekly_slot_number,
        }


# SlotAllotable model
class SlotAllotable(Base):
    __tablename__ = 'slot_allotables'

    id = db.Column(db.String, primary_key=True)
    division_id = db.Column(db.String, db.ForeignKey('divisions.id'))
    name = db.Column(db.String)
    continuous_slot = db.Column(db.Integer)
    weekly_frequency = db.Column(db.Integer)
    fixed_slot = db.Column(db.Boolean, default=False)
    next_slot = db.Column(db.String, db.ForeignKey('slot_allotables.id'), nullable=True)

    division = db.relationship('Division', backref=db.backref('slot_allotables', lazy=True))
    slot_allotable_entities = db.relationship('SlotAllotableEntity', backref=db.backref('slot_allotables', lazy=True), cascade='all, delete')



    def to_dict(self):
        return {
            "id": self.id,
            "division_id": self.division_id,
            "name": self.name,
            "division": self.division.to_dict() if self.division else None,
            "fixed_slot": self.fixed_slot,
            "continuous_slot": self.continuous_slot,
            "weekly_frequency": self.weekly_frequency,
            "next_slot": self.next_slot,
            "slot_allotable_entities": [
                entity.to_dict() for entity in self.slot_allotable_entities
            ] if self.slot_allotable_entities else []
        }

class FixedSlotAllotable(SlotAllotable):
    __tablename__ = 'fixed_slot_allotables'
    id = db.Column(db.String, db.ForeignKey('slot_allotables.id'), primary_key=True)
    start_time = db.Column(db.Time)
    end_time = db.Column(db.Time)
    working_day_id = db.Column(db.String, db.ForeignKey('working_days.id'))
    working_day = db.relationship('WorkingDay', backref=db.backref('breaks', lazy=True))
    def to_dict(self):
        base_dict = super().to_dict()
        base_dict.update({
            'start_time': self.start_time.strftime("%H:%M:%S"),
            'end_time': self.end_time.strftime("%H:%M:%S"),
            "working_day_id": self.working_day_id,
            "working_day": self.working_day.to_dict() if self.working_day else None
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
    faculty_name = db.Column(db.String)

    def to_dict(self):
        return {
            "id": self.id,
            "faculty_name": self.faculty_name
        }

# Subject model
class Subject(Base):
    __tablename__ = 'subjects'

    id = db.Column(db.String, primary_key=True)
    subject_name = db.Column(db.String)

    def to_dict(self):
        return {
            "id": self.id,
            "subject_name": self.subject_name
        }

# Division model
class Division(Base):
    __tablename__ = 'divisions'

    id = db.Column(db.String, primary_key=True)
    division_name = db.Column(db.String)
    standard_id = db.Column(db.String, db.ForeignKey('standards.id'))

    standard = db.relationship('Standard', backref=db.backref('divisions', lazy=True))

    def to_dict(self):
        return {
            "id": self.id,
            "division_name": self.division_name,
            "standard_id": self.standard_id,
            "standard": self.standard.to_dict() if self.standard else None
        }

# Standard model
class Standard(Base):
    __tablename__ = 'standards'

    id = db.Column(db.String, primary_key=True)
    standard_name = db.Column(db.String)
    department_id = db.Column(db.String, db.ForeignKey('departments.id'))

    department = db.relationship('Department', backref=db.backref('standards', lazy=True))

    def to_dict(self):
        return {
            "id": self.id,
            "standard_name": self.standard_name,
            "department_id": self.department_id,
            "department": self.department.to_dict() if self.department else None
        }

# Department model
class Department(Base):
    __tablename__ = 'departments'

    id = db.Column(db.String, primary_key=True)
    department_name = db.Column(db.String)
    university_id = db.Column(db.String, db.ForeignKey('universities.id'))

    university = db.relationship('University', backref=db.backref('departments', lazy=True))

    def to_dict(self):
        return {
            "id": self.id,
            "department_name": self.department_name,
            "university_id": self.university_id,
            "university": self.university.to_dict() if self.university else None
        }

# University model
class University(Base):
    __tablename__ = 'universities'

    id = db.Column(db.String, primary_key=True)
    university_name = db.Column(db.String)
    logo=db.Column(db.String)

    def to_dict(self):
        return {
            "id": self.id,
            "university_name": self.university_name,
            "logo":self.logo
        }

# FacultySubjectDivision model
class FacultySubjectDivision(AllotableEntity):
    __tablename__ = 'faculty_subject_division_allotables'
    id = db.Column(db.String, db.ForeignKey('allotable_entities.id'), primary_key=True)

    faculty_id = db.Column(db.String, db.ForeignKey('faculties.id'))
    subject_id = db.Column(db.String, db.ForeignKey('subjects.id'))
    division_id = db.Column(db.String, db.ForeignKey('divisions.id'))  

    faculty = db.relationship('Faculty', backref=db.backref('subject_divisions', lazy=True))
    subject = db.relationship('Subject', backref=db.backref('subject_divisions', lazy=True))
    division = db.relationship('Division', backref=db.backref('subject_divisions', lazy=True))



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
    

class SlotAllotableEntityMapper(Base):
    __tablename__ = 'slot_allotables_entities_mapper'
    slot_allotable_id = db.Column(db.String, db.ForeignKey('slot_allotables.id'), primary_key=True)
    allotable_entity_id = db.Column(db.String, db.ForeignKey('allotable_entities.id'), primary_key=True)

    slot_allotable =  db.relationship('SlotAllotable', backref=db.backref('slot_allotables', lazy=True))  
    allotable_entity =  db.relationship('AllotableEntity', backref=db.backref('allotable_entities', lazy=True))  

    def to_dict(self):
        return {
            "slot_alllotable_id":self.slot_allotable_id,
            "entity_id":self.allotable_entity_id,
            "slot_allotable":self.slot_allotable.to_dict() if self.slot_allotable else None,
            "allotable_entity":self.allotable_entity.to_dict() if self.allotable_entity else None,

        }

