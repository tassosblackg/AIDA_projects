# @tassosblackg
# Tassos Karageorgiadis
# Read a Sparce matrix from file and converted to CSR or CSC form
# -csr oprtion or (csc <- default)
# Please read Instructions.md file before run

# import numpy as np
import argparse
# from pysnooper import snoop

# @snoop('read_matrix.log')
def read_matrix(file_name):
    A = []
    with open(file_name, mode='r') as f:
        for l in f :
            if l :
                tmp_l = l.strip().split()
                if '=' in tmp_l: # pop last element
                    sp_name = tmp_l[0] # get the name of array
                elif '[' in tmp_l: # start of array entries
                    pass
                elif  ']' in tmp_l: #close bracket stop reading
                    pass
                else :
                    A.append(list(map(float,tmp_l))) # convert list of chars -> map of floats ->list of floats
    return A

# @snoop('csr.log')
def sp2csr(A):
    Anz,IA,JA =[],[],[]
    IA.append(0)
    nnz=0
    # CSR scan through rows
    for i in range(len(A)):
        for j in range(len(A[i])):
            if A[i][j] != 0 :
                nnz = nnz+1 # increase number of non-zeros values
                Anz.append(A[i][j])
                JA.append(j) # append column indx
        IA.append(nnz)
    # IA.append(nnz+1)

    return(Anz,JA,IA)

# @snoop('csc.log')
def sp2csc(A):
    Anz,IA,JA =[],[],[]
    IA.append(0)
    nnz=0
    # CSC scan through columns first
    for j in range(len(A[0])):
        for i in range(len(A)):
            if A[i][j] != 0 :
                nnz = nnz+1 # increase number of non-zeros values
                Anz.append(A[i][j])
                JA.append(i) # append row indx
        IA.append(nnz)
    # IA.append(nnz+1)

    return(Anz,JA,IA)

# parser menu
def parserM():

    parser=argparse.ArgumentParser(prog="handle_mps_files")
    parser.add_argument("-csr","--csr",action="store_true",help='read mps file or LP file to convert')
    parser.add_argument('input_file',type=str,help='<file_name>')
    args=parser.parse_args()
    # print(args)
    matrix = read_matrix(args.input_file)
    print(matrix)
    # A = read_matrix()
    if (args.csr):
        [Anz,JA, IA] = sp2csr(matrix)
        print('\nAnz= \n',Anz,'\nJA= \n',JA,'\nIA= \n',IA)
    else:
        [Anz,JA,IA] = sp2csc(matrix)
        print('\nAnz= \n',Anz,'\nJA= \n',JA,'\nIA= \n',IA)
# MAIN
if __name__=="__main__":
    parserM()
