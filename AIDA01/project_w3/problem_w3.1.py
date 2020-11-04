import numpy as np

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
                Q_i = D[row2]
                sum = 0
                for column in range(0, len(D[0]), step=1):
                    sum = sum + P_i[column] * np.log(P_i[column] / Q_i[column])
                KL_i.append(sum)
                Q_indx.append(row2)
        index_min = min(range(len(KL_i)), key=KL_i.__getitem__) # get the index of min(KL) of i
        #but the real index is stored inside Q_indx
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
    I_xy = 0
    # rows corresponds to X,columns corresponds to Y
    for i in range(P_xy.shape[0]): # rows
        for j in range(P_xy.shape[1]):# columns
            I_xy = I_xy + P_xy[i][j] * np.log(P_xy[i][j] / P_x[i]*P_y[j] )

    return I_xy
