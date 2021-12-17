# Scientific computing project - gravitational lensing

## Introduction
***
In this project I investigate a simplified model of gravitational lenses.
This work provides a tool for investigating strong lensing effects caused by planar,  smooth and transparent mass distributions on a veriety of background objects.
\
Einstein rings are reproduced, galaxy cluster inmages can be generated and lensed, images in jpg form can be lensed and movies of lensing objects moving into view can be computed.
\
Magnification maps and shape distortion maps are produced and investigated for convergence in the limit of finer grid sizes. Problems with the analysis are identified and limitations of the code are drawn when found.
\
Parameter studies are conducted to observe their effects on the result. One such conducted is the study of the effects of ellipticity of the planar lensing mass on the observed integrated luminosity of the background object.
\
Once the tool in tested to reproduce known physical results, not yet astronomically observed systems are modelled.
\
First, a 2 body problem is solved for a star and planet, which is then projected to 1D and lensed. This is done to observe the effects of lensing on transit data.
\
The same is the done for 2 bodies of comparable masses but much different luminosities (such that one is approximated to be dark). It is found that it is still possible to extract the ratio of sizes of the 2 bodies. This is done and implications to real physical systems are drawn. Systematic errors are studied, as well as more physical extension including misalignment of the 2 body CoM with the plane of the lens during the transit.


***

## Author: Maciej Tomasz Jarema
#### License: [MIT](https://choosealicense.com/licenses/mit/)

