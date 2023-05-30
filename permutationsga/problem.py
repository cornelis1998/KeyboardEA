from typing import Optional
import numpy as np
import pandas as pd
import datetime

class Solution:
    """
    Dataclass for containing the current solution (permutation) & corresponding fitness (if evaluated)
    """

    def __init__(self, e: Optional[np.ndarray]):
        self.evaluated = False
        self.e = e # encoded format
        self.s: Optional[np.ndarray] = None # actual solution: decoded format (for this assignment: always a permutation)
        self.f = np.inf # fitness

def copy_solution(s: Solution) -> Solution:
    r = Solution(s.e)
    r.s = s.s
    r.f = s.f
    r.evaluated = s.evaluated
    return r


class Problem:
    def get_length(self):
        return 0

    def evaluate(self, solution: Solution):
        return 0.0


class IdenticalDecoder(Problem):
    """
    Encoded solution is identical to the format the problem expects for evaluation.
    """

    def __init__(self, problem: Problem):
        self.problem = problem

    def get_length(self):
        return self.problem.get_length()

    def evaluate(self, sol: Solution):
        if sol.evaluated:
            return sol.s

        sol.s = sol.e
        return self.problem.evaluate(sol)

def invperm(permutation):
    """
    Invert a permutation

    Via https://stackoverflow.com/a/55737198
    """
    inv = np.empty_like(permutation)
    inv[permutation] = np.arange(len(inv), dtype=inv.dtype)
    return inv

class InvPermDecoder(Problem):
    """
    Encoded solution is the inverse permutation of the actual solution.
    (Or: the actual solution is the inverse of the encoded solution)
    """

    def __init__(self, problem: Problem):
        self.problem = problem

    def get_length(self):
        return self.problem.get_length()

    def evaluate(self, sol: Solution):
        if sol.evaluated:
            return sol.s

        sol.s = invperm(sol.e)
        return self.problem.evaluate(sol)

class RandomKeysDecoder(Problem):
    """
    Solution is encoded in random keys, decode first, then evaluate.
    """

    def __init__(self, problem: Problem):
        self.problem = problem

    def get_length(self):
        return self.problem.get_length()

    def evaluate(self, sol: Solution):
        if sol.evaluated:
            return sol.s

        assert sol.e is not None, "Ensure solution sol is initialized before use."

        sol.s = np.argsort(sol.e)
        return self.problem.evaluate(sol)

class VTRFound(Exception):
    pass

class ElitistTracker(Problem):
    """
    Keep track of the current best solution & evaluation count & other data.
    """
    def __init__(self, problem: Problem, vtr: Optional[float]):
        self.problem = problem
        self.vtr = vtr
        # Keep track of some statistics
        self.num_evaluations = 0
        self.time_of_first_evaluation: Optional[datetime.datetime] = None
         
        # Keep track of the current elitist
        self.current_elitist: Optional[Solution] = None

        # Keep track using a dataframe of all changes
        self.elitist_history = pd.DataFrame({
            '#evaluations': pd.Series(dtype='int'),
            'time (s)': pd.Series(dtype='float'),
            'genotype': pd.Series(dtype='object'), # numpy array
            'phenotype': pd.Series(dtype='object'), # numpy array
            'fitness': pd.Series(dtype='float'),
            'is_vtr': pd.Series(dtype='bool'),
        })

    def get_length(self):
        return self.problem.get_length()

    def evaluate(self, sol: Solution):
        if sol.evaluated:
            return sol.s

        if self.time_of_first_evaluation == None:
            self.time_of_first_evaluation = datetime.datetime.now()

        f = self.problem.evaluate(sol)
        self.num_evaluations += 1

        if self.current_elitist == None or f < self.current_elitist.f:
            self.current_elitist = copy_solution(sol)
            is_vtr = self.vtr != None and sol.f <= self.vtr
            new_row_df = pd.DataFrame({
                '#evaluations': [self.num_evaluations],
                'time (s)': [(datetime.datetime.now() - self.time_of_first_evaluation).total_seconds()],
                'genotype': [sol.e.copy()], # numpy array
                'phenotype': [sol.s.copy()], # numpy array
                'fitness': sol.f,
                'is_vtr': is_vtr,
            })
            self.elitist_history = pd.concat([self.elitist_history, new_row_df])

            if is_vtr:
                raise VTRFound()

        return f
