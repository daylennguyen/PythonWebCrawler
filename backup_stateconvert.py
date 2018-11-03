import queue
import re
import urllib.request

import CONSTANTS

#-------Do------------------------------------------------------------------------------#
# [x] Retrieve and open input file containing URLs
# [x] Retrieve plain text HTML located at the URLs from file
# [x] Read 1 URL from file
# [x] Read all urls from file using loop
# [x] Create an CSV file of the information containing alias' for kids
# [x] Create a graph using KTinker written classes
# [x] add Parallization
# [x] Graphing -
#			Place the links contained within the link doc in the middle
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
	#				When the state is initialized, this array is appended with the URLs from the given file. (SEE CONSTANTS.py)
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
	#				Initialized to 0, unless told otherwise; also represents the 
	#				current amount of assigned aliases.
	#
	def __init__(self, ToBeProcessed_URL_List=[], Processed_URL_List=[], Node_List=[], greatest_link_id=0):
		# ordered list of links which have been scanned
		self.state_Processed_URL_List = Processed_URL_List

		# Processed URLs, converted to WebCrawlerNodes
		self.state_node_list = Node_List

		# The Counter for the number of unique links found
		self.state_greatest_link_id = greatest_link_id

		# Initialize the list with the Links in the txtfile
		self.state_ToBeProcessed_URL_List = self.fileToList(CONSTANTS.URL_FILE)
		
		# The file where we will output our csv values
		self.state_Output_CSV = open(CONSTANTS.OUTPUT_CSV_FILE, "w")
	
	#ToString function; printed when calling str(  ) on this object 
	def __str__(self):
		return "\nToBeProcessed_URL_List:\n\t" +str(self.state_ToBeProcessed_URL_List) + "\nProcessed_URL_List:\n\t" + str(self.state_Processed_URL_List) + "\nNode_List:\n\t" +str(self.state_node_list) + "\ngreatest_link_id:\n\t" +str(self.state_greatest_link_id)

	# Retrieves the file from the root directory (./) 
	# then extracts each line as an index within the urls file
	def fileToList(self, filename):
		file = open(filename, 'r')
		urls = file.read().splitlines()
		file.close()
		return urls
	
	def processLinks(self):
		# psudo queue; uses a list and pops index zero during each iteration
		while(len(self.state_ToBeProcessed_URL_List) > 0 and len(self.state_Processed_URL_List) < 75):
			url = self.state_ToBeProcessed_URL_List.pop(0)
			if url not in self.state_Processed_URL_List:
				currentNode = FindAllLinksInURL(self.state_greatest_link_id, url)
				# Increment the alias
				self.state_greatest_link_id += 1
				self.state_node_list.append(currentNode)

			# Do not process the same link multiple times
			if url not in self.state_Processed_URL_List:
				self.state_Processed_URL_List.append(url)
				# process the children-table of the current link
				for child in currentNode.Children:
					# Avoid reprocessing
					if child not in self.state_Processed_URL_List:
						self.state_ToBeProcessed_URL_List.append(child)




# 	Representation of each parent/Link (Which may or may not have a parent)
# 	
#	@ChildrenAliasList:	A list of the aliases given to each child; will assist when drawing graph.
#
#	@Children:	Contains the string form of each child link found within the html of this node
#
#	@Alias: Unique alias assigned during processLinks, found in the WebCrawlerState; this node 
#		makes the relationship between nodes more distinguishable in many cases.
#
#   @URL: The URL of this Node in the form of a string
#
class WebCrawlNode():

	def setChildren(self, Children):
		self.Children = Children
		return self

	# 
	def pushChildAlias(self, LinkAlias):
		self.ChildrenAliasList.append(LinkAlias)
		return self.ChildrenAliasList
	
	#Constructor which is initiated during instantiation of a WebCrawlNode 
	def __init__(self, Alias, Children_Array=[], URL_String="", ChildrenAliasList=[]):
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
def FindAllLinksInURL(current_Alias, url_string):
	fileText = URLtoHTMLstring(url_string)
	matches = []
	linelist = re.findall(
		r'(?:(a (\s)?href(\s)?=(\s)?))[\"\'](((\s)?(http|ftp)?s?://)(.*?))?[\"\'](\s)?', fileText, re.I)
	for aline in linelist:
		# Check for no match
		if str(aline[4]) != '' and str(aline[4]) != ' ':
			matches.append(aline[4])
	return WebCrawlNode(current_Alias, matches, url_string)

# Function used to match a node's children with their given alias. 
def findChildAlias(childsLink, node_list):
	result = -1
	for node in node_list:
		if(node.URL == childsLink):
			result = node.Alias
	return result

########################################
							#############
							#MAIN METHOD#		
							##############
########################################
def main():
	State = CrawlerState()
	State.processLinks()

	State.state_Output_CSV.write(CONSTANTS.HEADER)
	
	print(CONSTANTS.HEADER)
	
	for node in State.state_node_list:
		Children_LinkNums = ""
		currentChildAlias = ""
		node.ChildrenAliasList = [ ]
		if len(node.Children) > 0:
			for child in node.Children:
				currentChildAlias = str(findChildAlias(child, State.state_node_list))
				
				if currentChildAlias != -1:
					Children_LinkNums = Children_LinkNums + (currentChildAlias) + " "
					node.pushChildAlias(currentChildAlias)
		print("alias:"+str(node.Alias) + "\n\turl: " + str(node.URL) + "\n\tkids:" + str(Children_LinkNums))
		State.state_Output_CSV.write("\n"+str(node.Alias) + "," + str(node.URL) + "," + str(Children_LinkNums))


	for node in State.state_node_list:
		print(str(node.ChildrenAliasList))

	State.state_Output_CSV.close()
main()
