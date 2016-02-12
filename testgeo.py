import unittest
from geothings import Point, Line, Chain, FourChain, Polygon
#from random import random


class TestGeothings(unittest.TestCase):
    def testLineThroughPoint(self):
        p = Point(-1, -1)
        a = Point(-2, 0)
        b = Point(-1, 0)
        c = Point(0, -1)

        # A line with slope = 45 degrees
        self.assertTrue(p.line_through_point(a) == Line(p,a))
        self.assertTrue(p.line_through_point(a) == Line(2, 2, -4))

        # A vertical line
        self.assertTrue(p.line_through_point(b) == Line(p, b))
        self.assertTrue(p.line_through_point(b) == Line(1, 0, -1))

        # A horizontal line
        self.assertTrue(p.line_through_point(c) == Line(p, c))
        self.assertTrue(p.line_through_point(c) == Line(0, 1, -1))

    def testOnLine(self):
        L = Line(-2, 1, 3)
        a = Point(1, 5)
        b = Point(-1, -2)
        self.assertTrue(a.on_line(L))
        self.assertFalse(b.on_line(L))

    def testMirrorPoint(self):
        L1 = Line(Point(2, 0), Point(0, 2))
        # A vertical line at x=1
        L2 = Line(1, 0, 1)
        p1 = Point(0, 0)
        p2 = Point(0, 2)
        p = Point(2, 2)

        self.assertTrue(p.mirror_point(L1) == p1)
        self.assertTrue(p.mirror_point(L2) == p2)


if __name__ == '__main__':
    unittest.main()
