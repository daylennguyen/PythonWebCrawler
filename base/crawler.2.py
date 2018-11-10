# -------Do------------------------------------------------------------------------------#
# [x] Retrieve and open input file contPzzzaining URLs
# [x] Retrieve plain text HTML located at the URLs from file
# [x] Read 1 URL from file
# [x] Read all urls from file using loop
# [x] Create an CSV file of the information containing alias' for kids
# [x] Create a graph using KTinker written classes
# [x] add Parallization
# [x] Graphing -
# 			Iterate over the node_list;
# 			Generation 0 is the number of links in the URL_File
# 			Generation 1 is the length of the child list within
# 			generation 0. (Cumulative)
# 			Count each and iterate depending on previous generation child count
#
# [o] Retrieve highest link page count
# [o]
# [o]
# -------Grading------------------------------------------------------------------------#
# • Graph is 7.5 pts
# • Parallelization 7.5 pts
# • Coding style and comments 5 pts
# • Sequential Web crawler 30 pts
#         o tags recognition
#         o graph building logic
#         o csv file and highest linked page count
# ------------------------------------------------------------------------------------------#
# import queue
from multiprocessing import Array, Process, current_process,Queue, Value

import multiprocessing
import re
import urllib.request
import copy
from gui import *


# CONSTANTS
REGEX4LINKS = r'(?:(a (\s)?href(\s)?=(\s)?))[\"\'](((\s)?(http|ftp)?s?://)(.*?))?[\"\'](\s)?'
HEADER = "Alias, URL, Children"
URL_FILE = "../urls/urls.txt"
OUTPUT_CSV_FILE = "../output/output.csv"
MSG_INVALID_TEXT = "invalid txt"
CHILD_FIRST_OCCURANCE = -1
PROC_LINKS_MAX = 75
DEBUG = True

'''
	Contains the current state of the script
	@ToBeProcessed_URL_List:
				When the state is initialized, this array is appended with
					the URLs from the given file. (SEE py)
					An array of urls to be processed, in-order of when the URL
				is initially scanned.
					Newly discorvered links are sent to the end of this array
				in the form of a string.
	
	@Processed_URL_List:
					An array containing an ordered list of urls which have
					been processed and transfered from the @ToBeProcessed_URL_List
					All URLs in this list are in the form of a string
	
	@Node_List:
					An array of WebCrawlerNodes in-order of FirstScanned-to-LastScanned
	
	@greatest_link_id:
					The value which is used to assign each node a unique alias.
					Used and incremeneted during the processLinks() function.
					Initialized to 0, unless told otherwise; also manrepresents the
					current amount of assigned aliases.
'''


