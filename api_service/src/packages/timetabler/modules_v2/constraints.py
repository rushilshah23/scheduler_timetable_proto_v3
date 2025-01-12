from src.packages.ga import Constraint
from dataclasses import dataclass
import random


debug = False

@dataclass
class NoSameSlotIdRepetition(Constraint):
    def apply_constraint(self, chromosome):
        total_penalty = 0
        # Count inversions and add a penalty based on the magnitude of the violation
        for i in range(len(chromosome.genes) - 1):
            for j in range(i + 1, len(chromosome.genes)):
                # if chromosome.genes[i].id == chromosome.genes[j].id:
                if chromosome.genes[i].working_day_id == chromosome.genes[j].working_day_id and chromosome.genes[i].start_time == chromosome.genes[j].start_time and chromosome.genes[i].end_time == chromosome.genes[j].end_time:
                    total_penalty += self.penalty 
        print(f"Total penalty for NoSameSlotIdRepetition constraint is - {total_penalty}") if debug else None
        if len(chromosome.genes) == 80:
            print(f"NoSameSlotIdRepetition slot Penalty - {total_penalty}")
        return total_penalty

    def repair_chromosome(self, chromosome):
        gene_index_to_remove = set()
        for i in range(len(chromosome.genes) - 1):
            for j in range(i + 1, len(chromosome.genes)):
                # if chromosome.genes[i].id == chromosome.genes[j].id:
                if chromosome.genes[i].working_day_id == chromosome.genes[j].working_day_id and chromosome.genes[i].start_time == chromosome.genes[j].start_time and chromosome.genes[i].end_time == chromosome.genes[j].end_time:
                    gene_index_to_remove.add(i) 
        # chromosome.genes.sort(key=lambda gene: gene.value)
        gene_index_to_remove = sorted(gene_index_to_remove,reverse=True)
        for index in gene_index_to_remove:
            del chromosome.genes[index]
        return chromosome
    




@dataclass
class FixedAllotablesAtFixedSlot(Constraint):

    # @staticmethod
    # def is_overlap(slot1, slot2) -> bool:
    #     """Checks if two slots overlap based on start and end times."""
    #     # return not (slot1.end_time <= slot2.start_time or slot1.start_time >= slot2.end_time)
    #     return  slot1.end_time == slot2.end_time or slot1.start_time == slot2.start_time

    
    def apply_constraint(self, chromosome):
        total_penalty = 0
        for i in range(len(chromosome.genes)):
            if (chromosome.genes[i].slot_alloted_to is not None):
                for allotable in self.data_pool.allotables:
                    if allotable.working_day_id == chromosome.genes[i].working_day_id:
                        if hasattr(allotable,'fixed_slot') == True:
                            if allotable.fixed_slot is True and allotable.start_time == chromosome.genes[i].start_time and allotable.end_time == chromosome.genes[i].end_time and chromosome.genes[i].slot_alloted_to != allotable:
                                total_penalty += self.penalty
        print(f"Total penalty for FixedAllotablesAtFixedSlot constraint is - {total_penalty}") if debug else None
        if len(chromosome.genes) == 80:
            print(f"FixedAllotablesAtFixedSlot slot Penalty - {total_penalty}")
        return total_penalty

    def repair_chromosome(self, chromosome):
        # Create a map for quick lookup of allotables by their key properties
        allotables_map = {
            (allotable.start_time, allotable.end_time, allotable.working_day_id): allotable
            for allotable in self.data_pool.allotables if allotable is not None
        }

        for gene in chromosome.genes:
            # Check if the gene's slot_alloted_to is valid
            if gene.slot_alloted_to:
                # Ensure the 'fixed_slot' field exists before accessing it
                if hasattr(gene.slot_alloted_to, "fixed_slot") and gene.slot_alloted_to.fixed_slot:
                    if (
                        gene.slot_alloted_to.working_day_id != gene.working_day_id
                        or gene.slot_alloted_to.start_time != gene.start_time
                        or gene.slot_alloted_to.end_time != gene.end_time
                        or gene.slot_alloted_to.division_id != gene.working_day.division_id
                    ):
                        # Repair by finding a valid allotable using the key
                        key = (gene.start_time, gene.end_time, gene.working_day_id)
                        valid_allotable = allotables_map.get(key, None)
                        if valid_allotable:
                            gene.slot_alloted_to = valid_allotable
                        else:
                            # If no valid allotable is found, unset the slot_alloted_to
                            gene.slot_alloted_to = None

        return chromosome





