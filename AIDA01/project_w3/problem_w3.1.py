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
    best_KL_indx=[]
    for row in range(0, len(D), 1):
        P_i = D[row]
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
