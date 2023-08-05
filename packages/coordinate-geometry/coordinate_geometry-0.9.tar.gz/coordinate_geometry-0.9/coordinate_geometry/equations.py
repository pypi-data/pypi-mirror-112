from coordinate_geometry.point import point
import math
import sys


class equation_type1:
    '''
    Slope and y intercept format
    '''

    def __init__(self, slope, y_intercept):
        self.slope = slope
        self.y_intercept = y_intercept
        self.a = -self.slope
        self.b = 1
        self.c = -y_intercept

    def distance(self, pt: point):
        d = round(abs((self.a * pt.x + self.b * pt.y + self.c) / (math.sqrt(self.a ** 2 + self.b ** 2))), 7)
        return d

    def foot_of_perpendicular(self, pt: point):
        s = round(-(self.a * pt.x + self.b * pt.y + self.c) / (self.a ** 2 + self.b ** 2), 7)
        x = pt.x + (self.a * s)
        y = pt.y + (self.b * s)
        return point(x, y)

    def image_of_point(self, pt: point):
        s = round(-2 * (self.a * pt.x + self.b * pt.y + self.c) / (self.a ** 2 + self.b ** 2), 7)
        x = pt.x + (self.a * s)
        y = pt.y + (self.b * s)
        return point(x, y)

    def __str__(self):
        s = f'{self.a} x + {self.b} y + {self.c} = 0'
        return s

    def __eq__(self, other):
        if self.a == 0 and self.b == 0:
            sys.stderr.write('Invalid equation of line entered')
            exit(1)
        if self.a != 0:
            if other.a != 0:
                A1 = 1
                A2 = 1
                B1 = self.b / self.a
                B2 = other.b / other.a
                C1 = self.c / self.a
                C2 = other.c / other.a
                if B1 == B2 and C1 == C2:
                    return True
            else:
                return False

        if self.b != 0:
            if other.b != 0:
                A1 = self.a / self.b
                A2 = other.a / other.b
                B1 = self.b / self.b
                B2 = other.b / other.b
                C1 = self.c / self.b
                C2 = other.c / other.b
                if round(B1, 7) == round(B2, 7) and round(C1, 7) == round(C2, 7) and round(A1, 7) == round(A2, 7):
                    return True
            else:
                return False

    def solve(self, other):
        if self == other:
            sys.stderr.write('Can not evaluate a single line')
            exit(1)

        x = round((other.c * self.b - self.c * other.b) / (other.b * self.a - self.b * other.a), 7)
        y = round((self.a * other.c - other.a * self.c) / (other.a * self.b - self.a * other.b), 7)
        return point(x, y)

    def is_parallel(self, other):
        if round(self.slope, 7) == round(other.slope, 7):
            return True
        else:
            return False

    def is_perpendicular(self, other):
        if round((self.slope * other.slope), 7) == -1:
            return True
        else:
            return False

    def angle(self, other):
        if self.is_parallel(other):
            return 0
        elif self.is_perpendicular(other):
            return math.pi / 2
        else:
            m1 = self.slope
            m2 = other.slope
            tan_angle = abs((m1 - m2) / (1 + (m1 * m2)))
            angle = math.atan(tan_angle)
            return round(angle, 7)


class equation_type2:
    '''
    General Format
    '''

    def __init__(self, a=0, b=0, c=0):
        self.a = a
        self.b = b
        self.c = c
        if b != 0:
            self.slope = -a / b
            self.y_intercept = -c / b
        else:
            self.slope = math.inf
            self.y_intercept = math.inf

    def distance(self, pt: point):
        d = round(abs((self.a * pt.x + self.b * pt.y + self.c) / (math.sqrt(self.a ** 2 + self.b ** 2))), 7)
        return d

    def foot_of_perpendicular(self, pt: point):
        s = round(-(self.a * pt.x + self.b * pt.y + self.c) / (self.a ** 2 + self.b ** 2), 7)
        x = pt.x + (self.a * s)
        y = pt.y + (self.b * s)
        return point(x, y)

    def image_of_point(self, pt: point):
        s = round(-2 * (self.a * pt.x + self.b * pt.y + self.c) / (self.a ** 2 + self.b ** 2), 7)
        x = pt.x + (self.a * s)
        y = pt.y + (self.b * s)
        return point(x, y)

    def __str__(self):
        s = f'{self.a} x + {self.b} y + {self.c} = 0'
        return s

    def __eq__(self, other):
        if self.a == 0 and self.b == 0:
            sys.stderr.write('Invalid equation of line entered')
            exit(1)
        if self.a != 0:
            if other.a != 0:
                A1 = 1
                A2 = 1
                B1 = self.b / self.a
                B2 = other.b / other.a
                C1 = self.c / self.a
                C2 = other.c / other.a
                if B1 == B2 and C1 == C2:
                    return True
            else:
                return False

        if self.b != 0:
            if other.b != 0:
                A1 = self.a / self.b
                A2 = other.a / other.b
                B1 = self.b / self.b
                B2 = other.b / other.b
                C1 = self.c / self.b
                C2 = other.c / other.b
                if round(B1, 7) == round(B2, 7) and round(C1, 7) == round(C2, 7) and round(A1, 7) == round(A2, 7):
                    return True
            else:
                return False

    def solve(self, other):
        if self == other:
            sys.stderr.write('Can not evaluate a single line')
            exit(1)

        x = round((other.c * self.b - self.c * other.b) / (other.b * self.a - self.b * other.a), 7)
        y = round((self.a * other.c - other.a * self.c) / (other.a * self.b - self.a * other.b), 7)
        return point(x, y)

    def is_parallel(self, other):
        if round(self.slope, 7) == round(other.slope, 7):
            return True
        else:
            return False

    def is_perpendicular(self, other):
        if round((self.slope * other.slope), 7) == -1:
            return True
        else:
            return False

    def angle(self, other):
        if self.is_parallel(other):
            return 0
        elif self.is_perpendicular(other):
            return math.pi / 2
        else:
            m1 = self.slope
            m2 = other.slope
            tan_angle = abs((m1 - m2) / (1 + (m1 * m2)))
            angle = math.atan(tan_angle)
            return round(angle, 7)