@dataclass
class IncompleteSlots(Constraint):
    def apply_constraint(self, chromosome):
        total_penalty = 0
        if len(self.data_pool.slots) > len(chromosome.genes):
            total_penalty += self.penalty * (len(self.data_pool.slots) - len(chromosome.genes))
        print(f"Total penalty for IncompleteSlots constraint is - {total_penalty}") if debug else None
        if len(chromosome.genes) == 80:
            print(f"IncompleteSlots slot Penalty - {total_penalty}")
        return total_penalty

    def repair_chromosome(self, chromosome):
        if len(self.data_pool.slots) > len(chromosome.genes):
            while len(chromosome.genes) < len(self.data_pool.slots):
                chromosome.genes.append(self.generic.gene_generator())
        return chromosome


@dataclass
class DuplicateAllotables(Constraint):
    def apply_constraint(self, chromosome):
        total_penalty = 0
        non_none_allotables = [allotable for allotable in self.data_pool.allotables if allotable is not None]

        # Track assigned allotables to find duplicates
        assigned_allotables = [
            slot.slot_alloted_to
            for slot in chromosome.genes
            if slot.slot_alloted_to is not None
        ]

        # Create a manual set for uniqueness
        unique_assigned = []
        for allotable in assigned_allotables:
            if allotable not in unique_assigned:
                unique_assigned.append(allotable)

        # Penalty for duplicates
        duplicate_count = len(assigned_allotables) - len(unique_assigned)
        total_penalty += duplicate_count


        print(f"Total penalty for DuplicateALlotables constraint is - {total_penalty}") if debug else None
        if len(chromosome.genes) == 80:
            print(f"DuplicateAllotables slot Penalty - {total_penalty}")
        return total_penalty * self.penalty


    def repair_chromosome(self, chromosome):
        return chromosome




