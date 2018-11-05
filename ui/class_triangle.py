""" TRIANGLE """
from class_polygon import Polygon
from class_point import Point

class Triangle(Polygon):
    """
    A line is a segment between two points.
    """
    def __init__(self, p1 = Point(), p2 = Point(), p3 = Point() ):
        Polygon.__init__(self, p1, p2, p3)
        self.p1 = p1
        self.p2 = p2
        self.p3 = p3

    def __str__(self): # Returns the string representation.
        strp = 'Point 1: {}, Point 2: {}, Point 3: {}'.format(self.p1, self.p2, self.p3)
        return strp


def main():
    # Defining a Polygon.
    print('defining a Triangle ...')
    first = Triangle()
    print('the default Triangle :', first)
    second = Triangle(Point(0,0), Point(5,0), Point(5,5))
    print('a userdefined Triangle :', second)

if __name__ == "__main__":
    main()
