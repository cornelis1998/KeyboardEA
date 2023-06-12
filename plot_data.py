import seaborn as sns
import pandas as pd
import matplotlib.pyplot as plt
from improved_functions import visualize_keyboard

# PLot results
data = pd.read_csv("Results\example_experiment_data_a.csv.gz")

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

# print(f'Starting fitness: {max(resampled_data.fitness)}\n Minimal fitness: {min(resampled_data.fitness)})
print(f'Starting fitness: {resampled_data["fitness"].max()}\nMinimal fitness: {resampled_data["fitness"].min()}')

min_idx = resampled_data[resampled_data["fitness"] == resampled_data["fitness"].min()].iloc[-1]
print(f'Printing visual for solution: {min_idx["genotype"]}')
visualize_keyboard(min_idx["genotype"])

sns.lineplot(data=resampled_data, x="#evaluations", y="fitness", errorbar=("pi", 95))
plt.show()