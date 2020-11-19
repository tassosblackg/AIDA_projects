from read_mps import mps2data
import argparse



# parser menu
def parserM():

    parser=argparse.ArgumentParser(prog="EPSA problem solve")
    parser.add_argument('input_file',type=str,help='<file_name>')
    args=parser.parse_args()

if __name__ == '__main__':
    parserM()
