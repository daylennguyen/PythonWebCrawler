import tkinter as tk
from tkinter import Tk, Canvas, Text
from random import randint
from show import ShowLine, ShowPoint, ShowRectangle, ShowTriangle 
from shapes import Point,Line,Polygon,Rectangle,Triangle

class Application(tk.Frame):
	def __init__(self, master=None):
		self.dimw = 400
		self.dimh = 950
		tk.Frame.__init__(self, master, width=self.dimw, height=self.dimh)
		self.pack()
		self.cnv = tk.Canvas(master, width=self.dimw, height=self.dimh)
		self.cnv.pack(side="bottom")
		self.master = master
		self.createWidgets()

	def createWidgets(self):
		self.Line = tk.Button(self)

		self.Line["text"] = "Random Line"
		self.Line["command"] = self.draw_line
		self.Line.pack(side="left")
		self.erase = tk.Button(self, text="Erase Board",
							   fg="blue", command=self.erase_all)
		self.erase.pack(side="bottom")

	def draw_line(self):
		ShowLine.draw_rand(self)

	def makeGrid(self,generation):
		self.cnv.create_line(0,10,self.dimw,10, arrow=tk.BOTH)
		spacer = (self.dimh/(generation+1))
		curPositionY = 0
		for num in range(0,generation):
			curPositionY = curPositionY+spacer
			self.cnv.create_line(0,curPositionY,self.dimw,curPositionY, arrow=tk.BOTH)
			
		


	def draw_rectangle(self):
		ShowRectangle.draw_rand(self)

	def erase_all(self):
		self.cnv.delete("all")
