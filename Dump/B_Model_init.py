# CoordInit.py to initialize the BxBy array.

# Inputs: none
# Outputs: ByBxCat array


## imports
import matlab.engine

## start the MATLAB engine in the background
eng = matlab.engine.start_matlab()

# add the path for the MATLAB functions and all subfolers (s)
s = eng.genpath("./MATLAB")
eng.addpath(s, nargout=0)


## initialize all input parameters
dpMoment = -1.321000939300081e+06
amplify = 1
interpolFact = 70
absBound = 2

# convert surround range to matlab 1 x absbound*2 + 1 array
surroundRange = list(range(-absBound, absBound + 1))
surroundRange = list(map(int,surroundRange))
surroundRangeMATLAB = matlab.double(surroundRange)

# set up physically boundary size of grid which will influence
# the dipole model
Xstart = matlab.double(-0.4)
Xend = matlab.double(0.4)
Ystart = matlab.double(0)
Yend = matlab.double(0.4)

# define number of samples per axis on the model
n = 21


## Call MATLAB to create the dipole field model n x n x 2
ByBxCat = eng.DipoleMake(Xstart,Xend,Ystart,Yend,n,dpMoment,nargout = 1)



