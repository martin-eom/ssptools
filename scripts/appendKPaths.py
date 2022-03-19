#!/usr/bin/env python

import sys
from ssptools.kpaths import read, makeCoordList

pointList, numList, nameList = read(sys.argv[1])
coordList = makeCoordList(pointList, numList, nameList)
with open(sys.argv[2], 'a') as file:
    for kpoint in coordList:
        file.write("\t%f\t%f\t%f\t%d\n" % (kpoint[0], kpoint[1], kpoint[2], 0))
with open(sys.argv[2], 'r') as file:
    lines = file.readlines()
nk_old = int(lines[1])
nk_new = nk_old + sum(numList)
lines[1] = " %d\n"%nk_new
with open(sys.argv[2], 'w') as file:
    for line in lines:
        file.write(line)
print("%d kpoints were appended to %s."%(nk_new-nk_old, sys.argv[2]))
