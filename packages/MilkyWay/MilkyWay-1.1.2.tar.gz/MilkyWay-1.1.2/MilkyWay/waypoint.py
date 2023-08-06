from .vector import Vector2D
import numpy as np
from math import radians

class Waypoint2D(Vector2D):
    '''
    Waypoint2D
    ========
    Implements a waypoint (x,y,theta,curvature)
    
    #Todo:
        Add 'get_angular'- good question
    '''

    def __init__(self, x:float, y:float, theta:float, curvature:float) -> None:
        super().__init__(x, y, theta)
        self.curvature = curvature

    def get_data(self):
        return [self.x, self.y, self.theta, self.curvature]

    def __repr__(self) -> str:
        return 'x: {}, y: {}, theta: {}, curvature: {}'.format(self.x, self.y, self.theta, self.curvature)
    
class Waypoint(Vector2D):
    '''
    A Waypoint that helps constructing the Spline
    '''

    def __init__(self, x:float, y:float, angle=None, k=1, k_start=None, k_end=None, points=10, der2=None) -> None:
        self.x = x
        self.y = y
        self.k_start = k
        self.k_end = k

        if k_start != None:
            self.k_start = k_start
        if k_end != None:
            self.k_end = k_end


        self.angle = angle
        self.points = points
        self.der2 = der2

        # 2 (x+y) + 1 if angle + 1 if der2
        self.amount_of_conditions = 1 + int(angle != None) + int(der2 != None)


    def get_condition_vector(self, last_point):
        ''' Returns the conditions that need to be met - vectorized '''

        # Declare x and y condition vector
        condition_vector_y = np.array([
            self.y,
            last_point.y
        ])

        condition_vector_x = np.array([
            self.x,
            last_point.x
        ])
        
        # Add angles
        if self.angle != None:
            condition_vector_x = np.append(condition_vector_x, np.cos(radians(self.angle)) * self.k_start)
            condition_vector_y = np.append(condition_vector_y, np.sin(radians(self.angle)) * self.k_start)

        if last_point.angle != None:
            condition_vector_x = np.append(condition_vector_x, np.cos(radians(last_point.angle)) * last_point.k_end)
            condition_vector_y = np.append(condition_vector_y, np.sin(radians(last_point.angle)) * last_point.k_end)


        # Add second derivatives
        if self.der2 != None:
            condition_vector_x = np.append(condition_vector_x, self.der2)
            condition_vector_y = np.append(condition_vector_y, self.der2)

        if last_point.der2 != None:
            condition_vector_x = np.append(condition_vector_x, last_point.der2)
            condition_vector_y = np.append(condition_vector_y, last_point.der2)

        return condition_vector_x, condition_vector_y

    def polyval(self, poly, val):
        """
        Calculating the 'per element' polynom value
        ---------------------
        Example:
        -------
            >>> poly = [1, 2, 3] # = x^2 + 2x + 3
            >>> polyval(poly, 2) # = [4, 2, 3] 
        """
        values = np.array([])
        
        for i, element in enumerate(poly):
            values = np.append(values, element * val**(len(poly)-i-1))

        return values

    def zero_fill(self, arr, length):
        '''
        Fills with zeros from right
        ---------
        Example:
        -------
            >>> arr = [1, 2, 3, 0]
            >>> zero_fill(arr, 5) # = [1, 2 ,3 ,0, 0]
        '''
        assert length >= len(arr), 'The fill length should be bigger that the array length'

        zeros = np.zeros(length)
        zeros[:len(arr)] = arr
        return zeros

    def get_conversion_matrix(self, last_point):
        '''
        Calculating the conversion matrix for solving the linear equation
        '''

        total_conditions = self.amount_of_conditions + last_point.amount_of_conditions
        conversion_matrix = np.empty((total_conditions,total_conditions), dtype=np.int8)

        i = 0

        # Adding first position condition
        start_location_vec = np.ones(total_conditions)
        start_location_vec = self.polyval(start_location_vec, 0)
        conversion_matrix[i] = start_location_vec  # Appending the array


        # Adding last position condodion
        last_location_vec = np.ones(total_conditions)
        last_location_vec = self.polyval(last_location_vec, 1)

        i += 1
        # Appending the array
        conversion_matrix[i] = last_location_vec


        # Adding starting angle requirement
        if hasattr(self, 'angle') and getattr(self, 'angle') != None:
            # Create vector
            start_angle_vec = np.polyder(np.ones(total_conditions))
            start_angle_vec = self.zero_fill(self.polyval(start_angle_vec, 0), total_conditions)
            i+=1

            conversion_matrix[i] = start_angle_vec

        # Adding last angle requirement
        if hasattr(last_point, 'angle') and getattr(last_point, 'angle') != None:
            # Create vector
            last_angle_vec = np.polyder(np.ones(total_conditions))
            last_angle_vec = self.zero_fill(self.polyval(last_angle_vec, 1), total_conditions)
            i+=1
            
            conversion_matrix[i] = last_angle_vec

        # Adding starting second derivative requirement
        if hasattr(self, 'der2') and getattr(self, 'der2') != None:
            # Create vector
            start_secder_vec = np.polyder(np.polyder(np.ones(total_conditions)))
            start_secder_vec = self.zero_fill(
                self.polyval(start_secder_vec, 0), total_conditions)
            i+=1

            conversion_matrix[i] = start_secder_vec

        # Adding last second derivative requirement
        if hasattr(last_point, 'der2') and getattr(last_point, 'der2') != None:
            # Create vector
            last_secder_vec = np.polyder(np.polyder(np.ones(total_conditions)))
            last_secder_vec = self.zero_fill(
                self.polyval(last_secder_vec, 1), total_conditions)
            i+=1

            conversion_matrix[i] = last_secder_vec


        return np.linalg.inv(conversion_matrix)

    def fix_angle(self, angle):
        '''

        fix_angle
        =========
        Sometimes, when there's a pure point(x,y) the generated trajectory is not stable/breaks
        because of inconsistency in the angles

        This function just sets the angle so theres no line breakign.
        '''
        if self.angle == None:
            self.angle = angle
            self.amount_of_conditions += 1

    def __repr__(self) -> str:
        return f'x: {self.x}, y: {self.y}, angle: {self.angle}'
