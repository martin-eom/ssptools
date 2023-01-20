from ase.io.vasp import read_vasp, write_vasp
import sys

write_vasp(sys.argv[1], read_vasp(sys.argv[1]), direct=True, sort=True)
