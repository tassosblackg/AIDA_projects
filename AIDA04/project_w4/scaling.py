from read_mps import mps2data
import numpy as np

def count_nz(A):
    row_nnz, col_nnz = [],[]
    # nnz across rows
    for i in range(A.shape[0]):
        count_i = 0
        for j in range(A.shape[1]):
            if(A[i][j] != 0):
                count_i = count_i + 1
        row_nnz.append(count_i)

    # nnz across cols
    for j in range(A.shape[1]):
        count_j = 0
        for i in range(A.shape[0]):
            if(A[i][j] != 0):
                count_j = count_j + 1
        col_nnz.append(count_j)

    return row_nnz,col_nnz

def scaleA(A,b,c):
    # calculate row scale factor
    r = []
    row_nnz,col_nnz = count_nz(A)
    sum_row = np.sum(A,axis=1) # length num of rows
    sum_col = np.sum(A,axis=0) # length num of cols
    for i in
    r.append(row_nnz/np.sum(A[i]))
    r = np.array(r) # final numpy scale r vector
