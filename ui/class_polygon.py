""" POLYGON """
from class_point import Point
class Polygon(Point):
    """
    A line is a segment between two points.
    """
    def __init__(self, p1 = Point(), p2 = Point(), p3 = Point(), p4 = Point()):
        self.p1 = p1
        self.p2 = p2
        self.p3 = p3
        self.p4 = p4
    def __str__(self): # Returns the string representation.
        strp = 'Point 1: {}, Point 2: {}, Point 3: {}, Point 4: {}'.format(self.p1, self.p2, self.p3, self.p4)
        return strp


def main():
    # Defining a Polygon.
    print('defining a Polygon ...')
    first = Polygon()
    print('the default Polygon :', first)
    second = Polygon(Point(0,0), Point(5,0),Point(8,8), Point(0,0))
    print('a userdefined Polygon :', second)

if __name__ == "__main__":
    main()
