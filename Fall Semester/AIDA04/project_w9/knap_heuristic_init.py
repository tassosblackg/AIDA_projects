# COmpt Week 9
# Construction Heuristic for Initial Solution
# author:@tassosblackg

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


# Init Heuristic Solution
# Goal: is to put as many objects in the sack as possible
def init_heuristic_solutionW(capacity, weights):
    '''
    Args:
        - capacity : a int value showing the maximum capacity of the sack
        - weights  : a list with weight values per item

    Returns:
        - solution : a list with ones and zeros, [1]: element in sack [0]: element not inside
    '''
    total_sum_w = sum(weights) # calculate total sum of weights
    solution = [1]*len(weights) # suppose best solution all objects in
    current_sum = total_sum_w
    sublistOfWeights = weights

    while(current_sum > capacity):
        max_Weight = max(sublistOfWeights)
        indexOfdroppedElement = sublistOfWeights.index(max_Weight) # get index of max weight value
        sublistOfWeights[indexOfdroppedElement] = 0
        current_sum = sum(sublistOfWeights) # new sum after removed element

        solution[indexOfdroppedElement] = 0

    return solution


# Calculate the profit based on a solution list
def calculate_total_profit(solution, profits):
    '''
    Args:
        - solution : a list with ones and zeros based on which item is in the sack or not
        - profits  : a list with values of profit per item

    Returns:
        - total_profit  : a value for the total profit of items inside the sack

    '''
    total_profit = 0
    for indx,s in enumerate(solution):
        if (s==1):
            total_profit = total_profit + profits[indx]
    return (total_profit)

# Read Problem Data
# IMPORTANT: args of Input file names must be with the corect order
# ---------------------------------------------------------------------------------------
# @ !Tip: Comment out line according on which problem you want to read data from !

capacity,weights,profits,solution_ohe = get_knap_data(cfile1,wfile1,pfile1,sfile1)
# capacity,weights,profits,solution_ohe = get_knap_data(cfile2,wfile2,pfile2,sfile2)
# capacity,weights,profits,solution_ohe = get_knap_data(cfile3,wfile3,pfile3,sfile3)

# ----------------------------------------------------------------------------------------

input_total_profit = calculate_total_profit(solution_ohe, profits)
print('--------------- Problem\'s Input Data -----------------------\n')
print('\n Capacity = ',capacity,'\n','\nWeight per item = \n',weights,'\n','\nProfits per item\n',profits,'\n','\nSolution O-H-E = \n',solution_ohe)
print('\nTotal Profit = ',input_total_profit,'\n')
print('\n----------------------------------------------------------\n')


# Initial solution problem 1
sol = init_heuristic_solutionW(capacity, weights)
prof = calculate_total_profit(sol,profits)

print('\nInit Simple Heuristic Solution = ',sol)
print('\nInit Simple Heuristic Max Profit = ',prof)