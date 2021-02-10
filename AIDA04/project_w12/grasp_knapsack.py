# COmpt Week 12
# Greedy Random Adaptive Search Procedure Algorithm
# author:@tassosblackg
# from pysnooper import snoop
import random

# Problem Data 1
cfile1 = 'knapsack_data/problem1/p01_c.txt' # capacity profit
pfile1 = 'knapsack_data/problem1/p01_p.txt' # profits profits
wfile1 = 'knapsack_data/problem1/p01_w.txt' # weights profits
sfile1 = 'knapsack_data/problem1/p01_s.txt' # solution profits

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
    contains numbers and space with new lines between each profit

    Input : file names
     c_file: (c->capcity)
     w_file: (w->weights)
     p_file: (p->profits)
     s_file: (s->solution)

    returns lists of integers with the data plus the capacity profit
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

# create a list with all the possible solutions
def powerset_posible_solutions(items):
	res = [[]]
	for item in items:
		newset = [r+[item] for r in res]
		res.extend(newset)
	return res


# select solution from the powerset
def knapsack_brutef_select(items, max_weight):
	knapsack = []
	best_weight = 0
	best_profit = 0
	for item_set in powerset_posible_solutions(items):
		set_weight = sum(map(weight, item_set))
		set_profit = sum(map(profit, item_set))
		if set_profit > best_profit and set_weight <= max_weight:
			best_weight = set_weight
			best_profit = set_profit
			knapsack = item_set
	return knapsack, best_weight, best_profit

# returns key to used for sorting based on weight value
def weight(item):
	return item[1]

# returns key to used for sorting based on profit value
def profit(item):
	return item[2]

# returns key to used for sorting based on profit/weight ratio
def pf(item):
	return float(profit(item))/weight(item)

# GRASP
def knapsack_greedy(items, max_weight, keyFunc= weight):
	knapsack = []
	knapsack_weight = 0
	knapsack_profit = 0
	items_sorted = sorted(items, key=keyFunc)
	while len(items_sorted) > 0:
		item = items_sorted.pop()
		if weight(item) + knapsack_weight <= max_weight:
			knapsack.append(item)
			knapsack_weight += weight(knapsack[-1])
			knapsack_profit += profit(knapsack[-1])
		else:
			break
	return knapsack, knapsack_weight, knapsack_profit


# ----------------------------- | Execution | -------------------------------------------------

# Read input data
capacity,weights,profits,best_solution_ohe = get_knap_data(cfile1,wfile1,pfile1,sfile1)
# capacity,weights,profits,solution_ohe = get_knap_data(cfile2,wfile2,pfile2,sfile2)
# capacity,weights,profits,solution_ohe = get_knap_data(cfile3,wfile3,pfile3,sfile3)


# Pack them up all toa lsit of tupples
items = list(zip([k for k in range(len(weights))],weights,profits)) # list of tuples [(id,weight,profit)]

print(weights,profits)
print('\n |> Items = ',items, '\n |> Max Capacity = ',capacity)

knapsack, opt_wt, opt_profit = knapsack_brutef_select(items, capacity)
print("\n@  ",knapsack, opt_wt, opt_profit)
r = []

knapsack, wt, prof = knapsack_greedy(items, capacity, profit)
print(knapsack,wt, prof)
r.append(float(prof)/opt_profit)

knapsack, wt, prof = knapsack_greedy(items, capacity, pf)
r.append(float(prof)/opt_profit)

print(r)
