#HANNAH FISHER
#this is super experimental...no idea if this will work or do anything

from MachineLearning import *

treeRoot = GO("mushrooms.txt", 0.5, True)

def tryToGetTheInputs(currentNode):
    if len(currentNode.childList) == 0:
        print "This example is: " + currentNode.name 
    elif len(currentNode.childList) == 1:
        tryToGetTheInputs(currentNode.childList[0])
    else:
        print "Need some info about " + currentNode.name #+ " ... please type your response in quotation marks"
        print "Here are your options:"
        for child in currentNode.childList:
            print "   " + child.name
        gotAttribute = raw_input("Which one best describes what you got? ")
        for child in currentNode.childList:
            if child.name == gotAttribute:
                tryToGetTheInputs(child)
        print "congrats! u either got to the end or u messed up... time to start over" 
        
        
tryToGetTheInputs(treeRoot)

#well that was fun
#why does the input have to be in quotes to not get an error??

