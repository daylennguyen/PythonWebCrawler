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
DEBUG = False

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
                 Node_List=[], greatest_link_id=0,
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
        self.currentGenNumber = 0
        self.currentGenSize = self.lenGenZero
        self.NextGenSize = 0
        self.crawl()
        return self.currentGenNumber

    def crawl(self):
        while(len(self.state_ToBeProcessed_URL_List) >
              0 and len(self.state_Processed_URL_List) < 75):
            # Count the number of each generation
            self.generationUpdate()
            url = self.state_ToBeProcessed_URL_List.pop(0)
            if url not in self.state_Processed_URL_List:
                children = Search4Links(
                    self.state_greatest_link_id, url, self.currentGenNumber)
                currentNode = WebCrawlNode(
                    self.currentGenNumber, self.state_greatest_link_id, children, url)
                self.pushNode(currentNode)
                # process the children-table of the current link
                for child in currentNode.Children:
                    # Avoid reprocessing
                    if child not in self.state_Processed_URL_List:
                        self.NextGenSize = self.NextGenSize + 1
                        self.state_ToBeProcessed_URL_List.append(child)

    def generationUpdate(self):
        if self.currentGenSize <= 0:
            self.currentGenNumber = self.currentGenNumber + 1
            self.currentGenSize = self.NextGenSize
            self.NextGenSize = 0
        self.currentGenSize = self.currentGenSize - 1
        return self.currentGenSize

    def pushNode(self, node):
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


def Search4Links(current_Alias, url_string, GenNum):
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

# ########### #
# MAIN METHOD #
# ########### #


def main():
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
    root.iconbitmap(r'favicon.ico')
    app = Application(generations, most[1], State.state_node_list, master=root)
    app.makeGrid()

    app.drawNodes(generations)
    app.drawNodesChildConnections()
    app.LabelGens()
    app.mainloop()


main()
