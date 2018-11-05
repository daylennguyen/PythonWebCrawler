import queue
import re
import urllib.request
from gui import *

#CONSTANTS
HEADER = "Alias, URL, Children"
URL_FILE = "../urls/urls3.txt"
OUTPUT_CSV_FILE = "../output/output.csv"
MSG_INVALID_TEXT = "invalid txt"
CHILD_FIRST_OCCURANCE = -1
PROC_LINKS_MAX = 75


#-------Do------------------------------------------------------------------------------#
# [x] Retrieve and open input file contPzzzaining URLs
# [x] Retrieve plain text HTML located at the URLs from file
# [x] Read 1 URL from file
# [x] Read all urls from file using loop
# [x] Create an CSV file of the information containing alias' for kids
# [x] Create a graph using KTinker written classes
# [x] add Parallization
# [x] Graphing -
#			Iterate over the node_list;
# 			Generation 0 is the number of links in the URL_File
#			Generation 1 is the length of the child list within
# 			generation 0. (Cumulative)
# 			Count each and iterate depending on previous generation child count
#
# [o] Retrieve highest link page count
# [o]
# [o]
#-------Grading------------------------------------------------------------------------#
# • Graph is 7.5 pts
# • Parallelization 7.5 pts
# • Coding style and comments 5 pts
# • Sequential Web crawler 30 pts
#         o tags recognition
#         o graph building logic
#         o csv file and highest linked page count
# ------------------------------------------------------------------------------------------#

# Contains the current state of the script


class CrawlerState():

	# Constructor, instantiated when creating a new instance of CrawlerState()
	#
	# @ToBeProcessed_URL_List:
	#				When the state is initialized, this array is appended with
	# 				the URLs from the given file. (SEE py)
	# 				An array of urls to be processed, in-order of when the URL is initially scanned.
	# 				Newly discorvered links are sent to the end of this array in the form of a string.
	#
	# @Processed_URL_List:
	# 				An array containing an ordered list of urls which have
	# 				been processed and transfered from the @ToBeProcessed_URL_List
	# 				All URLs in this list are in the form of a string
	#
	# @Node_List:
	#				An array of WebCrawlerNodes in-order of FirstScanned-to-LastScanned
	#
	# @greatest_link_id:
	#				The value which is used to assign each node a unique alias.
	#				Used and incremeneted during the processLinks() function.
	#				Initialized to 0, unless told otherwise; also manrepresents the
	#				current amount of assigned aliases.
	#
	def __init__(self, ToBeProcessed_URL_List=[], Processed_URL_List=[], Node_List=[], greatest_link_id=0, lenGenZero=0):
		# ordered list of links which have been scanned
		self.state_Processed_URL_List = Processed_URL_List

		# Processed URLs, converted to WebCrawlerNodes
		self.state_node_list = Node_List

		# The Counter for the number of unique links found
		self.state_greatest_link_id = greatest_link_id

		self.lenGenZero=len(self.fileToList(URL_FILE))

		# Initialize the list with the Links in the txtfile
		self.state_ToBeProcessed_URL_List = self.fileToList(URL_FILE)

		self.CreateCSVWriteHeader()

		# The file where we will output our csv values
	def CreateCSVWriteHeader(self):
		self.state_Output_CSV = open(OUTPUT_CSV_FILE, "w+")
		self.state_Output_CSV.write(HEADER)

	def WriteToCSV(self, Children_LinkNums, node):
		self.state_Output_CSV.write(
			"\n"+str(node.Alias) + "," + str(node.URL) + "," + str(Children_LinkNums))

	# Retrieves the file from the root directory (./)
	# then extracts each line as an index within the urls file
	def fileToList(self, filename):
		file = open(filename, "r+")
		urls = file.read().splitlines()
		file.close()
		return urls

	def processLinks(self, lenGenZero):
		# psudo queue; uses a list and pops index zero during each iteration
		currentGenNumber = 0
		currentGenSize=lenGenZero
		NextGenSize=0

		while(len(self.state_ToBeProcessed_URL_List) > 0 and len(self.state_Processed_URL_List) < 75):
			# Count the number of each generation
			if currentGenSize <= 0:
				currentGenNumber = currentGenNumber + 1
				currentGenSize = NextGenSize
				NextGenSize = 0

			url = self.state_ToBeProcessed_URL_List.pop(0)
			currentGenSize = currentGenSize - 1
			# avoid 2 links pointing to eachother causing infinite loop
			if url not in self.state_Processed_URL_List:
				currentNode = FindAllLinksInURL(self.state_greatest_link_id, url, currentGenNumber)
				# Increment the alias
				self.state_greatest_link_id += 1
				self.state_node_list.append(currentNode)
				self.state_Processed_URL_List.append(url)
				# process the children-table of the current link
				for child in currentNode.Children:
					# Avoid reprocessing
					if child not in self.state_Processed_URL_List:
						NextGenSize = NextGenSize + 1
						self.state_ToBeProcessed_URL_List.append(child)
						# ToString function; printed when calling str(  ) on this object

	def __str__(self):
		return "\nToBeProcessed_URL_List:\n\t" + str(self.state_ToBeProcessed_URL_List) + "\nProcessed_URL_List:\n\t" + str(self.state_Processed_URL_List) + "\nNode_List:\n\t" + str(self.state_node_list) + "\ngreatest_link_id:\n\t" + str(self.state_greatest_link_id)

