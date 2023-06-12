import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import string

from permutationsga.problem import Solution

# Partially Mapped Crossover with Random Sections and a Single Output Offspring
def crossover_pmx_so(indices, s0: Solution, s1: Solution):
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

# Partially Mapped Crossover with Predifined Sections
def crossover_pmx_ps(s0: Solution, s1: Solution):
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

def visualize_keyboard(solution):
    # Remove brackets and newline characters
    solution = solution.replace('[', '').replace(']', '').replace('\n', ' ')

    # Split the string into a list of strings
    solution = solution.split()

    # Convert each string element into an integer
    solution = np.array([int(item) for item in solution])

    alphabet_array = list(string.ascii_uppercase)
    rearranged = np.full(solution.size, None)

    for i in range(len(solution)):
        rearranged[i] = alphabet_array[solution[i]]

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




