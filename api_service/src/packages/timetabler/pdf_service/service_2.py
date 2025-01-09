import os

from fpdf import FPDF
from typing import List
from dataclasses import dataclass
from datetime import datetime
from src.packages.timetabler.business.domain import Slot
from enum import Enum



class CustomSet:
    def __init__(self):
        self.elements = []

    def add(self, element):
        if element not in self.elements:
            self.elements.append(element)

    def __contains__(self, element):
        return element in self.elements

    def __iter__(self):
        return iter(self.elements)

    def __len__(self):
        return len(self.elements)

    def items(self):
        return self.elements

    def get(self, element, default=None):
        return element if element in self.elements else default

    def __getitem__(self, index):
        return self.elements[index]

class DayEnum(Enum):
    MONDAY="MONDAY"
    TUESDAY="TUESDAY"
    WEDNESDAY="WEDNESDAY"
    THURSDAY="THURSDAY"
    FRIDAY="FRIDAY"
    SATURDAY="SATURDAY"
    SUNDAY="SUNDAY"




def day_order(day_name: str) -> int:
    # Get the position of the day from DayEnum
    try:
        return list(DayEnum).index(DayEnum[day_name.upper()])
    except KeyError:
        return float('inf')  # Handle invalid day names by placing them at the end


# Function to create shortform from a string (first 3 letters of each word)
def create_short_form(full_name: str) -> str:
    words = full_name.split()
    shortform = ''.join([word[:1].upper() for word in words])
    return shortform


def convert_time_to_12hr_format(time_obj) -> str:
    try:
        # Convert time object to string if it is not a string
        if isinstance(time_obj, datetime):
            time_str = time_obj.strftime('%H:%M:%S')
        else:
            time_str = time_obj

        # Parse the string and convert to 12-hour format
        time_obj = datetime.strptime(str(time_str), '%H:%M:%S')
        return time_obj.strftime('%I:%M %p').lstrip('0')  # Remove leading zero from hour
    except ValueError:
        return time_obj


@dataclass
class ClassTimetable:
    class_name: str
    slots: List[Slot]


class TimetablePDF(FPDF):
    def header(self):
        self.set_font("Arial", "B", 12)
        self.cell(0, 10, "Class Timetable", border=False, ln=True, align="C")
        self.ln(5)

    def footer(self):
        self.set_y(-15)
        self.set_font("Arial", "I", 8)
        self.cell(0, 10, f"Page {self.page_no()}", align="C")

    def add_timetable(self, class_name: str, slots: List[Slot]):
        # Collect unique times and days
        times = sorted({(slot.start_time, slot.end_time) for slot in slots if slot.start_time and slot.end_time})
        days = sorted({slot.working_day.day.day_name for slot in slots if slot.working_day and slot.working_day.day}, key=day_order)

        # Create a mapping for time and days
        timetable = {time: {day: "" for day in days} for time in times}
        subject_short_forms = {}
        faculty_short_forms = {}
        division_short_forms = {}

        # Process the slots
        for slot in slots:
            if slot.start_time and slot.end_time and slot.working_day and slot.working_day.day:
                time_key = (slot.start_time, slot.end_time)
                if slot.slot_alloted_to is not None:
                    if (
                        slot.slot_alloted_to
                        and hasattr(slot.slot_alloted_to, "subject")
                        and slot.slot_alloted_to.subject is not None
                        and hasattr(slot.slot_alloted_to, "faculty")
                        and slot.slot_alloted_to.faculty is not None
                        and hasattr(slot.slot_alloted_to, "division")
                        and slot.slot_alloted_to.division is not None
                    ):
                        # Add subject and faculty short form if not already added
                        subject_name = str(slot.slot_alloted_to.subject.subject_name)
                        faculty_name = str(slot.slot_alloted_to.faculty.faculty_name)
                        division_name = str(slot.slot_alloted_to.division.division_name)
                        if subject_name not in subject_short_forms:
                            subject_short_forms[subject_name] = create_short_form(subject_name)
                        if faculty_name not in faculty_short_forms:
                            faculty_short_forms[faculty_name] = create_short_form(faculty_name)
                        if division_name not in division_short_forms:
                            division_short_forms[division_name] = create_short_form(division_name)

                        # timetable[time_key][slot.working_day.day.day_name] = f"{division_short_forms[division_name]}-{subject_short_forms[subject_name]}"
                        timetable[time_key][slot.working_day.day.day_name] = f"{subject_short_forms[subject_name]}-{faculty_short_forms[faculty_name]}"

                    elif (
                            slot.slot_alloted_to
                            and hasattr(slot.slot_alloted_to, "fixed_slot")
                            and slot.slot_alloted_to.fixed_slot is True
                    ):
                        timetable[time_key][slot.working_day.day.day_name] = str(slot.slot_alloted_to.name) or ""
                else:
                    timetable[time_key][slot.working_day.day.day_name] = ""

        # Generate table
        self.add_page()
        self.set_font("Arial", "B", 14)
        self.cell(0, 10, f"Class: {class_name}", ln=True, align="L")
        self.ln(5)

        # Create table headers
        self.set_font("Arial", "B", 10)
        self.cell(33, 10, "Time", 1, align="C")
        for day in days:
            self.cell(30, 10, day, 1, align="C")
        self.ln()

        # Populate table rows
        self.set_font("Arial", "", 10)
        for time in times:
            self.cell(33, 10, f"{convert_time_to_12hr_format(time[0])}-{convert_time_to_12hr_format(time[1])}", 1, align="C")
            for day in days:
                self.cell(30, 10, timetable[time].get(day, ""), 1, align="C")  # Corrected the call to 'cell'
            self.ln()

        # Display short forms side by side in a compact horizontal manner
        self.ln(5)
        self.set_font("Arial", "I", 8)

        # Define width for short forms (we will use dynamic width as per content)
        max_width = 0  # To calculate the maximum width for dynamic allocation
        subject_items = list(subject_short_forms.items())
        faculty_items = list(faculty_short_forms.items())

        # Calculate the maximum width of subject short forms and faculty short forms
        for item in subject_items + faculty_items:
            width = self.get_string_width(f"{item[1]}: {item[0]}") + 4  # Add some padding for spacing
            max_width = max(max_width, width)

        # First, display all lecture short forms
        self.cell(0, 5, "Lecture Short Forms:", 0, 1, "L")
        self.set_font("Arial", "", 8)

        # Display subject short forms horizontally
        for item in subject_items:
            self.cell(max_width, 5, f"{item[1]}: {item[0]}", ln=False)  # Display in a single line
        self.ln()

        self.cell(0, 5, "", 0, 1, "L")

        # Then, display faculty names below the lecture short forms
        self.cell(0, 5, "Faculty Short Forms:", 0, 1, "L")
        self.set_font("Arial", "", 8)

        # Display faculty short forms horizontally
        for item in faculty_items:
            self.cell(max_width, 5, f"{item[1]}: {item[0]}", ln=False)  # Display in a single line
        self.ln(10)





