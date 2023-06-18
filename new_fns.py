import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import string

from typing import List
from permutationsga.problem import Solution
from permutationsga.qap import QAP, read_qaplib

## Initialization functions

class Initialization:
    def initialize(self, rng: np.random.Generator, population: List[Solution]):
        raise NotImplementedError()

class QWERTYRandom(Initialization):
    def __init__(self, length: int, prob: float = 0.5):
        self.length = length
        self.prob = prob

    def initialize(self, rng: np.random.Generator, population: List[Solution]):
        for solution in population:
            solution.e = self.QWERTY(rng)

    def QWERTY(self, rng: np.random.Generator):
        qwerty = "QWERTYUIOPASDFGHJKLZXCVBNM"

        letterpos = {i: letter for i, letter in enumerate(qwerty)}
        letterinv = {letter: i for i, letter in enumerate(qwerty)}

        sol = rng.permutation(self.length)
        for i in range(26):
            # if random < prob, swap letter at index with its correct letter
            if rng.uniform(0,1) < self.prob:
                target = letterinv[letterpos[i]]
                sol[i], sol[target] = sol[target], sol[i]

        letters, counts = np.unique(sol, return_counts=True)
        assert(len(letters) == 26)
        assert(np.all(counts == 1))

        return sol

class AZERTYRandom(Initialization):
    def __init__(self, length: int, prob: float = 0.5):
        self.length = length
        self.prob = prob

    def initialize(self, rng: np.random.Generator, population: List[Solution]):
        for solution in population:
            solution.e = self.AZERTY(rng)

    def AZERTY(self, rng: np.random.Generator):
        qwerty = "AZERTYUIOPQSDFGHJKLMWXCVBN"

        letterpos = {i: letter for i, letter in enumerate(qwerty)}
        letterinv = {letter: i for i, letter in enumerate(qwerty)}

        sol = rng.permutation(self.length)
        for i in range(26):
            # if random < prob, swap letter at index with its correct letter
            if rng.uniform(0,1) < self.prob:
                target = letterinv[letterpos[i]]
                sol[i], sol[target] = sol[target], sol[i]

        letters, counts = np.unique(sol, return_counts=True)
        assert(len(letters) == 26)
        assert(np.all(counts == 1))

        return sol

class ColemakRandom(Initialization):
    def __init__(self, length: int, prob: float = 0.5):
        self.length = length
        self.prob = prob

    def initialize(self, rng: np.random.Generator, population: List[Solution]):
        for solution in population:
            solution.e = self.Colemak(rng)

    def Colemak(self, rng: np.random.Generator):
        qwerty = "QWFPGJLUYARSTDHNEIOZXCVBKM"

        letterpos = {i: letter for i, letter in enumerate(qwerty)}
        letterinv = {letter: i for i, letter in enumerate(qwerty)}

        sol = rng.permutation(self.length)
        for i in range(26):
            # if random < prob, swap letter at index with its correct letter
            if rng.uniform(0,1) < self.prob:
                target = letterinv[letterpos[i]]
                sol[i], sol[target] = sol[target], sol[i]

        letters, counts = np.unique(sol, return_counts=True)
        assert(len(letters) == 26)
        assert(np.all(counts == 1))

        return sol

class DvorakRandom(Initialization):
    def __init__(self, length: int, prob: float = 0.5):
        self.length = length
        self.prob = prob

    def initialize(self, rng: np.random.Generator, population: List[Solution]):
        for solution in population:
            solution.e = self.Dvorak(rng)

    def Dvorak(self, rng: np.random.Generator):
        qwerty = "PYFGCRLAOEUIDHTNSQJKXBMWVZ"

        letterpos = {i: letter for i, letter in enumerate(qwerty)}
        letterinv = {letter: i for i, letter in enumerate(qwerty)}

        sol = rng.permutation(self.length)
        for i in range(26):
            # if random < prob, swap letter at index with its correct letter
            if rng.uniform(0,1) < self.prob:
                target = letterinv[letterpos[i]]
                sol[i], sol[target] = sol[target], sol[i]

        letters, counts = np.unique(sol, return_counts=True)
        assert(len(letters) == 26)
        assert(np.all(counts == 1))

        return sol

class BetterPermutationInitialization(Initialization):
    """
    Put the most used keys under 11, 12, 13, 14, 17, 18, 19 (with index 10, ..., 18)
    """

    def __init__(self, length: int, problem: QAP):
        self.length = length
        
        usage_matrix = problem.B
        self.usage_per_letter = np.sum(usage_matrix, axis=0)

    def initialize(self, rng: np.random.Generator, population: List[Solution]):

        letter_indices_sorted = np.argsort(self.usage_per_letter)
        least_used = letter_indices_sorted[:17]
        most_used = letter_indices_sorted[17:]

        for solution in population:
            # Shuffle both lists
            np.random.shuffle(least_used)
            np.random.shuffle(most_used)
            sol = np.concatenate([
                least_used[:10], 
                most_used, 
                least_used[10:],
                ])
            solution.e = sol

