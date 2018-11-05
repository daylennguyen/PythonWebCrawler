import tkinter as tk
from tkinter import Tk, Canvas, Text
from random import randint

from show import ShowLine, ShowPoint, ShowRectangle, ShowTriangle 

class Application(tk.Frame):
	def __init__(self, master=None):
		self.dim = 400
		tk.Frame.__init__(self, master, width=self.dim*2, height=self.dim)
		self.pack()
		self.cnv = tk.Canvas(master, width=self.dim*2, height=self.dim)
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

	def draw_point(self):
		ShowPoint.draw_rand(self)

	def draw_rectangle(self):
		ShowRectangle.draw_rand(self)

	def erase_all(self):
		self.cnv.delete("all")
