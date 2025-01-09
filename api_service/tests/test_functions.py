


# from unittest import TestCase
# from datetime import time,datetime,date,timedelta
# # from src.domain3 import WorkingDay, Day, DayEnum, Slot, Break, SlotAllotable
# # from other_utils import save_output_file
# from src.app import parse_input_json_to_python,generate_university_timetables_chromosome, generate_gene, get_total_slots_for_university
# # import  src.genetic_algorithm as ga
# # from src.constraints import SameFacultyAtDifferentLectureAtSameTime
# import json
# import os


# class TestEmptyTimetableCreation(TestCase):

#     def test_standard_case(self):

    
#         with open("./inputs/input_2.json", "r") as f:
#             input_data = json.load(f)

#         # university,departments,standards,divisions,slots,faculty_subject_division_list,  faculties, subjects = parse_input_json_to_python(input_data)

#         output = parse_input_json_to_python(input_data)
#         # from other_utils import save_output_file

#         print("Saving json parsed university input")
#         # save_output_file('output_2.json', output)
        

#         # university_timetables, allotables = generate_university_timetables_chromosome(output)
#         chromosome_length = get_total_slots_for_university(output)
#         fitness_evaluator = ga.FitnessEvaluator(constraints=[
#             # ga.SameFacultyAtDifferentLectureAtSameTime(penalty=1),
#             ga.NoLectureAtBreak(penalty=0.5)
#         ])
#         genetic_algo_university = ga.GeneticAlgorithm(
#             data_pool=output,
#             chromosome_length=chromosome_length//10,
#             fitness_evaluator=fitness_evaluator,
#             gene_generator=generate_gene,
#             population_size=chromosome_length//10
#         )
#         university_timetables = genetic_algo_university.run(chromosome_length,0.005)




#         print("Saving university timetable ...")
#         # print(university_timetables)
#         save_output_file('output_utt_1.json', university_timetables)