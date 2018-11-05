"""
Line is defined as a line segment between two points,
The line is a callable object,
The main program illustrates instantiations and the call method.
"""

from class_point import Point

class Line():
    """
    A line is a segment between two points.
    """
    def __init__(self, p1 = Point(), p2 = Point()):
        self.p1 = p1
        self.p2 = p2
        
    def __str__(self):
        """
        Returns the string representation.
        """
        strp = 'Endpoint 1: {}, Endpoint 2: {}'.format(self.p1, self.p2)
        return strp


def main():
    """
    Defining a line.
    """
    print('defining a line ...')
    first = Line()
    print('the default line :', first)
    second = Line(Point(3,4), Point(10,4))
    print('a horizontal line :', second)

if __name__ == "__main__":
    main()
