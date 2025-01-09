from dataclasses import dataclass
from typing import List, Optional
from src.packages.timetabler.business.domain import *
import json
from src.packages.timetabler.business.input_parser import parse_input_json_to_python

class DomainUtils:
    _instance = None  # This holds the singleton instance

    def __new__(cls, data_source=None):
        if cls._instance is None:
            # Create the singleton instance only once
            cls._instance = super(DomainUtils, cls).__new__(cls)


            cls._instance.data_source = data_source
            # with open("./inputs/input_2.json", "r") as f:
            #     input_data = json.load(f)
            # output = parse_input_json_to_python(input_data)
            # print(output)
            # cls._instance.data_source = output

        return cls._instance
    
    def get_university_by_id(self, id: int):
        """Get a university by ID."""
        for university in self.data_source["universities"]:
            if university.id == id:
                return university
        return None

    def get_department_by_id(self, id: int):
        """Get a department by ID."""
        for department in self.data_source["departments"]:
            if department.id == id:
                return department
        return None

    def get_standard_by_id(self, id: int):
        """Get a standard by ID."""
        for standard in self.data_source["standards"]:
            if standard.id == id:
                return standard
        return None

    def get_division_by_id(self, id: int):
        """Get a division by ID."""
        for division in self.data_source["divisions"]:
            if division.id == id:
                return division
        return None

    def get_subject_by_id(self, id: int):
        """Get a subject by ID."""
        for subject in self.data_source["subjects"]:
            if subject.id == id:
                return subject
        return None

    def get_faculty_by_id(self, id: int):
        """Get a faculty by ID."""
        for faculty in self.data_source["faculties"]:
            if faculty.id == id:
                return faculty
        return None

    def get_faculty_subject_division_list(self):
        """Get the list of all faculty subject divisions."""
        return self.data_source.get("faculty_subject_division_list", [])

    def get_working_day_from_id(self, id: int):
        """Get a working day by ID."""
        # print(f"Length of working days is - {len(self._instance.data_source["working_days"])}")
        for working_day in self.data_source["working_days"]:
            if working_day.id == id:
                return working_day
        return None

    def get_break_by_id(self, id: int):
        """Get a break by ID."""
        for break_item in self.data_source["breaks_list"]:
            if break_item.id == id:
                return break_item
        return None

            
    def get_all_universities(self) -> List:
        """Get all universities."""
        return self.data_source.get("universities", [])

    def get_all_departments(self) -> List:
        """Get all departments."""
        return self.data_source.get("departments", [])

    def get_all_standards(self) -> List:
        """Get all standards."""
        return self.data_source.get("standards", [])

    def get_all_divisions(self) -> List:
        """Get all divisions."""
        return self.data_source.get("divisions", [])

    def get_all_subjects(self) -> List:
        """Get all subjects."""
        return self.data_source.get("subjects", [])

    def get_all_faculties(self) -> List:
        """Get all faculties."""
        return self.data_source.get("faculties", [])

    def get_all_working_days(self) -> List:
        """Get all working days."""
        return self.data_source.get("working_days", [])

    def get_all_breaks(self) -> List:
        """Get all breaks."""
        return self.data_source.get("breaks_list", [])
    

    def get_working_days_of_a_divsion_by_dvision_id(self, division_id:str)->List:
        working_days = [working_day for working_day in self.data_source.get("working_days",[]) if working_day.division.id == division_id]
        return working_days
    
    def get_working_days_of_a_standard_by_standard_id(self, standard_id:str)->List:
        working_days = [working_day for working_day in self.data_source.get("working_days",[]) if working_day.division.standard.id == standard_id]
        return working_days
    
    def get_working_days_of_a_department_by_department_id(self, department_id:str)->List:
        working_days = [working_day for working_day in self.data_source.get("working_days",[]) if working_day.division.standard.department.id == department_id]
        return working_days
    
    def get_working_days_of_a_university_by_university_id(self, university_id:str)->List:
        working_days = [working_day for working_day in self.data_source.get("working_days",[]) if working_day.division.standard.department.university.id == university_id]
        return working_days


     

    # def get_allotables_of_a_working_day_by_working_day_id(self, working_day_id: str) -> List:
    #     fixed_allotables = [
    #         fixed_allotable for fixed_allotable in self.data_source.get("breaks_list", [])
    #         if fixed_allotable.working_day_id == working_day_id
    #     ]
    #     unfixed_allotables = [
    #         unfixed_allotable for unfixed_allotable in self.data_source.get("faculty_subject_division_list", [])
    #         if unfixed_allotable.working_day_id == working_day_id
    #     ]

    #     final_allotables = []
    #     final_allotables.extend(fixed_allotables)
    #     final_allotables.extend(unfixed_allotables)

    #     return final_allotables


    # def get_allotables_of_a_division_by_working_id(self, working_id: str) -> List:
    #     fixed_allotables_of_division = [
    #         fixed_allotable for fixed_allotable in self.data_source.get("breaks_list", [])
    #         if fixed_allotable.division.working_id == working_id
    #     ]
    #     unfixed_allotables_of_division = [
    #         unfixed_allotable for unfixed_allotable in self.data_source.get("faculty_subject_division_list", [])
    #         if unfixed_allotable.division.working_id == working_id
    #     ]

    #     final_allotables = []
    #     final_allotables.extend(fixed_allotables_of_division)
    #     final_allotables.extend(unfixed_allotables_of_division)

    #     return final_allotables


    def get_allotables_of_a_division_by_division_id(self, division_id: str) -> List:
        fixed_allotables_of_division = [
            fixed_allotable for fixed_allotable in self.data_source.get("breaks_list", [])
            if fixed_allotable.division_id == division_id
        ]
        unfixed_allotables_of_division = [
            unfixed_allotable for unfixed_allotable in self.data_source.get("faculty_subject_division_list", [])
            if unfixed_allotable.division_id == division_id
        ]

        final_allotables = []
        final_allotables.extend(fixed_allotables_of_division)
        final_allotables.extend(unfixed_allotables_of_division)

        return final_allotables


    def get_allotables_of_a_standard_by_standard_id(self, standard_id: str) -> List:
        fixed_allotables_of_standard = [
            fixed_allotable for fixed_allotable in self.data_source.get("breaks_list", [])
            if fixed_allotable.division.standard_id == standard_id
        ]
        unfixed_allotables_of_standard = [
            unfixed_allotable for unfixed_allotable in self.data_source.get("faculty_subject_division_list", [])
            if unfixed_allotable.division.standard_id == standard_id
        ]

        final_allotables = []
        final_allotables.extend(fixed_allotables_of_standard)
        final_allotables.extend(unfixed_allotables_of_standard)

        return final_allotables


    def get_allotables_of_a_department_by_department_id(self, department_id: str) -> List:
        fixed_allotables_of_department = [
            fixed_allotable for fixed_allotable in self.data_source.get("breaks_list", [])
            if fixed_allotable.division.standard.department_id == department_id
        ]
        unfixed_allotables_of_department = [
            unfixed_allotable for unfixed_allotable in self.data_source.get("faculty_subject_division_list", [])
            if unfixed_allotable.division.standard.department_id == department_id
        ]

        final_allotables = []
        final_allotables.extend(fixed_allotables_of_department)
        final_allotables.extend(unfixed_allotables_of_department)

        return final_allotables


    def get_allotables_of_a_university_by_university_id(self, university_id: str) -> List:
        fixed_allotables_of_university = [
            fixed_allotable for fixed_allotable in self.data_source.get("breaks_list", [])
            if fixed_allotable.division.standard.department.university_id == university_id
        ]
        unfixed_allotables_of_university = [
            unfixed_allotable for unfixed_allotable in self.data_source.get("faculty_subject_division_list", [])
            if unfixed_allotable.division.standard.department.university_id == university_id
        ]

        final_allotables = []
        final_allotables.extend(fixed_allotables_of_university)
        final_allotables.extend(unfixed_allotables_of_university)

        return final_allotables


    def get_departments_by_university_id(self, university_id: int) -> List[Department]:
        """Get departments by university ID."""
        departments = [
            department for department in self.data_source["departments"]
            if department.university_id == university_id
        ]
        return departments

    def get_standards_by_department_id(self, department_id: int)-> List[Standard]:
        """Get standards by department ID."""
        standards = [
            standard for standard in self.data_source["standards"]
            if standard.department_id == department_id
        ]
        return standards

    def get_divisions_by_standard_id(self, standard_id: int)-> List[Division]:
        """Get divisions by standard ID."""
        divisions = [
            division for division in self.data_source["divisions"]
            if division.standard_id == standard_id
        ]
        return divisions

    def get_working_days_by_division_id(self, division_id: int):
        """Get working days by division ID."""
        working_days = [
            working_day for working_day in self.data_source["working_days"]
            if working_day.division_id == division_id
        ]
        return working_days


