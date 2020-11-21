from read_mps import mps2data
import argparse
import numpy as np
from pysnooper import snoop

def get_basis_B(Eqin):
    """
    Create AB matrix with 1 or -1 in the main diagonial -- slack variables
    Create matrix B with columns indices for AB matrix of slack variables
    @Eqin: input Inequality vector for constraint type

    @returns: AB, CB and B matrices
    """
    AB = np.zeros((Eqin.shape[0],Eqin.shape[0]))
    for i,elmnt in enumerate(Eqin):
        if(elmnt == -1):
            AB[i][i] = 1
        elif(elmnt == 1):
            AB[i][i] = -1
        else:
            print("Eqin equality case not into account exiting..\n")
            exit(-1)
        Eqin[i] = 0 # convert Inequality to equality
    # array with indices on columns of AB
    B = np.arange(0, AB.shape[1], dtype=int)
    CB = np.zeros((1,len(B)))
    return(AB,B,CB,Eqin)

def get_XB(AB_inv,b):
    return(np.matmul(AB_inv,b))

def get_w(CB,AB_inv):
    return(np.matmul(CB,AB_inv))

def get_Sn(c,w,A):
    return(c-np.matmul(w,A))

def split_N(N,Sn):
    P,Q = [],[]
    for index,val in enumerate(Sn[0]):
        if val < 0:
            P.append(index)
        else:
            Q.append(index)
    return(P,Q)

def get_S0(Sn,P,lamda):
    tmp = []
    for indx,val in enumerate(P):
        tmp.append(lamda[indx]*Sn[0][val])
    return(sum(tmp))

def get_db(AB_inv,A,P,lamda):
    tmp = []
    for indx,val in enumerate(P):
        tmp.append(lamda[indx]*np.matmul(AB_inv,A[:,val]))
    return(sum(tmp))

@snoop('init_step.txt')
def init_step(A, b, c,Eqin):
    AB,B,CB,new_Eqin = get_basis_B(Eqin)
    AB_inv = np.linalg.inv(AB)
    XB =  get_XB(AB_inv, b)
    N = np.arange(0,A.shape[1],dtype=np.uint32) # N set column indices
    w = get_w(CB, AB_inv)
    Sn = get_Sn(c,w,A)
    P,Q = split_N(N, Sn)
    lamda = np.ones(len(P))
    S0 = get_S0(Sn, P, lamda)
    dB = get_db(AB_inv, A, P,lamda)

    return(AB,B,CB,new_Eqin,XB,Sn,P,Q,S0,dB)

def count_pos_db(db):
    numOfpos = 0
    for val in db:
        if val >= 0:
            numOfpos = numOfpos +1
    return numOfpos

def is_db_pos(numOfpos,db_len):
    if (numOfpos == db_len):
        cond = True
    else:
        cond = False
    return cond

# def epsa(A, b, c,Eqin):
#     AB,B,CB,XB,Sn,P,Q,S0,db = init_step(A,b,c,Eqin)
#     numOfiter = 0
#     while(len(P)!=0 and S0 !=0):
#         if( is_db_pos(count_pos_db,len(db)) ):
#             if(S0 == 0):
#                 break
#         else:
#             # check alpha and get r, k
#         # step 2 -pivoting
#
#         # step 3 - update
#         numOfiter = numOfiter + 1
# parser menu
def parserM():

    parser=argparse.ArgumentParser(prog="EPSA problem solve")
    parser.add_argument('input_file',type=str,help='<file_name>')
    args=parser.parse_args()

    problem_name, Rows, Bounds, min_max, A_mn, b_m, c_n,Eqin = mps2data(args.input_file)
    AB,B,CB,new_Eqin,XB,Sn,P,Q,S0,dB = init_step(A_mn, b_m, c_n, Eqin)
    numOfpos = count_pos_db(dB)
    print(numOfpos,len(dB))

if __name__ == '__main__':
    parserM()