@dataclass
class MissingAllotables(Constraint):
    def apply_constraint(self, chromosome):
        total_penalty = 0

        # Group slots in chromosome.genes by division ID
        division_slots = {}
        for slot in chromosome.genes:
            division_id = slot.working_day.division.id  # Use a unique identifier
            if division_id not in division_slots:
                division_slots[division_id] = []
            division_slots[division_id].append(slot)

        # Iterate over each division to check missing allotables
        for division_id, slots in division_slots.items():
            # Find all unique allotables assigned in this division
            unique_assigned_allotables = []
            for slot in slots:
                allotable = slot.slot_alloted_to
                if allotable is not None and allotable not in unique_assigned_allotables:
                    unique_assigned_allotables.append(allotable)

            # Find total slots for this division in data_pool
            division_total_slots = [
                slot for slot in self.data_pool.slots if slot.working_day.division.id == division_id
            ]

            # If all slots for this division have been created, check for missing allotables
            if len(slots) == len(division_total_slots):
                # Get all unique allotables for the division in the data_pool
                division_allotables = []
                for allotable in self.data_pool.allotables:
                    if allotable.division.id == division_id and allotable not in division_allotables:
                        division_allotables.append(allotable)

                # Find missing allotables
                missing_allotables = [
                    allotable for allotable in division_allotables if allotable not in unique_assigned_allotables
                ]

                # Add penalty for missing allotables
                total_penalty += len(missing_allotables)

        print(f"Total penalty for MissingAllotables constraint is - {total_penalty}") if debug else None
        # if len(chromosome.genes) == 80:
        print(f"MissingAllotables slot Penalty - {total_penalty}")
        return total_penalty * self.penalty

    def repair_chromosome(self, chromosome):
        # Group slots in chromosome.genes by division ID
        division_slots = {}
        for slot in chromosome.genes:
            division_id = slot.working_day.division.id
            if division_id not in division_slots:
                division_slots[division_id] = []
            division_slots[division_id].append(slot)

        # Iterate over each division to repair missing allotables
        for division_id, slots in division_slots.items():
            # Find total slots for this division in the data_pool
            division_total_slots = [
                slot for slot in self.data_pool.slots if slot.working_day.division.id == division_id
            ]

            # Repair only when the whole division is generated
            if len(slots) == len(division_total_slots):
                # Get all unique allotables for the division in the data_pool
                division_allotables = [
                    allotable for allotable in self.data_pool.allotables if allotable.division.id == division_id
                ]

                # Find all unique allotables currently assigned in this division
                unique_assigned_allotables = [
                    slot.slot_alloted_to for slot in slots if slot.slot_alloted_to is not None
                ]

                # Identify missing allotables
                missing_allotables = [
                    allotable for allotable in division_allotables if allotable not in unique_assigned_allotables
                ]

                # Assign missing allotables to available slots
                available_slots = [slot for slot in slots if slot.slot_alloted_to is None]
                for missing_allotable in missing_allotables:
                    if available_slots:
                        slot_to_repair = available_slots.pop(0)
                        slot_to_repair.slot_alloted_to = missing_allotable
                        unique_assigned_allotables.append(missing_allotable)

                # Handle duplicates within the division
                assigned_allotables = []
                for slot in slots:
                    if slot.slot_alloted_to in assigned_allotables:
                        # Replace duplicates with a unique unassigned allotable
                        unassigned_allotables = [
                            allotable for allotable in division_allotables
                            if allotable not in assigned_allotables
                        ]
                        if unassigned_allotables:
                            slot.slot_alloted_to = unassigned_allotables.pop(0)
                    if slot.slot_alloted_to is not None:
                        assigned_allotables.append(slot.slot_alloted_to)

        print("Chromosome repaired for divisions with fully generated slots") if debug else None
        return chromosome



# @dataclass
# class ContinuousSlot(Constraint):
#     def apply_constraint(self, chromosome):
#         total_penalty = 0
#         # Loop through the genes to check the continuity of the slots
#         for i in range(len(chromosome.genes) - 1):
#             current_gene = chromosome.genes[i]
#             if current_gene.slot_alloted_to is not None:
#                 continuous_slot_for_current_gene = chromosome.genes[i].continuous_slot
#                 for next_index in range(1, continuous_slot_for_current_gene+1):
#                     next_gene = chromosome.genes[i + next_index]
            
#                     # Check if the current slot end time is not equal to the next slot start time
#                     if current_gene.end_time != next_gene.start_time and current_gene.working_day_id != next_gene.working_day_id:
#                         # Apply penalty based on the gap between the slots
#                         gap = next_index
#                         total_penalty += self.penalty * gap  # You could adjust the penalty logic here
                    
#         print(f"Total penalty for ContinuousSlot constraint is - {total_penalty}") if debug else None
#         return total_penalty

#     def repair_chromosome(self, chromosome):
#         # Loop through the genes to repair the discontinuity of the slots
#         for i in range(len(chromosome.genes) - 1):
#             current_gene = chromosome.genes[i]
#             next_gene = chromosome.genes[i + 1]
            
#             # Check if there's a gap between the current and next slot
#             if current_gene.end_time != next_gene.start_time:
#                 # Repair logic: Adjust the next gene to be continuous with the current gene
#                 # This could mean setting the next gene's start time to the current gene's end time
#                 next_gene.start_time = current_gene.end_time
#                 next_gene.end_time = next_gene.start_time + (next_gene.end_time - next_gene.start_time)  # Adjust the duration
                
