from coordinate_geometry.point import point
from coordinate_geometry.equations import *


class Triangle:
    def __init__(self, A: point, B: point, C: point):
        self.A = A
        self.B = B
        self.C = C
        self.a = B.distance(C)
        self.b = A.distance(C)
        self.c = A.distance(B)

    def area(self):
        area = 0.5 * abs((self.A.x * (self.B.y - self.C.y)) + (self.B.x * (self.C.y - self.A.y)) + (
                self.C.x * (self.A.y - self.B.y)))
        return round(area, 5)

    def centroid(self):
        x = round((self.A.x + self.B.x + self.C.x) / 3.0, 7)
        y = round((self.A.y + self.B.y + self.C.y) / 3.0, 7)
        return point(x, y)

    def incenter(self):
        # a=B.distance(C)
        # b=self.distance(C)
        # c=self.distance(B)
        if self.a == 0 or self.b == 0 or self.c == 0:
            sys.stderr.write('Can not find the in_center of a line\n')
            exit(1)
        Ix = round((self.a * self.A.x + self.b * self.B.x + self.c * self.C.x) / (self.a + self.b + self.c) , 7)
        Iy = round((self.a * self.A.y + self.b * self.B.y + self.c * self.C.y) / (self.a + self.b + self.c) , 7)
        return point(Ix, Iy)

    def circumcenter(self):
        D = self.B.midpoint(self.C)
        mBC = self.B.slope(self.C)
        mPBC = -1 / mBC
        B1 = equation_type4(D, mPBC)

        E = self.A.midpoint(self.C)
        mAC = self.A.slope(self.C)
        mPAC = -1 / mAC
        B2 = equation_type4(E, mPAC)

        pt=B1.solve(B2)
        pt.x=round(pt.x,7)
        pt.y=round(pt.y,7)
        return pt


    def orthocenter(self):
        mBC = self.B.slope(self.C)
        mPBC = -1 / mBC
        B1 = equation_type4(self.A, mPBC)

        mAC = self.A.slope(self.C)
        mPAC = -1 / mAC
        B2 = equation_type4(self.B, mPAC)

        pt=B1.solve(B2)
        pt.x=round(pt.x,7)
        pt.y=round(pt.y,7)
        return pt
