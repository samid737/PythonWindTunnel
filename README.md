# Description

PythonWindTunnel is a 2D wind tunnel simulation model.

This program visualizes a 2D steady flow around an airfoil using Pygame.The Flow.py script computes the flow field using the vortex panel method. The source code for Flow.py is mainly from the Aerodynamics course lectured by Prof.Lorena A.Barba:

https://github.com/barbagroup/AeroPython

The airfoil, angle of attack and flow accuracy are parameters that can be adjusted if desired\n(increasing doubles the grid). After changing the parameters click the Recompute flow button to recompute. \n This might take up to 20 seconds depending on the desired accuracy and your computer.You can browse through some of the airfoils I have added to the program,but you can always add more .dat files.Please note that each .dat file must only contain coordinates in Selig format(see available .dat files as a reference) and datapoints must be seperated by tabs.

* If you have any questions or need help with installing/setting up the program (its tedious), you can always contact me and I will try to help you out:
  * D.sami-1@student.tudelft.nl

# Requirements:

This program is written using **Python 2.7**
The program requires the following libraries to work properly:

* PIL
* Numpy
* Scipy
* matplotlib

* PGU
* Pygame

The first part should be included in a standard python (x,y) distribution, found here;

https://python-xy.github.io/downloads.html

The other two are available here:

PGU:

http://pygame.org/project-PGU+-+Phil's+pyGame+Utilities-108-.html

Pygame:

http://www.pygame.org/download.shtml

They are also added as zip files in the repo. the pgu.zip should be extracted to the same directory.

# Usage

To run the program, run GUI.py from a python console (or python GUI.py from terminal / cmd). 
If there are import errors, try copying the entire project folder into the default work directory (C:\Python27\ it should be).
If again there are import errors, try running from an editor.

the following settings can be adjusted during simulation,but requires the user to click RECOMPUTE:

* angle of attack
* accuracy
* airfoil

Afterwards the program will output a streamplot, a pressure plot and the simulation.

the following can be adjusted freely by the user without recomputing:

* number of particles
* simulation speed



# Known issues/points of improvements:

The program should be stable in current state, with current calibration on parameters, but some remarks/improvements that can be made:

* the particles are a bit offset near the surface of the airfoil.
* Changing the ratio between the Nx and Ny, (which is 3:1 currently), might crash the program.
* Making the accuracy higher currently does not really have any significant benefit currently. The current accuracy setting is either low(30x10) or high(60x20) grid.
Any above resulted in innacurate flow.
* increasing the N, number of panels, might not work(some values will give integration errors and it will not plot the airfoil properly).
* increasing the current limit amount of particles (19). the lookup of the associated grid index in CollisionDetect() fails in some way.
* Program runs slow in Top secret Wind tunnel mode. I believe the blitting may be an issue, but i am not sure.

