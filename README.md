# Artificial Intelligence Nanodegree
## Introductory Project: Diagonal Sudoku Solver

# Question 1 (Naked Twins)
Q: How do we use constraint propagation to solve the naked twins problem?  
A: The nature of a pair of naked twins means that we know that anything else within their unit cannot be the values which are twinned. Because two boxes in one unit have the same two numbers and only those two numbers, we know that those two numbers can only appear in those boxes. Thus, we have a new constraint: other boxes in a unit with a pair of naked twins cannot have either of the values in the naked twins. We can propagate this constraint across the unit by removing the values of the naked twins from the possible values of other boxes in the unit. As with other forms of constraint propagation, this might reveal more naked twins, such that we can repeat the process again.

# Question 2 (Diagonal Sudoku)
Q: How do we use constraint propagation to solve the diagonal sudoku problem?  
A: We merely create an additional two units across which the constrain propagation techniques we use for standard sudoku must be applied. The core idea is the same. 

### Install

This project requires **Python 3**.

We recommend students install [Anaconda](https://www.continuum.io/downloads), a pre-packaged Python distribution that contains all of the necessary libraries and software for this project.
Please try using the environment we provided in the Anaconda lesson of the Nanodegree.

##### Optional: Pygame

Optionally, you can also install pygame if you want to see your visualization. If you've followed our instructions for setting up our conda environment, you should be all set.

If not, please see how to download pygame [here](http://www.pygame.org/download.shtml).

### Code

* `solution.py` - You'll fill this in as part of your solution.
* `solution_test.py` - Do not modify this. You can test your solution by running `python solution_test.py`.
* `PySudoku.py` - Do not modify this. This is code for visualizing your solution.
* `visualize.py` - Do not modify this. This is code for visualizing your solution.

### Visualizing

To visualize your solution, please only assign values to the values_dict using the ```assign_values``` function provided in solution.py