#         return chromosome


@dataclass
class ContinuousSlot(Constraint):
    def apply_constraint(self, chromosome):
        total_penalty = 0
        current_working_days = {}
        all_working_days = {}

        # Group slots by working day
        for slot in chromosome.genes:
            if slot.working_day_id not in current_working_days:
                current_working_days[slot.working_day_id] = []
            if slot not in current_working_days[slot.working_day_id]:
                current_working_days[slot.working_day_id].append(slot)

        for slot in self.data_pool.slots:
            if slot.working_day_id not in all_working_days:
                all_working_days[slot.working_day_id] = []
            all_working_days[slot.working_day_id].append(slot)

        # Iterate through each working day
        for working_day_id, slots in current_working_days.items():
            # Sort slots by start time
            slots.sort(key=lambda x: x.start_time)

            if len(slots) == len(all_working_days[working_day_id]):
                # Full working day generated
                for i in range(len(slots)):
                    current_slot = slots[i]

                    if current_slot.slot_alloted_to is not None:
                        if not current_slot.slot_alloted_to.fixed_slot:
                            continuous_slot_count = current_slot.slot_alloted_to.continuous_slot

                            # Ensure group_end is within bounds
                            
                            if i+continuous_slot_count>=len(slots):
                                total_penalty+=(i+continuous_slot_count)-len(slots)
                            group_end = min(i + continuous_slot_count, len(slots))

                            # Check if within bounds and continuity
                            if group_end <= len(slots):  # Check continuity for the full working day
                                for j in range(i, group_end):
                                    next_slot = slots[j]
                                    if next_slot.slot_alloted_to is None:
                                        total_penalty += 3
                                    elif next_slot.slot_alloted_to.fixed_slot is False:
                                        if (
                                            current_slot.slot_alloted_to.division_id != next_slot.slot_alloted_to.division_id
                                            or current_slot.slot_alloted_to.faculty_id != next_slot.slot_alloted_to.faculty_id
                                            or current_slot.slot_alloted_to.subject_id != next_slot.slot_alloted_to.subject_id
                                        ):
                                            total_penalty += 2
                                    elif next_slot.slot_alloted_to.fixed_slot is True:
                                        total_penalty+=1
                            else:
                                # Penalize if group exceeds bounds (incomplete group)
                                total_penalty += 1

                    # Skip unallocated slots
                    if current_slot.slot_alloted_to is None:
                        continue  # Skip unallocated slots
            else:
                # In-progress working day, checking for continuity
                for i in range(len(slots)):
                    group_end = 0
                    current_slot = slots[i]

                    if current_slot.slot_alloted_to is not None:
                        if not current_slot.slot_alloted_to.fixed_slot:
                            if current_slot.slot_alloted_to.weekly_frequency%current_slot.slot_alloted_to.continuous_slot !=0:
                                raise Exception("THis condition can't meet")
                            continuous_slot_count = current_slot.slot_alloted_to.continuous_slot

                            # Ensure group_end is within bounds
                            group_end = min(i + continuous_slot_count, len(slots))

                            # Check continuity and validity for in-progress working day
                            if group_end <= len(slots):  # Check continuity for the remaining day
                                for j in range(i, group_end):
                                    next_slot = slots[j]

                                    # Check if the next slot's start time doesn't match the current slot's end time
                                    if next_slot.start_time != current_slot.end_time:
                                        # Penalize if missing a slot
                                        total_penalty += 1
                                    elif next_slot.slot_alloted_to is None:
                                        total_penalty += 1
                                    elif next_slot.slot_alloted_to.fixed_slot is False:
                                        if (
                                            current_slot.slot_alloted_to.division_id != next_slot.slot_alloted_to.division_id
                                            or current_slot.slot_alloted_to.faculty_id != next_slot.slot_alloted_to.faculty_id
                                            or current_slot.slot_alloted_to.subject_id != next_slot.slot_alloted_to.subject_id
                                        ):
                                            total_penalty += 1
                                    elif next_slot.slot_alloted_to.fixed_slot is True:
                                        total_penalty+=1

                            else:
                                continue  # Skip checking beyond bounds (for in-progress slots)
                    i+=group_end
                    # Skip unallocated slots
                    if current_slot.slot_alloted_to is None:
                        continue  # Skip unallocated slots
        print(f"Total penalty for COntinuousSLots constraint is - {total_penalty}") if debug else None
        if len(chromosome.genes) == 20:
            print(f"Continuos slot Penalty - {total_penalty}")
            from time import sleep
            sleep(2)
        return total_penalty * self.penalty


    def repair_chromosome(self, chromosome):
        current_working_days = {}

        # Group slots by working day
        for slot in chromosome.genes:
            if slot.working_day_id not in current_working_days:
                current_working_days[slot.working_day_id] = []
            current_working_days[slot.working_day_id].append(slot)

        for working_day_id, slots in current_working_days.items():
            # Sort slots by start time
            slots.sort(key=lambda x: x.start_time)

            for i in range(len(slots)):
                current_slot = slots[i]

                # Skip unallocated slots
                if current_slot.slot_alloted_to is None:
                    continue

                # Skip fixed slots
                if current_slot.slot_alloted_to.fixed_slot is True:
                    continue

                continuous_slot_count = current_slot.slot_alloted_to.continuous_slot

                # Ensure group_end is within bounds
                group_end = min(i + continuous_slot_count, len(slots))

                # Check if continuity needs repair
                for j in range(i + 1, group_end):
                    next_slot = slots[j]

                    # Repair unallocated slots
                    if next_slot.slot_alloted_to is None:
                        # Find a compatible allotable from the data pool
                        compatible_slot = self._find_compatible_slot(current_slot, chromosome)
                        if compatible_slot:
                            next_slot.slot_alloted_to = compatible_slot
                    elif next_slot.slot_alloted_to.fixed_slot is False:
                        # Check if the next slot matches the current slot's attributes
                        if (
                            current_slot.slot_alloted_to.division_id != next_slot.slot_alloted_to.division_id
                            or current_slot.slot_alloted_to.faculty_id != next_slot.slot_alloted_to.faculty_id
                            or current_slot.slot_alloted_to.subject_id != next_slot.slot_alloted_to.subject_id
                        ):
                            # Find a compatible allotable from the data pool
                            compatible_slot = self._find_compatible_slot(current_slot, chromosome)
                            if compatible_slot:
                                next_slot.slot_alloted_to = compatible_slot
                        # IS i+=group_end needed so that it doesn't cause ripple effect  
                        i+=group_end

                    elif next_slot.slot_alloted_to.fixed_slot is True:
                        # Break the group if a fixed slot blocks continuity
                        break

        return chromosome

    def _find_compatible_slot(self, current_slot, chromosome):
        """
        Find a compatible slot_alloted_to from the data pool that matches
        the division_id, faculty_id, and subject_id of the current_slot
        but has a unique primary ID (not present in the chromosome).
        """
        used_ids = {slot.slot_alloted_to.id for slot in chromosome.genes if slot.slot_alloted_to}
        
        for allotable   in self.data_pool.allotables:
            if allotable is not None:
                if hasattr(allotable,'faculty_id') and hasattr(allotable,'division_id') and hasattr(allotable,'subject_id'):
                    if (
                        allotable.division_id == current_slot.slot_alloted_to.division_id
                        and allotable.faculty_id == current_slot.slot_alloted_to.faculty_id
                        and allotable.subject_id == current_slot.slot_alloted_to.subject_id
                        and allotable.id not in used_ids
                    ):
                        return allotable  # Return the first compatible allotable
        return None  # No compatible allotable found



