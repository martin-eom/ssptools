import sys
from pymatgen.io.vasp.outputs import Vasprun

def compareEV(data1, data2):
    bands1, bands2 = data1["output"]["eigenvalues"]['1'], data2["output"]["eigenvalues"]['1']
    nk, nbands = len(bands1), len(bands1[0])
    for i in range(nk):
        for ind in range(nbands):
            print(bands1[i][ind][0] - bands2[i][ind][0], bands1[i][ind][1] - bands2[i][ind][1])
    return sum(sum(abs(bands1[i][ind][0] - bands2[i][ind][0]) + abs(bands1[i][ind][1] - bands2[i][ind][1]) for i in range(nk)) for ind in range(len(bands1[0])))

