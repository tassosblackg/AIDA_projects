# Knapsack read data for problem
# Suppose each problem has one capacity inside file
# author : tassosblackg
import time
import argparse

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

# parser menu
def parserM():

    parser=argparse.ArgumentParser(prog="Knapsack read data")
    parser.add_argument('input_file1',type=str,help='<capacity_file_name>')
    parser.add_argument('input_file2',type=str,help='<weights_file_name>')
    parser.add_argument('input_file3',type=str,help='<profit_file_name>')
    parser.add_argument('input_file4',type=str,help='<solution_file_name>')
    args=parser.parse_args()

    start=time.time()
    c,w,p,s = get_knap_data(args.input_file1,args.input_file2,args.input_file3,args.input_file4)
    print("\nCapacity= ",c)
    print("\nWeights= ",w)
    print("\nProfits= ",p)
    print("\nSolution= ",s)

    end = time.time()
    print("Total time to run  : ",end-start,"\n")

if __name__ == '__main__':
    parserM()
