# Scientific computing project - gravitational lensing
***
In this project I investigate a simplified model of gravitational lenses.
This work provides a tool for investigating strong lensing effects caused by planar,  smooth and transparent mass distrivutions on a veriety of background objects.
\
Einstein rings are reproduced, galaxy cluster inmages can be generated and lensed, images in jpg form can be lensed and movies of lensing objects moving into view can be computed.
\
Magnification maps and shape distortion maps are produced and investigated for convergence in the limit of finer grid sizes.
Parameter studies are conducted to observe their effects on the result. One such conducted is the study of the effects of ellipticity of the planar lensing mass on the observed integrated luminosity of the background object.
\
Once the tool in tested to reproduce known physical results, not yet astronomically observed systems are modelled.
\
First, a 2 body problem is solved for a star and planet, which is then projected to 1D and lensed. This is done to observe the effects of lensing on transit data. A study of how lensing affects the measure planet to star radius ratio is conduced for a variety of core radii of the lensing source.
\
The same is the done for 2 bodies of comparable masses but much different luminosities (such that one is approximated to be dark). It is found that it is still possible to extract the ratio of sizes of the 2 bodies. This is done and implications to real physical systems are drawn.


***

## Author: Maciej Tomasz Jarema
#### License: [MIT](https://choosealicense.com/licenses/mit/)

## Table of Contents
1. [How to run](#How-to-run)
2. [Figures](#Figures)
3. [Choice of parameters](#Choice-of-parameters)
4. [times to run and used optimisations](#times-to-run-and-used-optimisations)

## How to run
To begin with, in order to run the presented code, a python interpreter is required (preferably spyder, as images may not show in VScode until plt.show() is included). The interpreter must be set to display figures automatically and not 'in-line'.
The libraries listed in the 'requirements.txt' file must also be installed.

Furthermore, to run the code, the working directory must be set to this Githubs repository file.

All the code files are structured such that the first cell comments on the files purpose in a comment and imports the modules.
\
The second cell is the main body of the code.
\
If more cells are present, these are only used to produce tests that can confirm funtionality of the above cells by testing known scenarios.

## Figures
Figures for the report were producing using codes contained in the fiel named 'Project_completed'. Here, I highlight which codes must be run for which study.

#### Figure 1
To reproduce Figure 1, the user must run code named 'TEST image .py'.
It is worth noting that this code only produces one figure, of set parameters, to produce figure.1.a and figure.1.b, it was run separately with different parameters ( see next section for params.).

#### Figure 2
Figure 2 was produced by running the file named: 'galaxy cluster generation and lensing .py'. This image is produced in a single run of the code.

#### Figure 3




## Choice of parameters

It is worh noting that parameters produced used for the figures in the report have been chosen as to present very well detailed results, sometimes at an expense of time. I will therefore document, what parameters were used for each figure, and alongside, what parameters are good to use when testing functionality in a reasonable time.

### Figure 1

##### fig.1.a:
    size = 21
    rc = 0.7
    eps = 0
    dom = 1
time to run (from restarted kernel) ~ 0.10s

##### fig.1.b
    size = 201
    rc = 0.7
    eps = 0
    dom = 1

time to run (from restarted kernel) ~ 0.12s

### Figure 1 (a & b)
    size = 2048
    rc = 0.2
    eps = 0
    dom = 3
    seeded = 143 (in pix_draw.gal_image)
    max_a = 0.32
    minor_max = 80
    gal_N = 70
    minor_major_multiplier = 4 (in pix_draw.gal_image)
time to run (from restarted kernel) ~ 2.7s

(time to generate galaxies ~ 1.7s)


### Figure 3


