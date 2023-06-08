# Imports
import gzip  # as some instance files may have been compressed
from tqdm import tqdm # progress bar

# Re-import dependencies (in case earlier import was skipped)
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

# This library supports the various instances from TSPLIB (from coordinates to fully explicit matrices)
import tsplib95 as tsp



from permutationsga.ga import (
    ConfigurableGA,
    RandomPermutationInitialization,
    crossover_ox,
    crossover_cx,
    crossover_pmx,
    TournamentSelection,
    FunctionBasedRecombinator,
    SequentialSelector,
    generate_uniform_indices,
    generate_sequential_indices,
    generate_sequential_wrapping_indices,
    RandomUniformInitialization,
    BetterPermutationInitialization,
    DifferentialEvolutionRecombinator,
)
from permutationsga.problem import (
    IdenticalDecoder,
    InvPermDecoder,
    RandomKeysDecoder,
    ElitistTracker,
)

from permutationsga.tsp import TSP
from permutationsga.qap import QAP, read_qaplib

def setup_ga(seed: int):
    # TSP
    # problem_base = TSP(tsp.parse(gzip.open("./instances/tsp/berlin52.tsp.gz").read().decode('utf8')))
    # QAP
    problem_base = QAP(*read_qaplib("./instances/qap/bur26a.dat"))

    problem = problem_base

    # Add the decoder - permutation encoding
    problem_decoder = IdenticalDecoder(problem)   # Identity, if using the permutation directly
    # problem_decoder = InvPermDecoder(problem)     # Inverse, if you want to reverse the direction in which the mapping occurs

    problem = problem_decoder

    # Add the tracker
    value_to_reach = 5426670 # see bur26a.sln
    problem_tracker = ElitistTracker(problem, value_to_reach)
    problem = problem_tracker

    # GA - Permutation
    # seed = 42 -- is an argument to this function now
    population_size = 2**10
    rng = np.random.default_rng(seed=seed + 1)
    l = problem.get_length()


    # crossover_fn = crossover_pmx; indices_gen = lambda: generate_sequential_indices(rng, l)
    # crossover_fn = crossover_pmx; indices_gen = lambda: generate_uniform_indices(rng, l, 0.5)
    # crossover_fn = crossover_ox; indices_gen = lambda: generate_sequential_indices(rng, l)
    # crossover_fn = crossover_cx; indices_gen = lambda: rng.integers(0, l - 1, size=1)
    crossover_fn = crossover_cx; indices_gen = lambda: generate_uniform_indices(rng, l, 0.05)

    # initialization = RandomPermutationInitialization(l)
    initialization = BetterPermutationInitialization(l, problem_base)
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
        seed, population_size, problem, initialization, recombinator, selection
    )

    return problem_tracker, ga

dfs = []
for seed in tqdm(range(42, 42+10)):
    tracker, ga = setup_ga(seed)
    # run a few generations
    for _ in tqdm(range(50), leave=False):
        ga.generation()
    # copy the elitist run data
    run_data = tracker.elitist_history.copy()
    # append metadata (e.g. seed, configuration, ..., anything that makes a run unique)
    run_data["seed"] = seed

    dfs.append(run_data)

pd.concat(dfs).to_csv("example_experiment_data.csv.gz", index=False)