class CrawlerState():
	def __init__(self, ToBeProcessed_URL_List=[], Processed_URL_List=[],
				 Node_List=[], greatest_link_id=Value("i",0),
				 lenGenZero=0, maxmentioned=0):
		# ordered list of links which have been scanned
		self.state_Processed_URL_List = Processed_URL_List
		# Processed URLs, converted to WebCrawlerNodes
		self.state_node_list = Node_List
		# The Counter for the number of unique links found
		self.state_greatest_link_id = greatest_link_id
		self.lenGenZero = len(self.fileToList(URL_FILE))
		# Initialize the list with the Links in the txtfile
		self.state_ToBeProcessed_URL_List = self.fileToList(URL_FILE)
		self.CreateCSVWriteHeader()

	def CreateCSVWriteHeader(self):
		self.state_Output_CSV = open(OUTPUT_CSV_FILE, "w+")
		self.state_Output_CSV.write(HEADER)

	def WriteToCSV(self, Children_LinkNums, node):
		self.state_Output_CSV.write(
			"\n"+str(node.Alias) + "," +
			str(node.URL) + "," + str(Children_LinkNums))

	def CSVWriteMost(self, mostmentioned):
		self.state_Output_CSV.write(
			"\nMost Mentioned Node:\t,"+str(mostmentioned))

	# Retrieves the file from the root directory (./)
	# then extracts each line as an index within the urls file
	def fileToList(self, filename):
		file = open(filename, "r+")
		urls = file.read().splitlines()
		file.close()
		return urls

	def getCumulativeChildList(self):
		cumulativeChildList = []
		for node in self.state_node_list:
			cumulativeChildList = cumulativeChildList + node.ChildrenAliasList
		return cumulativeChildList

	def processLinks(self):
		self.currentGenNumber = Value("i", 0)
		self.currentGenSize = Value( "i" ,self.lenGenZero )
		self.NextGenSize = Value("i",0)
		self.crawl()
		return self.currentGenNumber.value



	def crawl(self):

		# initialize
		node_queue = multiprocessing.Queue()
		#  producer inserts urls found in link search (form of string array)
		#  then the consumer will grab the front of the queue and check if it has been stored.
		#  if it has then skip, if it hasnt then output a webnode to the node_queue
		children_queue = multiprocessing.Queue()
		# meant to feed string urls to the producer
		url_queue = multiprocessing.Queue()
		completed = Value("i", 0);
		# create the two processes
		producer_stall = 0
		producer = Process(target=PRODUCER_PROCESS, args=(producer_stall,children_queue, url_queue, completed))
		consumer = Process(target=CONSUMER_PROCESS, args=(self.currentGenSize,self.NextGenSize, self.state_greatest_link_id, self.currentGenNumber,children_queue, node_queue, completed,self.state_Processed_URL_List))
		for urls_in_file in self.state_ToBeProcessed_URL_List:
				url_queue.put(urls_in_file)
		producer.start()
		consumer.start()
		stall_counter = 0
		while(stall_counter < 10000 and len(self.state_Processed_URL_List) < 75):
			stall_counter += 1
			if len(self.state_ToBeProcessed_URL_List) > 0:
				stall_counter =0
				url = self.state_ToBeProcessed_URL_List.pop(0)
				print(url)
				# ! and both processes use and update the same data pool
				if url not in self.state_Processed_URL_List:
					url_queue.put(url)
					self.state_Processed_URL_List.append(url)
					# if not children_queue.empty():
					# 	children_queue.get() 
					# When the consumer pushes a built node; check if
					# we recognize the url, ignore it if we do otherwise process it
			if not node_queue.empty():
				print(str(self.NextGenSize.value))
				currentNode = node_queue.get() 
				self.state_greatest_link_id.value += 1
				# go through the children and find whether we've processed them before
				self.state_node_list.append(currentNode)
				for child in currentNode.Children:
					if child not in self.state_Processed_URL_List:
						self.state_ToBeProcessed_URL_List.append(child)
						
				print(f'cur_node: {currentNode} ')
		completed.value = 1
		print(f'completed.value: {completed.value} ')

		producer.join()
		consumer.join()
		print(f'producer and consumer joined ')
		print(len(self.state_node_list))
		# after while execution
		# for num in range(0, node_queue.qsize()):
		# 	node_popped = node_queue.get()
		# 	print(f'node_popped: {node_popped}  num = {num}')
		# 	self.state_node_list.append(node_popped)
		
