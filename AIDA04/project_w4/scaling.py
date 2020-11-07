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
    # calculate row scale factor
    for i in range(len(sum_row)):
        r.append(row_nnz[i]/sum_row[i])
    r = np.array(r) # final numpy scale r vector
    # calculate col scale factor
    for j in range(len(sum_col)):
        s.append(col_nnz[j]/sum_col[j])
    s = np.array(s) # final numpy scale r vector
    # scale rows
    for i in range(A.shape[0]):
        A[i] = A[i]*r
        b[i] = b[i]*r
    # scale columns
    for j in range(A.shape[1]):
        A[:,j] = A[:,j]*s
        c[:,j] = c[:,j]*s

    return A,b,c
