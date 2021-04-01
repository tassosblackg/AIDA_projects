'''
Project Week 5-6 EPSA
author: @tassosblackg
Comments: problem while inveriting AB matrix determinant can be zero, so inversion can't happen
'''

from read_mps import mps2data
import argparse
import numpy as np
import time


def get_basis_B(A,c,Eqin):
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
    ABN = np.concatenate((A,AB),axis=1) # concatenate An with AB
    B = np.arange(A.shape[1], A.shape[1]+AB.shape[1], dtype=np.uint32)
    CB = np.zeros((1,len(B)))
    CBN = np.concatenate((c,CB),axis=1)
    return(ABN,B,CBN,Eqin)

def get_XB(AB_inv,b):
    return(np.matmul(AB_inv,b))

def get_w(CB,AB_inv):
    # print(CB.shape,AB_inv.shape)
    return(np.matmul(CB.reshape(1,-1),AB_inv))

def get_Sn(c,w,A):
    # print('Sn\n',c.shape,w.shape,A.shape)
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
    return((-1)*sum(tmp))


def init_step(A, b, c,Eqin):
    '''
    Calculate the Step 0 Vectors and Values
    '''
    ABN,B,CBN,new_Eqin = get_basis_B(A,c,Eqin)
    AB_inv = np.linalg.inv(ABN[:,B])
    XB =  get_XB(AB_inv, b)
    N = np.arange(0,A.shape[1],dtype=np.uint32) # N set column indices
    CB = CBN[0,B]
    w = get_w(CB, AB_inv)
    Sn = get_Sn(c,w,A)
    P,Q = split_N(N, Sn)
    lamda = np.ones(len(P))
    S0 = get_S0(Sn, P, lamda)
    dB = get_db(AB_inv, A, P,lamda)

    return(ABN,AB_inv,B,CBN,new_Eqin,XB,Sn,P,Q,S0,dB)

def count_pos_db(db):
    '''
    count positve elements inside dB vector
    '''
    numOfpos = 0
    for val in db:
        if val >= 0:
            numOfpos = numOfpos +1
    return numOfpos

def is_db_pos(numOfpos,db_len):
    '''
    Boolean if dB has only positive elements
    '''
    if (numOfpos == db_len):
        cond = True
    else:
        cond = False
    return cond

def get_alpha(dB,XB):
    a_indx,tmp = [],[]
    # print('DB',dB.shape)
    for indx,val in enumerate(dB):
        if val < 0:
            tmp.append(XB[indx]/(-val))
            a_indx.append(indx)
    np_tmp = np.array(tmp)
    alpha = min(np_tmp)
    min_i = np.argmin(np_tmp)
    r = a_indx[min_i] #

    return (alpha,r)

def get_HrP(AB_inv,r,A,P):
    return(np.matmul(AB_inv[r,],A[:,P]))

def get_HrQ(AB_inv,r,A,Q):
    return(np.matmul(AB_inv[r,],A[:,Q]))

def get_theta1(Sn,P,HrP):
    tmp, min_i = [],[]
    # Sp = Sn[0,P]
    for indx in range(len(P)):
        if HrP[indx] > 0:
            tmp.append(-Sn[0][P[indx]]/HrP[indx])
            min_i.append(indx)

    np_tmp = np.array(tmp)
    theta1 = min(np_tmp)
    ith = np.argmin(np_tmp)
    t1 = min_i[ith]


    return(theta1,t1)

def get_theta2(Sn,Q,HrQ):
    tmp, min_i = [],[]
    for indx in range(len(Q)):
        if HrQ[indx] < 0:
            tmp.append(-Sn[0][Q[indx]]/HrQ[indx])
            min_i.append(indx)
    if(len(tmp)!=0):
        np_tmp = np.array(tmp)
        theta2 = min(np_tmp)
        ith = np.argmin(np_tmp)
        t2 = min_i[ith]
    else:
        theta2 = float('inf')
        t2 = 'None'
    return(theta2,t2)

def epsa(A, b, c,Eqin):
    ABN,AB_inv,B,CBN,new_Eqin,XB,Sn,P,Q,S0,dB = init_step(A,b,c,Eqin)
    numOfiter = 0
    while(len(P)!=0 ):
        # if all dB values are positive or equal to zero
        if( is_db_pos(count_pos_db,len(dB)) ):
            if(S0 == 0):
                break
        else: # dB has <0 values
            # check alpha and get r, k
            if (len(dB) == 0): # means a=inf, so problem is unbounded
                print("\n LP1 is unbounded problem..exiting..\n")
                exit(-1)
            else:
                a,r = get_alpha(dB,XB)

                k = B[r]


        # ---------------------------------------|Step 2 - Pivoting|-------------------------------------------------------
        HrP = get_HrP(AB_inv,r,A,P)
        HrQ = get_HrQ(AB_inv,r,A,Q)
        theta1,t1 = get_theta1(Sn, P, HrP)
        theta2,t2 = get_theta2(Sn, Q, HrQ)
        if (theta1<theta2):
            l = P[t1]
        else:
            l = Q[t2]

        # ----------------------------------------- |Step 3 - Update|-------------------------------------------------------
        B[r] = l
        if (theta1<theta2):
            P.remove(l)
            Q.append(k)
        else:
            Q[t2] = k

        AB = ABN[:,B] # get new updated AB
        # with np.printoptions(threshold=np.inf):
        #     print(AB)
        # print('DET\n',)
        if(np.linalg.det(AB) == 0):
            print("Determinant of matrix AB is zero, can't get the inverse matrix..exiting\n")
            break
        AB_inv = np.linalg.inv(AB)
        XB = get_XB(AB_inv, b)
        CB = CBN[0,B] # new CB
        w = get_w(CB, AB_inv)
        N = P + Q           # concatenate new P and Q to form new N
        A = ABN
        c = CBN[0,N].reshape(1,-1) # format to 1xN

        Sn = get_Sn(c, w, A[:,N]) #??
        lamda = np.ones(len(P))
        S0 = get_S0(Sn, P, lamda)
        dB = get_db(AB_inv, A, P, lamda)

        numOfiter = numOfiter + 1

    return(numOfiter,S0)

# parser menu
def parserM():

    parser=argparse.ArgumentParser(prog="EPSA problem solve")
    parser.add_argument('input_file',type=str,help='<file_name>')
    args=parser.parse_args()

    start=time.time()
    problem_name, Rows, Bounds, min_max, A_mn, b_m, c_n,Eqin = mps2data(args.input_file)
    # AB,AB_inv,B,CB,new_Eqin,XB,Sn,P,Q,S0,dB = init_step(A_mn, b_m, c_n, Eqin) #<- change returns
    print('\nStarting EPSA..\n')
    numOfiter,S0 = epsa(A_mn, b_m, c_n,Eqin)
    print('\n|NumberOfIterations= ',numOfiter,' | S0= ',S0,' |\n')


    end = time.time()
    print("Total time to run read & epsa : ",end-start,"\n")

if __name__ == '__main__':
    parserM()
