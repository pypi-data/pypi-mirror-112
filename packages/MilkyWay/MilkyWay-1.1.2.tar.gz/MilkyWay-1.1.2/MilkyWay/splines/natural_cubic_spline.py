import sys
sys.path.append("..")

import numpy as np
from ..splines import CubicSpline

class NaturalCubicSpline(CubicSpline):
    '''
    NaturalCubicSpline
    =================

    Same as a cubic spline but with second derivatives set to 0 at edges
    '''
    def __init__(self, *args, k: int = 1, points: int = 10, plan=True) -> None:
        super(NaturalCubicSpline, self).__init__(*args, k=k, points=points, plan=plan)

    def _get_condition_vector(self, pos_begin: float, angle_begin: float, pos_end: float, angle_end: float) -> np.ndarray:
        # Setting second derivatives to 0
        return np.array([pos_begin, angle_begin, pos_end, angle_end, 0 ,0])

    def _get_conversion_matrix(self):
        return np.linalg.inv(np.array([[0, 0, 0, 0, 0, 1],
                                       [0, 0, 0, 0, 1, 0],
                                       [1, 1, 1, 1, 1, 1],
                                       [5, 4, 3, 2, 1, 0],
                                       [20, 12, 6, 2, 0, 0],
                                       [0, 0, 0, 1, 0, 0]]))
