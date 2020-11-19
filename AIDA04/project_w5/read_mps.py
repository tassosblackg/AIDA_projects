# first week read mps function fixed issues
# rows and columns name must start from 1 inside .mps file
# author @tassosblackg

import numpy as np
import re


def get_unique_cols(col_dict):
    """
    Create a list with columns names, from columns dictionary, dictionary has duplicants
    Get the unique columns names
    """
    col_indices = []
    for key in col_dict:
        col_indices.append(key[0])
    return(len(set(col_indices)))

def convert_string_to_int(string):
    return(int(re.search(r'\d+', string)[0]))


# Get Amn matrix of coefficients
def col2matrix(columns_dict,len_rows_dict,num_unique_col):
    '''
        Get COLUMNS section data aka the constraints' coefficients
        @columns_dict: the dicitonary with columns section data
        @len_rows_dict: the length of dictionary with rows data

        @returns: A_mn array with the coefficients
    '''
    A = np.zeros((len_rows_dict,num_unique_col)) #  matrix
    for  key in columns_dict:
        # get the 2d part of key_tuple => row_name (because rows with different name in col section)
        indx_i = convert_string_to_int(key[1]) -1  # get index for row i name
        indx_j = convert_string_to_int(key[0]) -1 # get index for column j name -1 because starting counting from 0
        # print(indx_i,indx_j)
        if (indx_i !=-1):
            A[indx_i][indx_j]=columns_dict[key] # get value from dictionary
        else:
            print("Error Wrong Name for Row inside Columns section Row doesn;t exist in ROWS section!\n");

    return A

# Get objectives function coefficients dictionary and convert it to matrix
def objectiveF_coef2matrix(columns_dict,obj_func_dict,num_unique_col):
    '''
        Get objective's function coefficients dictionary and convert it to matrix/vector
        @columns_dict : the dictionary of columns' section data
        @obj_func_dict: the dictionary of objectives function's values

        @returns : c array of objective function's coefficients
    '''

    obj_coef = [0]*num_unique_col
    for indx_c, key in enumerate(obj_func_dict):
        indx = convert_string_to_int(key) -1 #indx starting from 0
        if(indx!=-1):
            obj_coef[indx] = obj_func_dict[key]
        else:
            print("Error wrong name column from objective function dict i=-1\n")
    return obj_coef

def rows2matrix(rows_dict):
    '''
        Convert Rows constraints from categorical to numerical values and covert dictionary to matrix
        @rows_dict: the dictionary with row's section data

        @returns : Eqin array
    '''
    Eq = []
    for key in rows_dict:
        if (rows_dict[key] == 'E'):
            Eq.append(0)
        elif (rows_dict[key] == 'G'):
            Eq.append(1)
        elif (rows_dict[key] == 'L'):
            Eq.append(-1)
        else:

            print("Error with Rows constraint Type see Row.keys()..\n")

    return Eq

def rhs2matrix(rhs_dict,len_rows_dict):
    '''
        Convert RHS constraints covert dictionary to matrix
        @rhs_dict : right hand constraints values
        @len_rows_dict: the length of dictionary with row's section data

        @returns : Eqin array
    '''
    b=[0]*len_rows_dict
    for key in rhs_dict:
        indx = convert_string_to_int(key) -1
        if(indx != -1):
            b[indx] = rhs_dict[key]
        else:
            print("Error in RHS2matrix rhs_dict key not found in rows_dict\n!")

    return (b)


def mps2data(file_name):
    '''
        Read a .mps and return matrices with data
        @file_name: a mps file
        @returns: problem_name, Rows,Bounds dicitonaries an Amn,b,c,Eqin numpy arrays
    '''
    # boolean
    in_ROWS_section = False
    in_COLS_section = False
    in_RHS_section = False

    Rows,Bounds,RHS ={}, {},{} # dictionaries {'row_name':value}
    Cols = {} # Cols is { ('col_name,row_name'):value }
    obj = {}  # obj is {'col_name':value}, for Row_name == Objective function name

    with open(file_name,'r') as f:
        for l in f:

            if( (len(l) == 0) or (l[:1] == '*') ): # if space or comment
                pass
            elif(l[:6]=='ENDATA'):
#                   BOUNDS, RANGES are optional so might not exist, make False all the previous flags
                in_BOUNDS_section = False
                in_RHS_section = False
                print("EOF reached..\n")
