import unittest
from geothings import Point, Line, Chain, Polygon
from random import random, randint


class TestGeothings(unittest.TestCase):
    def testLineThroughPoint(self):
        p = Point(-1, -1)
        a = Point(-2, 0)
        b = Point(-1, 0)
        c = Point(0, -1)

        # A line with slope = 45 degrees
        self.assertTrue(p.line_through_point(a) == Line(p, a))
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

        self.assertEqual(p.mirror_point(L1), p1)
        self.assertEqual(p.mirror_point(L2), p2)

    def testLineProps(self):
        L1 = Line(Point(0, 0), Point(1, 1))
        L2 = Line(Point(-1, -3), Point(6, 2))
        Lo = Line(Point(2, 2), Point(7, 7))
        Lp = Line(Point(0, -1), Point(1, 0))
        Lr = Line(Point(2, 0), Point(0, 2))
        Lv = Line(Point(1, 2), Point(1, 4))
        Lh = Line(Point(3, 5), Point(-4, 5))

        self.assertFalse(L1.is_horizontal)
        self.assertFalse(L1.is_vertical)
        self.assertTrue(Lv.is_vertical)
        self.assertTrue(Lh.is_horizontal)

        self.assertEqual(Lh.slope, 0)
        self.assertEqual(Lh.intercept, 5)
        self.assertEqual(Lv.slope, float('inf'))
        self.assertEqual(Lv.intercept, 1)

        self.assertEqual(L1.slope, 1)
        self.assertEqual(L1.intercept, 0)

        self.assertFalse(L1.is_overlapping(L2))
        self.assertTrue(L1.is_overlapping(Lo))

        self.assertFalse(L1.is_perpendicular(L2))
        self.assertTrue(L1.is_perpendicular(Lr))

        self.assertFalse(L1.is_parallel(L2))
        self.assertTrue(L1.is_parallel(Lp))

    def testParallelThroughPoint(self):
        L1 = Line(Point(0, 0), Point(1, 1))
        Lp = Line(Point(0, -1), Point(1, 0))
        p = Point(2, 1)
        self.assertEqual(L1.parallel_through_point(p), Lp)

    def testPerpendicularThroughPoint(self):
        L1 = Line(Point(0, 0), Point(1, 1))
        Lr = Line(Point(2, 0), Point(0, 2))
        p = Point(1, 1)
        self.assertEqual(L1.perpendicular_through_point(p), Lr)

    def testPointOfIntersection(self):
        L1 = Line(Point(0, 0), Point(1, 1))
        L2 = Line(-2, 1, 3)
        p = Point(-3, -3)
        self.assertEqual(L1.point_of_intersection(L2), p)

    def testChainNextPrev(self):
        n = 10
        points = [Point(random() * n, random() * n) for i in range(n)]
        C = Chain(points)
        p1 = points[0]
        pn = points[n-1]
        p6 = points[6]

        self.assertEqual(C.previous(p1), None)
        self.assertEqual(C.next(pn), None)
        self.assertEqual(C.previous(p6), points[5])
        self.assertEqual(C.next(p6), points[7])

    def testPolygonEq(self):
        n = 10
        r = randint(1, n)
        points1 = [Point(random() * n, random() * n) for i in range(n)]
        points2 = [points1[i % n] for i in range(r, n + r)]
        P1 = Polygon(points1)
        P2 = Polygon(points2)
        self.assertEqual(P1, P2)

    def testPolygonNextPrev(self):
        n = 10
        points = [Point(random() * n, random() * n) for i in range(n)]
        P = Polygon(points)
        p1 = points[0]
        pn = points[n-1]
        p6 = points[6]

        self.assertEqual(P.previous(p1), pn)
        self.assertEqual(P.next(pn), p1)
        self.assertEqual(P.previous(p6), points[5])
        self.assertEqual(P.next(p6), points[7])


if __name__ == '__main__':
    unittest.main()
