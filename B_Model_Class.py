# Create the class to organize the Dipole model function calls

# imports
import matlab.engine
from math import ceil

class BModelClass:
    def  __init__(self):
        ## Start the MATLAB engine
        self.eng = matlab.engine.start_matlab()

        # Add the MATLAB path for functions
        s = self.eng.genpath("./MATLAB")
        self.eng.addpath(s, nargout=0)

        # Initialize parameters
        self.amplify = 10 # this has not been shown to have appreciable effect on accuracy, but it exists for MATLAB consistency
        #self.interpol_fact = 70 # this is not relevant except for preset data imports that require interpolation
        self.abs_bound = 7 # change this factor to increase the search range around every next point
        self.dp_moment = -1.321000939300081e+06 * self.amplify

        # Initialize the surround range as a MATLAB array
        self.surround_range = list(range(-self.abs_bound, self.abs_bound + 1))
        self.surround_range = matlab.double(self.surround_range)

        # Set up physically boundary size of grid
        self.grid_meter_range = 0.2
        self.X_start = matlab.double(-self.grid_meter_range)
        self.X_end = matlab.double(self.grid_meter_range)
        self.Y_start = matlab.double(0)
        self.Y_end = matlab.double(self.grid_meter_range)

        # Define number of samples per axis on the model
        self.samples_per_axis = 401

        # Initialize non-init vars to None
        (self.BxByCat,
         self.initial_index_x,
         self.initial_index_y,
         self.next_index_x,
         self.next_index_y
         ) = (matlab.double(ceil(self.samples_per_axis/2)),
              matlab.double(1),
              None, None, None)

        # start the start flag on true to note that no initial coordinate has been found, yet
        # you should also do this in your main script for clarity, but it's here in case
        # you forget
        self.start_flag = True

    def create_dipole_model(self):
        # BxByCat is the model for all the vectors, and it includes X
        # Y, U and V, where U and V are the vectors starting at X and Y
        # in the model magnetic field for a dipole
        self.BxByCat = self.eng.DipoleMake(
            self.X_start, self.X_end, self.Y_start, self.Y_end,
            self.samples_per_axis, self.dp_moment,
            nargout = 1
        )

        # Always convert your python to matlab numbers
        self.BxByCat = matlab.double(self.BxByCat)

    def get_initial_indexes(self, initial_bx, initial_by):
        # Return the initial x and y coordinates
        # Example (initial_bx, initial_by):
        # (7.921874243730248, -1.006199903942106e+03)
        index_x, index_y = self.eng.MagIndInit(
            self.BxByCat,
            matlab.double(initial_bx),
            matlab.double(initial_by),
            nargout=2)
        self.initial_index_x = matlab.double(index_x)
        self.initial_index_y = matlab.double(index_y)

    def get_next_index(self, next_bx, next_by):
        try:
            # Get the next x and y coordinates based on new magnetometer information
            # always remember to feed the image your MATLAB double conversions
            next_bx = matlab.double(next_bx)
            next_by = matlab.double(next_by)
            self.next_index_x, self.next_index_y = self.eng.MagIndNext3(
                self.BxByCat,
                self.initial_index_x, self.initial_index_y,
                next_bx, next_by,
                self.surround_range,
                nargout = 2
            )
            # Set the next first index to be the next index
            # this means it's automatically loaded for the next incoming next_bx, next_by
            self.initial_index_x = self.next_index_x
            self.initial_index_y = self.next_index_y

        except Exception as e:
            print(f"Error in get_next_index: {e}")

    def close_engine(self):
        # Shut down the MATLAB engine
        self.eng.quit()
