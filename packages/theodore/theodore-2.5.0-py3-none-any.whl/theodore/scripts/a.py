import argparse
parser = argparse.ArgumentParser(description=None)
parser.add_argument('mo_file', nargs='+', help='an integer for the accumulator')
parser.add_argument('-ifile', help='an integer for the accumulator')

args = parser.parse_args()
print(args)
