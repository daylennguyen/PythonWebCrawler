
class Point():
    """
    Stores a point on the plane.
    """
    def __init__(self, x=0, y=0):
        """
        Defines the coordinates.
        """
        self.xpt = x
        self.ypt = y

    def __str__(self):
        """
        Returns the string representation.
        """
        return '(' + str(self.xpt) \
                   + ', ' \
                   + str(self.ypt) + ')'

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