class equation_type3:
    '''
    Intercept Format
    '''

    def __init__(self, x_intercept, y_intercept):
        self.a = y_intercept
        self.b = x_intercept
        self.c = -(x_intercept * y_intercept)
        self.y_intercept = y_intercept

        if self.b != 0:
            self.slope = -self.a / self.b
        else:
            self.slope = math.inf

    def distance(self, pt: point):
        d = round(abs((self.a * pt.x + self.b * pt.y + self.c) / (math.sqrt(self.a ** 2 + self.b ** 2))), 7)
        return d

    def foot_of_perpendicular(self, pt: point):
        s = round(-(self.a * pt.x + self.b * pt.y + self.c) / (self.a ** 2 + self.b ** 2), 7)
        x = pt.x + (self.a * s)
        y = pt.y + (self.b * s)
        return point(x, y)

    def image_of_point(self, pt: point):
        s = round(-2 * (self.a * pt.x + self.b * pt.y + self.c) / (self.a ** 2 + self.b ** 2), 7)
        x = pt.x + (self.a * s)
        y = pt.y + (self.b * s)
        return point(x, y)

    def __str__(self):
        s = f'{self.a} x + {self.b} y + {self.c} = 0'
        return s

    def __eq__(self, other):
        if self.a == 0 and self.b == 0:
            sys.stderr.write('Invalid equation of line entered')
            exit(1)
        if self.a != 0:
            if other.a != 0:
                A1 = 1
                A2 = 1
                B1 = self.b / self.a
                B2 = other.b / other.a
                C1 = self.c / self.a
                C2 = other.c / other.a
                if B1 == B2 and C1 == C2:
                    return True
            else:
                return False

        if self.b != 0:
            if other.b != 0:
                A1 = self.a / self.b
                A2 = other.a / other.b
                B1 = self.b / self.b
                B2 = other.b / other.b
                C1 = self.c / self.b
                C2 = other.c / other.b
                if round(B1, 7) == round(B2, 7) and round(C1, 7) == round(C2, 7) and round(A1, 7) == round(A2, 7):
                    return True
            else:
                return False

    def solve(self, other):
        if self == other:
            sys.stderr.write('Can not evaluate a single line')
            exit(1)

        x = round((other.c * self.b - self.c * other.b) / (other.b * self.a - self.b * other.a), 7)
        y = round((self.a * other.c - other.a * self.c) / (other.a * self.b - self.a * other.b), 7)
        return point(x, y)

    def is_parallel(self, other):
        if round(self.slope, 7) == round(other.slope, 7):
            return True
        else:
            return False

    def is_perpendicular(self, other):
        if round((self.slope * other.slope), 7) == -1:
            return True
        else:
            return False

    def angle(self, other):
        if self.is_parallel(other):
            return 0
        elif self.is_perpendicular(other):
            return math.pi / 2
        else:
            m1 = self.slope
            m2 = other.slope
            tan_angle = abs((m1 - m2) / (1 + (m1 * m2)))
            angle = math.atan(tan_angle)
            return round(angle, 7)


