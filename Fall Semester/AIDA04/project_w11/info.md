# Week 11 Computer Optimization
### MSc Artificial Intelligence & Data Analytics

## Task: Genetic Algorithm for Knapsack problem

 - Read a file from data folder to get max_caapcity, profits, weights and best_solution in order to compare.

-   Set parameters for knapsack:

    1.| **population_size** = 30

        set the size of population to be created, number of possible solutions

     2.| **mutation_denominator** = 100

         random selection in a range of numbers
         | mutation_denominator defines the end of the range for random func
         *e.g.* select 1 number out of 100

     3.|  **numofGen** = 5*len(weights) # number of iterations

         Number of iterations/generation to run the genetic algorithm
         -> defines end condition of algorithm

     4.|  **convegence_percentage** = 0.8

        also defines the end condition, but using convergence ratio


## Execute program
$> **python3** *ga_knsapsack.py*

## Output
Generates two output files, one keeps the population set (***population_out.txt***) and the other the elite solution/indivitual (***foutput.txt***). By elite means the solution with the maximum fitness/profit score.


Tassos Karageorgiadis

| January 2021 |
