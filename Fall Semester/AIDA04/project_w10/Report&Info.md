# Week 10 Computer Optimization
### MSc Artificial Intelligence & Data Analytics

## Task: Create an Improve initial solution heuristic

### Idea of the initial heuristic method:
The initial heuristic gives an solution base only on the items' total weight to be smaller than the capacity of the sack. So, we try to fit as many items inside the sack.

### Idea for Improving heuristic method:
Get the Items that left outside the sack and check <ins>*if any of them has a **bigger profit** and its **weight is smaller** than an item inside the sack*</ins>. If this is true, **swap** the two items **in** and **out** of the sack. Repeat that process for all the left-over items, in way to be check with all the items inside the sack.

Then I calculate the new max profit of the items inside the sack.
> **def** improve_initial_solution(init_solution, weights, profits)

Finally, calculate the percentage of profit improvement
> **def** improvement_perc(old_profit, new_profit)

## Results :
The improvement percentage is preferred to the total profit of items in the sack.

For ***problem 1***  we have an improvement of **30.1%**,

> **initial_solution** =\[1, 1, 1, 1, 0, 1, 0, 0, 0, 0\],
>
> Init Simple Heuristic Max Profit =  309
>
> **improved_solution** =\[1, 0, 0, 0, 0, 0, 1, 1, 1, 1\]
>
> New max profit =  402


For ***problem 2***  we have an improvement of **35.39%**,

> **initial_solution** =\[1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0\],
>
>Init Simple Heuristic Max Profit =  1249
>
> **improved_solution** =\[0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1\]
>
> New max profit =  1691


For ***problem 3***  we have an improvement of **43.18%**,

> **initial_solution** = \[0, 1, 0, 1, 1\],
>
> Init Simple Heuristic Max Profit =  44
>
> **improved_solution** =\[1, 0, 1, 0, 1\]
>
> New max profit =  63


## Testing for different knapsack problem data:
See lines: **167-169** inside --**knap_improve.py**--, comment in/out the preferred line to load the data you want.

## Executing:
Running the code:
> python3 knap_improve.py

### Author:

Tassos Karageorgiadis

*| December 2020 |*
