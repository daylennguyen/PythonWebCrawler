import queue
import re
import urllib.request

import CONSTANTS

#-------Do------------------------------------------------------------------------------#
# - Retrieve and open input file containing URLs
# - Retrieve plain text HTML located at the URLs from file
# - Read 1 URL from file
# - Read all urls from file using loop
#-------Grading------------------------------------------------------------------------#
# • Graph is 7.5 pts
# • Parallelization 7.5 pts
# • Coding style and comments 5 pts
# • Sequential Web crawler 30 pts
#         o tags recognition
#         o graph building logic
#         o csv file and highest linked page count
# ------------------------------------------------------------------------------------------#


class CrawlerState():
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

	def __str__(self):
		return str(self)

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





class WebCrawlNode():
	def setChildren(self, Children):
		self.Children = Children
		return self

	def pushChildAlias(self, LinkAlias):
		self.ChildrenAliasList.append(LinkAlias)
		return self.ChildrenAliasList

	def __init__(self, LinkNumber, Children_Array=[], URL_String="", ChildrenAliasList=[]):
		self.ChildrenAliasList = ChildrenAliasList
		self.Children = Children_Array
		self.LinkNumber = LinkNumber
		self.URL = URL_String

	def __str__(self):
		return str("----------\n"+self.URL + "\n\n\t ***children:***" + str(self.Children))


def URLtoHTMLstring(url_string):
	try:
		page = urllib.request.urlopen(url_string)
		pageText = page.read()
	except:
		pageText = "invalid txt"
	return str(pageText)


def FindAllLinksInURL(current_linkNumber, url_string):
	fileText = URLtoHTMLstring(url_string)
	matches = []
	linelist = re.findall(
		r'(?:(a (\s)?href(\s)?=(\s)?))[\"\'](((\s)?(http|ftp)?s?://)(.*?))?[\"\'](\s)?', fileText, re.I)
	for aline in linelist:
		if str(aline[4]) != '' and str(aline[4]) != ' ':
			matches.append(aline[4])
	return WebCrawlNode(current_linkNumber, matches, url_string)


# where the processed list is appended with urls in txtdoc
# and the tobeprocessed list is filled with their children


# def InitializeWebCrawler(CurrProcessed_URL_List, ToBeProcessed_URL_List):

#     return processed


def findChildLinkNumber(childsLink, node_list):
	result = -1
	for node in node_list:
		if(node.URL == childsLink):
			result = node.LinkNumber
	return result


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
				currentChildAlias = str(findChildLinkNumber(child, State.state_node_list))
				
				if currentChildAlias != -1:
					Children_LinkNums = Children_LinkNums + (currentChildAlias) + " "
					node.pushChildAlias(currentChildAlias)
		print("alias:"+str(node.LinkNumber) + "\n\turl: " + str(node.URL) + "\n\tkids:" + str(Children_LinkNums))
		State.state_Output_CSV.write("\n"+str(node.LinkNumber) + "," + str(node.URL) + "," + str(Children_LinkNums))
		# print(str(node.ChildrenAliasList))

	for node in State.state_node_list:
		print(str(node.ChildrenAliasList))

	State.state_Output_CSV.close()

	
# print(currentNodeChildren_LinkNumArray)

# current_linkNumber+=1

# node_list.append(node)


# for child in node.Children:
#         if child not in Processed_URL_List:
#                 ToBeProcessed_URL_List.append(child)
# print(child)
# print("#########################")
main()