class equation_type4:
    '''
    Point , Slope Format
    '''

    def __init__(self, pt: point, slope):
        m = slope
        self.a = -slope
        self.b = 1
        self.c = (m * pt.x - pt.y)
        self.slope = slope
        if self.b != 0:
            self.y_intercept = -self.c / self.b
        else:
            self.y_intercept = math.inf

    def distance(self, pt: point):
        d = round(abs((self.a * pt.x + self.b * pt.y + self.c) / (math.sqrt(self.a ** 2 + self.b ** 2))), 7)
        return d

    def foot_of_perpendicular(self, pt: point):
        s = round(-(self.a * pt.x + self.b * pt.y + self.c) / (self.a ** 2 + self.b ** 2), 7)
        x = pt.x + (self.a * s)
        y = pt.y + (self.b * s)
        return point(x, y)

    def image_of_point(self, pt: point):
        s = round(-2 * (self.a * pt.x + self.b * pt.y + self.c) / (self.a ** 2 + self.b ** 2), 7)
        x = pt.x + (self.a * s)
        y = pt.y + (self.b * s)
        return point(x, y)

    def __str__(self):
        s = f'{self.a} x + {self.b} y + {self.c} = 0'
        return s

    def __eq__(self, other):
        if self.a == 0 and self.b == 0:
            sys.stderr.write('Invalid equation of line entered')
            exit(1)
        if self.a != 0:
            if other.a != 0:
                A1 = 1
                A2 = 1
                B1 = self.b / self.a
                B2 = other.b / other.a
                C1 = self.c / self.a
                C2 = other.c / other.a
                if B1 == B2 and C1 == C2:
                    return True
            else:
                return False

        if self.b != 0:
            if other.b != 0:
                A1 = self.a / self.b
                A2 = other.a / other.b
                B1 = self.b / self.b
                B2 = other.b / other.b
                C1 = self.c / self.b
                C2 = other.c / other.b
                if round(B1, 7) == round(B2, 7) and round(C1, 7) == round(C2, 7) and round(A1, 7) == round(A2, 7):
                    return True
            else:
                return False

    def solve(self, other):
        if self == other:
            sys.stderr.write('Can not evaluate a single line')
            exit(1)

        x = round((other.c * self.b - self.c * other.b) / (other.b * self.a - self.b * other.a), 7)
        y = round((self.a * other.c - other.a * self.c) / (other.a * self.b - self.a * other.b), 7)
        return point(x, y)

    def is_parallel(self, other):
        if round(self.slope, 7) == round(other.slope, 7):
            return True
        else:
            return False

    def is_perpendicular(self, other):
        if round((self.slope * other.slope), 7) == -1:
            return True
        else:
            return False

    def angle(self, other):
        if self.is_parallel(other):
            return 0
        elif self.is_perpendicular(other):
            return math.pi / 2
        else:
            m1 = self.slope
            m2 = other.slope
            tan_angle = abs((m1 - m2) / (1 + (m1 * m2)))
            angle = math.atan(tan_angle)
            return round(angle, 7)


class equation_type5:
    '''
    Two Point Format
    '''

    def __init__(self, pt: point, pt2: point):
        m = slope = (pt2.y - pt.y) / (pt2.x - pt.x)

        self.a = -slope
        self.b = 1
        self.c = (m * pt.x - pt.y)
        self.slope = slope
        if self.b != 0:
            self.y_intercept = -self.c / self.b
        else:
            self.y_intercept = math.inf

    def distance(self, pt: point):
        d = round(abs((self.a * pt.x + self.b * pt.y + self.c) / (math.sqrt(self.a ** 2 + self.b ** 2))), 7)
        return d

    def foot_of_perpendicular(self, pt: point):
        s = round(-(self.a * pt.x + self.b * pt.y + self.c) / (self.a ** 2 + self.b ** 2), 7)
        x = pt.x + (self.a * s)
        y = pt.y + (self.b * s)
        return point(x, y)

    def image_of_point(self, pt: point):
        s = round(-2 * (self.a * pt.x + self.b * pt.y + self.c) / (self.a ** 2 + self.b ** 2), 7)
        x = pt.x + (self.a * s)
        y = pt.y + (self.b * s)
        return point(x, y)

    def __str__(self):
        s = f'{self.a} x + {self.b} y + {self.c} = 0'
        return s

    def __eq__(self, other):
        if self.a == 0 and self.b == 0:
            sys.stderr.write('Invalid equation of line entered')
            exit(1)
        if self.a != 0:
            if other.a != 0:
                A1 = 1
                A2 = 1
                B1 = self.b / self.a
                B2 = other.b / other.a
                C1 = self.c / self.a
                C2 = other.c / other.a
                if B1 == B2 and C1 == C2:
                    return True
            else:
                return False

        if self.b != 0:
            if other.b != 0:
                A1 = self.a / self.b
                A2 = other.a / other.b
                B1 = self.b / self.b
                B2 = other.b / other.b
                C1 = self.c / self.b
                C2 = other.c / other.b
                if round(B1, 7) == round(B2, 7) and round(C1, 7) == round(C2, 7) and round(A1, 7) == round(A2, 7):
                    return True
            else:
                return False

    def solve(self, other):
        if self == other:
            sys.stderr.write('Can not evaluate a single line')
            exit(1)

        x = round((other.c * self.b - self.c * other.b) / (other.b * self.a - self.b * other.a), 7)
        y = round((self.a * other.c - other.a * self.c) / (other.a * self.b - self.a * other.b), 7)
        return point(x, y)

    def is_parallel(self, other):
        if round(self.slope, 7) == round(other.slope, 7):
            return True
        else:
            return False

    def is_perpendicular(self, other):
        if round((self.slope * other.slope), 7) == -1:
            return True
        else:
            return False

    def angle(self, other):
        if self.is_parallel(other):
            return 0
        elif self.is_perpendicular(other):
            return math.pi / 2
        else:
            m1 = self.slope
            m2 = other.slope
            tan_angle = abs((m1 - m2) / (1 + (m1 * m2)))
            angle = math.atan(tan_angle)
            return round(angle, 7)
