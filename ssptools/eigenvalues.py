def compareEV(bands1, bands2):
    #bands1, bands2 = data1["output"]["eigenvalues"]['1'], data2["output"]["eigenvalues"]['1']
    nk, nbands = len(bands1), len(bands1[0])
    for i in range(nk):
        for ind in range(nbands):
            print(bands1[i][ind][0] - bands2[i][ind][0], bands1[i][ind][1] - bands2[i][ind][1])
    return sum(sum(abs(bands1[i][ind][0] - bands2[i][ind][0]) + abs(bands1[i][ind][1] - bands2[i][ind][1]) for i in range(nk)) for ind in range(len(bands1[0])))

def weighted_kpoint_inds(bands, kpts_weights):
    return [i for i, weight in enumerate(kpts_weights) if weight != 0], [bands[i] for i, weight in enumerate(kpts_weights) if weight != 0]

def seperateBands(kpoint):
    v_bands, c_bands = [], []
    for ev in kpoint:
        if ev[1] == 0:
            c_bands.append(ev[0])
        else:
            v_bands.append(ev[0])
    c_bands.sort()
    v_bands.sort(reverse = True)
    return c_bands, v_bands

def alignment(bands, **kwargs):
    if "scheme" in kwargs.keys() and kwargs["scheme"] == "bzavg":   # eigenvalues should only inclued weighted kpoints
        if "nvb" in kwargs.keys():
            nvb = kwargs["nvb"]
        else:
            nvb = 2
        if "ncb" in kwargs.keys():
            ncb = kwargs["ncb"]
        else:
            ncb = 1
        branchpoint = 0.
        for kpoint in bands:
            c_bands, v_bands = seperateBands(kpoint)
            branchpoint += sum(c_bands[:ncb]) / ncb + sum(v_bands[:nvb]) / nvb
        return branchpoint / (2 * len(bands))
    else:
        if len(bands) < 1 or max(len(kpoint) for kpoint in bands) < 1:
            return 0
        else:
            occupied_states = []
            for kpoint in bands:
                occupied_states += [ev[0] for ev in kpoint if ev[1] != 0]
            if len(occupied_states) < 1:
                return 0
            else:
                return max(occupied_states)

def gaps(bands):
    for i, kpoint in enumerate(bands):    # first set of eigenvalues should be at gamma
        c_bands, v_bands = seperateBands(bands[i])
        if i == 0:
            vmax, cmin = v_bands[0], c_bands[0]
            direct_gap = gamma_gap = cmin - vmax
        else:
            vmax, cmin = max(vmax, v_bands[0]), min(cmin, c_bands[0])
            direct_gap = min(direct_gap, c_bands[0] - v_bands[0])
    indirect_gap = cmin - vmax
    return gamma_gap, direct_gap, indirect_gap
