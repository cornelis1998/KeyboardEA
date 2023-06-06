import numpy as np

# Define the keyboard layout as a list for easy indexing.
keyboard_layout = list('QWERTYUIOPASDFGHJKLZXCVBNM')

# Define the sections.
left_keys = list('QWERASDFZXCV')
middle_keys = list('TYGHBN')
right_keys = list('UIOPJKLM')

# Use list comprehension to create the sections based on the indices in the keyboard layout.
left_section = np.array([keyboard_layout.index(key) for key in left_keys])
middle_section = np.array([keyboard_layout.index(key) for key in middle_keys])
right_section = np.array([keyboard_layout.index(key) for key in right_keys])

# Combine the sections into a list.
keyboard_sections = np.array([left_section, middle_section, right_section]
, dtype=object)

section = np.random.choice(keyboard_sections)

print('test')

