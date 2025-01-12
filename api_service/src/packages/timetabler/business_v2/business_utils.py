from datetime import datetime, timezone, time,timedelta
from src.packages.timetabler.business.domain import *
from src.packages.timetabler.business.utils import get_new_id
from typing import List, Dict
from src.packages.timetabler.business.domain_utils import DomainUtils
class Utils:




    @staticmethod
    def get_empty_slots_with_timing(start_time: time, end_time: time,working_day:WorkingDay,weekly_slot_number:int=0, slot_duration: int=30*60) -> List[Slot]:
        """
        Generate a list of empty slots between start_time and end_time.
        :param start_time: The starting time for the day.
        :param end_time: The end time for the day.
        :param slot_duration: The duration of each slot in seconds.
        :return: A list of empty slots.
        """
        start_datetime = datetime.combine(datetime.today(), start_time)
        end_datetime = datetime.combine(datetime.today(), end_time)

        if start_datetime > end_datetime:
            raise ValueError("Start time cannot be greater than End time")

        slots = []
        current_time = start_datetime
        daily_slot_number = 0

        while current_time + timedelta(seconds=slot_duration) <= end_datetime:
            next_time = current_time
            current_time = next_time + timedelta(seconds=slot_duration)
            # slots.append(Slot(id=slot_id, start_time=next_time.strftime("%H:%M"), end_time=current_time.strftime("%H:%M"),working_day_id=working_day.id, working_day=working_day))
            slots.append(Slot(id=get_new_id(), start_time=next_time.time(), end_time=current_time.time(),working_day_id=working_day.id, working_day=working_day, daily_slot_number=daily_slot_number, weekly_slot_number=weekly_slot_number))

            daily_slot_number += 1
            weekly_slot_number+=1

        if current_time < end_datetime:
            # slots.append(Slot(id=slot_id, start_time=current_time.strftime("%H:%M"), end_time=end_datetime.strftime("%H:%M"),working_day_id=working_day.id, working_day=working_day))
            slots.append(Slot(id=get_new_id(), start_time=current_time.time(), end_time=end_datetime.time(),working_day_id=working_day.id, working_day=working_day, weekly_slot_number=weekly_slot_number, daily_slot_number=daily_slot_number))


        return slots

    @staticmethod
    def find_slots_for_a_time_range(working_day: WorkingDay, start_time: time, end_time: time) -> List[int]:
        """
        Find slot numbers within a time range.
        :param working_day: The working day that contains the slots.
        :param start_time: The start time for the range.
        :param end_time: The end time for the range.
        :return: A list of slot IDs.
        """
        slot_numbers = []
        empty_slots_for_the_week = Utils.get_empty_slots_with_timing(working_day.start_time, working_day.end_time,slot_duration= working_day.slot_duration, working_day=working_day)


        start_slot = None
        end_slot = None


        for slot in empty_slots_for_the_week:
            if slot.working_day_id == working_day.id:
                if slot.start_time == start_time.strftime("%H:%M") and slot.end_time == end_time.strftime("%H:%M"):
                    slot_numbers.append(slot.id)
                    return slot_numbers

                if slot.start_time == start_time.strftime("%H:%M"):
                    start_slot = slot.weekly_slot_number

                if slot.end_time == end_time.strftime("%H:%M"):
                    end_slot = slot.weekly_slot_number

                if start_slot is not None and end_slot is not None:
                    for i in range(start_slot, end_slot):
                        slot_numbers.append(i)
                    slot_numbers.append(end_slot)

        if start_slot is None or end_slot is None:
            raise ValueError("Start Time or End Time goes beyond the working hours.")

        return slot_numbers

    @staticmethod
    def create_weekly_slots_table(working_days: List[WorkingDay]) -> List[Slot]:
        """
        Create a timetable with empty slots, marking the occupied slots as well.
        :param working_days: The working days list.
        :return: A dictionary with days and their corresponding slots.
        """
        # empty_time_table = defaultdict(list)
        empty_time_table:List[Slot] = []
        
        weekly_slot_number_count = 0

        for work_day in working_days:
            day = work_day.day

            slots = Utils.get_empty_slots_with_timing(work_day.start_time, work_day.end_time,work_day,weekly_slot_number_count, work_day.slot_duration)
            if slots:  # Ensure the list is not empty
                max_weekly_slot_number = max(slots, key=lambda slot: slot.weekly_slot_number).weekly_slot_number
                weekly_slot_number_count = max(weekly_slot_number_count, max_weekly_slot_number)+1
            else:
                max_weekly_slot_number = None  # Handle the case where slots is empty
            # empty_time_table[day.day_name] = slots
            empty_time_table.extend(slots)
            # for break_lecture in work_day.breaks:
            #     break_range = Utils.find_slots_for_a_time_range(work_day, break_lecture.slot.start_time, break_lecture.slot.end_time)
            #     for break_slot_number in break_range:
            #         for slot in empty_time_table[day.day_name]:
            #             if slot.id == break_slot_number:
            #                 slot.slot_alloted_to = None  # Mark slot as occupied by break
        return empty_time_table

    # @staticmethod
    # def create_per_slot_slots_table(slot_id: str) -> List[Slot]:
    #     """
    #     Create a timetable with empty slots, marking the occupied slots as well.
    #     :param working_days: The working days list.
    #     :return: A dictionary with days and their corresponding slots.
    #     """
    #     # empty_time_table = defaultdict(list)
    #     empty_time_table:List[Slot] = []
        
    #     weekly_slot_number_count = 0
    #     working_day:Slot = DomainUtils().get_working_day_from_id(id=working_day_id)
        
    #     day = working_day.day

    #     slots = Utils.get_empty_slots_with_timing(working_day.start_time, working_day.end_time,working_day,weekly_slot_number_count, working_day.slot_duration)
    #     if slots:  # Ensure the list is not empty
    #         max_weekly_slot_number = max(slots, key=lambda slot: slot.weekly_slot_number).weekly_slot_number
    #         weekly_slot_number_count = max(weekly_slot_number_count, max_weekly_slot_number)+1
    #     else:
    #         max_weekly_slot_number = None  # Handle the case where slots is empty
    #     # empty_time_table[day.day_name] = slots
    #     empty_time_table.extend(slots)

    #     return empty_time_table


    # @staticmethod
    # def create_slot_from_slot_id(working_day_id: str) -> List[Slot]:
    #     """
    #     Create a timetable with empty slots, marking the occupied slots as well.
    #     :param working_days: The working days list.
    #     :return: A dictionary with days and their corresponding slots.
    #     """
    #     # empty_time_table = defaultdict(list)
    #     empty_time_table:List[Slot] = []
        
    #     weekly_slot_number_count = 0
    #     working_day:WorkingDay = DomainUtils().get_working_day_from_id(id=working_day_id)
        
    #     day = working_day.day

    #     slots = Utils.get_empty_slots_with_timing(working_day.start_time, working_day.end_time,working_day,weekly_slot_number_count, working_day.slot_duration)
    #     if slots:  # Ensure the list is not empty
    #         max_weekly_slot_number = max(slots, key=lambda slot: slot.weekly_slot_number).weekly_slot_number
    #         weekly_slot_number_count = max(weekly_slot_number_count, max_weekly_slot_number)+1
    #     else:
    #         max_weekly_slot_number = None  # Handle the case where slots is empty
    #     # empty_time_table[day.day_name] = slots
    #     empty_time_table.extend(slots)

    #     return empty_time_table


    @staticmethod
    def create_working_day_slots_table(working_day_id: str) -> List[Slot]:
        """
        Create a timetable with empty slots, marking the occupied slots as well.
        :param working_days: The working days list.
        :return: A dictionary with days and their corresponding slots.
        """
        # empty_time_table = defaultdict(list)
        empty_time_table:List[Slot] = []
        
        weekly_slot_number_count = 0
        working_day:WorkingDay = DomainUtils().get_working_day_from_id(id=working_day_id)
        
        day = working_day.day

        slots = Utils.get_empty_slots_with_timing(working_day.start_time, working_day.end_time,working_day,weekly_slot_number_count, working_day.slot_duration)
        if slots:  # Ensure the list is not empty
            max_weekly_slot_number = max(slots, key=lambda slot: slot.weekly_slot_number).weekly_slot_number
            weekly_slot_number_count = max(weekly_slot_number_count, max_weekly_slot_number)+1
        else:
            max_weekly_slot_number = None  # Handle the case where slots is empty
        # empty_time_table[day.day_name] = slots
        empty_time_table.extend(slots)

        return empty_time_table



    @staticmethod
    def create_division_slots_table(division_id: str) -> List[Slot]:
        """
        Create a timetable with empty slots, marking the occupied slots as well.
        :param working_days: The working days list.
        :return: A dictionary with days and their corresponding slots.
        """
        # empty_time_table = defaultdict(list)
        empty_time_table:List[Slot] = []

        working_days_ids:List[str] = DomainUtils().get_working_days_of_a_divsion_by_dvision_id(division_id=division_id)

        for working_day_id in working_days_ids:

            working_day_slots = Utils.create_working_day_slots_table(working_day_id=working_day_id)
            empty_time_table.extend(working_day_slots)
 


    @staticmethod
    def create_standard_slots_table(standard_id: str) -> List[Slot]:
        """
        Create a timetable with empty slots, marking the occupied slots as well.
        :param working_days: The working days list.
        :return: A dictionary with days and their corresponding slots.
        """
        # empty_time_table = defaultdict(list)
        empty_time_table:List[Slot] = []
        working_days_ids:List[str] = DomainUtils().get_working_days_of_a_standard_by_standard_id(standard_id==standard_id)

        for working_day_id in working_days_ids:

            working_day_slots = Utils.create_working_day_slots_table(working_day_id=working_day_id)
            empty_time_table.extend(working_day_slots)
 

    @staticmethod
    def create_department_slots_table(department_id: str) -> List[Slot]:
        """
        Create a timetable with empty slots, marking the occupied slots as well.
        :param working_days: The working days list.
        :return: A dictionary with days and their corresponding slots.
        """
        # empty_time_table = defaultdict(list)
        empty_time_table:List[Slot] = []
        working_days_ids:List[str] = DomainUtils().get_working_days_of_a_department_by_department_id(department_id==department_id)

        for working_day_id in working_days_ids:

            working_day_slots = Utils.create_working_day_slots_table(working_day_id=working_day_id)
            empty_time_table.extend(working_day_slots)
 
    @staticmethod
    def create_university_slots_table(university_id: str) -> List[Slot]:
        """
        Create a timetable with empty slots, marking the occupied slots as well.
        :param working_days: The working days list.
        :return: A dictionary with days and their corresponding slots.
        """
        # empty_time_table = defaultdict(list)
        empty_time_table:List[Slot] = []
        working_days:List[str] = DomainUtils().get_working_days_of_a_university_by_university_id(university_id=university_id)

        for working_day in working_days:
            working_day_id = working_day.id

            working_day_slots = Utils.create_working_day_slots_table(working_day_id=working_day_id)
            empty_time_table.extend(working_day_slots)
        return empty_time_table
 



    @staticmethod
    def sort_slots(slots:List[Slot])->List[Slot]:

        def day_order(day_name: str) -> int:
            # Get the position of the day from DayEnum
            try:
                return list(DayEnum).index(DayEnum[day_name.upper()])
            except KeyError:
                return float('inf')  # Handle invalid day names by placing them at the end

        return sorted(
            slots,
            key=lambda slot: (
                slot.working_day.division.standard.department.department_name,
                slot.working_day.division.standard.standard_name,
                slot.working_day.division.division_name,
                day_order(slot.working_day.day.day_name),
                slot.start_time,
                slot.end_time,
            )
        )
