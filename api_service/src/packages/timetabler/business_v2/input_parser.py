from typing import List, Dict
from src.packages.timetabler.business_v2.domain import *
from src.packages.timetabler.business_v2.utils import get_new_id,convert_str_to_time
# from timetabler.business.business_utils import Utils
from datetime import datetime, timedelta

# def generate_slot_objects(obj, start_time, end_time, slot_duration):
def generate_slot_objects(obj,slot_duration):

    """
    Generates a list of cloned objects with updated start_time and end_time properties.

    Args:
        obj (dict): The object to clone (can be a dictionary or a class instance).
        start_time (time): The start time of the range.
        end_time (time): The end time of the range.
        slot_duration (int): Duration of each slot in seconds.

    Returns:
        list: A list of cloned objects with updated times.
    """
    # current_start = start_time
    current_start = obj.start_time
    end_time = obj.end_time

    slots = []
    
    while current_start < end_time:
        current_end = (datetime.combine(datetime.min, current_start) + timedelta(seconds=slot_duration)).time()
        if current_end > end_time:
            break
        
        # Clone the object
        if isinstance(obj, dict):
            cloned_obj = obj.copy()
        else:
            cloned_obj = obj.__class__(**{k: v for k, v in obj.__dict__.items()})
        
        # Update start_time and end_time attributes
        if isinstance(cloned_obj, dict):
            cloned_obj["start_time"] = current_start
            cloned_obj["end_time"] = current_end
        else:
            setattr(cloned_obj, "start_time", current_start)
            setattr(cloned_obj, "end_time", current_end)
        
        slots.append(cloned_obj)
        current_start = current_end
    
    return slots

