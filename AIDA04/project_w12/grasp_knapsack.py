# COmpt Week 12
# Greedy Random Adaptive Search Procedure Algorithm
# author:@tassosblackg
# from pysnooper import snoop
import random

# Problem Data 1
cfile1 = 'knapsack_data/problem1/p01_c.txt' # capacity value
pfile1 = 'knapsack_data/problem1/p01_p.txt' # profits values
wfile1 = 'knapsack_data/problem1/p01_w.txt' # weights values
sfile1 = 'knapsack_data/problem1/p01_s.txt' # solution values

# Problem Data 2
cfile2 = 'knapsack_data/problem2/p02_c.txt' # ..
pfile2 = 'knapsack_data/problem2/p02_p.txt' # ..
wfile2 = 'knapsack_data/problem2/p02_w.txt' # ..
sfile2 = 'knapsack_data/problem2/p02_s.txt' # ..

# Problem Data 2
cfile3 = 'knapsack_data/problem3/p03_c.txt' # ..
pfile3 = 'knapsack_data/problem3/p03_p.txt' # ..
wfile3 = 'knapsack_data/problem3/p03_w.txt' # ..
sfile3 = 'knapsack_data/problem3/p03_s.txt' # ..

# Read Data Func
def get_knap_data(c_file, w_file, p_file, s_file):
    '''
    Get Knapsack problem data from 4 different files, each file
    contains numbers and space with new lines between each value

    Input : file names
     c_file: (c->capcity)
     w_file: (w->weights)
     p_file: (p->profits)
     s_file: (s->solution)

    returns lists of integers with the data plus the capacity value
    '''

    with open(c_file,'r') as f1:
        line = f1.readline().strip()
        capacity = int(line)
    with open(w_file,'r') as f2:
        weights = []
        for line in f2:
            weights.append(int(line.strip()))
    with open(p_file,'r') as f3:
        profits = []
        for line in f3:
            profits.append(int(line.strip()))
    with open(s_file,'r') as f4:
        solution_ohe = []
        for line in f4:
            solution_ohe.append(int(line.strip()))

    return capacity, weights,profits,solution_ohe


# Read input data
capacity,weights,profits,best_solution_ohe = get_knap_data(cfile1,wfile1,pfile1,sfile1)
# capacity,weights,profits,solution_ohe = get_knap_data(cfile2,wfile2,pfile2,sfile2)
# capacity,weights,profits,solution_ohe = get_knap_data(cfile3,wfile3,pfile3,sfile3)

# Pack them up all to a dictionary
items = {} # items: [0:id,1:weight,2:profits]
items[0] = [k for k in range(len(weights))] # id == idx of list item
items[1] = weights
items[2] = value

print('\n |> Items = ',items, '\n |> Max Capacity = ',capacity)