def create_university_directory(university_id: str):
    import uuid
    id = uuid.uuid4()
    """
    Create a directory for the university.
    """
    # university_dir = f"zip_timetables/{university_id}_university"
    university_dir = f"zip_timetables/{id}_university"

    if not os.path.exists(university_dir):
        os.makedirs(university_dir)
    return university_dir

def save_division_pdf(pdf: TimetablePDF, division_name: str, university_dir: str):
    """
    Save a PDF for a division's timetable.
    """
    division_dir = os.path.join(university_dir, division_name)
    if not os.path.exists(division_dir):
        os.makedirs(division_dir)
    
    pdf.output(os.path.join(division_dir, f"{division_name}_timetable.pdf"))

def save_faculty_pdf(pdf: TimetablePDF, faculty_name: str, university_dir: str):
    """
    Save a PDF for a faculty's timetable.
    """
    faculty_dir = os.path.join(university_dir, faculty_name)
    if not os.path.exists(faculty_dir):
        os.makedirs(faculty_dir)
    
    pdf.output(os.path.join(faculty_dir, f"{faculty_name}_timetable.pdf"))

def save_combined_timetable_pdf(pdf: TimetablePDF, university_dir: str, class_timetables: List[ClassTimetable], faculty_slots_dict: dict):
    """
    Save a combined PDF for the entire university including both class and faculty timetables.
    """
    # Generate timetables for classes (divisions)
    for class_timetable in class_timetables:
        pdf.add_timetable(class_timetable.class_name, class_timetable.slots)

    # Add a page separator
    pdf.add_page()
    pdf.set_font("Arial", "B", 14)
    pdf.cell(0, 10, "Faculty Timetables", ln=True, align="L")
    pdf.ln(5)

    # Generate timetables for faculties
    for faculty_name, slots_for_faculty in faculty_slots_dict.items():
        pdf.add_timetable(faculty_name, slots_for_faculty)

    # Save the combined PDF
    pdf.output(os.path.join(university_dir, "combined_timetables.pdf"))

def create_class_timetable_pdfs(slots: List[Slot], university_id: str='UNI_1') -> None:
    """
    Create class and faculty timetables in PDF format.
    """
    class_timetables: List[ClassTimetable] = []
    divisions_list = CustomSet()
    for slot in slots:
        if slot.working_day and slot.working_day.division:
            divisions_list.add(slot.working_day.division.division_name)

    # Create a university directory
    university_dir = create_university_directory(university_id)

    # Generate timetables for classes (divisions)
    for division_name in divisions_list:
        slots_for_division = [
            division_slot for division_slot in slots
            if division_slot.working_day and division_slot.working_day.division and division_slot.working_day.division.division_name == division_name
        ]
        class_timetables.append(ClassTimetable(class_name=division_name, slots=slots_for_division))

    # Generate timetables for faculties (faculty-wise)
    faculty_slots = CustomSet()
    for slot in slots:
        if slot.slot_alloted_to and hasattr(slot.slot_alloted_to, 'faculty') and slot.slot_alloted_to.faculty:
            faculty_slots.add(slot.slot_alloted_to.faculty.faculty_name)

    faculty_slots_dict = {faculty: [] for faculty in faculty_slots.items()}
    for slot in slots:
        if slot.slot_alloted_to and hasattr(slot.slot_alloted_to, 'faculty') and slot.slot_alloted_to.faculty:
            faculty_slots_dict[slot.slot_alloted_to.faculty.faculty_name].append(slot)

    # Generate and save PDFs for classes
    for class_timetable in class_timetables:
        pdf = TimetablePDF()
        pdf.add_timetable(class_timetable.class_name, class_timetable.slots)
        save_division_pdf(pdf, class_timetable.class_name, university_dir)

    # Generate and save PDFs for faculties
    for faculty_name, slots_for_faculty in faculty_slots_dict.items():
        pdf = TimetablePDF()
        pdf.add_timetable(faculty_name, slots_for_faculty)
        save_faculty_pdf(pdf, faculty_name, university_dir)

    # Save the combined PDF including both class and faculty timetables
    combined_pdf = TimetablePDF()
    save_combined_timetable_pdf(combined_pdf, university_dir, class_timetables, faculty_slots_dict)

    print(f"PDFs for the university '{university_id}' have been created and stored.")
    return university_dir, university_id
