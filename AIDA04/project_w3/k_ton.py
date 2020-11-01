# K-ton & singleton reduction on A_mn matrix
# Week 3
# author: @tassosblackg
# All matrices must be numpy ones
# A matrix must have shape(M,N)
# b vector must have shape(M,)
# c vector must have shape(1,N)
# Eqin vector must have shape (M,)


import time
import argparse
import numpy as np
from read_mps import mps2data


def singleton(A,b,c,Eq,C0):
    '''
        If nnz in row = 1 redundant A,b,c,Eq
        @params A_mn coefficients,b_{mx1} right-hand values, c_{1xn} objective func coefficients,Eq_{mx1} in/equality

        @returns A,b,c,Eq,c0
    '''
    start_row = A.shape[0] - 1 #indx of last row

    while(start_row>=0):
        nnz = 0
        for col in range(A.shape[1]):
            if(A[start_row][j] != 0):
                nnz = nnz +1
                position = (start_row,j) # keep last nnz position tuple (i,j)

        if (A[position[0]][position[1]]>= 0):
            # singleton case
            if((nnz == 1) and (Eq[start_row] == 0) ):
                xk = b[position[0]]/A[position[0]][position[1]]
                b = b - xk*A[:,position[1]]

                if (c[positon[1]] != 0):
                    C0 = C0 - c[position[1]]*xk

                start_i = A.shape[0] # in case there is new singleton re-iterate A matrix
                    #delete row
                A = np.delete(A,position[0],axis=0) # deletes the row of A array
                A = np.delete(A,position[1],axis=1) # deletes the column of A array
                b = np.delete(b,position[0],axis=0)
                Eq = np.delete(Eq,position[0],axis=0)
                c = np.delete(c,position[1],axis=1)

            else: # move to next line
                start_row = start_row - 1
        else:
            print("LP is infeasible.. abort\n")
            exit(0)

    return A,b,c,Eq,C0


def k_ton(A,b,c,Eq,k):
    '''
        If nnz in row = k redundant A,b,c,Eq
        @params A_mn coefficients,b right-hand values, c objective func coefficients,Eq inequality

        @returns A,b,c,Eq,c0
    '''
    if (k > A.shape[1]):
        print("Error: k is bigger that columns length of array A, choose a \{k\} <len(columns)\n")
        exit(0)
    else:

        C0 = 0
        start_row = A.shape[0] - 1 # begin from last row go backwards
        while(start_row>=0):
            nnz = 0
            for col in range(A.shape[1]):
                if(A[start_row][j] != 0):
                    nnz = nnz +1
                    position = (start_row,j) # keep last nnz position tuple (i,j)

            if((nnz == k)):
                b[position[0]] = b[position[0]]/A[position[0]][position[1]]
                A[position[0]] = A[position[0]]/A[position[0]][position[1]]
                Eq[position[0]] = -1

                for r in range(A.shape[0]): # for each row in  column where k-ton found
                    if(( A[r][position[1]] >=0) and (r != position[0]) ): # check all in that column except -k
                        b[r] = b - A[r][position[1]]*b[position[0]] # upd all other b, in a row where xk nz
                        A[r] = A[r] - A[r][position[1]]*A[position[0]]

                if (c[positon[1]] != 0):
                    C0 = C0 - c[position[1]]*b[position[0]]
                    c = c - c[position[1]]*np.transpose(A[position[0]])
                #    finally delete column k
                A = np.delete(A,position[1],axis=1)

                start_i = A.shape[0] #  re-iterate A matrix from start to see for new k-tons
            else:
                start_i = start_ - 1

    return (A,b,c,Eq,C0)

# parser menu
def parserM():

    parser=argparse.ArgumentParser(prog="k_ton reduction")
    parser.add_argument('k',type=int,help='k number of non zeros to search for')
    parser.add_argument('input_file',type=str,help='<file_name>')
    args=parser.parse_args()

    start=time.time()
    problem_name, Rows, Bounds, min_max, A_mn, b_m, c_n,Eqin = mps2data(args.input_file)

    if (args.k == 1):

        A,b,c,Eq,C0 = singleton(A_mn, b_m, c_n,Eqin,C0=0)

    else:
        A,b,c,Eq,C0 = k_ton(A_mn, b_m, c_n,Eqin, args.k)
        # after finish k_ton check for singleton
        A,b,c,Eq,C0 = singleton(A,b,c,Eq,C0)

    end = time.time()
    print("Total time to run : ",end-start,"\n")

# MAIN
if __name__=="__main__":
    parserM()
