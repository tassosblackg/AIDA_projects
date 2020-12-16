# COmpt Week 9
# Construction Heuristic for Initial Solution
# author:@tassosblackg


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