# from src.packages.timetabler.business.domain import  University, Department, Standard, Division, Subject, Faculty, WorkingDay, Break, FacultySubjectDivision
# from sqlalchemy import text
# from typing import List, Optional
# from src.utils.database import get_db
# from sqlalchemy.orm import Session



# from sqlalchemy.orm import Session
# from src.packages.timetabler.models import (
#     University, Department, Standard, Division, Subject, Faculty, 
#     WorkingDay, Day, Slot, Break, FacultySubjectDivision
# )


# class DomainUtils:
#     _instance = None  # This holds the singleton instance

#     def __new__(cls, data_source=None):
#         if cls._instance is None:
#             # Create the singleton instance only once
#             cls._instance = super(DomainUtils, cls).__new__(cls)
#         return cls._instance

#     @staticmethod
#     def get_db_session() -> Session:
#         """Retrieve a database session."""
#         db = next(get_db())
#         return db


#     def get_university_by_id(self, id: int) -> Optional[University]:
#         """Get a university by ID."""
#         with self.get_db_session() as db:
#             query = text("SELECT * FROM universities WHERE id = :id")
#             result = db.execute(query, {"id": id}).fetchone()
#             return result

#     def get_department_by_id(self, id: int) -> Optional[Department]:
#         """Get a department by ID."""
#         with self.get_db_session() as db:

