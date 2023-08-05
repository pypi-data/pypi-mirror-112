import sys


class point:
    def __init__(self, x=0, y=0):
        self.x = x
        self.y = y

    def __eq__(self, other):
        if self.x == other.x and self.y == other.y:
            return True
        else:
            return False

    def distance(self, other):
        d = (((self.x - other.x) ** 2) + ((self.y - other.y) ** 2)) ** (0.5)
        return round(d, 7)

    def section(self, other, m, n, external=False):
        if m < 0 or n < 0:
            sys.stderr.write('Expected positive input of m and n')
            exit(1)

        if not external:
            x = (m * other.x + n * self.x) / (m + n)
            y = (m * other.y + n * self.y) / (m + n)
            return point(round(x, 7), round(y, 7))
        else:
            if (m - n) == 0:
                sys.stderr.write('External division not possible')
                exit(1)
            else:
                x = (m * other.x - n * self.x) / (m - n)
                y = (m * other.y - n * self.y) / (m - n)
            return point(round(x, 7), round(y, 7))

    def __str__(self):
        s = f'( {self.x} , {self.y} )'
        return s

    def area_of_triangle(self, p2, p3):
        area = 0.5 * abs((self.x * (p2.y - p3.y)) + (p2.x * (p3.y - self.y)) + (p3.x * (self.y - p2.y)))
        return round(area, 7)

    def centroid(self, p2, p3):
        x = (self.x + p2.x + p3.x) / (3.0)
        y = (self.y + p2.y + p3.y) / (3.0)
        return point(round(x, 7), round(y, 7))

    def incenter(self, B, C):
        a = B.distance(C)
        b = self.distance(C)
        c = self.distance(B)
        if a == 0 or b == 0 or c == 0:
            sys.stderr.write('Can not find the in_center of a line')
            exit(1)
        Ix = round((a * self.x + b * B.x + c * C.x) / (a + b + c), 7)
        Iy = round((a * self.y + b * B.y + c * C.y) / (a + b + c), 7)
        return point(Ix, Iy)

    def slope(self, other):
        if self == other:
            sys.stderr.write('Can not find slope of a single point\n')
            exit(1)
        elif self.x == other.x:
            sys.stderr.write('Slope not defined')
            exit(1)
        else:
            dy = self.y - other.y
            dx = self.x - other.x
            return round(dy / dx, 7)

    def midpoint(self,other):
        x=(self.x+other.x)/2
        y=(self.y+other.y)/2
        return point(round(x, 7), round(y, 7))