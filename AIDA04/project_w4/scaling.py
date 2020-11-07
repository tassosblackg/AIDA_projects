from read_mps import mps2data
import numpy as np


def scaleA(A,b,c):

    r,s = [],[]
    row_nnz = (A!=0).sum(0)
    col_nnz = (A!=0).sum(1)
    sum_row = np.sum(A,axis=1) # length num of rows
    sum_col = np.sum(A,axis=0) # length num of cols
    # calculate row scale factor
    for i in range(len(sum_row)):
        r.append(row_nnz[i]/np.sum(sum_row[i]))
    r = np.array(r) # final numpy scale r vector
    # calculate col scale factor
    for j in range(len(sum_col)):
        s.append(col_nnz[j]/np.sum(sum_col[j]))
    s = np.array(s) # final numpy scale r vector
