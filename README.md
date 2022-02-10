# Solid-State-Physics Tools (ssptools)

## Preamble

This package contains classes and scripts developed by the author for his work in solid state physics, mainly for working with the input and output
of the Vienna Ab initio Simulation Package. These tools are very specific in their use. The primary purpose of having them on the PyPI is to enable
easier editing of scripts while working on multiple devices. However you may still find some scipts to be of use to you.

## Scripts

### 2POS.py

Uses `read` and `write` from `ase` to convert a file containing a crystal structure to POSCAR or any other file-type acceptable to `ase`.
```console
2POS.py <input-filename> <output-filename (optional)>
```
### appendKPaths.py

Appends kpoints specified in a json file to KPOINTS input of vasp.\
To perform electronic band structure calculations with vasp it is sometimes required to use a combined KPOINTS file that contains both
a $\Gamma$-centered grid and the bandpaths along which the dispersion should be calculated. The kpoints along the bandpaths will be appended
to an existing KPOINTS files which already contains the grid-points in multiples of the reciprocal lattice vectors as a list. So far
only `"type": reciprocal` is implemented. To get the list you can run vasp with a \"normal\" grid-KPOINTS and immediately abort it.
This will create IBZKPT, which contains the list. The json file
containing the bandpath-kpoints should be formulated like this:
```python
{
    "type": "reciprocal",
    "straights": [
            {
                "endpoint": [0, 0, 0],
                "npoints": 1,
                "name": "$\Gamma$"
            },
            {
                "endpoint": [0.333333, 0.333333, 0.],
                "npoints": 40,
                "name": "K"
            },
            {
                "endpoint": [0.333333, 0.333333, 0.5],
                "npoints": 40,
                "name": "K"
            }
        ]

}
```
The band path is given in straights. They are defined by an endpoint, its name and the number of points along it.
The startpoint of a straight is the endpoint of the previous straight in the list. Therefore the first straight must have `"npoints": 1`. "name"
is the label given to the xticks when plotted using `plotBS.py`.\

```console
appendKPaths.py <QPOINTS.json> <KPOINTS>
```

### compareEV.py

Compares the eigenvalues of all kpoints between two vasprun.xml files. Let n1 be the number of kpoints in the first file. The first n1 kpoints
in the second file have to be exactly the same as those in the first.
```console
compareEV.py <vasprun1.xml> <vasprun2.xml>
```
Be warned that the output is extremely lazy.

### plotBS.py

Plots the bandstructure from vasprun.xml files that used KPOINTS files created with `appendKPaths.py` along the paths defined in the json file.\
If you split your vasp calculation along different segments you can plot them in one graph by giving the files in the order which they appear in the
graph as command line arguments.
```console
plotBS.py <vasprun1.xml> <QPOINTS1.json> <vasprun2.xml> <QPOINTS2.json> ...
```