#--------------------------------------------------------------------
# 	Representation of each parent/Link (Which may or may not have a parent)
#	@ChildrenAliasList:	A list of the aliases given to each child; will assist when drawing graph.
#	@Children:	Contains the string form of each child link found within the html of this node
#	@Alias: Unique alias assigned during processLinks, found in the WebCrawlerState; this node
#	makes the relationship between nodes more distinguishable in many cases.
#   @URL: The URL of this Node in the form of a string
#___________________________________________________________
class WebCrawlNode():

	def setChildren(self, Children):
		self.Children = Children
		return self

	#
	def pushChildAlias(self, LinkAlias):
		self.ChildrenAliasList.append(LinkAlias)
		return self.ChildrenAliasList

	# Constructor which is initiated during instantiation of a WebCrawlNode
	def __init__(self, Generation, Alias, Children_Array=[], URL_String="", ChildrenAliasList=[]):
		print(str(Generation))

		self.Generation = Generation
		self.ChildrenAliasList = ChildrenAliasList
		self.Children = Children_Array
		self.Alias = Alias
		self.URL = URL_String

	def __str__(self):
		return str("----------\n"+str(self.URL) + "\n\n\t ***children:***" + str(self.Children))

# Uses the imported urllib to scan the html contents found at the given url_string
# this is then returned in the form of a String
def URLtoHTMLstring(url_string):
	try:
		page = urllib.request.urlopen(url_string)
		pageText = page.read()
	except:
		pageText = "invalid txt"
	return str(pageText)

#	Uses Regex to extract the links from a given url_string
#	each link found at the location is considered a child node
#	and is placed within matches[].
#	@return the extracted information in the form of a new 			WebCrawlNode
def FindAllLinksInURL(current_Alias, url_string, GenNum):
	fileText = URLtoHTMLstring(url_string)
	matches = []
	linelist = re.findall(
		r'(?:(a (\s)?href(\s)?=(\s)?))[\"\'](((\s)?(http|ftp)?s?://)(.*?))?[\"\'](\s)?', fileText, re.I)
	for aline in linelist:
		# Check for no match
		if str(aline[4]) != '' and str(aline[4]) != ' ':
			matches.append(aline[4])
	return WebCrawlNode(GenNum, current_Alias, matches, url_string)

# Function used to match a node's children with their given alias.
def findChildAlias(childsLink, node_list):
	result = CHILD_FIRST_OCCURANCE
	for node in node_list:
		if(node.URL == childsLink):
			result = node.Alias
	return result


