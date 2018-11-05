"""
Inheriting from the class Line, a canvas data attribute
is added, as well as a method to draw a line on the canvas.
The main program pops a new window with a canvas and draws
10 lines on that canvas.
"""

from tkinter import Tk, Canvas
from random import randint
# import class_point
from class_point import Point as Point 
from class_line import Line as Line
from class_showpoint import ShowPoint as ShowPoint


class ShowLine(Line):
    """
    Extends the Line class with a draw method.
    """
    def __init__(self, c, p1=Point(), p2 = Point()):
        """
        Defines the line through two points
        """
        Line.__init__(self, p1, p2)
        self.cnv = c

    def draw(self):
        """
        Draws the line on canvas.
        """
        s1 = ShowPoint(self.cnv, self.p1.xpt, self.p1.ypt)
        s2 = ShowPoint(self.cnv, self.p2.xpt, self.p2.ypt)
        s1.draw()
        s2.draw()
        self.cnv.create_line(self.p1.xpt, self.p1.ypt, self.p2.xpt, self.p2.ypt)

    def draw_rand(self):
        xrd = randint(6, (self.dim*2)-6)
        yrd = randint(6, self.dim-6)
        xrd2 = randint(6, (self.dim*2)-6)
        yrd2 = randint(6, self.dim-6)
        s1 = ShowPoint(self.cnv, xrd, yrd)
        s2 = ShowPoint(self.cnv, xrd2, yrd2)
        s1.draw()
        s2.draw()
        self.cnv.create_line(xrd, yrd, xrd2, yrd2)

def main():
    """
    Shows 10 lines on canvas.
    """
    top = Tk()
    dim = 400
    cnv = Canvas(top, width=dim, height=dim)
    cnv.pack()
    lines = []
    for _ in range(10):
        xrd = randint(6, dim-6)
        yrd = randint(6, dim-6)
        xrd2 = randint(6, dim-6)
        yrd2 = randint(6, dim-6)
        lines.append(ShowLine(cnv, Point(xrd,yrd), Point(xrd2, yrd2)))
    for line in lines:
        line.draw()
    top.mainloop()

if __name__ == "__main__":
    main()
