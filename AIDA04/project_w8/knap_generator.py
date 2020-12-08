# Data Generator for Knapsack
# Give Inputs:
#       NumerOfRecords
#       capacity_start_range
#       capacity_end_range
# author: @tassosblackg
import argparse
import random
import numpy as np


def knap_data(NumOfObjects,crange_start,crange_end):
    """
    Get as Input 3 integers

    returns one integer and two lists of integers
    """
    capacity = random.randint(crange_start+11,crange_end+11)

    weights = random.sample(range(1, capacity-1), NumOfObjects)
    profits = random.sample(range(2, capacity-1), NumOfObjects) * 2

    return capacity,weights,profits


def datamat2txts(c,w,p):
    name = 'knap_'+str(len(w))
    ext = '.txt'

    with open(name+'_c'+ext,'w') as f:
        f.write(str(c))
    with open(name+'_w'+ext,'w') as f:
        for i in w:
            f.write(str(i)+'\n')
    with open(name+'_p'+ext,'w') as f:
        for j in p:
            f.write(str(j)+'\n')

# c,w,p=knap_data(5,2,10)
# datamat2txts(c,w,p)


# parser menu
def parserM():

    parser=argparse.ArgumentParser(prog="Knapsack read data")
    parser.add_argument('numOfRecords',type=int,help='<Give Number of Records integer>')
    parser.add_argument('cstart_r',type=int,help='<Give range_start integer>')
    parser.add_argument('cend_r',type=int,help='<Give range_end integer>')

    args=parser.parse_args()

    # Get capacity_int,weights_list,profits_list Array
    c,w,p = knap_data(args.numOfRecords,args.cstart_r,args.cend_r)
    datamat2txts(c,w,p)


if __name__ == '__main__':
    parserM()
