import matplotlib.pyplot as plt
import matplotlib.patches as patches
import string
import numpy as np

def visualize_keyboard(solution):
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

keyboard_layout = np.array([1,0,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25])

visualize_keyboard(keyboard_layout)
