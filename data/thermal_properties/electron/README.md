# Electronic entropy calculations

Calculations of electronic entropy are divided into two different
subfolders: `uncharged` and `charged`. 

- `uncharged`: This folder includes calculations used to generate SI
  Figure 3 for MoTe2 with zero excess charge (Q=0). Non-colinear spin
  orbit coupling is included in these calculations at temperatures T =
  0,10,20,..., 1000 K. Due to the band gap of 2H phase at zero excess
  charge, the electronic entropy of 2H is zero for temperatures up to
  ~900 K, so that the electronic entropy difference looks the same as
  the 1T' electronic entropy.

- `charged`: This folder contains calculations for the electronic
  entropy of charged 2H and 1T' phases.  We use values of charge 
  
  `ch = -0.05, -0.04, -0.03, ..., 0.10` e/f.u.
  
  and
  
  `T = 0, 20, 40, ..., 200, 400, 600, 800, 1000` K
  
  to map out the entropy surface as a function of T and Q. The results
  are shown in SI Figure 2.

