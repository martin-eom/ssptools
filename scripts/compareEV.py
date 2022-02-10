#!/usr/bin/env python

import sys
from pymatgen.io.vasp.outputs import Vasprun
from ssptools.compare import compareEV

print("Compares bands of sys.argv[1] and sys.argv[2] for the first nk kpoints where nk is the number of kpoints in sys.argv[1].\nUse as\n\tpython compareEV.py <filename of 1st vasprun.xml> <filename of 2nd vasprun.xml>")
data1, data2 = Vasprun(sys.argv[1]).as_dict(), Vasprun(sys.argv[2]).as_dict()
print(compareEV(data1, data2))
