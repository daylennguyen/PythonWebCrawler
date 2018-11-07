import tkinter as tk
import random
from tkinter import Tk, Canvas, Text
from random import randint
from show import ShowLine, ShowPoint, ShowRectangle, ShowTriangle
from shapes import Point, Line, Polygon, Rectangle, Triangle


class Application(tk.Frame):
	def __init__(self, generations, most, node_list, noderadius=0, nodeCoordinates=[], spacerY=0,
				 spacerX=0, master=None):
		self.noderadius = noderadius
		self.nodeCoordinates = nodeCoordinates
		self.spacerY = spacerY
		self.spacerX = spacerX
		self.node_list = node_list
		self.generations = generations
		self.most = most
		self.dimw = 400
		self.dimh = 950
		tk.Frame.__init__(self, master, width=self.dimw, height=self.dimh)
		self.pack()
		self.cnv = tk.Canvas(master, width=self.dimw, height=self.dimh)
		self.cnv.pack(side="bottom")
		self.master = master
		self.createWidgets()

	def createWidgets(self):
		# self.Line = tk.Button(self)
		# self.Line["text"] = "Random Line"
		# self.Line["command"] = self.draw_line
		# self.Line.pack(side="left")
		self.erase = tk.Button(self, text="Erase Board",
							   fg="blue", command=self.erase_all)
		self.erase.pack(side="bottom")

	def draw_line(self):
		ShowLine.draw_rand(self)

	def makeGrid(self):
		# self.cnv.create_line(0, 10, self.dimw, 10, arrow=tk.BOTH)
		self.spacerY = (self.dimh/(self.generations+1))
		self.spacerX = (self.dimw/(self.most+1))
		curPositionY = 0
		curPositionX = 0
		for num in range(0, self.generations):
			curPositionY = curPositionY+self.spacerY
			self.cnv.create_line(0, curPositionY, self.dimw,
								 curPositionY, arrow=tk.LAST)
		for num in range(0, self.most):
			curPositionX = curPositionX+self.spacerX
			# self.cnv.create_line(curPositionX, 0, curPositionX,
			# 					 self.dimh, arrow=tk.BOTH)

	def acceptNodes(self, NodeList):
		self.node_list = NodeList
	def RollColors(self):
		r = lambda: random.randint(0,255)
		color = '#{:02x}{:02x}{:02x}'.format(r(), r(), r())
		return color


	def drawNodesChildConnections(self):
		# r = lambda: random.randint(0,255)
		for num in range(0,len(self.node_list)):

			print(f'NodeNum:{num}')
			for child in (self.node_list[num].ChildrenAliasList):
				child = int(child)
				a=self.nodeCoordinates[round(self.node_list[num].Alias)][0] 
				b=self.nodeCoordinates[round(self.node_list[num].Alias)][1]
				c=self.nodeCoordinates[int(child)][0]
				d=self.nodeCoordinates[round(child)][1]
				print( f'\n\tChild:{child} \tcoordinates: {self.nodeCoordinates[round(child)]}\t')
				print(str( f'\n\ta = {str(a)}  \n\tb =  {str(b)} \n\tc =  {str(c)} \n\td =  {str(d)}' ))
				self.cnv.create_line( 
					round(self.nodeCoordinates[int(
						self.node_list[num].Alias)][0]) , 
						round(self.nodeCoordinates[int(self.node_list[num].Alias)][1]) , 
						round(self.nodeCoordinates[int(child)][0]) , 
						round(self.nodeCoordinates[int(child)][1]) - self.noderadius, 
						arrow=tk.LAST)


	def drawNodes(self,generations):
		print(self.spacerY)
		print(self.dimh)
		GenerationSpacer = self.spacerY
		currentNodePositionY = GenerationSpacer/2
		currentNodePositionX = 0
		   # Divide the width by the num of kids in the generation
		PreviousNodeGen = -1
		generationList = []
		NodeWidthForGen = self.spacerX/2.5
		self.noderadius = NodeWidthForGen
		nodeCoordinates=[]

		for node in self.node_list:
			generationList.append(node.Generation)
		for node in self.node_list:
			NumNodesInGeneration = generationList.count(node.Generation)
			   # check if we are in a new generation
			   #NEST FIRST TWO IF THEN HAVE ELSE TO REMOVE REPITITION
			if PreviousNodeGen == -1:
				PreviousNodeGen = node.Generation
				NodesInGenerationSpacer = (self.dimw/(NumNodesInGeneration+1))
				currentNodePositionX = NodesInGenerationSpacer
				self.cnv.create_circle(currentNodePositionX, currentNodePositionY,NodeWidthForGen)
				# if we are, then save it and calculate the initial
				# space between each node in the generation
			elif node.Generation != PreviousNodeGen:
				PreviousNodeGen = node.Generation
				NodesInGenerationSpacer = self.dimw/NumNodesInGeneration
				currentNodePositionX = NodesInGenerationSpacer - NodeWidthForGen
				currentNodePositionY = currentNodePositionY + GenerationSpacer
				self.cnv.create_circle(currentNodePositionX, currentNodePositionY,NodeWidthForGen)
				# same generation?
			else:# then increment the position
				currentNodePositionX = (currentNodePositionX + NodesInGenerationSpacer)
			self.cnv.create_circle(currentNodePositionX, currentNodePositionY,NodeWidthForGen)
			coords=[int(currentNodePositionX), int(currentNodePositionY)]
			self.nodeCoordinates.append( coords )
			print(str(node.Alias)+str(coords))
			self.cnv.create_text(currentNodePositionX, currentNodePositionY, text='N'+str(node.Alias))



	def _create_circle(self, x, y, r, **kwargs):
		return self.create_oval(x-r, y-r, x+r, y+r, **kwargs)

	tk.Canvas.create_circle = _create_circle

	def LabelGens(self):
		curPositionY = 10
		for num in range(0, self.generations+1):
			self.cnv.create_text(20, curPositionY, text='Gen '+str(num))
			curPositionY = curPositionY + (self.spacerY)

	def retrieveHalf():
		return NULL

	def draw_rectangle(self):
		ShowRectangle.draw_rand(self)

	def erase_all(self):
		self.cnv.delete("all")
