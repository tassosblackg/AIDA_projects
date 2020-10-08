# author: @tassosblackg
#
import sys
import argparse











#parser menu
def parserM(args):
    if(len(args)<2):
        print("ERROR: Invalid call of script, requieres two inputs..\n")
        print(" args[0]: '-r' otpion to read .mps file or '-w' to read text file with matrices to convert to .mps\n")
        print(" args[1]: file_name, e.g. file1.mps, or fileX.txt \n")
        print(" IMPORTANT: make sure to use file's path too, in case script and files are not in the same dir/ \n")
        exit()

    parser=argparse.ArgumentParser(prog="handle_mps_files")
    parser.add_argument('path_to_video',type=str,help='chose one video input file..')

    args=parser.parse_args()





if __name__=="__main__":
    parserM(sys.argv)
