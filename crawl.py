import urllib.request
import re

#
#-------Do-------#
# - Retrieve and open input file containing URLs
# - Retrieve plain text HTML located at the URLs from file
# - Read 1 URL from file
# - Read all urls from file using loop
#
#


#-------Grading-------#
# • Graph is 7.5 pts
# • Parallelization 7.5 pts
# • Coding style and comments 5 pts
# • Sequential Web crawler 30 pts
#         o tags recognition
#         o graph building logic
#         o csv file and highest linked page count




# absolute links = 
# absolute link defines a specific location of the Web file or document including the protocol, the domain name, the directory/s and the name of the document itself
class WebCrawl():

        def __init__(self):
                self

        def __str__(self):
                return str(self)


def URLtoHTMLstring(url_string):
        page = urllib.request.urlopen(url_string)
        pageText = page.read()
        # print(str(pageText))
        return str(pageText)

def regexFindAllLinksInURL(url_string): 
        # filevar = open(url_string, 'r')
        fileText = URLtoHTMLstring(url_string)
        print("\n")
        # print(fileText)
        matches = [ ]
        linelist = re.findall(r'(?:((href|src)(\s)?=(\s)?))?[\"\'](((\s)?(http|ftp)?s?://)(.*?))?[\"\'](\s)?', fileText,re.I)
        # linelist = re.findall('(?:(href( )?=( )?))"((http|ftp)s?://.*?)"', fileText,re.I)
#
        for aline in linelist:
                # print(str(aline))
                if str(aline[4]) != '':
                        print(str(aline[4]) )
                        
                


        if(len(linelist) != 0): matches.append(linelist)
        # links = re.findall(, html)
        # filevar.close()
        return matches


def fileToList(filename):
        file = open(filename, 'r')
        urls = file.read().splitlines()
        return urls



def main():
        # extract the urls from the txt file (one per line) 
        # place them into a table
        urlList= fileToList('urls6.txt')

        
        # retrieve the html from the url
        htmlList=URLtoHTMLstring(urlList[2])
        
        regexFindAllLinksInURL(urlList[2])
        # resulting_html = str(getHTML(countdict))
        print(urlList[0])
    


# matchObj = re.match( r'(.*) are (.*?) .*', line, re.M|re.I)

# if matchObj:
#    print "matchObj.group() : ", matchObj.group()
#    print "matchObj.group(1) : ", matchObj.group(1)
#    print "matchObj.group(2) : ", matchObj.group(2)
# else:
#    print "No match!!"


# fo.write( "Python is a great language.\nYeah its great!!\n");
main()
