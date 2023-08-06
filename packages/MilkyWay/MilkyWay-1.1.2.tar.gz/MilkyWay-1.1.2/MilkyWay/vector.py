'''
Implements vectors

Author: Hali Lev Ari
Version: 1.0
'''
from math import sqrt

class Point2D:
    '''
    Implements a 2D point (x, y)
    '''
    def __init__(self, x:float, y:float) -> None:
        self.x = x
        self.y = y

    def get_distance(self, other):
        ''' 
        get_distance
        ============
        Returns the euclidean distance between this waypoint and another
        -----------------
        '''
        return sqrt((self.x - other.x)**2 + (self.y - other.y)**2)

    def get_point(self):
        return self.x, self.y

    def same_point_as(self, other):
        ''' Checks if the other point has the same x and y '''
        return self.x == other.x and self.y == other.y


class Vector2D(Point2D):
    """
    Vector2D
    ========

    Description:
    ------------
        Implements a generic 2D vector

    ToDo:
    -----
        Check if it needs genertic vector operations (addition, multiplication, ETC....)

    Since:
    -----
        Version: 1.0
    """

    def __init__(self, x:float, y:float, theta:float) -> None:
        '''
        Init
        ====

        Arguments:
        ----------

            x: x coordinate
            y: y coordinate
            theta: The angle of the vector
        '''
        # Initilize the variables
        super().__init__(x, y)
        self.theta = theta
