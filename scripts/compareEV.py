#!/usr/bin/env python

import sys
from ssptools.io.main import readXML, getBands
from ssptools.eigenvalues import compareEV

print("Compares bands of sys.argv[1] and sys.argv[2] for the first nk kpoints where nk is the number of kpoints in sys.argv[1].\nUse as\n\tpython compareEV.py <filename of 1st vasprun.xml> <filename of 2nd vasprun.xml>")
data1, data2 = getBands(readXML(sys.argv[1])), getBands(readXML(sys.argv[2]))
print(compareEV(data1, data2))
