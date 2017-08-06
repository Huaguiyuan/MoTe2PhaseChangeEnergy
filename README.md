# Low energy consumption phase change memory via electrostatic gating of monolayer MoTe2

This repo contains all data and plotting files needed to generate the
figures found in 

```
Rehn, D.A., Li, Y., & Reed, E.J. Theoretical potential for low energy consumption phase change memory utilizing
electrostatically-induced structural phase transitions in 2D materials. (in preparation).
```

In this paper, we compute the energy input required to induce a phase transition via electrostatic gating in monolayer MoTe2. See the video below for a view of how this works.

<p align="center"><img src=figures/fig1/video.gif width=500px></p>

We include 3 top-level directories:

- `data`: All input files and scripts related to generating data
  needed for figures.
- `figures`: Scripts used to generate figures in the paper. The
  scripts reference the data in the `data` directory directly (no data
  is provided in the `figures` folder.
- `table`: Provides a python file for computing numbers that are found
  in the table of the paper.

