# Charged electron entropy calculations

To generate data in this folder, run two different python
files. First, run:

	$ python getEntropy.py

This will generate two files: `entropy2H.dat` and `entropyTp.dat`,
which correspond to the electron entropies of 2H and 1T' phase at a
range of temperatures and excess charges.

Next, run:

	$ python getTdS_TV.py
	
	
This will use `entropy2H.dat` and `entropyTp.dat` to generate two new
files: `TdS.dat` and `TV.dat`