#             query = text("SELECT * FROM departments WHERE id = :id")
#             result = db.execute(query, {"id": id}).fetchone()
#             return result

#     def get_standard_by_id(self, id: int) -> Optional[Standard]:
#         """Get a standard by ID."""
#         with self.get_db_session() as db:

#             query = text("SELECT * FROM standards WHERE id = :id")
#             result = db.execute(query, {"id": id}).fetchone()
#             return result

#     def get_division_by_id(self, id: int) -> Optional[Division]:
#         """Get a division by ID."""
#         with self.get_db_session() as db:

#             query = text("SELECT * FROM divisions WHERE id = :id")
#             result = db.execute(query, {"id": id}).fetchone()
#             return result

#     def get_subject_by_id(self, id: int) -> Optional[Subject]:
#         """Get a subject by ID."""
#         with self.get_db_session() as db:

#             query = text("SELECT * FROM subjects WHERE id = :id")
#             result = db.execute(query, {"id": id}).fetchone()
#             return result

#     def get_faculty_by_id(self, id: int) -> Optional[Faculty]:
#         """Get a faculty by ID."""
#         with self.get_db_session() as db:

#             query = text("SELECT * FROM faculties WHERE id = :id")
#             result = db.execute(query, {"id": id}).fetchone()
#             return result

#     def get_working_day_from_id(self, id: int) -> Optional[WorkingDay]:
#         """Get a working day by ID."""
#         with self.get_db_session() as db:

#             query = text("SELECT * FROM working_days WHERE id = :id")
#             result = db.execute(query, {"id": id}).fetchone()
#             return result

#     def get_break_by_id(self, id: int) -> Optional[Break]:
#         """Get a break by ID."""
#         with self.get_db_session() as db:

#             query = text("SELECT * FROM breaks WHERE id = :id")
#             result = db.execute(query, {"id": id}).fetchone()
#             return result

#     def get_all_universities(self) -> List[University]:
#         """Get all universities."""
#         with self.get_db_session() as db:

