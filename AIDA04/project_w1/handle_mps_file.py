# author: @tassosblackg
# convert to dictioneries

import argparse
import numpy as np
# from pysnooper import snoop

# @snoop('mps2data_.log')
def mps2data(file):
    '''
    Read a .mps and return matrices with data
    '''
    in_ROWS_section = False
    in_COLS_section = False
    in_RHS_section = False
    Rtypes, Rnames, Cnames, Rindx = [],[],[],[]
    Rows = dict()
    Bounds = dict()
    A,c,b =[],[],[]
    with open(file,'r') as f:
        for l in f:
            if( (len(l) == 0) or (l[:1] == '*') ):
                pass

# ------------------  NAME
            elif(l[:4] == 'NAME'): #field 1
                problem_name = l[14:22].strip() # field 3, through away spaces
            elif(l[:4] == 'ROWS'): #field 1
                in_ROWS_section = True
                # pass
            elif(in_ROWS_section and l[:7] != 'COLUMNS'): # => inside ROWS section
                field1 = l[:4].strip() # Constraint Type
                field2 = l[4:13].strip() # Row Name -indx
                if(field1 == 'N'): #objective func
                    obj_func_name = field2 #name of objective fuction
                else:
                    Rows[int(field2)] = field1 # create Dictionary {key=Row_i, value in ['E','G','L'] }

            elif(l[:7]=='COLUMNS'): # => inside COLUMNS section
                in_ROWS_section = False # outside the ROWS section
                in_COLS_section = True  # inside COLUMNS section

            elif(in_COLS_section and l[:7] != 'COLUMNS'):
                col_indx = int(l[5:13].strip()) # Col_name drop first_letter take number -> indx
                field4 = float(l[24:37].strip()) # Get value from field 4, convert to float
                if(l[14:23].strip() == obj_func_name):
                    c[col_indx] = field4
                else: # row_name is not objective_function
                    row_indx = int(l[15:23].strip()) # Row_name -> indx
                    A[row_indx,col_indx] = field4
                    if(len(l) > 40): # there is field5 field6
                        row_indx = int(l[40:48].strip()) # field5 row_idx
                        A[row_indx,col_indx] = float(l[50:62].strip()) #field6 value

            elif(l[:4] == 'RHS'):
                in_COLS_section = False
                in_RHS_section = True

            elif(in_RHS_section and l[:4] != 'RHS'):
                in_RHS_section = False
                row_indx = int(l[15:23].strip()) # row_indx
                b[row_indx] = float(l[24:36].strip()) # get value
                if(len(l) > 40):
                    row_indx = int(l[40:48].strip()) # field 5 -> row_indx
                    b[row_indx] = float(l[50:62].strip()) # field 6 value
            elif(l[:4] == 'RANGES'):
                in_RHS_section = False
                ''' ignore RANGES'''
            elif(l[:6] == 'BOUNDS'):
                in_BOUNDS_section = True
            elif(in_BOUNDS_section and l[:6] != 'BOUNDS'):
                col_indx = int(l[15:23].strip()) # get column name -> indx
                values = [l[:4].strip(),l[25:37].strip()] # create a list contains [Type, Value] for each Bound
                Bounds[col_indx] = values

            elif(l[:4]=='ENDATA'):
                in_BOUNDS_section = False
                print("EOF reached..\n")

        f.close()

#------------------ Convert ['E', 'G', 'L'] -> [0,1,-1] ----------------------------------------------------------------------------------
    for key in Rows:
        if (Rows[key] == 'E'):
            Rows[key] = 0
        elif (Rows[key] == 'G'):
            Rows[key] = 1
        elif (Rows[key] == 'L'):
            Rows[key] = -1
        else:
            print("Error with Rows constraint Type see Row.keys()..\n")

#------------------------------- RHS vector from 1xN to Nx1 format Transpose--------------------------------------------
    min_max = 1
    return (problem_name,np.array(b).T,np.array(A),np.array(c),min_max, Rows, Bounds)

    # return (problem_name,Rtypes,Rnames,Cnames, Rindx)

def data2mps(file):
    f = open(file,'r')
    line = f.readline()



# parser menu
def parserM():

    parser=argparse.ArgumentParser(prog="handle_mps_files")
    parser.add_argument("-r","--read",action="store_true",help='read mps file or LP file to convert')
    parser.add_argument('input_file',type=str,help='<file_name>')


    args=parser.parse_args()
    print(args)
    if (args.read):
        mps2data(args.input_file)
    else:
        data2mps(args.input_file)



if __name__=="__main__":
    parserM()