# ! end ########################################################




	def generationUpdate(currentGenSize,currentGenNumber,NextGenSize):
			if currentGenSize.value <= 0:
				currentGenNumber.value = currentGenNumber.value + 1
				currentGenSize.value = NextGenSize.value
				NextGenSize.value = 0
			currentGenSize.value = currentGenSize.value - 1
			return currentGenSize

	def pushNode(self, node):
		# multiprocessing.lock
		self.state_greatest_link_id += 1
		self.state_node_list.append(node)
		self.state_Processed_URL_List.append(node.URL)

	def findMostChildren(self):
		resultAlias = ''
		current_max_count = 0
		result = []
		for node in self.state_node_list:
			currentChildCount = len(node.Children)
			if currentChildCount > current_max_count:
				current_max_count = currentChildCount
				resultAlias = node.Alias
		result = [resultAlias, current_max_count]
		if DEBUG is True:
			print(
				f'Most Children: Node{result[0]} with a children count of {result[1]}')
		return result

	# ToString function; printed when calling str(  ) on this object
	def __str__(self):
		return f"""\nToBeProcessed_URL_List:\n\t" +
		{str(self.state_ToBeProcessed_URL_List)} +
		"\nProcessed_URL_List:\n\t" + {str(self.state_Processed_URL_List)} +
		"\nNode_List:\n\t" + {str(self.state_node_list)} +
		"\ngreatest_link_id:\n\t" +
		{str(self.state_greatest_link_id)}"""

	def findMostMentioned(self, cumulativeChildList):
		countsPerAlias = []
		for node in self.state_node_list:
			alias = str(node.Alias)
			countsPerAlias.append(cumulativeChildList.count(alias))
		maxes = []
		maxValue = max(countsPerAlias)
		self.maxmentioned = maxValue
		maxcounts = countsPerAlias.count(max(countsPerAlias))
		for num in range(0, maxcounts):
			maxes.append(countsPerAlias.index(maxValue))
		return maxes


# --------------------------------------------------------------------
# 	Representation of each parent/Link (Which may or may not have a parent)
# 	@ChildrenAliasList:	A list of the aliases given to each child; will
#   assist when drawing graph.
# 	@Children:	Contains the string form of each child link found within
#   the html of this node
# 	@Alias: Unique alias assigned during processLinks, found in the
#   WebCrawlerState; this node
# 	makes the relationship between nodes more distinguishable in many cases.
#   @URL: The URL of this Node in the form of a string
# ___________________________________________________________
class WebCrawlNode():
	def setChildren(self, Children):
		self.Children = Children
		return self

	def pushChildAlias(self, LinkAlias):
		self.ChildrenAliasList.append(LinkAlias)
		return self.ChildrenAliasList

	# Constructor which is initiated during instantiation of a WebCrawlNode
	def __init__(self, Generation, Alias, Children_Array=[], URL_String="",
				 ChildrenAliasList=[]):
		# print(str(Generation))
		self.Generation = Generation
		self.ChildrenAliasList = ChildrenAliasList
		self.Children = Children_Array
		self.Alias = Alias
		self.URL = URL_String

	def __str__(self):
		return str("----------\n"+str(self.URL) +
				   "\n\n\t ***children:***" + str(self.Children))

# Uses the imported urllib to scan the html contents
# found at the given url_string
# this is then returned in the form of a String


def URLtoHTMLstring(url_string):
	try:
		page = urllib.request.urlopen(url_string)
		pageText = page.read()
	except:
		pageText = "invalid txt"
	return str(pageText)


'''
	Uses Regex to extract the links from a given url_string
	each link found at the location is considered a child node
	and is placed within matches[].
	@return the extracted information in the form of a new WebCrawlNode
'''


def Search4Links(url_string):
	matches = []
	fileText = URLtoHTMLstring(url_string)
	linelist = re.findall(REGEX4LINKS, fileText, re.I)
	for aline in linelist:
		# Check for no match
		if str(aline[4]) != '' and str(aline[4]) != ' ':
			matches.append(aline[4])
	return matches
	# WebCrawlNode(GenNum, current_Alias, matches, url_string)

# def RegexPlainHTML()

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
	print(f'node.Children ======= {node.Children}')
	if len(node.Children) > 0:  # ensure that the node has children
		for child in node.Children:
				# iterate over the children and find their alias
			currentChildAlias = str(
				findChildAlias(child, state.state_node_list))
			if int(currentChildAlias) >= 0 and currentChildAlias not in node.ChildrenAliasList:
				Children_LinkNums = Children_LinkNums + \
					(currentChildAlias) + " "
				node.pushChildAlias(currentChildAlias)
	state.WriteToCSV(Children_LinkNums, node)  # write it to the csv
	if DEBUG is True:
		print("[G" + str(node.Generation) + "]alias:"+str(node.Alias) +
			  "\n\turl: " + str(node.URL) + "\n\tkids:" + str(Children_LinkNums))


