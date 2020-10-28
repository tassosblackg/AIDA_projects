# author: @tassosblackg
# Case of '$' character is not taken into account
# RANGES section are ignored in our use cases
# RANGES section is ignored
import time
import argparse
import numpy as np
from pysnooper import snoop

# search for string key in dictionary return index i of the position
def get_dict_indx(my_dict,key2search):
    for indx, key in enumerate(my_dict):
        if(key2search in key):
            break
        else:
            indx =-1 # not found
    return indx

# Get Amn matrix of coefficients
def col2matrix(columns_dict,rows_dict):
    '''
        Get COLUMNS section data aka the constraints' coefficients
        @columns_dict: the dicitonary with columns section data
        @rows_dict: the dictionary with rows data

        @returns: A_mn array with the coefficients
    '''

    A = [ [0]*len(columns_dict) ]*len(rows_dict) #init M x N  array with 0
    for indx_j, key in enumerate(columns_dict):
        key_row_name = key[1] # get the 2d part of key_tuple => row_name
        indx_i = get_dict_indx(rows_dict, key_row_name)
        if (indx_i !=-1):
            A[indx_i][indx_j]=columns_dict[key] # get value from dictionary
        else:
            print("Error Wrong Name for Row inside Columns section Row doesn;t exist in ROWS section!\n");
    return A

# Get objectives function coefficients dictionary and convert it to matrix
def objectiveF_coef2matrix(columns_dict,obj_func_dict):
    '''
        Get objective's function coefficients dictionary and convert it to matrix/vector
        @columns_dict : the dictionary of columns' section data
        @obj_func_dict: the dictionary of objectives function's values

        @returns : c array of objective function's coefficients
    '''
    obj_coef = [0]*len(columns_dict)
    for indx_c, key in enumerate(obj_func_dict):
        indx = get_dict_indx(columns_dict, key)
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

@snoop('mps2dataD2_.log')
def mps2data(file_name):
    '''
        Read a .mps and return matrices with data
    '''
    # boolean
    in_ROWS_section = False
    in_COLS_section = False
    in_RHS_section = False

    Rows,Bounds,RHS ={}, {},{} # dictionaries {'row_name':value}
    Cols = {} # Cols is { ('col_name,row_name'):value }
    obj = {}  # obj is {'col_name':value}, for Row_name == Objective function name
    A,c,b,Eq =[],[],[],[] # lists

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
#                    Has fields 5,6
                if(len(l)>40):
                    field5 = l[39:48].strip()
                    field6 =float(l[50:62].strip())
#                    ROW1 ,Value2 (Field3,Field4)
                if( (l[14:23].strip() == obj_func_name) ): #<-is it constraint's row or objective's function??
                    obj[col_indx] = field4
                else: # row_name is not objective_function
                    field3 = l[14:23].strip() # Row_name_1 -> indx
                    Cols[col_indx,field3] = field4
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

    c = objectiveF_coef2matrix(Cols, obj)
    A = col2matrix(Cols,Rows)
#------------------ Convert ['E', 'G', 'L'] -> [0,1,-1] ----------------------------------------------------------------------------------
    Eqin=rows2matrix(Rows)
#------------------------------- RHS vector from 1xN to Nx1 format Transpose--------------------------------------------
    min_max = 1
    b_m = np.array(b).reshape(-1,1)
    A_mn = np.array(A)
    c_n = np.array(c)
    Eqin = np.array(Eq).reshape(-1,1)
    return (problem_name, Rows, Bounds, min_max, A_mn, b_m, c_n)


# @snoop('txtFmps.log')
def data2mps(file_name):
    '''
    Reads a .txt file with matrix data
    & write them to a .mps file format
    '''
    A,b,c,E, BS = [],[],[],[],[]
    in_A,in_b,in_c,in_BS, in_Eq = [False]*5

    with open(file_name,'r') as f:
        for l in f:
            tmp_l = l.split()
            if tmp_l : # not an empty line

#----------------- A
                if (l[:1] == 'A' ):
                    tmp_l = l[3:].split()
                    in_A = True
                    A.append(tmp_l)
                elif(in_A and l[-2]!= ']'):
                    A.append(tmp_l)
                elif(in_A and l[-2] == ']'): # end of block
                    in_A = False
                    tmp_l[-1] = tmp_l[-1].replace(']','')
                    A.append(tmp_l)
#---------------- b
                elif (l[:1] == 'b'):
                    in_b = True
                    tmp_l = l[3:].split()
                    b.append(tmp_l)
                elif(in_b and l[-2]!= ']'):
                    b.append(tmp_l)
                elif(in_b and l[-2] == ']'): # end of block
                    in_b = False
                    tmp_l[-1] = tmp_l[-1].replace(']','')
                    b.append(tmp_l)
