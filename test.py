import matplotlib.pyplot as plt
import matplotlib.patches as patches

def visualize_keyboard(solution):
    # Rows based on QWERTY keyboard
    row_indices = [[0, 9], [10, 18], [19, 25]]
    
    fig, ax = plt.subplots(figsize=(12, 3))
    
    # Loop through rows
    for row_number, (row_start, row_end) in enumerate(row_indices):
        for idx in range(row_start, row_end + 1):
            key = solution[idx]
            
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

keyboard_layout = list("QWERTYUIOPASDFGHJKLZXCVBNM")
visualize_keyboard(keyboard_layout)