def PRODUCER_PROCESS(producer_stall,SHARED_CHILDREN_Q, url_Q, completed):
			# ! PRODUCER add children to the CHILDREN_QQQQ
			producer_has_processed = []

			print('[ PRODUCER ] process executing')
			while completed.value is not 1 and producer_stall is not 150:
				producer_stall += 1
				if not url_Q.empty():
					producer_stall = 0
					get = url_Q.get()
					# print(get)
					if get not in producer_has_processed:
						producer_has_processed.append(get)
						print(f'[ PRODUCER ] has retrieved {get} ')
						children = [get] + Search4Links(get) 
						if children is not []:
							SHARED_CHILDREN_Q.put(children)


# creates nodes from the urls found by the producer; while doing a check to see if it has scanned the url before 
def CONSUMER_PROCESS(currentGenSize,NextGenSize, state_greatest_link_id, currentGenNumber,SHARED_CHILDREN_Q,nodeQ, completed, PROCESSED_LIST):
			#! CONSUMER WILL GET THE FRONT OF THE CHILD QUEUE AND
			#!  PUSH A WEBNODE TO THE NODEQ 
			print('*[ CONSUMER ]  process executing')

			while completed.value is not 1:
			# process the children ListObject at the head of the q
				if not SHARED_CHILDREN_Q.empty():
											# ! Generation update
						if currentGenSize.value <= 0:
							print('*[ CONSUMER ] is in if statement desu')
							currentGenNumber.value = currentGenNumber.value + 1
							currentGenSize.value = NextGenSize.value
							NextGenSize.value = 0
						currentGenSize.value = currentGenSize.value - 1
						childrenset = SHARED_CHILDREN_Q.get()
						url = childrenset.pop(0)


						# reconstruct the children in array form
						children = []
						for child in childrenset:
							children.append(child)
							if child not in PROCESSED_LIST:
								NextGenSize.value = NextGenSize.value + 1
								PROCESSED_LIST.append(child)
						print(f'*[ CONSUMER ] NextGenSize.value is = {NextGenSize.value} \t currentGenSize.value = {currentGenSize.value} \t currentGenNumber = {currentGenNumber.value} \tstate_greatest_link_id.value = {state_greatest_link_id.value} ')
						nodeQ.put(WebCrawlNode(currentGenNumber.value, state_greatest_link_id.value, children, url))




# ########### #
# MAIN METHOD #
# ########### #
if __name__ == '__main__':
	# initialize the state
	State = CrawlerState()
	# crawl urls
	generations = State.processLinks()

	# assign aliases to the nodes and print them to the csv
	for node in State.state_node_list:
		# assigns the generations as well
		asignAliasToChildren(node, State)
	cumList = State.getCumulativeChildList()
	most = State.findMostChildren()
	mm = State.findMostMentioned(cumList)
	if DEBUG is True:
		spacer = f"%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%\n"
		print(f"Node that was mentioned most: N{str(mm)}")
		print(
			f'Node with the most children is NODE[{most[0]}] with {most[1]} children')
		print(f'\n{spacer}\tCUMULATIVE-CHILD-LIST\n{spacer}{cumList}\n{spacer}')
	State.CSVWriteMost(mm)
	State.state_Output_CSV.close()
	# identify the generation of each node
	root = tk.Tk()
	# root.iconbitmap(r'favicon.ico')
	app = Application(generations, most[1], State.state_node_list, master=root)
	app.makeGrid()

	app.drawNodes(generations)
	app.drawNodesChildConnections()
	app.LabelGens()
	app.mainloop()
