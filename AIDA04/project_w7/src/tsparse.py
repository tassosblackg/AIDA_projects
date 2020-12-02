# Symetric TSP data parser
# Get two list with X, Y coordinates
# 1-1 pairs between the two lists
# e.g. Point_1 = (X[0],Y[0])
#author: tassosblackg
import time
import argparse

DATA_TAG = 'NODE_COORD_SECTION'


def get_tsp_data(file_name):
    '''
    Get Symetric TSP data
    @Iput: file name

    @returns: two lists of integers X,Y which are 1-1 conected 
    '''
    x, y = [],[]
    data_section = False
    with open(file_name,'r') as f:
        for line in f:
            l = line.strip()
            l_splitted = l.split()

            # Input coordinates
            if l == DATA_TAG:
                data_section = True
                continue

            elif l == 'EOF':
                data_section = False


            if data_section :
                print(len(l_splitted))
                x.append(int(l_splitted[1]))
                y.append(int(l_splitted[2]))

    return x,y

# parser menu
def parserM():

    parser=argparse.ArgumentParser(prog="Knapsack read data")
    parser.add_argument('input_file1',type=str,help='<capacity_file_name>')

    args=parser.parse_args()

    start=time.time()
    x, y = get_tsp_data(args.input_file1)
    print("\n (a) X_coord= ",x, '\n\n [Length X = ', len(x),']\n')
    print("\n (b) Y_cord= ",y, '\n\n [Length Y = ', len(y),']\n')
    end = time.time()
    print("\nTotal time to run  : ",end-start,"\n")


if __name__ == '__main__':
    parserM()