#             query = text("SELECT * FROM universities")
#             result = db.execute(query).fetchall()
#             return result

#     def get_all_departments(self) -> List[Department]:
#         """Get all departments."""
#         with self.get_db_session() as db:

#             query = text("SELECT * FROM departments")
#             result = db.execute(query).fetchall()
#             return result

#     def get_all_standards(self) -> List[Standard]:
#         """Get all standards."""
#         with self.get_db_session() as db:

#             query = text("SELECT * FROM standards")
#             result = db.execute(query).fetchall()
#             return result

#     def get_all_divisions(self) -> List[Division]:
#         """Get all divisions."""
#         with self.get_db_session() as db:

#             query = text("SELECT * FROM divisions")
#             result = db.execute(query).fetchall()
#             return result

#     def get_all_subjects(self) -> List[Subject]:
#         """Get all subjects."""
#         with self.get_db_session() as db:

#             query = text("SELECT * FROM subjects")
#             result = db.execute(query).fetchall()
#             return result

#     def get_all_faculties(self) -> List[Faculty]:
#         """Get all faculties."""
#         with self.get_db_session() as db:

#             query = text("SELECT * FROM faculties")
#             result = db.execute(query).fetchall()
#             return result

#     def get_all_working_days(self) -> List[WorkingDay]:
#         """Get all working days."""
#         with self.get_db_session() as db:

#             query = text("SELECT * FROM working_days")
#             result = db.execute(query).fetchall()
#             return result

#     def get_all_breaks(self) -> List[Break]:
#         """Get all breaks."""
#         with self.get_db_session() as db:

#             query = text("SELECT * FROM breaks")
#             result = db.execute(query).fetchall()
#             return result

#     def get_working_days_of_a_division_by_division_id(self, division_id: int) -> List[WorkingDay]:
#         """Get working days of a division by division ID."""
#         with self.get_db_session() as db:

#             query = text("SELECT * FROM working_days WHERE division_id = :division_id")
#             result = db.execute(query, {"division_id": division_id}).fetchall()
#             return result

#     def get_working_days_of_a_standard_by_standard_id(self, standard_id: int) -> List[WorkingDay]:
#         """Get working days of a standard by standard ID."""
#         with self.get_db_session() as db:

#             query = text("""
#                 SELECT * FROM working_days
#                 JOIN divisions ON working_days.division_id = divisions.id
#                 WHERE divisions.standard_id = :standard_id
#             """)
#             result = db.execute(query, {"standard_id": standard_id}).fetchall()
#             return result

#     def get_working_days_of_a_department_by_department_id(self, department_id: int) -> List[WorkingDay]:
#         """Get working days of a department by department ID."""
#         with self.get_db_session() as db:

#             query = text("""
#                 SELECT * FROM working_days
#                 JOIN divisions ON working_days.division_id = divisions.id
#                 JOIN standards ON divisions.standard_id = standards.id
#                 WHERE standards.department_id = :department_id
#             """)
#             result = db.execute(query, {"department_id": department_id}).fetchall()
#             return result

#     def get_working_days_of_a_university_by_university_id(self, university_id: int) -> List[WorkingDay]:
#         """Get working days of a university by university ID."""
#         with self.get_db_session() as db:

#             query = text("""
#                 SELECT * FROM working_days
#                 JOIN divisions ON working_days.division_id = divisions.id
#                 JOIN standards ON divisions.standard_id = standards.id
#                 JOIN departments ON standards.department_id = departments.id
#                 JOIN universities ON departments.university_id = universities.id
#                 WHERE universities.id = :university_id
#             """)
#             result = db.execute(query, {"university_id": university_id}).fetchall()
#             return result

#     def get_allotables_of_a_division_by_division_id(self, division_id: int) -> List[FacultySubjectDivision]:
#         """Get allotables for a division by division ID."""
#         with self.get_db_session() as db:

#             query = text("SELECT * FROM faculty_subject_divisions WHERE division_id = :division_id")
#             result = db.execute(query, {"division_id": division_id}).fetchall()
#             return result

#     def get_allotables_of_a_standard_by_standard_id(self, standard_id: int) -> List[FacultySubjectDivision]:
#         """Get allotables for a standard by standard ID."""
#         with self.get_db_session() as db:

