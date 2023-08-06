
import os, sys
tmp = sys.argv.pop(0)

ifile = 'dens_ana.in'
while len(sys.argv)>0:
    print(sys.argv)
    arg = sys.argv.pop(0)
    if arg in ["-h", "-H", "--help"]:
        ihelp()
    elif arg == '-ifile' or arg == '-f':
        ifile = sys.argv.pop(0)
