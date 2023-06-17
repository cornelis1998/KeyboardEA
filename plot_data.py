import seaborn as sns
import pandas as pd
import matplotlib.pyplot as plt
from new_fns import visualize_keyboard

instances = ['a']

for inst in instances:
    # PLot results
    data = pd.read_csv(f"Results\example_experiment_data_{inst}.csv.gz")

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

    print(f'Instance Bur26{inst}:')
    print(f'Starting fitness: {resampled_data["fitness"].max()}\nMinimal fitness: {resampled_data["fitness"].min()}')

    min_idx = resampled_data[resampled_data["fitness"] == resampled_data["fitness"].min()].iloc[-1]
    print(f'Printing visual for solution: {min_idx["genotype"]}')
    # visualize_keyboard(min_idx["genotype"])

    sns.lineplot(data=resampled_data, x="#evaluations", y="fitness", errorbar=("pi", 95))
    # plt.show()