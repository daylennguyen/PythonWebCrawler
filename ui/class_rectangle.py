""" RECTANGLE """
from class_polygon import Polygon
from class_point import Point

class Rectangle(Polygon):
    """
    A line is a segment between two points.
    """
    def __init__(self, p1 = Point(), p2 = Point()):
        Polygon.__init__(self, p1, p2)
        self.p1 = p1
        self.p2 = p2
        self.p3 = Point(p2.xpt, p1.ypt)
        self.p4 = Point(p1.xpt, p2.ypt)

    def __str__(self): # Returns the string representation.
        strp = 'Point 1: {}, Point 2: {}, Point 3: {}, Point 4: {}'.format(self.p1, self.p2, self.p3, self.p4)
        return strp


def main():
    # Defining a Polygon.
    print('defining a Rectangle ...')
    first = Rectangle()
    print('the default Rectangle :', first)
    second = Rectangle(Point(0,0), Point(5,5))
    print('a userdefined Rectangle :', second)

if __name__ == "__main__":
    main()
