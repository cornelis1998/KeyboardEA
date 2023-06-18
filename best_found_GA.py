# Imports
import pandas as pd
from tqdm import tqdm # progress bar

from permutationsga.qap import QAP, read_qaplib

from permutationsga.ga import (
    ConfigurableGA,
    RandomPermutationInitialization,
    TournamentSelection,
    FunctionBasedRecombinator,
    SequentialSelector
)
from permutationsga.problem import (
    IdenticalDecoder,
    ElitistTracker
)

# Import newly created functions to configure GA
from new_fns import *

## Setup GA
def setup_ga(seed: int, inst):
    # QAP
    problem_base = QAP(*read_qaplib(f"./instances/qap/bur26{inst}.dat"))
    problem = problem_base

    # Add the decoder - permutation encoding
    problem_decoder = IdenticalDecoder(problem)   # Identity, if using the permutation directly
    # problem_decoder = InvPermDecoder(problem)     # Inverse, if you want to reverse the direction in which the mapping occurs

    problem = problem_decoder

    # Add the tracker
    value_to_reach_dict = {'a': 5426670, 'b': 3817852, 'c': 5426795, 'd': 3821225, 'e': 5386879, 'f': 3782044, 'g': 10117172, 'h': 7098658}
    value_to_reach = value_to_reach_dict[inst]    

    problem_tracker = ElitistTracker(problem, value_to_reach)
    problem = problem_tracker

    # GA - Permutation
    # seed = 42 -- is an argument to this function now
    population_size = 2**10
    l = problem.get_length()

    ## Choose crossover function
    crossover_fn = crossover_pmx_predef_secs; indices_gen = None

    ## Choose mutation function
    mutation_fn = None

    initialization = RandomPermutationInitialization(l) 
    parent_selection = SequentialSelector()
    recombinator = FunctionBasedRecombinator(
        indices_gen,
        crossover_fn,
        parent_selection,
        population_size * 2, # Note: double as we are including the previous population
        include_what="population"
    )
    selection = TournamentSelection()
    ga = ConfigurableGA(
        seed, population_size, problem, initialization, recombinator, selection, mutation_fn
    )

    return problem_tracker, ga

instances = ['a', 'b']

for inst in instances:
    dfs = []
    for seed in tqdm(range(42, 42+10)):
        tracker, ga = setup_ga(seed, inst)
        # run a few generations
        for _ in tqdm(range(25), leave=False):
            ga.generation()
        # copy the elitist run data
        run_data = tracker.elitist_history.copy()
        # append metadata (e.g. seed, configuration, ..., anything that makes a run unique)
        run_data["seed"] = seed

        dfs.append(run_data)

    pd.concat(dfs).to_csv(f"Results\example_experiment_data_{inst}.csv.gz", index=False)

