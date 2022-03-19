import sys, json
from numpy import array
from numpy.linalg import norm
from ssptools.io.main import getBands, getKpoints, getKweights, get_system
from ssptools.eigenvalues import alignment, weighted_kpoint_inds
import matplotlib.pyplot as plt

class BSData:
    def __init__(self, *argv, **kwargs):
        # loading from BSData-shaped json
        if len(argv) == 1:
            with open(argv[0], 'r') as file:
                argd = json.load(file)
                self.rec_vec = array(argd["rec_vec"])
                self.kpoints = [array(kp) for kp in argd["kpoints"]]
                self.x_data  = argd["x_data"]
                self.bands   = argd["bands"]
                self.xticks  = argd["xticks"]
                self.labels  = argd["labels"]
                self.name    = argd["name"]
        # loading from opened vasprun.xml (pymatgen Vasprunner as_dict) and QPOINTS.json
        elif len(argv) == 2:
            data, JSON = argv[0], argv[1]
            self.x_data = [0.]
            self.xticks = []
            self.name = get_system(data)
            numlist, self.labels = [straight["npoints"] for straight in JSON["straights"]], [straight["name"] for straight in JSON["straights"]]
            nk = sum(numlist)
            self.rec_vec = array(data["input"]["lattice_rec"]["matrix"])
            self.kpoints = [kp[0]*self.rec_vec[0] + kp[1]*self.rec_vec[1] + kp[2]*self.rec_vec[2] for kp in getKpoints(data)]
            last = self.kpoints[-nk]
            for kpoint in self.kpoints[-nk+1:]:
                self.x_data.append(self.x_data[-1] + norm(kpoint-last))
                last = kpoint
            bands = getBands(data)
            if "auto_align" in kwargs and kwargs["auto_align"] == True:
                weighted_ind, weighted_bands = weighted_kpoint_inds(bands, getKweights(data))
                if "LSORBIT" in data['input']['incar'].keys() and data['input']['incar']['LSORBIT'] == True:
                    div = 1
                else:
                    div = 2
                if "6H" in self.name:   E0 = alignment(weighted_bands, scheme = "bzavg", nvb = 24 // div, ncb = 12 // div)
                elif "4H" in self.name: E0 = alignment(weighted_bands, scheme = "bzavg", nvb = 16 // div, ncb = 8 // div)
                elif "2H" in self.name: E0 = alignment(weighted_bands, scheme = "bzavg", nvb = 8 // div,  ncb = 4 // div)
                elif "3C" in self.name: E0 = alignment(weighted_bands, scheme = "bzavg", nvb = 12 // div, ncb = 6 // div)
                else: E0 = alignment(bands, **kwargs)
            else:
                E0 = alignment(bands, **kwargs)
            self.bands = [[ev[i][0] - E0 for ev in bands[-nk:]] for i in range(len(bands[0]))]
            for i in range(len(numlist)):
                self.xticks.append(self.x_data[sum(numlist[:i+1]) - 1])
        # giving all attributes manually
        else:
            self.rec_vec    = argv[0]
            self.kpoints    = argv[1]
            self.x_data     = argv[2]
            self.bands      = argv[3]
            self.xticks     = argv[4]
            self.labels     = argv[5]
            self.name       = argv[6]

    def write(self, filename):
        JSON = {}
        JSON["rec_vec"] = [[comp for comp in vec] for vec in self.rec_vec]
        JSON["kpoints"] = [[comp for comp in kp] for kp in self.kpoints]
        JSON["x_data"]  = self.x_data
        JSON["bands"]   = self.bands
        JSON["xticks"]  = self.xticks
        JSON["labels"]  = self.labels
        JSON["name"]    = self.name
        with open(filename, 'w') as file:
            json.dump(JSON, file, indent = 4)

# for joining consecutive straights in k-space, must give them in the order in which they are plotted
def joinBSs(BSDatas):
    nsteps = len(BSDatas)
    rec_vec, name = BSDatas[0].rec_vec, BSDatas[0].name
    kpoints, x_data, bands, xticks, labels = BSDatas[0].kpoints, BSDatas[0].x_data, BSDatas[0].bands, BSDatas[0].xticks, BSDatas[0].labels
    for i in range(1, nsteps):
        kpoints += BSDatas[i].kpoints[1:]
        xstep = x_data[-1]
        x_data  += [x + xstep for x in BSDatas[i].x_data[1:]]
        for ind in range(len(bands)):
            bands[ind] += BSDatas[i].bands[ind][1:]
        xticks += [tick + xstep for tick in BSDatas[i].xticks[1:]]
        labels += BSDatas[i].labels[1:]
    return BSData(rec_vec, kpoints, x_data, bands, xticks, labels, name)

def openJSON(filename):
    with open(filename, 'r') as file:
        return json.load(file)
