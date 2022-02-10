import setuptools

with open("README.md", 'r', encoding="utf-8") as fh:
	long_description = fh.read()

setuptools.setup(
	name="ssptools",
	version="0.1.0",
	author="Martin Keller",
	description="Various specialized tools for working with the input and output of VASP",
        long_description=long_description,
        classifiers=[
                "Programming Language :: Python :: 3",
                "License :: OSI Approved :: MIT License",
                "Operating System :: OS Independent"
        ],
        packages=setuptools.find_packages(),
        python_requires=">=3.4",
        install_requires =[
                "ase",
                "matplotlib",
                "numpy",
                "pymatgen"
        ],
        scripts=[
            "scripts/2POS.py",
            "scripts/appendKPaths.py",
            "scripts/compareEV.py",
            "scripts/plotBS.py"
        ]
)
