import sys
from ase.io import read, write
from pymatgen.io.vasp.outputs import Vasprun
import json

def readXML(filename):
    return Vasprun(filename).as_dict()

def getBands(data):
    return data['output']['eigenvalues']['1']

def getKpoints(data):
    return data['input']['kpoints']['kpoints']

def getKweights(data):
    return data['input']['kpoints']['kpts_weights']

def aseRead(*argv, **kwargs):
    read(*argv, **kwargs)

def aseWrite(*argv, **kwargs):
    write(*argv, **kwargs)

def get_system(data):
    if "SYSTEM" in data['input']['incar'].keys():
        return data['input']['incar']['SYSTEM']
    else:
        return "unknown_system"
