"""
Stores coordinates of a point on the plane.
The main program illustrates two instantiations.
"""

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
   

def main():
    """
    Instantiates two points.
    """
    print('instantiating two points ...')
    first = Point()
    print('p =', first)
    second = Point(3, 4)
    print('q =', second)

if __name__ == "__main__":
    main()
