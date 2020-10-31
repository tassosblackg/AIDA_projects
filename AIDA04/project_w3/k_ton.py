import numpy as np
from read_mps import mps2data


def singleton(A,b,c,Eq):
    '''
        If nnz in row = 1 redundant A,b,c,Eq
        @params A_mn coefficients,b_{mx1} right-hand values, c_{1xn} objective func coefficients,Eq_{mx1} in/equality

        @returns A,b,c,Eq,c0
    '''
    C0 = 0
    start_row = A.shape[0] - 1 #indx of last row

    while(start_row>=0):
        nnz = 0
        for col in range(A.shape[1]):
            if(A[start_row][j] != 0):
                nnz = nnz +1
                position = (start_row,j) # keep last nnz position tuple (i,j)
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

    return A,b,c,Eq,C0


def k_ton(A,b,c,Eq,k):
        '''
            If nnz in row = k redundant A,b,c,Eq
            @params A_mn coefficients,b right-hand values, c objective func coefficients,Eq inequality

            @returns A,b,c,Eq,c0
        '''
    pass