def find_continuos_slot_count(start_time, end_time, slot_duration)->int:
    # 9 am - 10 30 am ---- slot_duration 30 min ---- output 3
    start_dt = datetime.combine(datetime.today(), start_time)
    end_dt = datetime.combine(datetime.today(), end_time)
    
    # Calculate the difference in seconds
    total_duration_seconds = (end_dt - start_dt).total_seconds()
    # Divide by slot duration to find the number of slots
    num_slots = int(total_duration_seconds // slot_duration)
    return num_slots


def clone_faculty_subject_divisions(original_object, num_clones):
    """
    Create multiple clones of a FacultySubjectDivision object with different IDs.
    
    Args:
        original_object (FacultySubjectDivision): The original object to clone.
        num_clones (int): The number of clones to create.
    
    Returns:
        list: A list of cloned FacultySubjectDivision objects.
    """
    clones = []
    for _ in range(num_clones):
        # Create a clone with a new ID
        clone = FacultySubjectDivision(
            id=get_new_id(),
            name=original_object.name,
            faculty_id=original_object.faculty_id,
            subject_id=original_object.subject_id,
            division_id=original_object.division_id,
            faculty=original_object.faculty,
            subject=original_object.subject,
            division=original_object.division,
            continuous_slot=original_object.continuous_slot,
            weekly_frequency=original_object.weekly_frequency  # Copying the same frequency
        )
        clones.append(clone)
    return clones



def parse_input_json_to_python(input_data: Dict):
    slots: List[Slot] = []
    faculty_subject_division_list: List[FacultySubjectDivision] = []
    subjects_list: List[Subject] = []
    faculties_list:List[Faculty] = []

    departments_list = []
    standards_list = []
    divisions_list=[]
    working_days_list=[]


    fixed_allotables = []
    unfixed_allotables = []

    entities = []
    break_entities = []
    faculty_subject_division_entities = []
    


    # Create university
    university = University(
        id=get_new_id(),
        university_name=input_data["university_name"],
    )

    


    # Parse departments
    for dept_data in input_data["departments"]:
        department = Department(
            id=get_new_id(),
            department_name=dept_data["departmentName"],
            university_id=university.id,
            university=university
        )
        departments_list.append(department)

    # Parse standards
    for std_data in input_data["standards"]:
        department = next((dept for dept in departments_list if dept.department_name == std_data['departmentName']), None)
        standard = Standard(
            id=get_new_id(),
            standard_name=std_data["standardName"],
            department_id=department.id,
            department=department
        )
        standards_list.append(standard)

    # Parse divisions
    for div_data in input_data["divisions"]:
        standard = next((std for std in standards_list if std.standard_name == div_data['standardName']), None)
    
        division = Division(
            id=get_new_id(),
            division_name=div_data["divisionName"],
            standard_id=standard.id,
            standard=standard
        )
        divisions_list.append(division)

    # Parse working days
    for working_day in input_data["workingDays"]:
        division = next((div for div in divisions_list if div.division_name == working_day['divisionName']), None)
        if division is None:
            raise Exception("Invalid division in working days section - ",working_day['divisionName'])
        schedule = working_day['schedule']
        for day_data in schedule:
            day_enum = DayEnum[day_data["dayName"]]

            day = Day(
                id=get_new_id(),
                day_name=day_enum.value
            )
            working_day = WorkingDay(
                id=get_new_id(),
                day_id=day.id,
                # start_time=datetime.strptime(day_data["startTime"], "%I:%M%p").time(),
                # end_time=datetime.strptime(day_data["endTime"], "%I:%M%p").time(),
                start_time=convert_str_to_time(day_data["startTime"]),
                end_time=convert_str_to_time(day_data["endTime"]),
                slot_duration=day_data["slotSize"],
                day=day,
                division_id=division.id,
                division=division
            )

            working_days_list.append(working_day)

            # Parse breaks
            for break_data in day_data.get("breaks", []):
                raw_break_obj = Break(
                    id=get_new_id(),
                    division_id=division.id,
                    division=division,
                    name=break_data["breakName"],
                    start_time=convert_str_to_time(break_data["startTime"]),
                    end_time=convert_str_to_time(break_data["endTime"]),
                    working_day_id=working_day.id,
                    working_day=working_day,
                    continuous_slot=1,
                    weekly_frequency=1

                )
                slot_divided_break = generate_slot_objects(obj=raw_break_obj,slot_duration=working_day.slot_duration )
                breaks_list.extend(slot_divided_break)
                # slot = Slot(
                #     id=get_new_id(),
                #     start_time=Utils.convert_str_to_time(break_data["startTime"]),
                #     end_time=Utils.convert_str_to_time(break_data["endTime"]),
                #     working_day_id=working_day.id,
                #     working_day=working_day,
                #     slot_alloted_to=Break(
                #         id=get_new_id(),
                #         name=break_data["breakName"],
                #         division_id=division.id,
                #         division=division
                #     )
                # )
                # slots.append(slot)
    for subject in input_data['subjects']:
        subject_instance = Subject(get_new_id(),subject['subjectName'])
        subjects_list.append(subject_instance)

    for faculty in input_data['faculties']:
        faculty_instance = Faculty(get_new_id(),faculty['facultyName'])
        faculties_list.append(faculty_instance)

    # # Parse subjects and faculties
    # subjects = {sub["subjectName"]: Subject(id=get_new_id(), subject_name=sub["subjectName"]) for sub in input_data["subjects"]}
    # faculties = {fac["facultyName"]: Faculty(id=get_new_id(), faculty_name=fac["facultyName"]) for fac in input_data["faculties"]}

    # Parse subject-faculty-division relationships
    for rel_data in input_data["subjectFacultyDivision"]:
        division = next((div for div in divisions_list if div.division_name == rel_data['divisionName']), None)
        faculty = next((fac for fac in faculties_list if fac.faculty_name == rel_data['facultyName']), None)
        subject = next((sub for sub in subjects_list if sub.subject_name == rel_data['subjectName']), None)


        
        if not (division or subject or faculty):
            raise Exception("Invalid division or subject or faculty")
            # continue  # Skip if division not found

        raw_faculty_subject_division_obj = FacultySubjectDivision(
            id=get_new_id(),
            name=f"{subject.subject_name} - {faculty.faculty_name}",
            faculty_id=faculty.id,
            subject_id=subject.id,
            division_id=division.id,
            faculty=faculty,
            subject=subject,
            division=division,
            continuous_slot=rel_data['compulsoryContinuousSlots'],
            weekly_frequency=rel_data['weeklyFrequency']

        )
        weekly_frequency_clones_faculty_subject_division_obj = clone_faculty_subject_divisions(raw_faculty_subject_division_obj, raw_faculty_subject_division_obj.weekly_frequency)

        faculty_subject_division_list.extend(weekly_frequency_clones_faculty_subject_division_obj)

    return {
        "university": university,
        "departments": departments_list,
        "standards":standards_list,
        "divisions":divisions_list,
        "subjects":subjects_list,
        "faculties":faculties_list,
        "slots": slots,
        "faculty_subject_division_list": faculty_subject_division_list,
        "working_days":working_days_list,
        "breaks_list":breaks_list,
        "universities":universities
    }



