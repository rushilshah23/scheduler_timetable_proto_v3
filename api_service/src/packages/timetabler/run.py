
from timetabler.modules.ga_scale import generate_timetable

from timetabler.business.business_utils import Utils
from timetabler.business.utils import save_output_file


if __name__ == "__main__":
    # print(ascending_sequence_machine.perform_ga())





    # fittest_chromosome = timetable_generator.perform_ga()
    
    fittest_chromosome = generate_timetable()

    # print(fittest_chromosome)
    university_timetables = fittest_chromosome
    university_timetables = Utils.sort_slots(fittest_chromosome.genes)


    print("Saving university timetable ...")
    # print(university_timetables)
    save_output_file('output_utt_1.json', university_timetables)
    from .pdf_service.service_2 import create_class_timetable_pdfs

    create_class_timetable_pdfs(university_timetables)