# Keyboard Layout Optimization using Evolutionary Algorithms
In this project, a method for keyboard layout optimization is discussed. We have recieved a base method from the TU Delft Course, and were asked to analyse the results and improve them somehow. We have tried a few different approaches. These approaches are explained in our paper. All of the added functions can be found in the `new_fns.py` file. 

## Initialization methods
We have tried a few new initialization methods. `QWERTYRandom`, `AZERTYRandom`, `ColemakRandom` and `DvorakRandom` all create an initial population with keyboards that are based on those popular layouts. The class `QwertyPermutationInitialization` also creates a random initial population based on QWERTY and AZERTY layouts. 

Another initialization class was added that creates an initial layout population where the most used keys are on the middle row. This one is called `BetterPermutationInitialization`, although the results were worse.

The initialization classes can be used in the same way as the given `RandomPermutationInitialization` class. There are some arguments added to the functions of some classes.

## Crossover and mutation functions
A few new improved crossover pmx functions were written. First, one that creates only one child: `crossover_pmx_single_off`. Secondly, two variations called `crossover_pmx_predef_secs` and `crossover_pmx_adjusted_chance`. Three new implementations of swap, scramble and insertion mutation can also be found here. The results of these functions can be found in our paper.

## Visualization
The last thing we have written is a piece of code that can visualize the found keyboard layouts. This is used by the function `visualize_keyboard`. 

## Solutions
By running best_found_GA.py we produced the final results as presented in our paper.
Modifying the setup_ga function allows for running the experiment with other settings.

To run the hyper-parameter sweep, see the bigger_sweep branch in this repostiory.
Here we have a setup that allows for quickly searching the optimal parameters for the GA

For more details, see our paper.



# TU Delft Documentation
The basis of this project was given as a starting point. The documentation below is the project discription as it was shared on Brightspace.

## EA-Course - Permutations
When using Evolutionary Algorithms, one particularly important aspect of applying such an EA is the choice of **encoding**. In many cases the encoding used is trivial, for example a mapping from positions on a discrete string to the variables used within evaluation, or similarly for continuous variables. Such encodings are commonplace, and you have already (potentially unknowingly) encountered them.

The right encoding can however provide significant benefits to the performance of an EA! Specific encodings can be used to avoid infeasible solutions by construction, bias the search space towards regions of interest, or allow for better & more effective recombination. In this assignment we utilize various encodings (and crossover operators) to investigate their applicability to a particularly common (yet constrained) search space: Permutations.

Permutations are used to define sequences, orderings of preference, or unique one-to-one mappings. If you ever had a problem that takes such a solution as input, permutations are a common way to mathematically write down a solution. One (easy) way to encode permutations is a discrete search space, assigning a value 1 through the string length. Yet this introduces ties invalidating the solution, as such the ties need to be broken somehow.

Alternative encodings can help with avoiding this problem entirely, but come with their own up and downsides.
- Can you provide a way to write down a solution (or generate and preserve) such that this is not an issue (i.e. any value encodes a valid permutation)? 
- What kind of evolutionary algorithm do you need to use (or, if you have the time: works best)? (discrete, continuous, specialized?)
- What are the downsides of the decisions made?

## Recommended Reading
You do not necessarily have to come up with an encoding yourself! Here are some suggested papers:
- Bean, James C. 1994. ‘Genetic Algorithms and Random Keys for Sequencing and Optimization’. ORSA Journal on Computing 6 (2): 154–60. https://doi.org/10.1287/ijoc.6.2.154.
- Krömer, Pavel, Vojtěch Uher, and Václav Snášel. 2022. ‘Novel Random Key Encoding Schemes for the Differential Evolution of Permutation Problems’. IEEE Transactions on Evolutionary Computation 26 (1): 43–57. https://doi.org/10.1109/TEVC.2021.3087802.

Other things to keep in mind is the space in which a permutation is defined. Permutations can be used as a mapping from A->B, or as a mapping from B->A (note: one is the inverse permutation of the other!). Depending which of the two methods is used, resulting permutations will be different, yet still describe the same solution. The differences are important however, as the way in which solutions are recombined can be different, in addition to the linkage exhibited by the problem.

## Problems
In this assignment we will be looking at two problems: the Travelling Salesperson Problem (TSP) & the Quadratic Assignment Problem (QAP). Both of these problems use permutations as input to their evaluation function, but they are quite different in how the permutation is utilized. Given their differences, it is likely

### TSP
For TSP the permutation is used as a sequence of cities, in the order in which they will be visited, minimizing the total distance between sequential cities.

- We will be using instances from TSPLIB: http://comopt.ifi.uni-heidelberg.de/software/TSPLIB95/
- Furthermore, we will focus on the symmetric instances.
- Parsing will be done through `tsplib95`

### QAP
QAP is used, for example, for assigning facilities to locations, where each facility needs one location, and each location can only be used once. Each facility requires resources from the other facilities, while there is a cost for transferring resources from one location to the next: the assignment should be such that facilities with significant transfers are in positions with low transferring costs between one another.

- We will be using instances from QAPLIB: http://www.mgi.polymtl.ca/anjos/qaplib/
