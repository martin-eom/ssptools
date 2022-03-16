#!/usr/bin/env python

import sys, json
import matplotlib.pyplot as plt
from matplotlib.ticker import (MultipleLocator, FormatStrFormatter, AutoMinorLocator)
from pymatgen.io.vasp.outputs import Vasprun
from ssptools.io.main import readXML
from ssptools.BSData import BSData, joinBSs, openJSON

nsteps = len(sys.argv)//2
xmlFiles, jsonFiles = [sys.argv[2*n+1] for n in range(nsteps)], [sys.argv[2*n+2] for n in range(nsteps)]
combinedData = joinBSs([BSData(readXML(xmlFiles[i]), openJSON(jsonFiles[i]), auto_align = True) for i in range(len(xmlFiles))])

x = combinedData.x_data

for band in combinedData.bands:
    plt.plot(combinedData.x_data, band, color = "orange")
plt.ylim([-15, 9])
plt.xlim([combinedData.x_data[0], combinedData.x_data[-1]])
plt.ylabel("Energy [eV]")
plt.xticks(ticks = combinedData.xticks, labels = combinedData.labels)
plt.grid(axis = 'both')
plt.savefig("%s_bands.png"%combinedData.name)
plt.show()
plt.close()
combinedData.write("%s_bands.json"%combinedData.name)
