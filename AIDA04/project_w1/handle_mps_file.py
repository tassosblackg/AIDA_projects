# author: @tassosblackg
# convert to dictioneries

import argparse
from pysnooper import snoop
# A,b,c,E_qin = [],[],[],[],[]

@snoop('mps2data_.log')
def mps2data(file):
    '''
    Read a .mps and return matrices with data
    '''
    in_ROWS_section = False
    Rtypes, Rnames, Cnames, Rindx = [],[],[],[]

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
                Rtypes.append(l[:4].strip()) # Get all types ['N','L','E','G'] per RowName
                Rnames.append(l[4:13].strip()) # Get RowsNames

            elif(l[:7]=='COLUMNS'): # => inside COLUMNS section
                in_ROWS_section = False # outside the ROWS section
                in_COLS_section = True  # inside COLUMNS section

            elif(in_COLS_section and l[:7] != 'COLUMNS'):
                Cnames.append(l[4:13].strip())
                Rindx.append(l[14:23].strip())

            elif(in_COLS_section and l[:4] != 'RHS'):
                in_COLS_section = False

            elif(l[:4] == 'RHS'):
                pass

            elif(l[:4]=='ENDATA'):
                print("EOF reached..\n")
    f.close()

    return (problem_name,Rtypes,Rnames,Cnames, Rindx)

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
        name,Rt,Rn,Cn,Ri = mps2data(args.input_file)
        print(name)
        print(Rt,'\n',Rn)
        print(Cn,'\n',Ri)

    else:
        data2mps(args.input_file)



if __name__=="__main__":
    parserM()
