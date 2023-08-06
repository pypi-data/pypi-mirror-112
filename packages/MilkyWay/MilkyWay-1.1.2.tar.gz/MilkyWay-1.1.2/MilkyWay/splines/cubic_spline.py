import sys
sys.path.append("..")

import numpy as np
from ..trajectory import Trajectory
from ..vector import Vector2D
from math import *
from ..waypoint import Waypoint2D as Waypoint
from matplotlib import pyplot as plt

class CubicSpline(Trajectory):
    '''
    CubicSpline
    ============

    Cubic spline parametric curve interpolation.
    Built in trajectory type.

    Implements the Trajectory class
    '''

    def __init__(self, *args, k: int = 1, points: int = 10, plan=True) -> None:
        """
        Description:
        ------------
            Changes the object trajectory starting and finising point

        Arguments:
        ----------
            *args- Takes 0 or 2 Trajectory arguments
            k:  Curvature (defaults to 1)
            points: Number of points to sample (defaults to 10)
            plan: If it should 'plan' the trajectory at the init (recommended to lower runtime load)

        Returns:
        --------
            Whether the points are valid

        Raises:
        -------
        ValueError
            If V1 and V2 are on the same x,y

        """

        super().__init__()

        # Conversion matrix (Ax = Y => x=A^-1 * Y) => A^-1
        self.conversion_matrix = self._get_conversion_matrix()

        self.waypoints = np.array([])
        self.coeffs = {}
        self.planned = False


        if len(args) != 2:
            print(self.__class__.__name__ + ' takes exactly 0 or 2 arguments')
            return

        V1, V2 = args

        # Init trajectory variables
        self.create_trajectory(V1, V2, k, points, plan=plan)

    def _get_conversion_matrix(self):
        return np.linalg.inv(np.array([[0, 0, 0, 1],
                                       [0, 0, 1, 0],
                                       [1, 1, 1, 1],
                                       [3, 2, 1, 0]]))

    def plan(self):
        # Calculate the coeffitients for the X polynom
        self.coeffs['x_coeffs'] = self.calc_coeffs(self.first_point.x,
                                    np.cos(
                                        radians(self.first_point.theta)) * self.k,
                                    self.last_point.x,
                                    np.cos(radians(self.last_point.theta)) * self.k)

        # Deriving the polynom
        self.coeffs['xd_coeffs'] = np.polyder(self.coeffs['x_coeffs'])
        self.coeffs['xdd_coeffs'] = np.polyder(self.coeffs['xd_coeffs'])

        # Calculate the coeffitients for the Y polynom
        self.coeffs['y_coeffs'] = self.calc_coeffs(self.first_point.y,
                                    np.sin(
                                        radians(self.first_point.theta)) * self.k,
                                    self.last_point.y,
                                    np.sin(radians(self.last_point.theta)) * self.k)
        # Deriving the polynom
        self.coeffs['yd_coeffs'] = np.polyder(self.coeffs['y_coeffs'])
        self.coeffs['ydd_coeffs'] = np.polyder(self.coeffs['yd_coeffs'])
        self.planned = True

    def get_linear_points(self, points=None) -> np.ndarray:
        """
        get_linear_points
        =================

        Description:
        ------------
            Creates a numpy array of Vector2D consists of linearly picked points

        Notes:
        ------
            Fast picking
            Samples may vari in length and and not have consistant distance

        Arguments:
        ----------
            amount_of_points: The amount of points to return

        Returns:
        --------
            Vector2D array

        rtype:
        ------
            np.ndarray
        """
        if points==None:
            points = self.points

        if not self.planned:
            self.plan()

        # Creating points to sample from
        s = np.linspace(0, 1, points)

        # Sampling every function
        self.x = np.polyval(self.coeffs['x_coeffs'], s)
        xd = np.polyval(self.coeffs['xd_coeffs'], s)
        xdd = np.polyval(self.coeffs['xdd_coeffs'], s)
        self.y = np.polyval(self.coeffs['y_coeffs'], s)
        yd = np.polyval(self.coeffs['yd_coeffs'], s)
        ydd = np.polyval(self.coeffs['ydd_coeffs'], s)

        # Calculating theta and the curvature
        self.curvature = np.abs(xd*ydd-yd*xdd) / (xd**2 + yd**2)**1.5
        self.theta = np.arctan2(yd, xd)

        # Generating a waypoint array
        self.waypoints = np.array([Waypoint(x, y, t, c) for x, y, t, c in zip(
            self.x, self.y, self.theta, self.curvature)])

        return self.waypoints

    def create_trajectory(self, first_point:Vector2D, last_point:Vector2D, k:float, points:int,plan=True) -> bool:
        """
        create_trajectory
        =================

        Description:
        ------------
            Changes the object trajectory starting and finising point

        Arguments:
        ----------
            V1: The first point of the trajectory
            V2: The last point of the trajectory
            k:  Curvature (defaults to 1)
            number_of_point: The number of points to sample

        Returns:
        --------
            Whether the points are valid

        Raises:
        -------
        ValueError
            If V1 and V2 are on the same x,y
            Ilegal number of points
        """


        # Checking that its not the same point
        if first_point.same_point_as(last_point):
            self.possible_trajectory = False
            raise ValueError('Picked 2 points in the same place')

        if points.__class__.__name__ != 'int' or points < 2:
            raise ValueError('Invalid number of points')

        # Not the same point - can create a trajectory
        self.possible_trajectory = True

        # Set instance variables
        self.first_point = first_point
        self.last_point = last_point
        self.points = points
        self.k = k

        self.waypoints = np.array([])

        if plan:
            self.plan()

    def _get_condition_vector(self, pos_begin:float, angle_begin:float, pos_end:float, angle_end:float) -> np.ndarray:
        return np.array([pos_begin, angle_begin, pos_end, angle_end])

    def calc_coeffs(self, pos_begin:float, angle_begin:float, pos_end:float, angle_end:float) -> np.ndarray:
        """
        calc_coeffs
        =================

        Description:
        ------------
            Constructs the desired polynom

        Arguments:
        ----------
            pos_begin: First point
            angle_begin: First angle
            pos_end: First point
            angle_end: First angle

        Returns:
        --------
            The coefficients of the desired polynom

        """

        condition_vector = self._get_condition_vector(pos_begin, angle_begin, pos_end, angle_end)

        # Apply conversion matrix
        desired_coeffs = self.conversion_matrix.dot(condition_vector)
        
        return desired_coeffs   

    def get_equidistant_points(self, amount_of_points: int) -> np.ndarray:
        """
        get_equidistant_points
        =================

        Description:
        ------------
            Creates a numpy array of Vector2D consists of equidistant points

        Notes:
        ------
            Require preprocessing
            A bit slower than the linearly picked

        Arguments:
        ----------
            amount_of_points: The amount of points to return

        Returns:
        --------
            Vector2D array

        rtype:
        ------
            np.ndarray
        """
        raise NotImplementedError

    def sample(self,type='linear'):
        if self.planned:
            self.__getattribute__(type)()
