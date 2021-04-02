# Generate Random Data
# for TSP problem
# author: @tassosblackg
import argparse
import numpy as np

DATA_TAG = 'NODE_COORD_SECTION'

def tsp_coord_data(numOfRecords,range_start,range_end):
    # numOfRecordsx2 array, N records with X,Y columns
    coord_xy = np.random.uniform(range_start, range_end, [numOfRecords,2]).round(3)

    return(coord_xy)

def coord_array2txt(array):
    file_name='tsp_'+str(array.shape[0])+'.txt'

    with open(file_name,'w') as f:
        f.write('Name : '+file_name +'\n')
        f.write(DATA_TAG+'\n')
        for i,elmnt in enumerate(array):
            line =str(i+1)+'\t'+str(elmnt[0])+'\t'+str(elmnt[1])+'\n'
            f.write(line)
        f.write('EOF')



# mat=tsp_coord_data(20, 12.3, 1020.32)
# coord_array2txt(mat)
# parser menu
def parserM():

    parser=argparse.ArgumentParser(prog="Knapsack read data")
    parser.add_argument('numOfRecords',type=int,help='<Give Number of Records integer>')
    parser.add_argument('start_r',type=int,help='<Give range_start integer>')
    parser.add_argument('end_r',type=int,help='<Give range_end integer>')

    args=parser.parse_args()

    # Get numpy Array
    mat = tsp_coord_data(args.numOfRecords,args.start_r,args.end_r)
    coord_array2txt(mat)


if __name__ == '__main__':
    parserM()
