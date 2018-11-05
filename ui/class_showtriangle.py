"""
Inheriting from the class Line, a canvas data attribute
is added, as well as a method to draw a line on the canvas.
The main program pops a new window with a canvas and draws
10 lines on that canvas.
"""

from tkinter import Tk, Canvas
from random import randint

# 
from class_point import Point
from class_triangle import Triangle
# from class_showpoint import ShowPoint

class ShowTriangle(Triangle):
    """
    Extends the Polygon class with a draw method.
    """
    def __init__(self, c, p1=Point(), p2=Point(), p3=Point()):
        """Defines the line through two points"""
        Triangle.__init__(self, p1, p2, p3)
        self.cnv = c

    def draw(self):
        """Draws the polygon on canvas."""
        self.cnv.create_polygon(self.p1.xpt, self.p1.ypt, self.p2.xpt, self.p2.ypt, self.p3.xpt, self.p3.ypt, fill='', outline='black')
    def draw_rand(self):
        xrd = randint(6, (self.dim*2)-6)
        yrd = randint(6, self.dim-6)
        xrd2 = randint(6, (self.dim*2)-6)
        yrd2 = randint(6, self.dim-6)
        xrd3 = randint(6, (self.dim*2)-6)
        yrd3 = randint(6, self.dim-6)
        # self.cnv.create_rectangle(self.p1.xpt, self.p1.ypt, self.p2.xpt, self.p2.ypt,)
        self.cnv.create_polygon(xrd, yrd, xrd2, yrd2, xrd3, yrd3, fill='', outline='black')

def main():
    """
    Shows 10 lines on canvas.
    """
    top = Tk()
    dim = 400
    cnv = Canvas(top, width=dim, height=dim)
    cnv.pack()
    lines = []
    for _ in range(5):
        xrd = randint(6, dim-6)
        yrd = randint(6, dim-6)
        xrd2 = randint(6, dim-6)
        yrd2 = randint(6, dim-6)
        xrd3 = randint(6, dim-6)
        yrd3 = randint(6, dim-6)
        lines.append(ShowTriangle(cnv, Point(xrd,yrd), Point(xrd2, yrd2), Point(xrd3, yrd3)))
    for line in lines:
        line.draw()
    top.mainloop()

if __name__ == "__main__":
    main()
