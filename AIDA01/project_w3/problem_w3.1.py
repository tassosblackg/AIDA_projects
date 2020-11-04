import numpy as np
import argparse

def read_matrix(file_name):
    '''
    Reads a .txt file with specific format an coverted to a list/array 2D
    '''
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



def calculate_min_KLdivergence(D):
    '''
    Find the Y distribution which has the smallest KL divergence given a X distribution

    @D: An 2D [NxM] list/array each row corresponds to a distribution i

    @returns: A list with an index for each i, showing whith whom j!=i has the smallest KL divergence
    '''

    best_KL_indx=[]
    for row in range(0, len(D), 1):
        P_i = D[row]
        KL_i,Q_indx = [],[]

        for row2 in range(0, len(D), 1):
            if(row2!=row):
                    # division with zero error
                if(D[row2] == 0):
                    Q_i = 0.0001
                else:
                    Q_i = D[row2]
                sum = 0
                for column in range(0, len(D[0]), step=1):
                    sum = sum + P_i[column] * np.log(P_i[column] / Q_i[column])
                KL_i.append(sum)
                Q_indx.append(row2)

        index_min = min(range(len(KL_i)), key=KL_i.__getitem__) # get the index of min(KL) of i

        # but the real index is stored inside Q_indx
        best_KL_indx.append(Q_indx[index_min]) # index of best fit distribution among 1-N, for i!=j

    return best_KL_indx

def calculate_MI(input_mat):
    '''
    Calculate Mutual Information between X, Y a set of discrete random variables

    @input_mat: An 2D [NxN] list/array read from a file given as text

    @returns: An number corresponds to the mutual information between X,Y
    '''

    P_xy = np.array(input_mat) # convert 2D list to numpy array
    P_x = np.sum(P_xy,axis=1) # get Px by suming for each row the column's values
    P_y = np.sum(P_xy,axis=0) # get Py by suming for each column the row's values
    is_valid_Pxy(P_x,P_y) # check if not valid distribution exit()
    I_xy = 0
    # rows corresponds to X,columns corresponds to Y
    for i in range(P_xy.shape[0]): # rows
        for j in range(P_xy.shape[1]):# columns
            # in order to devide with zero set a small number
            if(P_x[i]==0 or P_y[i] == 0):
                denuminator = 0.0001
            else:
                denuminator = P_x[i]*P_y[i]

            I_xy = I_xy + P_xy[i][j] * np.log(P_xy[i][j] / denuminator )

    return I_xy

def check_kl_matrix(A):
    mat = np.array(A)
    row_sum = np.sum(A,axis=1) # each row must sum to 1
    for i in range(A.shape[0]):
        if(row_sum[i] != 1):
            print("Error each distribution/row must sum to 1, check your input file again\n")
            exit(-1)

def is_valid_Pxy(px,py):
    sum_px = np.sum(px)
    sum_py = np.sum(py)
    if (sum_px != 1 or sum_py != 1):
        print("Error P(X,Y) is not valid, check sum of px or py is not 1\n")
        exit(-1)

def is_negative(A):
    mat = np.array(A)
    has_negative = mat[mat<0]
    if (len(has_negative)!=0):
        printf("Error your input matrix has some negative values check again\n")
        exit(-1)

# parser menu
def parserM():

    parser=argparse.ArgumentParser(prog="handle_mps_files")
    parser.add_argument("-kl","--kl",action="store_true",help='read txt file  to convert')
    parser.add_argument('input_file',type=str,help='<file_name>')
    args=parser.parse_args()

    if (args.kl):
        A = read_matrix(args.input_file)
        check_kl_matrix(A)
        is_negative(A)
        best_KL = calculate_min_KLdivergence(A)
        print(best_KL)
    else:
        A = read_matrix(args.input_file)
        is_negative(A)
        I_xy = calculate_MI(A)
        print("I_xy",I_xy)
    end = time.time()

# MAIN
if __name__=="__main__":
    parserM()
