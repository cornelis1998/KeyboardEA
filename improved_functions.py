import numpy as np
import random
from permutationsga.problem import Solution
from permutationsga.qap import QAP, read_qaplib


class crossoverChances():
    def __init__(self, rng, filename):
        self.filename = filename
        self.rng = rng
    def get_specific_p(self):
        #Read file
        file = (self.filename)
        _,A,_ =read_qaplib(file)
        #Calculate the mean to see what keys have the largest pressing time on average
        A_mean= np.mean(A, axis=0)
        A_p = A_mean/100
        p_library = {index: value for index, value in enumerate(A_p)}

        return A_p, p_library


    def crossover_pmx_Tom_adjusted_chance(self, indices, s0: Solution, s1: Solution):
        assert s0.e is not None, "Ensure solution s0 is initialized before use."
        assert s1.e is not None, "Ensure solution s1 is initialized before use."

        #Make a copy of the solution to use for chance assignment
        copy_s0 = np.copy(s0.e)

        #Get chance library for specific instance
        _ , p_library = self.get_specific_p()

        #Make a list of chances p for current solution s0
        p_per_solution = [p_library[key] for key in copy_s0]

        #Determine section to swap
        swap_or_not = [self.rng.random() < p for p in p_per_solution]
        section = [index for index, value in enumerate(swap_or_not) if value]

        # Offspring initialization
        off = np.full(s0.e.size, np.nan)

        subset_p0 = s0.e[section]
        subset_p1 = s1.e[section]

        # Map of replaced elements
        to_replace = {key: value for key, value in zip(subset_p0, subset_p1)}

        # Replace elements in offspring using subsets
        off[section] = subset_p0

        for i in range(len(s0.e)):
            if i not in section:
                elem = s1.e[i]
                while elem in to_replace:
                    elem = to_replace[elem]
                off[i] = elem

        # Ensure all values are integers
        off = off.astype(int)
        assert len(off) == len(np.unique(off)), "Some numbers appear more than once"

        return [Solution(off)]

def crossover_pmx_Tom(indices, s0: Solution, s1: Solution):
    assert s0.e is not None, "Ensure solution s0 is initialized before use."
    assert s1.e is not None, "Ensure solution s1 is initialized before use."

    # Offspring initialization
    off = np.full(s0.e.size, np.nan)

    # Get parents subsets according to given indices
    subset_p0 = s0.e[indices]
    subset_p1 = s1.e[indices]

    # Map of replaced elements
    to_replace = {key: value for key, value in zip(subset_p0, subset_p1)}

    # Replace elements in offspring using subsets
    off[indices] = subset_p0

    for i in range(len(s0.e)):
        if i not in indices:
            elem = s1.e[i]
            while elem in to_replace:
                elem = to_replace[elem]
            off[i] = elem
    
    # Ensure all values are integers
    off = off.astype(int)
    assert len(off) == len(np.unique(off)), "Some numbers appear more than once"

    return [Solution(off)]

def crossover_pmx_Tom_lmr(indices, s0: Solution, s1: Solution):
    assert s0.e is not None, "Ensure solution s0 is initialized before use."
    assert s1.e is not None, "Ensure solution s1 is initialized before use."

    # Define the keyboard layout as a list for easy indexing.
    keyboard_layout = list('QWERTYUIOPASDFGHJKLZXCVBNM')

    ## Choose section divider
    # Define the sections left-middle-right.
    # left_keys = list('QWERASDFZXCV')
    # middle_keys = list('TYGHBN')
    # right_keys = list('UIOPJKLM')

    # Define the sections toprow-middlerow-bottomrow
    left_keys = list('QWERTYUIOP')
    middle_keys = list('ASDFGHJKL')
    right_keys = list('ZXCVBNM')

    # Use list comprehension to create the sections based on the indices in the keyboard layout.
    left_section = np.array([keyboard_layout.index(key) for key in left_keys])
    middle_section = np.array([keyboard_layout.index(key) for key in middle_keys])
    right_section = np.array([keyboard_layout.index(key) for key in right_keys])

    # Combine the sections into a list.
    keyboard_sections = np.array([left_section, middle_section, right_section], dtype=object)

    section = np.random.choice(keyboard_sections)

    # Offspring initialization
    off = np.full(s0.e.size, np.nan)

    # Get parents subsets according to given indices
    section = np.random.choice(keyboard_sections)
    subset_p0 = s0.e[section]
    subset_p1 = s1.e[section]

    # Map of replaced elements
    to_replace = {key: value for key, value in zip(subset_p0, subset_p1)}

    # Replace elements in offspring using subsets
    off[section] = subset_p0

    for i in range(len(s0.e)):
        if i not in section:
            elem = s1.e[i]
            while elem in to_replace:
                elem = to_replace[elem]
            off[i] = elem
    
    # Ensure all values are integers
    off = off.astype(int)
    assert len(off) == len(np.unique(off)), "Some numbers appear more than once"

    return [Solution(off)]

def swap_mutation(s0: Solution, mutation_probability):
    # Copy the original layout.
    mutated_layout = np.copy(s0.e)

    # Perform mutation.
    if np.random.random() < mutation_probability:
        # Select two random indices.
        idx1, idx2 = np.random.choice(len(s0.e), 2, replace=False)
        # Swap the keys at these indices.
        mutated_layout[idx1], mutated_layout[idx2] = s0.e[idx2], s0.e[idx1]

    return Solution(mutated_layout)

def scramble_mutation(s0: Solution, mutation_probability):
    mutated_layout = np.copy(s0.e)

    # Perform mutation.
    if np.random.random() < mutation_probability:
        # Select a random subset of indices.
        subset_size = np.random.randint(1, len(s0.e))
        subset_indices = np.random.choice(len(s0.e), size=subset_size, replace=False)

        # Scramble the genes in these positions.
        np.random.shuffle(mutated_layout[subset_indices])

    return Solution(mutated_layout)

def insertion_mutation(s0: Solution, mutation_probability):
    # Copy the original layout.
    mutated_layout = np.copy(s0.e)

    # Perform mutation.
    if np.random.random() < mutation_probability:
        # Select two random indices.
        idx1, idx2 = np.random.choice(len(s0.e), 2, replace=False)
        # Remove the element at idx1 and insert it at idx2
        value_to_insert = mutated_layout[idx1]
        mutated_layout = np.delete(mutated_layout, idx1)
        mutated_layout = np.insert(mutated_layout, idx2, value_to_insert)

        assert len(s0.e) == len(mutated_layout), "The mutation caused a change in the solution size"

    return Solution(mutated_layout)



