import seaborn as sns
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

def convert_list_to_int(l):
    int_array = []
    s = ""
    for i in range(len(l)):
        if l[i] != " " and l[i] != "[" and l[i] != "]" and l[i] != "\n":
            if l[i-1] != " ":
                s = l[i-1] + l[i]
            else:
                s = l[i]
        else:
            if s != "":
                int_array.append(int(s))

    int_array = list(dict.fromkeys(int_array))
    return int_array

def print_layout(layout):
    letters = ['a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p','q','r', 's', 't','u','v','w','x','y','z']
    
    counter = 0
    for key in layout:
        print(letters[key], end=" ")
        if counter == 9 or counter == 18:
            print()
        counter += 1



# PLot results
data = pd.read_csv("example_experiment_data.csv.gz")

# First, determine the configurations
aggregating_columns = ["seed"]
unique_configurations = data.groupby(aggregating_columns).size().rename("x").reset_index().drop(columns="x")

# Second, determine the unique #evaluations
unique_evaluations = pd.DataFrame({'#evaluations': data["#evaluations"].sort_values().unique()})

# Construct a list of wanted sampling points by cross join
# Note: order is important, as we'll fill in the missing samples by taking the previous non-missing value
#       and this should be from the same run.
requested_samples = pd.merge(unique_configurations, unique_evaluations, how="cross")
resampled_data = pd.merge(requested_samples, data, how="left", on=aggregating_columns + ["#evaluations"]).ffill()

best_layout = resampled_data.genotype[np.argmin(resampled_data.fitness)]
print("best fitness: ", min(resampled_data.fitness))
print("best layout: ")

best_layout = convert_list_to_int(best_layout)
print_layout(best_layout)

# solution bur26a
optimal_layout = [25, 14, 10, 6, 3, 11, 12, 1, 5, 17, 0, 4, 8, 20, 7, 13, 2, 19, 18, 24, 16, 9, 15, 23, 22, 21]
print()
print("Optimal layout bur26a: ")
print_layout(optimal_layout)

sns.lineplot(data=resampled_data, x="#evaluations", y="fitness")
plt.show()