#HANNAH FISHER
#MACHINE LEARNING

####################################
import math
import random
######################################
#given: the name of a file to read as a string
#do: read through each line of the file, collecting information and storing it in many different global variables
#return: nothing
def readData(fileName):
    global categoryTitle #name of category as dictionary key
    global allExamples #list of dictionaries where key is attribute type and value is actual thing
    global allAttributes  #list of attributes and category
    global attributesWithoutCategory #list of attributes excluding category
    allExamples = []
    dataFile = open(fileName, "r")
    firstLine = dataFile.readline() 
    allAttributes = firstLine.strip().split(",")
    attributesWithoutCategory = list(allAttributes)
    categoryTitle = attributesWithoutCategory.pop(0)
    for line in dataFile:
        lineList = line.strip().split(",")
        lineDictionary = {}
        for index in range(0,len(lineList )):
            lineDictionary.update({allAttributes[index]: lineList[index]})
        allExamples.append(lineDictionary)
    dataFile.close()
################################################
#given: a list of examples to train on
#do: fill in the two global dictionaries created below with the data from the training example lsit
#return: nothing
def getInfoFromData(trainingExampleList):
    global attributesAndOptionsDictionary #dictionary whose key is attribute type and value is list of possible options maybe including category
    global attributesAndOptionsDictionaryWithCategory 
    attributesAndOptionsDictionary = {}
    for attribute in allAttributes:
        attributesAndOptionsDictionary.update({attribute: []})    
    for example in trainingExampleList:
        for attribute in example.keys():
            if example[attribute] in attributesAndOptionsDictionary[attribute]:
                pass
            else:
                attributesAndOptionsDictionary[attribute].append(example[attribute])        
    attributesAndOptionsDictionaryWithCategory = dict(attributesAndOptionsDictionary)
    del attributesAndOptionsDictionary[allAttributes[0]]    
################################################
#node class
class node:
    def __init__(self, name):
        self.name = name
        self.childList = []
    def addChild(self, childNode):
        self.childList.append(childNode)
    def __str__(self):
        return self.name
################################################
#given: a list of examples and a list of attributes
#do: calculate entropy for each attribute, then use that to calculate gain for each attribute
#return: a dictionary whose key is an attribute and whose value is the information gain that attribute would yield
def calculateGainBetter(listOfExamples, listOfAttributes):
    attributeGainDictionary = {}
    for attribute in listOfAttributes:
        attributeValueCategoryOccurences = {} #key is attribute value and value is dictionary whose key is category option and value is number of occurences
        attributeValueOccurences = {} #key is attribute value and value is number of times it occurs among examples
        categoryOccurences = {} #key is category value and value is number of times it occurs among examples
        totalNum = len(listOfExamples)
        for attributeValue in attributesAndOptionsDictionary[attribute]:
            attributeValueCategoryOccurences.update({attributeValue: {}})
            attributeValueOccurences.update({attributeValue: 0.0})
            for categoryValue in attributesAndOptionsDictionaryWithCategory[categoryTitle]:
                attributeValueCategoryOccurences[attributeValue].update({categoryValue: 0.0})
                categoryOccurences.update({categoryValue: 0.0}) #super repetitive
        for example in listOfExamples:
            exampleAttributeValue = example[attribute]
            exampleCategoryValue = example[categoryTitle]
            attributeValueCategoryOccurences[exampleAttributeValue].update({exampleCategoryValue: attributeValueCategoryOccurences[exampleAttributeValue][exampleCategoryValue] + 1})
            attributeValueOccurences.update({exampleAttributeValue: attributeValueOccurences[exampleAttributeValue] + 1})
            categoryOccurences.update({exampleCategoryValue: categoryOccurences[exampleCategoryValue] + 1})
        attributeEntropy = 0.0
        for categoryValue in attributesAndOptionsDictionaryWithCategory[categoryTitle]:
            entropy = (categoryOccurences[categoryValue]/totalNum) * math.log((categoryOccurences[categoryValue]/totalNum), 2) 
            attributeEntropy -= entropy
        attributeGain = attributeEntropy
        for attributeValue in attributesAndOptionsDictionary[attribute]:
            subsetEntropy = 0.0
            for categoryValue in attributeValueCategoryOccurences[attributeValue].keys():
                categoryValueOccurences = attributeValueCategoryOccurences[attributeValue][categoryValue]
                if categoryValueOccurences > 0:
                    entropy =(categoryValueOccurences/attributeValueOccurences[attributeValue]) * math.log((categoryValueOccurences/attributeValueOccurences[attributeValue]), 2) 
                    subsetEntropy -= entropy
            gain = (attributeValueOccurences[attributeValue]/totalNum) * subsetEntropy
            attributeGain -= gain
        attributeGainDictionary.update({attribute: attributeGain})
    return attributeGainDictionary
