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

# Read Data Func
def get_knap_data(c_file,w_file,p_file,s_file):
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
def init_heuristic_solutionW(capacity,weights):
    total_sum_w = sum(weights) # calculate total sum of weights
    solution = [1]*len(weights) # suppose best solution all objects in
    current_sum = total_sum_w
    sublistOfWeights = weights

    while(current_sum >capacity):
        max_Weight = max(sublistOfWeights)
        indexOfdroppedElement = sublistOfWeights.index(max_Weight) # get index of max weight value
        sublistOfWeights[indexOfdroppedElement] = 0
        current_sum = sum(sublistOfWeights) # new sum after removed element

        solution[indexOfdroppedElement] = 0

    return solution    

# Read Problem Data
# IMPORTANT: args of Input file names must be with the corect order
capacity,weights,profits,solution_ohe = get_knap_data(cfile1,wfile1,pfile1,sfile1)
print(capacity,weights,profits,solution_ohe)



init_heuristic_solutionW(capacity,weights)
