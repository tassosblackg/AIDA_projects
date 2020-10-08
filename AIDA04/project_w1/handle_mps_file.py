# author: @tassosblackg
#
import sys
import argparse


def mps2data(file):
    print(str(file))


def data2mps(file):
    print(str(file),2)



#parser menu
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
