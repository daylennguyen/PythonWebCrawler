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
		self.Point = tk.Button(self)
		self.Rectangle = tk.Button(self)

		self.Line["text"] = "Random Line"
		self.Line["command"] = self.draw_line

		self.Point["text"] = "Random Point"
		self.Point["command"] = self.draw_point

		self.Rectangle["text"] = "Random Rectangle"
		self.Rectangle["command"] = self.draw_rectangle

		self.Line.pack(side="left")
		self.Point.pack(side="left")
		self.Rectangle.pack(side="left")
		self.erase = tk.Button(self, text="Erase Board",
							   fg="blue", command=self.erase_all)
		self.erase.pack(side="bottom")
		self.QUIT = tk.Button(self, text="QUIT", fg="red",
							  command=root.destroy)
		self.QUIT.pack(side="bottom")

	def draw_line(self):
		ShowLine.draw_rand(self)

	def draw_point(self):
		ShowPoint.draw_rand(self)

	def draw_rectangle(self):
		ShowRectangle.draw_rand(self)

	def erase_all(self):
		self.cnv.delete("all")


if __name__ == "__main__":
	root = tk.Tk()
	app = Application(master=root)
	app.mainloop()
