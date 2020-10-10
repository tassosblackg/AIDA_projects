# author: @tassosblackg
#

import argparse

A,b,c,E_qin = [],[],[],[],[]


def mps2data(file):
    '''
    Read a .mps and return matrices with data
    '''

    with open(file,'r') as f:
        for l in f:
            if( (len(l) == 0) or (l[:1] == '*') ):
                pass

# ------------------  NAME
            elif(l[:4] == 'NAME'): #field 1
                problem_name = l[14:22] # field 3
            elif(l[:4] == 'ROWS'): #field 1
                in_ROWS_section = True
                pass
            elif(in_ROWS_section and l[:7] != 'COLUMNS'): # => inside ROWS section
                    
            elif(l[:7]=='COLUMNS'):
                in_ROWS_section = False # outside the ROWS section
                in_COLS_section = True  # inside COLUMNS section
    f.close()

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
