# # A simple script to test out MATLAB Engine
#
# # imports
# import matlab.engine
#
# # start the MATLAB engine in the background
# eng = matlab.engine.start_matlab()
#
# # add the path for the MATLAB functions and all subfolers (s)
# s = eng.genpath("./MATLAB")
# eng.addpath(s, nargout=0)
#
# eng.DipoleModel(nargout=0)
#
# # WORKS! But no plotting, that's okay I will now make a function to take in magnetometer reading
# # and add to python array each next path coordinate
#

# Testing the class system

from B_Model_Class import BModelClass

B_model = BModelClass()
B_model.create_dipole_model()

init_bx = -2117
    #0.921874243730248
init_by = -26064
    #-1.006199903942106e+03

B_model.get_initial_indexes(init_bx, init_by)

next_bx = 0
next_by = -1.00e+02

B_model.get_next_index(
    next_bx, next_by
)

print(B_model.next_index_x, B_model.next_index_y)