#             query = text("""
#                 SELECT * FROM faculty_subject_divisions
#                 JOIN divisions ON faculty_subject_divisions.division_id = divisions.id
#                 WHERE divisions.standard_id = :standard_id
#             """)
#             result = db.execute(query, {"standard_id": standard_id}).fetchall()
#             return result

#     def get_allotables_of_a_department_by_department_id(self, department_id: int) -> List[FacultySubjectDivision]:
#         """Get allotables for a department by department ID."""
#         with self.get_db_session() as db:

#             query = text("""
#                 SELECT * FROM faculty_subject_divisions
#                 JOIN divisions ON faculty_subject_divisions.division_id = divisions.id
#                 JOIN standards ON divisions.standard_id = standards.id
#                 WHERE standards.department_id = :department_id
#             """)
#             result = db.execute(query, {"department_id": department_id}).fetchall()
#             return result

#     def get_allotables_of_a_university_by_university_id(self, university_id: int) -> List[FacultySubjectDivision]:
#         """Get allotables for a university by university ID."""
#         with self.get_db_session() as db:

#             query = text("""
#                 SELECT * FROM faculty_subject_divisions
#                 JOIN divisions ON faculty_subject_divisions.division_id = divisions.id
#                 JOIN standards ON divisions.standard_id = standards.id
#                 JOIN departments ON standards.department_id = departments.id
#                 JOIN universities ON departments.university_id = universities.id
#                 WHERE universities.id = :university_id
#             """)
#             result = db.execute(query, {"university_id": university_id}).fetchall()
#             return result

#     def get_departments_by_university_id(self, university_id: int) -> List[Department]:
#         """Get departments by university ID."""
#         with self.get_db_session() as db:

#             query = text("SELECT * FROM departments WHERE university_id = :university_id")
#             result = db.execute(query, {"university_id": university_id}).fetchall()
#             return result

#     def get_standards_by_department_id(self, department_id: int) -> List[Standard]:
#         """Get standards by department ID."""
#         with self.get_db_session() as db:

#             query = text("SELECT * FROM standards WHERE department_id = :department_id")
#             result = db.execute(query, {"department_id": department_id}).fetchall()
#             return result

#     def get_divisions_by_standard_id(self, standard_id: int) -> List[Division]:
#         """Get divisions by standard ID."""
#         with self.get_db_session() as db:

#             query = text("SELECT * FROM divisions WHERE standard_id = :standard_id")
#             result = db.execute(query, {"standard_id": standard_id}).fetchall()
            
#             return result

#     def get_working_days_by_division_id(self, division_id: int) -> List[WorkingDay]:
#         """Get working days by division ID."""
#         with self.get_db_session() as db:

#             query = text("SELECT * FROM working_days WHERE division_id = :division_id")
#             result = db.execute(query, {"division_id": division_id}).fetchall()
#             return result






#     def store_data_in_database(self, parsed_data: dict):
#         """
#         Store parsed data into the database using raw SQL queries.

#         :param parsed_data: Dictionary containing the parsed data
#         """
#         with self.get_db_session() as db_session:
#             try:
#                 # Save universities
#                 university = parsed_data["university"]
#                 query = text("""
#                     INSERT INTO universities (id, university_name) 
#                     VALUES (:id, :name)
#                     ON CONFLICT (id) DO NOTHING
#                 """)
#                 db_session.execute(query, {"id": university.id, "name": university.university_name})
#                 # Save departments
#                 for department in parsed_data["departments"]:
#                     query = text("""
#                         INSERT INTO departments (id, department_name, university_id) 
#                         VALUES (:id, :name, :university_id)
#                         ON CONFLICT (id) DO NOTHING
#                     """)
#                     db_session.execute(query, {"id": department.id, "name": department.department_name, "university_id": department.university_id})

#                 # Save standards
#                 for standard in parsed_data["standards"]:
#                     query = text("""
#                         INSERT INTO standards (id, standard_name, department_id) 
#                         VALUES (:id, :name, :department_id)
#                         ON CONFLICT (id) DO NOTHING
#                     """)
#                     db_session.execute(query, {"id": standard.id, "name": standard.standard_name, "department_id": standard.department_id})

