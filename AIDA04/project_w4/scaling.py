import argparse
import time
from read_mps import mps2data
import numpy as np


def scaleA(A,b,c):
    """
    Calculate scaling factor for row,cols and adjust matrix A and vectors b,c
    @A : nnz coefficients matrix
    @b : right-hand values
    @c : objective function's coefficients
    @returns A,b,c scaled formatted
    """

    r,s = [],[]
    row_nnz = (A!=0).sum(1) # count nnz elements of each row
    col_nnz = (A!=0).sum(0) # count nnz elements of each column
    sum_row = np.sum(A,axis=1) # length num of rows
    sum_col = np.sum(A,axis=0) # length num of cols
    print(A.shape)
    print(sum_row.shape)
    # calculate row scale factor
    for i in range(len(sum_row)):
        r.append(row_nnz[i]/sum_row[i])
    r = np.array(r) # final numpy scale r vector
    print(r.shape)
    # calculate col scale factor
    for j in range(len(sum_col)):
        s.append(col_nnz[j]/sum_col[j])
    s = np.array(s) # final numpy scale r vector
    print(A[0,:].shape)
    # scale rows
    for i in range(A.shape[0]):
        A[i] = A[i,:]*r[i]
        b[i] = b[i]*r[i]
    # scale columns
    for j in range(A.shape[1]):
        A[:,j] = A[:,j]*s[j]
        c[:,j] = c[:,j]*s[j]

    return A,b,c



# parser menu
def parserM():

    parser=argparse.ArgumentParser(prog="scaling matrix and vectors")
    parser.add_argument('input_file',type=str,help='<file_name>')
    args=parser.parse_args()

    start=time.time()
    print("reading..\n")
    problem_name, Rows, Bounds, min_max, A_mn, b_m, c_n,Eqin = mps2data(args.input_file)
    print("scaling...\n")

    A,b,c = scaleA(A_mn, b_m, c_n)
    print("\nA=\n",A,"\nb =\n",b,"\nc =\n",c,"\nEq =\n",Eqin)

    end = time.time()
    print("Total time to run scale : ",end-start,"\n")

# MAIN
if __name__=="__main__":
    parserM()