# --------------------------------------------------| NAME section |---------------------------------------------------------------------
            elif(l[:4] == 'NAME'): #field 1
                problem_name = l[14:22].strip() # field 3, through away spaces

#--------------------------------------------------| ROWS section |-----------------------------------------------------------------------
            elif(l[:4] == 'ROWS'): #field 1
                in_ROWS_section = True

            elif(in_ROWS_section and l[:7] != 'COLUMNS'): # => inside ROWS section
                field1 = l[:4].strip() # Constraint Type
                field2 = l[4:13].strip() # Row Name -indx
                if(field1 == 'N'): #objective func
                    obj_func_name = field2 #name of objective fuction
                else:
                    Rows[field2] = field1 # create Dictionary {key=Row_i, value in ['E','G','L'] }

#--------------------------------------------------| COLUMNS section |-----------------------------------------------------------------------
            elif(l[:7]=='COLUMNS'): # => inside COLUMNS section
                in_ROWS_section = False
                in_COLS_section = True

            elif(in_COLS_section and l[:3] != 'RHS'):
                col_indx = l[4:13].strip() # Col_name
                field4 = float(l[24:37].strip()) # Get value from field 4, convert to float
#                    ROW1 ,Value2 (Field3,Field4)
                if( (l[14:23].strip() == obj_func_name) ): #<-is it constraint's row or objective's function??
                    obj[col_indx] = field4
                else: # row_name is not objective_function
                    field3 = l[14:23].strip() # Row_name_1 -> indx
                    Cols[col_indx,field3] = field4
#                    Has fields 5,6
                if(len(l)>40):
                    field5 = l[39:48].strip()
                    field6 =float(l[50:62].strip())

#                    ROW2 ,Value2 (Field5,Field6)
                    if((l[39:48].strip() == obj_func_name)):
                        obj[col_indx]=float(l[50:62].strip())
                    else:
                            Cols[col_indx,field5] = field6 #field6 value
#
# #--------------------------------------------------| RHS section |-----------------------------------------------------------------------
            elif(l[:3] == 'RHS'):
                in_COLS_section = False
                in_RHS_section = True
#               Check if not reach next section RANGES, and BOUNDS are optional so you have to check all cases
            elif(in_RHS_section and (l[:7] != 'RANGES' and l[:6] != 'BOUNDS' and  l[:6] != 'ENDATA')): # inside RHS section, until next section
                row_indx_1 = l[14:23].strip() # row_indx -> field2
                RHS[row_indx_1]= float(l[24:36].strip()) # get value->field 3
                if(len(l) > 40):
                    row_indx_2 = l[39:48].strip() # field 5 -> row_indx name
                    RHS[row_indx_2] = float(l[50:62].strip()) # field 6 value
# #--------------------------------------------------| RANGES section |-----------------------------------------------------------------------
            elif(l[:7] == 'RANGES'):
                in_RHS_section = False
                ''' ignore RANGES'''

# #--------------------------------------------------| BOUNDS section |-----------------------------------------------------------------------
            elif(l[:6] == 'BOUNDS'):
                in_BOUNDS_section = True
                in_RHS_section = False

            elif(in_BOUNDS_section and l[:6] != 'ENDATA'):
                col_indx = l[14:23].strip() # get column name -> 'indx'
                values = [l[:4].strip(),l[25:37].strip()] # create a list contains [Type, Value] for each Bound
                Bounds[col_indx] = values
# #--------------------------------------------------| ENDATA section |-----------------------------------------------------------------------

        f.close()

    num_unique_col =get_unique_cols(Cols) # column index is appeared multiple times
    # convert objective's function dictionary to an array/list
    c = objectiveF_coef2matrix(Cols, obj,num_unique_col)
    # convert coefficients dictionary to array/list
    A = col2matrix(Cols,len(Rows),num_unique_col)
#------------------ Convert ['E', 'G', 'L'] -> [0,1,-1] ----------------------------------------------------------------------------------
    Eq=rows2matrix(Rows)
#------------------- Convert right-hand constraints to array missing row values =zero
    b = rhs2matrix(RHS,len(Rows))
#-------------------------------  lists/arrays to numpy format --------------------------------------------
    min_max = 1
    b_m = np.array(b)
    A_mn = np.array(A)
    c_n = np.array(c).reshape(1,-1) # C must be 1xN
    Eqin = np.array(Eq)
    print("\n Finish reading",problem_name, ".mps...\n")

    return (problem_name, Rows, Bounds, min_max, A_mn, b_m, c_n,Eqin)
