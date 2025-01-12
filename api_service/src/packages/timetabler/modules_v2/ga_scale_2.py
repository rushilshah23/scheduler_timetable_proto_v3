from src.packages.ga import Gene, Chromosome, DNA,FitnessEvaluator,GeneticAlgorithmConfig,GeneticAlgorithmFunctionalities,GeneticAlgorithmMachine, DataPool
from dataclasses import dataclass
import random
from typing import List
from timetabler.business.domain import * 
from timetabler.modules.constraints import NoSameSlotIdRepetition,FixedAllotablesAtFixedSlot,IncompleteSlots,AllAllotablesMapped
import json
from timetabler.business.input_parser import parse_input_json_to_python
from timetabler.business.domain_utils import DomainUtils
from timetabler.business.business_utils import Utils
from timetabler.business.utils import save_output_file
import copy


@dataclass
class SlotData(DataPool):
    allotables: List[SlotAllotable]
    slots: List[Slot]

    def __post_init__(self):
        if len(self.allotables) > len(self.slots):
            while len(self.allotables) < len(self.slots):
                self.allotables.append(None)

                

def slots_generator( working_day_id=None, division_id=None, standard_id=None, department_id=None, university_id=None):
    slots:List[Slot] = []
    # if slot_id is not None:
    #     slots.extend(Utils.cr(working_day_id=working_day_id))
    if working_day_id is not None:
        slots.extend(Utils.create_working_day_slots_table(working_day_id=working_day_id))
    elif division_id is not None:
        slots.extend(Utils.create_division_slots_table(division_id=division_id))
    elif standard_id is not None:
        slots.extend(Utils.create_standard_slots_table(standard_id=standard_id))
    elif department_id is not None:
        slots.extend(Utils.create_department_slots_table(department_id=department_id))
    elif university_id is not None:
        slots.extend(Utils.create_university_slots_table(university_id=university_id))
    return slots

def slot_allotables_generator(working_day_id=None, division_id=None, standard_id=None, department_id=None, university_id=None):
    allotables:List[SlotAllotable] = []

    if working_day_id is not None:
        working_day:WorkingDay = DomainUtils().get_working_day_from_id(id=working_day_id)
        division_id = working_day.division_id
        probable_allotables_for_working_day = DomainUtils().get_allotables_of_a_division_by_division_id(division_id=division_id)
        allotables.extend(probable_allotables_for_working_day)
    elif division_id is not None:
        probable_allotables_for_division = DomainUtils().get_allotables_of_a_division_by_division_id(division_id=division_id)
        allotables.extend(probable_allotables_for_division)       
    elif standard_id is not None:
        probable_allotables_for_standard = DomainUtils().get_allotables_of_a_standard_by_standard_id(standard_id=standard_id)
        allotables.extend(probable_allotables_for_standard)       
    elif department_id is not None:
        probable_allotables_for_department = DomainUtils().get_allotables_of_a_department_by_department_id(department_id=department_id)
        allotables.extend(probable_allotables_for_department)   
    elif university_id is not None:
        probable_allotables_for_university = DomainUtils().get_allotables_of_a_university_by_university_id(university_id=university_id)
        allotables.extend(probable_allotables_for_university) 
    return allotables

@dataclass
class TimetableGenerics(GeneticAlgorithmFunctionalities):
    data_pool:SlotData

    # semi_fitness_evaluator:FitnessEvaluator

    def __post_init__(self):
        self.editable_data_pool:SlotData = self.data_pool

    def gene_generator(self, mutation_mode=False)->Gene:


        if mutation_mode is True:
            allotables = self.data_pool.allotables
            slots = self.data_pool.slots 
        else:
            allotables = self.editable_data_pool.allotables
            slots = self.editable_data_pool.slots
        if len(allotables) < len(slots):
            allotables.extend([None] * (len(slots) - len(allotables)))
        # print(f"ALlotable length - {len(allotables)} SLots length  = {len(slots)}")
        random_allotable = random.choice(allotables)
        random_slot =  random.choice(slots)
        gene = random_slot
        gene.slot_alloted_to = random_allotable
        if mutation_mode is False:
            self.editable_data_pool.allotables.remove(random_allotable)
            self.editable_data_pool.slots.remove(random_slot)
        return gene

    def chromosome_generator(self)->Chromosome:
        chromosome:Chromosome = Chromosome()
        self.editable_data_pool = copy.deepcopy(self.data_pool)
        while len(self.editable_data_pool.slots) > 0:
            gene = self.gene_generator()
                
            # if gene not in chromosome.genes:
            chromosome.genes.append(gene)

        # print(f"Chromosme length - {len(chromosome.genes)}\t Data pool length = {len(self.data_pool.slots)}")
        return chromosome


    def mutator(self,chromosome:Chromosome)->Chromosome:

        mutation_index = random.randint(0, len(chromosome.genes) - 1)
        chromosome.genes[mutation_index] = self.gene_generator(mutation_mode=True)

        # chromosome = self.chromosome_generator()
        return chromosome

def create_semi_chromosome(global_data_pool:DataPool=None)->Chromosome:
    CHROMOSOME_LENGTH = len(global_data_pool.slots)
    generics = TimetableGenerics(
        CHROMOSOME_LENGTH=CHROMOSOME_LENGTH,
        data_pool=global_data_pool
    )
    fitness_evaluator = FitnessEvaluator(
        max_score=CHROMOSOME_LENGTH * 2,
        constraints=[
            IncompleteSlots(5, data_pool=global_data_pool, type='HARD', generic=generics),
            NoSameSlotIdRepetition(1 / 2, data_pool=global_data_pool, type='HARD', generic=generics),
            # AllAllotablesMapped(1, data_pool=global_data_pool, type='HARD', generic=generics),
            FixedAllotablesAtFixedSlot(2, data_pool=global_data_pool, type='HARD', generic=generics)
        ]
    )

    ga_config = GeneticAlgorithmConfig(
        MAX_GENERATION=1000,
        DNA_SIZE=100,
        MUTATION_RATE=0.05,
        REPAIR_MODE=False
    )

    timetable_generator = GeneticAlgorithmMachine(
        fitness_evaluator=fitness_evaluator,
        generics=generics,
        ga_config=ga_config
    )

    chromosome = timetable_generator.perform_ga()

    return chromosome

from src.utils.timer import timer

@timer
def generate_timetable(university_id:str=None):
    with open("./timetabler/data/inputs/input_2.json", "r") as f:
        input_data = json.load(f)
    output = parse_input_json_to_python(input_data)
    DomainUtils(data_source=output)
    save_output_file('stage_1_output.json', output)

    final_chromosome = Chromosome(genes=[])
    all_allotables = []
    universities = DomainUtils().get_all_universities()
    university = DomainUtils().get_university_by_id(universities[0].id)
    print(university)
    global_data_pool = SlotData(slots=slots_generator(university_id=university.id), allotables=slot_allotables_generator(university_id=university.id))

    final_chromosome = create_semi_chromosome(global_data_pool=global_data_pool)
    save_output_file('all_allotables.json', all_allotables)

    return final_chromosome