# @dataclass
# class ContinuousSlot(Constraint):
#     def apply_constraint(self, chromosome):
#         total_penalty = 0
        
#         # Group genes by working day
#         working_day_slots = {}
#         for gene in chromosome.genes:
#             if gene.working_day_id not in working_day_slots:
#                 working_day_slots[gene.working_day_id] = []
#             working_day_slots[gene.working_day_id].append(gene)

#         # Check continuity within each working day
#         for working_day_id, slots in working_day_slots.items():
#             # Sort slots by start time
#             slots.sort(key=lambda slot: slot.start_time)
            
#             for i in range(len(slots) - 1):
#                 current_slot = slots[i]
#                 next_slot = slots[i + 1]
                
#                 # Check if the current slot's end_time matches the next slot's start_time
#                 if current_slot.end_time != next_slot.start_time:
#                     total_penalty += self.penalty
#                     if debug:
#                         print(
#                             f"Penalty added for working_day_id={working_day_id}: "
#                             f"current_slot.end_time={current_slot.end_time}, next_slot.start_time={next_slot.start_time}"
#                         )
        
#         return total_penalty



#     def repair_chromosome(self, chromosome):
#         # Track used allotables (use list to maintain uniqueness)
#         used_allotables = [
#             gene.slot_alloted_to.id for gene in chromosome.genes if gene.slot_alloted_to is not None
#         ]