class QwertyPermutationInitialization(Initialization):
    """
    initialize population with 10% qwerty, 10% azerty and 80% randomized
    """

    def __init__(self, length: int):
        self.length = length

    def initialize(self, rng: np.random.Generator, population: List[Solution]):
        qwerty = [16, 22, 4, 17, 19, 24, 20, 8, 14, 15, 0, 18, 3, 5, 6, 7, 9, 10, 11, 25, 23, 2, 21, 1, 13, 12]
        azerty = [0, 25, 4, 17, 19, 24, 20, 8, 14, 15, 16, 18, 3, 5, 6, 7, 9, 10, 11, 12, 22, 23, 2, 21, 1, 13]
        # colemak = [16, 22, 5, 15, 6, 9, 11, 20, 24, 0, 17, 18, 19, 3, 7, 13, 4, 8, 14, 25, 23, 2, 21, 1, 10, 12]
        # dvorak = [15, 24, 5, 6, 2, 17, 11, 0, 14, 4, 20, 8, 3, 7, 19, 13, 18, 16, 9, 10, 23, 1, 12, 22, 21, 25]
        for solution in population:
            np.random.seed = 42
            x = np.random.random(size=1)
            if (x < 0.1):
                solution.e = qwerty
            elif (x >= 0.1 and x < 0.2):
                solution.e = azerty
            # elif (x >= 0.2 and x < 0.25):
            #     solution.e = colemak
            # elif (x >= 0.25 and x < 0.3):
            #     solution.e = dvorak
            else:
                solution.e = rng.permutation(self.length)

## Crossover functions

def crossover_pmx_single_off(indices, s0: Solution, s1: Solution):
    # Partially Mapped Crossover with Random Sections and a Single Output Offspring
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

def crossover_pmx_predef_secs(s0: Solution, s1: Solution):
    # Partially Mapped Crossover with Predifined Sections
    assert s0.e is not None, "Ensure solution s0 is initialized before use."
    assert s1.e is not None, "Ensure solution s1 is initialized before use."

    # Define the keyboard layout as a list for easy indexing.
    keyboard_layout = list('QWERTYUIOPASDFGHJKLZXCVBNM')

    keyboard_sections = []

    ## Choose section divider
    # Define the sections left-middle-right.
    keyboard_sections.append(list('QWERASDFZXCV'))
    keyboard_sections.append(list('TYGHBN'))
    keyboard_sections.append(list('UIOPJKLM'))

    # Define the sections toprow-middlerow-bottomrow
    # keyboard_sections.append(list('QWERTYUIOP'))
    # keyboard_sections.append(list('ASDFGHJKL'))
    # keyboard_sections.append(list('ZXCVBNM'))

    # Define four sections
    # keyboard_sections.append(list('QWERASDZX'))
    # keyboard_sections.append(list('TFGCV'))
    # keyboard_sections.append(list('YHJBN'))
    # keyboard_sections.append(list('UIOPKLM'))

    # Create the sections based on the indices in the keyboard layout.
    for i in range(len(keyboard_sections)):
        keyboard_sections[i] = np.array([keyboard_layout.index(key) for key in keyboard_sections[i]])

    section_idx = np.random.choice(len(keyboard_sections))
    section = keyboard_sections[section_idx]

    # Offspring initialization
    off = np.full(s0.e.size, np.nan)

    # Get parents subsets according to given indices
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

def crossover_pmx_adjusted_chance(self, indices, s0: Solution, s1: Solution):
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

## Mutation functions

def swap_mutation(s0: Solution, mutation_probability):
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
    mutated_layout = np.copy(s0.e)

    # Perform mutation.
    if np.random.random() < mutation_probability:
        # Select two random indices.
        idx1, idx2 = np.random.choice(len(s0.e), 2, replace=False)
        # Insert and shift
        value_to_insert = mutated_layout[idx1]
        mutated_layout = np.delete(mutated_layout, idx1)
        mutated_layout = np.insert(mutated_layout, idx2, value_to_insert)

        assert len(s0.e) == len(mutated_layout), "The mutation caused a change in the solution size"

    return Solution(mutated_layout)

## Data analist
def visualize_keyboard(solution):
    # Convert string into int array
    solution = solution.replace('[', '').replace(']', '').replace('\n', ' ')
    solution = solution.split()
    solution = np.array([int(item) for item in solution])

    alphabet_array = list(string.ascii_uppercase)
    rearranged = np.full(solution.size, None)

    for i in range(len(solution)):
        rearranged[i] = alphabet_array[(solution[i])]

    # Rows based on QWERTY keyboard
    row_indices = [[0, 9], [10, 18], [19, 25]]
    
    fig, ax = plt.subplots(figsize=(12, 3))
    
    # Loop through rows
    for row_number, (row_start, row_end) in enumerate(row_indices):
        for idx in range(row_start, row_end + 1):
            key = rearranged[idx]
            
            # Compute x position
            x = (idx - row_start) + 0.5 * row_number
            
            # Compute y position
            y = -row_number
            
            # Draw the rectangle
            width = 0.9
            height = 0.9
            rect = patches.Rectangle((x, y), width, height, linewidth=1, edgecolor='black', facecolor='lightgray')
            ax.add_patch(rect)
            
            # Draw the character inside the rectangle
            ax.text(x + width / 2, y + height / 2, key, ha='center', va='center', fontsize=12, fontweight='bold')
    
    ax.set_xlim(-1, 15)
    ax.set_ylim(-3, 1)
    ax.axis('off')
    
    plt.show()