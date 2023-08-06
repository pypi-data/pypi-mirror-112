import sys
sys.path.append("..")
from ..trajectory import Trajectory
import numpy as np
from math import radians
from ..waypoint import Waypoint, Waypoint2D
from matplotlib import pyplot as plt

class Spline(Trajectory):
    '''
    Spline
    =================

    Closer to the 'Path' class
    We recommend using Spline rather than the 'Path' class
    '''

    waypoints = []
    x = np.array([])
    y = np.array([])
    theta = np.array([])
    curvature = np.array([])
    coeffs = {}

    def __init__(self, *args, plan=True, sample='linear', default_no_points=10) -> None:
        '''
        args: More than 1 Waypoint
        '''
        if len(args) < 2:
            print('Spline needs more than 1 Waypoints')
            return
        
        self.checkpoints = list(args) # Needs a better name
        self.default_no_points = default_no_points

        if plan:
            self.plan_all(sample=sample)
            
        self.planned = plan


    def reset(self):
        self.waypoints = []
        self.x = np.array([])
        self.y = np.array([])
        self.theta = np.array([])
        self.curvature = np.array([])
        self.coeffs = {}

    def plan_all(self, sample='linear'):
        '''
        Planning the trajectory for every pair of points
        ---------
        '''
        self.reset()
        self.__recursive_plan(0)
        self.reset()
        for i in range(len(self.checkpoints)-1):
            # Planning
            self.__plan(self.checkpoints[i], self.checkpoints[i+1])

            # Sampling
            self.__sample_current(self.checkpoints[i].points, sample=sample)


    def __recursive_plan(self, i):
        '''
        Ok so turns out this isn't broken, I have no idea why it's important but never touch this function.
        It somehow fixes the broken angles at non-specified waypoint.
        '''
        if i == len(self.checkpoints)-2:
            # Plan
            self.__plan(self.checkpoints[i], self.checkpoints[i+1])

            # Sampling
            self.__sample_current(2)

            # Encase point doesnt have an angle (to be consistant and not have "breaking" lines)
            self.checkpoints[i+1].fix_angle(self.theta[-1])

            return

        elif self.checkpoints[i+1].angle == None:
            if self.checkpoints[i+2].angle == None:
                self.__recursive_plan(i+1)

            # Plan
            self.__plan(self.checkpoints[i], self.checkpoints[i+1])

            # Sampling
            self.__sample_current(2)

            # Encase point doesnt have an angle (to be consistant and not have "breaking" lines)
            self.checkpoints[i+1].fix_angle(self.theta[-1])

        self.__recursive_plan(i+1)
        

    def __plan(self, first_point: Waypoint, last_point: Waypoint):
        # Set the conversion matrix
        self.__set_conversion_matrix(first_point, last_point)

        # Get condition vector
        x_condition_vec, y_condition_vec = first_point.get_condition_vector(last_point)

        # Calculate the coeffitients for the X polynom
        self.coeffs['x_coeffs']  = self.calc_coeffs(x_condition_vec)

        # Deriving the polynom
        self.coeffs['xd_coeffs'] = np.polyder(self.coeffs['x_coeffs'])
        self.coeffs['xdd_coeffs'] = np.polyder(self.coeffs['xd_coeffs'])

        # Calculate the coeffitients for the Y polynom
        self.coeffs['y_coeffs'] = self.calc_coeffs(y_condition_vec)
        # Deriving the polynom
        self.coeffs['yd_coeffs'] = np.polyder(self.coeffs['y_coeffs'])
        self.coeffs['ydd_coeffs'] = np.polyder(self.coeffs['yd_coeffs'])

    def __sample_current(self, points, sample='linear'):
        if points==None:
            points = self.default_no_points


        # Creating points to sample from
        s = self.get_s(points, sample=sample)

        # Sampling every function
        self.x = np.append(self.x, np.polyval(self.coeffs['x_coeffs'], s))
        xd = np.polyval(self.coeffs['xd_coeffs'], s)
        xdd = np.polyval(self.coeffs['xdd_coeffs'], s)
        self.y = np.append(self.y, np.polyval(self.coeffs['y_coeffs'], s))
        yd = np.polyval(self.coeffs['yd_coeffs'], s)
        ydd = np.polyval(self.coeffs['ydd_coeffs'], s)

        # Calculating theta and the curvature
        self.curvature = np.append(self.curvature, np.abs(xd*ydd-yd*xdd) / (xd**2 + yd**2)**1.5)
        self.theta = np.append(self.theta, np.arctan2(yd, xd))

        # Generating a waypoint array
        self.waypoints.extend([Waypoint2D(x, y, t, c) for x, y, t, c in zip(
            self.x, self.y, self.theta, self.curvature)])


    def _get_condition_vector(self, first_point: Waypoint, last_point: Waypoint) -> np.ndarray:
        # Setting second derivatives to 0
        return first_point._get_condition_vector(last_point)

    def __set_conversion_matrix(self, first_point: Waypoint, last_point: Waypoint):
        # Returns the convarsion matrix
        self.conversion_matrix = first_point.get_conversion_matrix(last_point)

    def calc_coeffs(self, condition_vector) -> np.ndarray:
        """
        calc_coeffs
        =================

        Description:
        ------------
            Constructs the desired polynom

        Returns:
        --------
            The coefficients of the desired polynom

        """

        # Apply conversion matrix
        desired_coeffs = self.conversion_matrix.dot(condition_vector)

        return desired_coeffs

    def get_s(self, points,sample='linear'):
        '''
        get_s
        =====

        Returning the sample points
        ---------------
        '''

        if sample == 'linear':
            return  np.linspace(0, 1, points)

    def get_linear_points(self) -> list:
        self.plan_all()
        return [(wp.get_data()) for wp in self.waypoints]

    def get_equidistant_points(self, amount_of_points: int) -> np.ndarray:
        raise NotImplementedError()

    def plot(self, show=True, scatter=True):
        ''' Plotting the trajectory '''

        if self.planned:
            if scatter:
                special_xs, special_ys = [point.x for point in self.checkpoints], [point.y for point in self.checkpoints]
                plt.scatter(special_xs, special_ys)
            super().plot(show=show)
