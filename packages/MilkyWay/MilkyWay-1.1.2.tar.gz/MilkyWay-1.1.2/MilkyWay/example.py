from milkyway.waypoint import Waypoint
from milkyway.splines import *

def test():
	# Creating the spline
	spline = Spline(Waypoint(0, 0, angle=90, points=100),
	                        Waypoint(1, 1, angle=90, der2=0,k=2, points=100), Waypoint(2, 0, angle=0))
	
	# Plotting the spline
	spline.plot()
	
	# Another example
	a = Waypoint(0, 0, angle=90, points=100, k=1)
	mid1 = Waypoint(0.7, 0.8, points=100, k_start=0.6)
	b = Waypoint(1, 1, points=100, k_end=0.6)
	mid2 = Waypoint(1.5, 1, points=100, der2=0)
	c = Waypoint(2, 0, angle=0, k=2)


	spline = Spline(a, mid1, b, mid2, c)

	spline.plot(scatter=True)
