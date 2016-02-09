from __future__ import division
import math
import sys


class Point(object):
    """Euclid: A point is that which has no part."""
    def __init__(self, x=0, y=0):
        self.x = x
        self.y = y

    def __str__(self):
        return "(" + str(self.x) + ", " + str(self.y) + ")"

    def __eq__(self, that):
        return self.x == that.x and self.y == that.y

    def __hash__(self):
        return hash((self.x, self.y))

    def line_through_point(self, p):
	"""Returns the line through two points."""
        # Is a vertical line
        if (p.x == self.x):
            return Line(1, 0, p.x)
        else:
            a = self.y - p.y
            b = p.x - self.x
            c = self.x*(self.y - p.y) + self.y*(p.x - self.x)
            return Line(a, b, c)

    def euclidean_distance(self, p):
        try:
            return math.sqrt((self.x - p.x) ** 2 + (self.y - p.y) ** 2)
        except:
            print "Unexpected Error:", sys.exc_info()
            raise

    def on_line(self, l):
    	"""Returns true if the given point is on line l"""
        try:
            return ((l.a * self.x) + (l.b * self.y) == l.c)
        except:
            print "Unexpected Error:", sys.exc_info()
            raise

    def mirror_point(self, p1=None, p2=None):
   	"""Returns the mirror reflection of self across a line p1,
    	    or a line through p1 and p2."""
        L = p1 if (p2 is None) else Line(p1, p2)
        perpL = L.perpendicular_through_point(self)
        p = L.point_of_intersection(perpL)
        return Point(2*p.x - self.x, 2*p.y - self.y)

    def move(self,x,y):
	"""Moves the point to the new (x,y) position."""
	self.x = x
	self.y = y



class Line(object):
    """Euclid: A line is breadthless length.""" 
    def __init__(self, a=None, b=None, c=None):
	"""A line is defined by two points and described by the equation ax + by = c 

	   You can create one by passing the values a, b, c of the equation 
	   OR by passing it two points.
	"""
        # if line is defined by two points a and b
        if (c is None):
            # check for a vertical line
            if (a.x == b.x):
                self.a = 1
                self.b = 0
                self.c = a.x
            else:
                self.a = b.y - a.y
                self.b = a.x - b.x
                self.c = (a.x-b.x)*a.y - (a.y-b.y)*a.x
        else:
            # Line is in format ax + by = c
            self.a = a
            self.b = b
            self.c = c

        try:
            if (not self.is_well_defined):
                raise ValueError(
                    "Line is not well defined! \n" +
                    "a and b cannot both be zero in L: ax + by = c")
        except ValueError as e:
            print e

    def __str__(self):
        return "x = " + str(self.c) if self.is_vertical \
            else "y = " + str(self.slope) + "x + " + str(self.intercept)

    def __eq__(self, that):
        if (self.is_vertical and that.is_vertical):
            return self.c == that.c
        else:
            self.slope == that.slope and self.intercept == that.intercept

    def __hash__(self):
        return hash((self.a, self.b, self.c))

    @property
    def is_well_defined(self):
        return (self.a and self.a != 0) or (self.b and self.b != 0)

    @property
    def is_horizontal(self):
        return True if self.a == 0 else False

    @property
    def is_vertical(self):
        return True if self.b == 0 else False

    @property
    def slope(self):
        return float('inf') if (self.is_vertical) else ((-1) * self.a/self.b)

    @property
    def intercept(self):
        return float('inf') if self.is_vertical else self.c/self.b

    def is_perpendicular(self, l):
        return True if (self.slope * l.slope == -1) else False

    def is_parallel(self, l):
        return True if (self.slope == l.slope) else False

    def is_overlapping(self, l):
    	"""Returns true if the two lines are the same."""
        return True if (self.slope == l.slope) and \
            (self.intercept == l.intercept) \
            else False

    def parallel_through_point(self, p):
    	"""Computes the equation of the line through p that is
    	   parallel to self: L ': ax + by = a*p.x + b*p.y."""
        return Line(1, 0, p.x) if self.is_vertical \
            else Line(self.a, self.b, (self.a * p.x) + (self.b * p.y))

    def perpendicular_through_point(self, p):
    	"""Computes the equation of the line through p that is
    	   perpendicular to  self: L': -abx + ay = -b*p.x + a*p.y."""
        if self.is_horizontal:
            return Line(1, 0, p.x)
        else:
            a = -1 * self.b
            b = self.a
            c = (self.a * p.y) - (self.b * p.x)
            return Line(a, b, c)

    def point_of_intersection(self, that):
    	"""Returns the intersection point with another line."""
        # if lines are parallel return None
        if (self.is_parallel(that)):
            return None
        else:
            if (self.is_vertical):
                return Point(self.c, that.c/that.b - that.a/that.b*self.c)

            if (that.is_vertical):
                return Point(that.c, self.c/self.b - self.a/self.b*that.c)

            x = (that.c/that.b - self.c/self.b) / \
                (that.a/that.b - self.a/self.b)
            y = that.c/that.b - that.a/that.b*x
            return Point(x, y)


class Chain(object):
    def __init__(self, points):
	"""An open polygonal chain is formed by an ordered list of points CW."""
        self.points = points
        self.n = len(points)

    def __hash__(self):
        return hash(self.points)

    def __str__(self):
        point_str = ""
        for point in self.points:
            if point_str:
                point_str += ", "
            point_str += str(point)
        return point_str

    def next(self,current_point):
	"""Returns the next point (in CW direction) along the chain.
	   If the current point is the last point or does not exist, returns null.
	"""
	if not current_point in self.points:
	    return None
	else: 
	    current_index = self.points.index(current_point)

	# if current point is the last in the list return None
	return None if current_index == self.n-1 else self.points[current_index+1]	


    def previous(self,current_point):
	"""Returns the previous point (in CW direction) along the chain.
	   If the current point is the first point or does not exist, returns null.
	"""
	if not current_point in self.points:
	    return None
	else: 
	    current_index = self.points.index(current_point)
	# if current point is the first in the list return None
	return None if current_index == 0 else self.points[current_index-1]	


class Polygon(Chain):
    """"A polygon is a closed chain."""
    def __init__(self, points):
	Chain.__init__(self, points)