## Table of Contents
1. [How to run](##How-to-run)
2. [Figures](##Figures)
3. [Choice of parameters](##Choice-of-parameters)
4. [Used optimisations](##Used-optimisations)

## How to run
To begin with, in order to run the presented code, a python interpreter is required (preferably spyder, as images may not show in VScode until plt.show() is included). The interpreter must be set to display figures automatically and not 'in-line'.
The libraries listed in the 'requirements.txt' file must also be installed.

Furthermore, to run the code, the working directory must be set to this Githubs repository file.

In the repository file, the fnished results, latest codes and the figure report of the project are all located in the file named 'Project_completed'.

All the code files are structured such that the first cell comments on the files purpose in a comment and imports the modules.
\
The second cell is the main body of the code.
\
If more cells are present, these are only used to produce tests that can confirm funtionality of the above cells by testing known scenarios.

## Figures
Figures for the report were producing using codes contained in the fiel named 'Project_completed'. Here, I highlight which codes must be run for which study. Note that thef igure names in the files do not directly correspond to their positions in the final report.

It is worh noting that parameters produced used for the figures in the report have been chosen as to present very well detailed results, sometimes at an expense of time. I will therefore document, what parameters were used for each figure, and alongside, what parameters are good to use when testing functionality in a reasonable time.

### Figure 1
To reproduce Figure 1, the user must run code named 'TEST image .py'.
It is worth noting that this code only produces one figure, of set parameters, to produce figure.1.a and figure.1.b, it was run separately with different parameters.

Parameters:

#### left:
    size = 21
    rc = 0.7
    eps = 0
    dom = 1
time to run (from restarted kernel) ~ 0.10s

#### right
    size = 201
    rc = 0.7
    eps = 0
    dom = 1

time to run (from restarted kernel) ~ 0.12s

### Figure 2
These figures are produced by files from 'additional codes \\ convergence study'. The top row images are produced by file named: 'mag convergence testing' and bottom, error anaylis was made using: 'mag convergence testing systematic'.

Parameters:

for convergence testing:

    rc = 0.7
    eps = 0
    dom = 1
    initial_img = 19
    init_N = 19
    N_max = 1200
    inset plots from msplits = 1, 20, 21, 40

time to run: 

for systematic error testing:

    rc = 0.7
    eps = 0
    dom = 1
    initial_img_start = 21
    initial_img_end = 121

time to run: 


### Figure 3
Magnification maps are produced by codes in file 'codes for tasks from sheet \\ advanced'. Named 'mag map RGB test' for top and 'magnification map' for bottom.

Note that these use modularised functions to RGB mark pixels uniquely and to search for them in the transformed image.

Used paramters:

for test image:

    size = 5

time to run ~ 1s

for magnification map:

    rc = 0
    eps = 0
    size = 400

    NOTE never exceed size of 4096 (sqrt(256^3)), not only becuase the time to run would not be concievable, but even when optimised to deal with such (hypothetically), RGB colours could not longer remain unique to each pixel.

    dom = 2

time to run ~


### Figure 4
Shape distortion maps produced by codes from file 'additional codes \\ shape distortions'. The files are intuitively named '1D graph' and '2D map'.

Parameters:
for 1D:

    rc = 0
    eps = 0
    size = 301
    dom = 2
    disp_max = 100

time to run < 10s

for 2D:

    rc = 0
    eps = 0
    dom = 2
    size = 201
    disp_max = 90

time to run: ~3 mins
To run faster, for simple testing, decrease size from 401 to a smaller (odd) number, e.g. 201.

### Figure 5
Produced by running the file named: 'galaxy cluster generation and lensing .py'. This image is produced in a single run of the code.

Note that most of the code for this is modularised.

The generation of galaxies occurs through a module I have written (in Project_completed.modules) called 'draw_pxiels', with a fucntion called: 'gal_image'.
The lensing occurs through a function I have written in file named 'lensing_function' in 'Project_completed.modules' with function called 'lens'.

Parameters:

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

### Figure 6
Produced by running file named: 'Jpg image lensing' from 'Project_completed\codes for tasks from sheet\advanced', produced in a single run of the code.
Again, the lensing is completed by the modularised fucntion (lens)

The image is supplied in the 'Project_completed' file, and holds no copyright, it is my own image of Messier 65 taken with a Messier Bresser telescope.

Parameters:

    rc = 0
    eps = 0
    dom = 2
    image path: 'Project_completed\\my image M65.jpg'
    image size (extracted, not input parameter) : 1121
time to run (from restarted kernel) ~ 0.3s

NB.

A simulation of the lensing object being moved onto the jpg image has also been produced and can be found in the same file, named 'jpg movie', simply needs to be run, nothing to set.


### Figure 7
Produced by running file named: 'ellipticity' from 'Project_completed\additional codes', produced in a single run of the code. The lines linking inset plots to their original positions have been input in image post processing. It is possible to add them in code, but it was omitted.
Again, the lensing is completed by the modularised fucntion (lens) and plotting a spherical source is done by a function 'draw_sphere' from file 'pix_draw' imported from 'Project_completed.modules.draw_pxiels'.

Parameters:

    rc = 0.2
    dom = 4
    size = 600
    size_obj = 30
    eps_N = 300
    eps tested in range (0, 1)
time to run: 

### Figure 8
TOP: Transit data with and without lensing, produced by file in 'additional codes \\ lesned 2 body'. Codes used to produce it:
'(star + planet) extracting ratio of radii' for fast plot and result
'(star + planet) lensed with animation' for result with animated lensed transit.

Animated transit runs with same (almost) parameters as not animated:

    size = 800   size=300 for  animated
    eps = 0
    rc = 0
    dom = 4
    t_max = 0.5 * year
    t_number = 300    t_number = 200 for animated
    For star:
        Mass=2e30, 
        size=40, 
        x=0, 
        y=0, 
        vx=0, 
        vy=0.
    For Planet:
        Mass=6e24,
        size=12,
        x=maxR,
        y=0,
        vx=0
        vy=-29800)

with defined constants:

    year = 3.156e7
    maxR = 1.496e11
    size_source = 4e11

Time to run not measured, no reason for aniamtion.

time to run with no animation ~ 30s.

NOTE: In animation, ~ 0.2yrs (animation time) pass before planet comes into view.
Figure includes a snapshow from simulation.


### Figure 9
Figure showing the extension of the radtio study to when both bodies move, and hence when luminosity of both changes. SHowing that it is still possible to extract the ratio, to within a small systematic error.

Parameters:

    size = 600
    eps = 0
    rc = 0.15
    dom = 6
    t_max = 0.6 * year
    t_number = 800
    Brighter star:

        Mass=2e30,
        size=60,
        x=-maxR/2,
        y=0,
        vx=0,
        vy=20000
    
    Dim star (called Planet in code, as it is dark):

        Mass=2e30,
        size=18,
        x=maxR/2,
        y=0,
        vx=0,
        vy=-20000


with constants:

    year = 3.156e7
    maxR = 1.49e11
    size_source = 2.5e11

time to run: ~ 30s