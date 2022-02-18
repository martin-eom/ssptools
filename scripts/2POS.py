#!/usr/bin/env python

import sys
from ase.io import read, write

try:
    if len(sys.argv) == 2:
        out_name = "POSCAR"
    else:
        out_name = sys.argv[2]
    write(out_name, read(sys.argv[1]), direct = True)
except Exception:
    print("Copies a crystal structure file into a new format (by default into \"POSCAR\").\nUse as\n\tpython 2POS.py <file with crystal structure> <(optional) name of new file>")