#---------------- c
                elif (l[:1] == 'c'):
                    in_c = True
                    tmp_l = l[3:].split()
                    c.append(tmp_l)
                elif(in_c and l[-2]!= ']'):
                    c.append(tmp_l)
                elif(in_c and l[-2] == ']'): # end of block
                    in_c = False
                    tmp_l[-1] = tmp_l[-1].replace(']','')
                    c.append(tmp_l)
#---------------- Eqin
                elif (l[:4] == 'Eqin'):
                    in_Eq = True
                    tmp_l = l[6:].split()
                    E.append(tmp_l)
                elif(in_Eq and l[-2]!= ']'):
                    E.append(tmp_l)
                elif(in_Eq and l[-2] == ']'): # end of block
                    in_Eq = False
                    tmp_l[-1] = tmp_l[-1].replace(']','')
                    E.append(tmp_l)
#---------------- BS
                elif (l[:2] == 'BS' ):
                    in_BS = True
                    tmp_l = l[4:].split()
                    BS.append(tmp_l)
                elif(in_BS and l[-1]!= ']'):
                    BS.append(tmp_l)
                elif(in_BS and l[-1] == ']'): # end of block
                    tmp_l = l.split()
                    in_BS = False
                    tmp_l[-1] = tmp_l[-1].replace(']','')
                    BS.append(tmp_l)
#------------------ ProblemType
                elif (l[:6] == 'MinMax'):
                    in_BS = False
                    problem_type = tmp_l[0].split("=")[1] # tmp_l has one string input -> line "MinMax=1" or "MaxMin=-1"

                elif (l[:6] == 'MaxMin'):
                    problem_type = tmp_l[0].split("=")[1]
                else :
                    pass
            else:
                pass
    f.close()
#-------------------------- | Writting Matrices to .mps file \-------------------------------------
    mps_file_name = file_name[:-3]+'mps' # take txt file & change extension
    with open(mps_file_name,'w') as f:
        line = 'NAME'+str(' '*11)+str(mps_file_name[:-4])+':'
        f.write(line+'\n') # Write first line
        f.write('ROWS'+'\n') #ROWS
        type = 'None'
#----------- Write Type, Row data
        for indx, t in enumerate(E):
            if (t[0] == '-1'):
                type = 'L'
            elif (t[0] == '0'):
                type = 'E'
            elif(t[0] == '1'):
                type = 'G'
            else :
                print("Error: type in E not exists\n")

            line = ' '+type+str(' '*2)+'R'+str(indx)+'\n'
            f.write(line)
#-------------- Columns
        f.write('COLUMNS'+'\n')
        for col_indx in range(len(c)): # objective func col values
            line = str(' '*4)+'COL'+str(col_indx)+str(' '*12)+str(c[col_indx][0]) #
            f.write(line+'\n')
#--------------- A matrix write
            for row_indx in range(0,len(A),2):
                chunk = b[row_indx:row_indx+2]
                line = str(' '*4)+'COL'+str(col_indx)
                for el in chunk:
                    l +=str(' '*2)+'R'+str(row_indx)+str(' '*2)+str(el[0])
                line+=l
                f.write(line+'\n')
                line=''

#--------------- RHS
        f.write('RHS'+'\n')
        line = str(' '*4)+'RHS'
        l=''
        for i in range(0, len(b),2):
            chunk = b[i:i+2]
            l=''
            for el in chunk:
                l +=str(' '*2)+'R'+str(i)+str(' '*3)+str(el[0]) # line row,value pairs
            line += l
            f.write(line+'\n')
#------------- BOUNDS
        f.write('BOUNDS'+'\n')
        for r in BS:
            line = ' '+str(r[1])+' '+'B'+str(' '*2)+str(r[0])+str(' '*2)+str(r[1])
            f.write(line+'\n')

        f.write('ENDATA')

    f.close()
    return(A,b,c,E,BS)
# parser menu
def parserM():

    parser=argparse.ArgumentParser(prog="handle_mps_files")
    parser.add_argument("-r","--read",action="store_true",help='read mps file or LP file to convert')
    parser.add_argument('input_file',type=str,help='<file_name>')
    args=parser.parse_args()
    # print(args)
    start=time.time()
    if (args.read):
        problem_name, Rows, Bounds, min_max, A_mn, b_m, c_n = mps2data(args.input_file)
    else:
        A,b,c,E,BS = data2mps(args.input_file)
        print(A,b,c,E,BS)
    end = time.time()
    print("Total time to handle .mps : ",end-start,"\n")
# MAIN
if __name__=="__main__":
    parserM()
