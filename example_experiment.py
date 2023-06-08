# Imports
import gzip  # as some instance files may have been compressed
from tqdm import tqdm # progress bar

# Re-import dependencies (in case earlier import was skipped)
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

# This library supports the various instances from TSPLIB (from coordinates to fully explicit matrices)
import tsplib95 as tsp
import wandb
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
    DifferentialEvolutionRecombinator, QWERTYRandom, AZERTYRandom, DvorakRandom, ColemakRandom,
)
from permutationsga.problem import (
    IdenticalDecoder,
    InvPermDecoder,
    RandomKeysDecoder,
    ElitistTracker,
)

from improved_functions import *

from permutationsga.tsp import TSP
from permutationsga.qap import QAP, read_qaplib

NUM_ITERATIONS = 5


def setup_ga(seed: int, hyperparameters):
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
    population_size = 2**hyperparameters["population_size"]
    rng = np.random.default_rng(seed=seed + 1)
    l = problem.get_length()

    # Choose initialization method
    initializationMethod = hyperparameters["initialization_method"]
    initializationProb = hyperparameters["initialization_prob"]
    if initializationMethod == "randomPermutation":
        initialization = RandomPermutationInitialization(l)
    elif initializationMethod == "qwertyR":
        initialization = QWERTYRandom(l, initializationProb)
    elif initializationMethod == "azertyR":
        initialization = AZERTYRandom(l, initializationProb)
    elif initializationMethod == "colemakR":
        initialization = ColemakRandom(l, initializationProb)
    elif initializationMethod == "dvorakR":
        initialization = DvorakRandom(l, initializationProb)

    ## Choose crossover function and probability
    p = hyperparameters["crossover_rate"]
    method = hyperparameters["crossover_fn"]

    if method == "ox":
        crossover_fn = crossover_ox;
        indices_gen = lambda: generate_sequential_indices(rng, l)
    elif method == "pmx":
        crossover_fn = crossover_pmx;
        indices_gen = lambda: generate_uniform_indices(rng, l, p)
    elif method == "cx":
        crossover_fn = crossover_cx;
        indices_gen = lambda: generate_uniform_indices(rng, l, p)
    elif method == "pmx_tom":
        crossover_fn = crossover_pmx_Tom;
        indices_gen = lambda: generate_uniform_indices(rng, l, p)
    elif method == "pmx_lmr":
        crossover_fn = crossover_pmx_Tom_lmr;
        indices_gen = lambda: generate_uniform_indices(rng, l, p) # is ignored

    ## Choose mutation function
    mutationMethod = hyperparameters["mutation_fn"]
    if mutationMethod == "swap":
        mutation_fn = swap_mutation
    elif mutationMethod == "scramble":
        mutation_fn = scramble_mutation
    elif mutationMethod == "insertion":
        mutation_fn = insertion_mutation
    elif mutationMethod == "none":
        mutation_fn = None

    # Choose selection method
    selectionMethod = hyperparameters["selection"]
    if selectionMethod == "tournament":
        selection = TournamentSelection()
    elif selectionMethod == "sequential":
        selection = SequentialSelector()

    recombinator = FunctionBasedRecombinator(
        indices_gen,
        crossover_fn,
        selection,
        population_size * 2, # Note: double as we are including the previous population
        include_what="population"
    )

    mutation_rate = hyperparameters["mutation_rate"]

    ga = ConfigurableGA(
        seed, population_size, problem, initialization, recombinator, selection, mutation_fn, mutation_rate
    )

    return problem_tracker, ga


def train():
    run = wandb.init()
    hyperparameters = run.config

    num_gens = hyperparameters["num_generations"]
    runs = []
    for seed in tqdm(range(42, 42 + NUM_ITERATIONS)):
        tracker, ga = setup_ga(seed, hyperparameters)
        run = []
        best = float('inf')

        for _ in tqdm(range(num_gens), leave=False):
            if len(ga.population) != 2**hyperparameters["population_size"]:
                raise ValueError("Population size is incorrect")
            ga.generation()

            run.append(tracker.current_elitist.f)

        runs.append(run)


    # get min, max, mean, std of fitness at each generation
    for run in runs:
        print("len(run): ", len(run))


    for gen in range(num_gens):
        min_fitness = float('inf')
        max_fitness = float('-inf')
        total_fitness = 0
        fitness_values = []

        # iterate through all dfs
        for run in runs:

            if gen < len(run):
                fitness = run[gen]
                min_fitness = min(min_fitness, fitness)
                max_fitness = max(max_fitness, fitness)
                total_fitness += fitness
                fitness_values.append(fitness)

        if not fitness_values:
            continue

        # calculate mean and standard deviation
        mean_fitness = total_fitness / len(fitness_values) if fitness_values else 0
        std_fitness = np.std(fitness_values, ddof=1) if len(fitness_values) > 1 else 0

        # report results to wandb
        wandb.log({"generation": gen, "min_fitness": min_fitness, "max_fitness": max_fitness,
                   "mean_fitness": mean_fitness, "std_fitness": std_fitness})


if __name__ == "__main__":
    train()
