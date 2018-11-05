"""
Inheriting from the class Point, a canvas data attribute is 
added to Point and a method to draw the point on the canvas.
The main program pops a new window with a canvas and draws ten
random points on the canvas.
"""

from tkinter import Tk, Canvas
from random import randint
from class_point import Point

class ShowPoint(Point):
    """
    Extends the class Point
    with a draw method on a Tkinter Canvas.
    """
    def __init__(self, c, x=0, y=0):
        """
        Defines the point (x, y)
        and stores the canvas cnv.
        """
        Point.__init__(self, x, y)
        self.canvas = c

    def draw(self):
        """
        Draws the point on canvas.
        """
        (xpt, ypt) = (self.xpt, self.ypt)
        self.canvas.create_oval(xpt-2, ypt-2, \
            xpt+2, ypt+2, fill='SkyBlue2')

    def draw_rand(self):
        xrd = randint(6, (self.dim*2)-6)
        yrd = randint(6, self.dim-6)
        ShowPoint(self.cnv, xrd,yrd).draw()

def main():
    """
    Shows 10 random points on canvas.
    """
    top = Tk()
    dim = 400
    cnv = Canvas(top, width=dim, height=dim)
    cnv.pack()
    points = []
    for _ in range(10):
        xrd = randint(6, dim-6)
        yrd = randint(6, dim-6)
        points.append(ShowPoint(cnv, xrd, yrd))
    for point in points:
        point.draw()
    top.mainloop()

if __name__ == "__main__":
    main()
