##################################################
# Submission for: Arshdeep Gill and Daylen Nguyen
# -----------------------------------------------
# --FiltersLambdaRegex.py------------------------
# -----------------------------------------------
#  Python script which contains various functions
#  correlating with Filters, Lambda functions and 
#  Regular Expressions
#
##################################################
import re


# tests whether the arg(x) is even 
def isEven(x): return (x%2 == 0)


# tests the arg(x) to find whether it is positive
def isPositive(x): return (x>0)


# tests whether the arg(x) is odd
def isOdd(x): return (x%2 == 1)


# A filter which takes in a function 
# (afunction) as a parameter then applies it
# to the given list (aList). 
# If the return of the function call is true, 
# the element is to which it was called will be added to the result 
def myFilter(afunction, aList):
	result = []
	for el in aList:
		if afunction(el) == True:
			result.append(el)
	return result

# Depending on the integer passed, the function will return an anonymous function
# 1 = addition; 2 = multiplication
def add_or_multiply(choiceOneOrTwo):
	# 1 = add
	if choiceOneOrTwo == 1:
		result = lambda numOne, numTwo: numOne+numTwo
	# 2 = multiply
	elif choiceOneOrTwo == 2:
		result = lambda numOne, numTwo: numOne*numTwo
	return result

#//////// //////// //////// REGEX EXERCISES START //////// //////// ////////#

# Searches a file for the regex: All words ending in 'y' (72)
def wordEndY(file): return regexFindAllInFile(file, r"\b(\w*.y)\b")


# Searches a file for the regex: All words starting with 'a' and ending in 'r' (4)	
def aWordR(file): return regexFindAllInFile(file, r"\b(a+\w*.r)\b")	


# Searches a file for the regex: All four-letter words where the middle two letters are vowels (14)
def fourLettersMiddleTwoVowels(file): return regexFindAllInFile(file, r"\b\w[aeiou]{2}\w\b")	


# iterates through each line in the file while searching for matches 
# correlating with the regular expression string, restring
def regexFindAllInFile(file, restring): 
	matches = 0
	for aline in file:
	    linelist = re.findall(restring, aline, re.I)
	    if(len(linelist) != 0): print(linelist)
	    matches += len(linelist)
	file.close()
	return matches


# Main function: executes tests for the functions above.
def main():
	StringList = [ 'apple', 'banana', 'cherry', 'apricot' ]
	print(myFilter(
		lambda x: x[0] == 'a', StringList)
	)
	print(myFilter(
		lambda x: x[0] == 'a', StringList)
	)

	NumList= [-1, 2, 3, 4]
	print("myFilter(isEven, NumList) = " + str(myFilter(isEven, NumList)))
	print("myFilter(isPositive, NumList) = " + str(myFilter(isPositive, NumList)))
	print("myFilter(isOdd, NumList) = " + str(myFilter(isOdd, NumList)))

	print("add_or_multiply(1)(1,2) = "+str(add_or_multiply(1)(1,2)))
	print("add_or_multiply(2)(1,2) = "+str(add_or_multiply(2)(1,2)))
	print("add_or_multiply(1)(25,75) = "+str(add_or_multiply(1)(25,75)))

#//////// //////// //////// REGEX TESTS START //////// //////// ////////#
	filevar = open("declaration.txt", 'r')	
	print("Len is = "+str(wordEndY(filevar)))
	print("/*********************************************/")
	filevar = open("declaration.txt", 'r')	
	print("Len is = "+str(aWordR(filevar)))
	print("/*********************************************/")
	filevar = open("declaration.txt", 'r')	
	print("Len is = "+str(fourLettersMiddleTwoVowels(filevar)))

main()

# End script