#                 # Save divisions
#                 for division in parsed_data["divisions"]:
#                     query = text("""
#                         INSERT INTO divisions (id, division_name, standard_id) 
#                         VALUES (:id, :name, :standard_id)
#                         ON CONFLICT (id) DO NOTHING
#                     """)
#                     db_session.execute(query, {"id": division.id, "name": division.division_name, "standard_id": division.standard_id})

#                 # Save subjects
#                 for subject in parsed_data["subjects"]:
#                     query = text("""
#                         INSERT INTO subjects (id, subject_name) 
#                         VALUES (:id, :name)
#                         ON CONFLICT (id) DO NOTHING
#                     """)
#                     db_session.execute(query, {"id": subject.id, "name": subject.subject_name})

#                 # Save faculties
#                 for faculty in parsed_data["faculties"]:
#                     query = text("""
#                         INSERT INTO faculties (id, faculty_name) 
#                         VALUES (:id, :name)
#                         ON CONFLICT (id) DO NOTHING
#                     """)
#                     db_session.execute(query, {"id": faculty.id, "name": faculty.faculty_name})

#                 # Save working days
#                 for working_day in parsed_data["working_days"]:
#                     query = text("""
#                         INSERT INTO working_days (id, day_id, start_time,end_time, slot_duration, division_id) 
#                         VALUES (:id, :day_id, :start_time,:end_time, :slot_duration, :division_id)
#                         ON CONFLICT (id) DO NOTHING
#                     """)
#                     db_session.execute(query, {"id": working_day.id, "day_id": working_day.day_id, "start_time":working_day.start_time,"end_time":working_day.end_time, "slot_duration":working_day.slot_duration, "division_id":working_day.division_id})

#                 # Save breaks
#                 for break_item in parsed_data["breaks_list"]:
#                     # Insert into slot_allotables table
#                     query_slot_allotables = text("""
#                         INSERT INTO slot_allotables (
#                             id, division_id, name, continuous_slot, weekly_frequency, fixed_slot
#                         ) 
#                         VALUES (
#                             :id, :division_id, :name, :continuous_slot, :weekly_frequency, :fixed_slot
#                         )
#                         ON CONFLICT (id) DO NOTHING
#                     """)
#                     db_session.execute(query_slot_allotables, {
#                         "id": break_item.id,
#                         "division_id": break_item.division_id,
#                         "name": break_item.name,
#                         "continuous_slot": break_item.continuous_slot,
#                         "weekly_frequency": break_item.weekly_frequency,
#                         "fixed_slot": break_item.fixed_slot
#                     })

#                     # Insert into breaks table
#                     query_breaks = text("""
#                         INSERT INTO breaks (
#                             id, start_time, end_time, working_day_id
#                         )
#                         VALUES (
#                             :id, :start_time, :end_time, :working_day_id
#                         )
#                         ON CONFLICT (id) DO NOTHING
#                     """)
#                     db_session.execute(query_breaks, {
#                         "id": break_item.id,
#                         "start_time": break_item.start_time,
#                         "end_time": break_item.end_time,
#                         "working_day_id": break_item.working_day_id
#                     })

#                 # Save faculty-subject-division relationships
#                 for relationship in parsed_data["faculty_subject_division_list"]:
#                     query = text("""
#                         INSERT INTO faculty_subject_division (faculty_id, subject_id, division_id) 
#                         VALUES (:faculty_id, :subject_id, :division_id)
#                         ON CONFLICT (faculty_id, subject_id, division_id) DO NOTHING
#                     """)
#                     db_session.execute(query, {
#                         "faculty_id": relationship.faculty_id,
#                         "subject_id": relationship.subject_id,
#                         "division_id": relationship.division_id
#                     })

#                 # Commit transaction
#                 db_session.commit()
#                 print("Parsed data successfully stored in the database.")
#             except Exception as e:
#                 db_session.rollback()
#                 print(f"Error occurred while storing data in the database: {e}")
#                 raise