#         # Group genes by working day
#         working_day_slots = {}
#         for gene in chromosome.genes:
#             if gene.working_day_id not in working_day_slots:
#                 working_day_slots[gene.working_day_id] = []
#             working_day_slots[gene.working_day_id].append(gene)

#         # Repair continuity for each working day
#         for working_day_id, slots in working_day_slots.items():
#             # Sort slots by start time
#             slots.sort(key=lambda slot: slot.start_time)
            
#             for i in range(len(slots) - 1):
#                 current_slot = slots[i]
#                 next_slot = slots[i + 1]
                
#                 # If slots are not continuous, adjust the next slot
#                 if current_slot.end_time != next_slot.start_time:
#                     duration = next_slot.end_time - next_slot.start_time
#                     next_slot.start_time = current_slot.end_time
#                     next_slot.end_time = next_slot.start_time + duration

#                     # Check if the allotable is duplicate or missing
#                     if (
#                         next_slot.slot_alloted_to is None 
#                         or next_slot.slot_alloted_to.id in used_allotables
#                     ):
#                         # Fetch a new unique allotable
#                         available_allotables = [
#                             a for a in self.data_pool.allotables if a.id not in used_allotables
#                         ]
#                         if available_allotables:
#                             new_allotable = available_allotables.pop(0)
#                             next_slot.slot_alloted_to = new_allotable
#                             used_allotables.append(new_allotable.id)
#                             if debug:
#                                 print(
#                                     f"Reassigned allotable for working_day_id={working_day_id}: "
#                                     f"new_allotable.id={new_allotable.id}"
#                                 )
        
#         return chromosome


class WeeklyFrequencyLimit(Constraint):
    def apply_constraint(self, chromosome):
        total_penalty = 0
        current_working_days = {}
        all_working_days = {}

        # Group slots by working day
        for slot in chromosome.genes:
            if slot.working_day_id not in current_working_days:
                current_working_days[slot.working_day_id] = []
            current_working_days[slot.working_day_id].append(slot)

        for slot in self.data_pool.slots:
            if slot.working_day_id not in all_working_days:
                all_working_days[slot.working_day_id] = []
            all_working_days[slot.working_day_id].append(slot)

        # Iterate through each working day
        for working_day_id, slots in current_working_days.items():
            # Sort slots by start time
            slots.sort(key=lambda x: x.start_time)

            if len(slots) == len(all_working_days[working_day_id]):
                print(f"gENERATING full working day for id {working_day_id}\t {len(slots)}\t {len(all_working_days[working_day_id])}")
                # Full working day generated
                for i in range(len(slots)):
                    current_slot = slots[i]
