import numpy as np
from permutationsga.problem import Solution

def invperm(permutation):
    """
    Invert a permutation

    Via https://stackoverflow.com/a/55737198
    """
    inv = np.empty_like(permutation)
    inv[permutation] = np.arange(len(inv), dtype=inv.dtype)
    return inv

def crossover_pmx(indices, s0: Solution, s1: Solution):
    assert s0.e is not None, "Ensure solution s0 is initialized before use."
    assert s1.e is not None, "Ensure solution s1 is initialized before use."

    # Prepare copies, and the inverse to perform lookups on.
    r0 = np.copy(s0.e)
    r0inv = invperm(r0)
    r1 = np.copy(s1.e)
    r1inv = invperm(r1)

    for i in indices:
        # We want r0[i], r1[i] = r1[i], r0[i], but that could invalidate the permutation.
        # We know that r1[i] == r0[r0inv[r1[i]]] (other way around is similar.) by definition
        #   of the inverse permutation
        # Therefore we can get r0[i] = r1[i], while perserving uniqueness by swapping
        # r0[i] and r0[r0inv[r1[i]]]
        o = r0inv[r1[i]]
        r_o, r_i = r0[o], r0[i]
        r0[i], r0[o] = r_o, r_i
        # To update r0inv, a similar swap should be performed on r0inv:
        r0inv[r_i], r0inv[r_o] = r0inv[r_o], r0inv[r_i]
        
        # Equivalently for r1 - perform swap
        o = r1inv[r0[o]]
        r_o, r_i = r1[o], r1[i]
        r1[i], r1[o] = r_o, r_i
        # To update r1inv, a similar swap should be performed on r0inv:
        r1inv[r_i], r1inv[r_o] = r1inv[r_o], r1inv[r_i]

    return [Solution(r0), Solution(r1)]

# create two arrays
indices = np.array([3, 4, 5, 6])
arr1 = np.array([9, 0, 7, 2, 8, 6, 5, 3, 1, 4])
arr2 = np.array([2, 5, 7, 9, 4, 6, 0, 3, 8, 1])

sol1, sol2 = crossover_pmx(indices, Solution(arr1), Solution(arr2))
print('test')