def asignAliasToChildren(node, state):
	Children_LinkNums = ""
	currentChildAlias = ""
	node.ChildrenAliasList = []
	if len(node.Children) > 0:  # ensure that the node has children
		for child in node.Children:
				# iterate over the children and find their alias
			currentChildAlias = str(
				findChildAlias(child, state.state_node_list))
			if currentChildAlias != -1:
				Children_LinkNums = Children_LinkNums + \
					(currentChildAlias) + " "
				node.pushChildAlias(currentChildAlias)
	state.WriteToCSV(Children_LinkNums, node)  # write it to the csv
	print("[G"+ str(node.Generation) +"]alias:"+str(node.Alias) + "\n\turl: " +
		  str(node.URL) + "\n\tkids:" + str(Children_LinkNums))


#############
#MAIN METHOD#
#############
def main():
	# initialize the state
	State = CrawlerState()
	# crawl urls
	State.processLinks(State.lenGenZero)
	# assign aliases to the nodes and print them to the csv
	for node in State.state_node_list:
		asignAliasToChildren(node, State)
	State.state_Output_CSV.close()
	#identify the generation of each node
	root = tk.Tk()
	app = Application(master=root)
	app.mainloop()
main()


	# def getCumulativeChildList(self):
	# 	cumulativeChildList = [ ]
	# 	for node in self.state_node_list:
	# 		cumulativeChildList = cumulativeChildList + node.ChildrenAliasList
	# 	return cumulativeChildList
	
	# def findMostChildren(self):
	# 	current_max = 0
	# 	for node in self.state_node_list:
	# 		currentChildCount = len(node.Children)
	# 		if currentChildCount > current_max:
	# 			current_max = currentChildCount
	# 	return current_max

	# def findMostMentioned(self, cumulativeChildList):
	# 	MentionCountPerAlias = []
	# 	cMostMentioned = []
	# 	currentRemoveCount = 1
	# 	IndexJumper = 0

	# 	for node in self.state_node_list:
	# 		current = cumulativeChildList.count(node.Alias)
	# 		for i in range(1, current):
	# 			cumulativeChildList.remove(node.Alias)
	# 		MentionCountPerAlias.append(current)
	# 	MaxMentionCount=max(MentionCountPerAlias)
	# 	#could be multiple with same max mention count
	# 	while(max(MentionCountPerAlias) == MaxMentionCount and currentRemoveCount != len(MentionCountPerAlias)):
	# 		maxNodeAlias = MentionCountPerAlias.index(MaxMentionCount) + currentRemoveCount
	# 		cMostMentioned.append(maxNodeAlias)
	# 		currentRemoveCount = currentRemoveCount + 1



	# 		# if node not in cMostMentioned:
	# 		# 	if cumulativeChildList.count(node.Alias) > cMaxMentionCount:

		
	# def processLinks(self, lenGenZero):
	# 	# psudo queue; uses a list and pops index zero during each iteration
	# 	currentGenNumber = 0
	# 	currentGenSize=lenGenZero
	# 	NextGenSize=0

	# 	while(len(self.state_ToBeProcessed_URL_List) > 0 and len(self.state_Processed_URL_List) < 75):
	# 		# Count the number of each generation
	# 		if currentGenSize <= 0:
	# 			currentGenNumber = currentGenNumber + 1
	# 			currentGenSize = NextGenSize
	# 			NextGenSize = 0

	# 		url = self.state_ToBeProcessed_URL_List.pop(0)
	# 		currentGenSize = currentGenSize - 1
	# 		# avoid 2 links pointing to eachother causing infinite loop
	# 		if url not in self.state_Processed_URL_List:
	# 			currentNode = FindAllLinksInURL(self.state_greatest_link_id, url, currentGenNumber)
	# 			# Increment the alias
	# 			self.state_greatest_link_id += 1
	# 			self.state_node_list.append(currentNode)
	# 			self.state_Processed_URL_List.append(url)
	# 			# process the children-table of the current link
	# 			for child in currentNode.Children:
	# 				# Avoid reprocessing
	# 				if child not in self.state_Processed_URL_List:
	# 					NextGenSize = NextGenSize + 1
	# 					self.state_ToBeProcessed_URL_List.append(child)
	# 					# ToString function; printed when calling str(  ) on this object
	# 		# else:
