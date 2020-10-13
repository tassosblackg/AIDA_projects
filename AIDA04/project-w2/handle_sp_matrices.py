# @tassosblackg
# Tassos Karageorgiadis
# Read a Sparce matrix from file and converted to CSR or CSC form


import argparse


def read_matrix(file_name):
    pass

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
        IA.append(IA[i-1]+nnz)
    IA.append(nnz+1)

    return(Anz,JA,IA)

def sp2csc(A):
    pass


# parser menu
def parserM():

    parser=argparse.ArgumentParser(prog="handle_mps_files")
    parser.add_argument("-csr","--csr",action="store_true",help='read mps file or LP file to convert')
    parser.add_argument('input_file',type=str,help='<file_name>')
    args=parser.parse_args()
    # print(args)
    matrix = read_matrix(args.input_file)


    if (args.csr):
        [Anz,JA, IA] = sp2csr(matrix)
    else:
        [Anz,JA,IA] = sp2csc(matrix)

# MAIN
if __name__=="__main__":
    parserM()
