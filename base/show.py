import tkinter as tk

from tkinter import Tk, Canvas, Text
from shapes import *

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

class ShowLine(Line):
	"""
	Extends the Line class with a draw method.
	"""
	def __init__(self, c, p1=Point(), p2=Point()):
		"""
		Defines the line through two points
		"""
		Line.__init__(self, c, p1, p2)
		self.cnv = c
		self.draw_rand = self.draw_rand
		self.c.create_text(100,150)

	def draw(self,cnv):
		"""Draws the line on canvas."""
		s1 = ShowPoint(self.cnv, self.p1.xpt, self.p1.ypt)
		s2 = ShowPoint(self.cnv, self.p2.xpt, self.p2.ypt)
		s1.draw()
		s2.draw()
		cnv.create_line(self.p1.xpt, self.p1.ypt,
							 self.p2.xpt, self.p2.ypt, arrow=tk.BOTH)
				

	def draw_rand(self):
		# x1,y1,x2,y2
		self.cnv.create_line(100, 100, 200, 100, arrow=tk.FIRST)
		self.cnv.create_text(100,100, text=12345)




class ShowRectangle(Rectangle):
	"""
	Extends the Polygon class with a draw method.
	"""
	def __init__(self, c, p1=Point(), p2=Point()):
		"""Defines the line through two points"""
		Rectangle.__init__(self, p1, p2)
		self.cnv = c
	"""Draws the polygon on canvas."""
	def draw(self):
		self.cnv.create_rectangle(
			self.p1.xpt, self.p1.ypt, self.p2.xpt, self.p2.ypt,)


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
		self.canvas.create_oval(xpt-2, ypt-2,
								xpt+2, ypt+2, fill='SkyBlue2')