#################################################
#given: a list of examples and a list of attributes 
#do: recursively create the tree
#return: the root node of the decision tree
def ID3(listOfExamples, listOfAttributes):
    listOfAllCategories = []
    for example in listOfExamples:
        listOfAllCategories.append(example[categoryTitle])
    listOfRepresentedCategories = list(set(listOfAllCategories))
    categoryFrequencyDictionary = {}
    for categoryType in listOfRepresentedCategories:
        counter = 0
        for category in listOfAllCategories:
            if category == categoryType:
                counter += 1
        categoryFrequencyDictionary.update({categoryType: counter})
    mostRepresentedCategory = listOfRepresentedCategories[0]
    for category in listOfRepresentedCategories:
        if categoryFrequencyDictionary[category] > categoryFrequencyDictionary[mostRepresentedCategory]:
            mostRepresentedCategory = category
    if len(listOfRepresentedCategories) == 1:
        return node(mostRepresentedCategory)
    if listOfAttributes == None or len(listOfAttributes) == 0:
        return node(mostRepresentedCategory)
    attributeGainDictionary = calculateGainBetter(listOfExamples, listOfAttributes)
    attributeList = attributeGainDictionary.keys()
    attributeList = sorted(attributeList, key = lambda attribute : attributeGainDictionary[attribute], reverse = True)
    greatestGainAttribute = attributeList[0]
    currentNode = node(greatestGainAttribute)
    attributeValueOccurenceDictionary = {} #key is attribute value and value is number of occurences
    attributeValueExamplesDictionary = {} #key is attribute value and value is list of examples which have that attribute value
    for attributeValue in attributesAndOptionsDictionary[greatestGainAttribute]:
        attributeValueOccurenceDictionary.update({attributeValue: 0})
        attributeValueExamplesDictionary.update({attributeValue: []})
    for example in listOfExamples:
        attributeValue = example[greatestGainAttribute]
        attributeValueOccurenceDictionary.update({attributeValue: attributeValueOccurenceDictionary[attributeValue] + 1})
        listForAttributeValue = attributeValueExamplesDictionary[attributeValue]
        listForAttributeValue.append(example)
        attributeValueExamplesDictionary.update({attributeValue: listForAttributeValue})
    for attributeValue in attributesAndOptionsDictionary[greatestGainAttribute]:
        nodeForAttributeValue = node(attributeValue)
        currentNode.addChild(nodeForAttributeValue)
        if attributeValueOccurenceDictionary[attributeValue] == 0:
            categoryChild = node(listOfAllCategories[0])
            nodeForAttributeValue.addChild(categoryChild)
        else:
            exampleSublist = attributeValueExamplesDictionary[attributeValue]
            attributeSublist = list(listOfAttributes)
            if greatestGainAttribute in listOfAttributes:
                attributeSublist.remove(greatestGainAttribute)
            nodeForAttributeValue.addChild(ID3(exampleSublist, attributeSublist))
    return currentNode
############################################### 
#given: a node and the current level of indentation
#do: recursively print the tree by indenting each successive level 
#return: nothing
def displayTree(node, currentIndentation):
    toPrint = "-"
    for indent in range(currentIndentation):
        toPrint += "--"
    toPrint += node.name
    print(toPrint)
    for child in node.childList:
        displayTree(child, currentIndentation + 1)
##############################################
#given: an example and the current node
#do: recursively determine the category of the example
#return: the category to which the example belongs 
def determineCategoryFromTree(example, currentNode):
    if len(currentNode.childList) == 0:
        return currentNode.name
    elif len(currentNode.childList) == 1:
        return determineCategoryFromTree(example, currentNode.childList[0])
    else: #current node must be an attribute
        nextPath = example[currentNode.name]
        for node in currentNode.childList:
            if node.name == nextPath:
                return determineCategoryFromTree(example, node)
            #may run into a problem if my testing examples have attribute values which were not present in training examples
        return determineCategoryFromTree(example, currentNode.childList[0])
        #^^this is kind of dumb, but better to get the wrong answer than an error
############################################
#given: a list of examples to test and the root node of the decision tree
#do: use the decision tree to categorize each example and calculate the percentage of succesful categorizations
#return: the percentage of correctly categorized examples
def test(testingExampleList, treeRoot):
    if len(testingExampleList) == 0:
        return "Sorry, you can't test on 0 examples..."
    correctCounter = 0.0
    for example in testingExampleList:
        category = determineCategoryFromTree(example, treeRoot)
        if category == example[categoryTitle]:
            correctCounter += 1
    percentageCorrect = correctCounter / len(testingExampleList) * 100
    return str(percentageCorrect)
#################################################
#given: the file name of the text file with the data and a number between 0 and 1 representing the portion of the data set to use for training, and a boolean which denotes whether to print out all the results
#do: everything - read file, create and display decision tree, test the decision tree
#return: the root of the tree created during ID3 algorithm 
def GO(textFileName, fractionForTraining, shouldPrint):
    readData(textFileName)
    random.shuffle(allExamples)
    numberForTraining = len(allExamples) * fractionForTraining
    trainingExampleList = allExamples[0: int(numberForTraining)]
    testingExampleList = allExamples[int(numberForTraining): len(allExamples)]
    getInfoFromData(trainingExampleList)
    treeRoot = ID3(trainingExampleList, attributesWithoutCategory)
    if shouldPrint:
        print("Data set: " + textFileName)
        print("Decision tree for categorizing this data set:")
        displayTree(treeRoot, 0)
        print("Number of training examples: " + str(len(trainingExampleList)))
        print("Number of testing examples: " + str(len(testingExampleList)))
        print("Percentage of correctly categorized examples in testing:")
        percentageCorrect = test(testingExampleList, treeRoot)
        print(percentageCorrect) #+ "%"
    return treeRoot
#############################################

#test data options:
# "tennis.txt"
# "mushrooms.txt"
# "congress84.txt"
# "titanic.txt"

GO("tennis.txt", 1, True)
print("--------------------------------")
GO("mushrooms.txt", 0.1, True)

#NOTES
#started over on the first night because my read data wasn't organizing the way I wanted
#had to redo the entire entropy and gain calculator because I was confused when I wrote it
#had big problems with the mushroom data set until I started shuffling the data before subdividing it 

#so apparently every single odor except for none is poisonous... ?? except anise, which is edible
#what the heck kind of color is buff ??