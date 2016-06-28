import csv
import operator


def populateBreedDict(breedFile):
       breedDict = {}
       for row in breedFile:
              breedDict[row[0]] = row[1]
       return breedDict



def dictLayers(inDict):
       """ takes the dictionary, and returns a selection of incrasing layer variability   smallest node is outList[0] """
       outDict = {}
       outList = []
       count = 0
       for key, values in inDict.items():
              if count == 0:
                     layer = 0
                     count = 1
                     for value in values:
                            outDict[layer]= [value]
                            layer +=1
                            
              if count > 0:
                     layer = 0
                     for value in values:
                            if not value in outDict[layer]:
                                   outDict[layer].append(value)
                            layer +=1

       resDict = {}
       for layer, value in outDict.items():
              resDict[layer] =  len(value)
              

       sortedDict = sorted(resDict.items(), key=operator.itemgetter(1))  # returns tuple
       
       for layer in sortedDict:
              outList.append(layer[0])
       return outList


def obsLayers(inListOfObservations):
       """ takes the dictionary, and returns a selection of incrasing layer variability   smallest node is outList[0] """
       outDict = {}
       outList = []
       count = 0
       
       for key in inListOfObservations:
              #key  =  observation(key)
              
              VarList = key.listVars()
              


              
              if count == 0:
                     layer = 0
                     count = 1
                     for value in VarList:
                            outDict[layer]= [value]
                            layer +=1
                            
              if count > 0:
                     layer = 0
                     count +=1
                     for value in VarList:
                            if not value in outDict[layer]:
                                   outDict[layer].append(value)
                            layer +=1

       resDict = {}
       for layer, value in outDict.items():
              resDict[layer] =  len(value)
              

       sortedDict = sorted(resDict.items(), key=operator.itemgetter(1))  # returns tuple
       
       for layer in sortedDict:
              print layer
              outList.append(layer[0])
       print count
       return outList
            
              

##class Observation:
##       """ individual observation, feeds nodes """
##
##
##       def __init__(self, ident):
##              self.id = ident
##              self.classVar = ''
##              self.age = 0
##              self.Type = ''
##              self.subType = ''
##              self.countOccurance = 0



class Node:
       """Define a node """


       
       def __init__(self, Layer,Contains,Parent,Child):
              self.Layer = Layer
              self.Parents = [Parent]
              self.Children = [Child]
              self.Contains = [Contains]
              
              


class observation:

       """ Observation class to store values """

       #classifier = 0
       def __init__(self, AnimalID):
              self.classVar = ''
              self.AnimalID = AnimalID
              self.name = 0
              self.OutcomeType = ''
              self.OutcomeSubtype = ''
              self.kind = 0.5
              self.SexuponOutcome = 0
              self.AgeuponOutcome = 0
              self.breed = 0
              self.Color = ''

              self.Zscore = 0

       def animalKind(self, animal):
              if animal == 'Cat':
                     self.kind = 1
              if animal == 'Dog':
                     self.kind = 0
              
       def animalBreed(self, breed, breedDict):
              if self.kind == 1:
                     # it's a cat
                     if '/' in breed or 'Mix' in breed or 'mix' in breed:
                            # its a mix
                            self.breed = -1
                     else:
                            self.breed = -2
              if self.kind == 0:
                     # dogs
                     #listofWords = breed.split(' ')
                     found = False
                     for key, value in breedDict.items():
                            
                            listofWords = str(key).split(' ')
                            for el in listofWords:
                                   
                                   if el in breed:
                                          self.breed = (float(value) * 4)
                                          found = True
                                   
                       #~ default            
                     if found == False:       
                            self.breed = 1
                            
       def hasName(self,name):
              if len(name) > 1:
                     self.name = 1
              else:
                     self.name = -1
                     
                     
       def chooseAge(self,age):
              if 'months' in age or 'weeks' in age:
                     self.AgeuponOutcome = 5 ####
              if 'years' in age:
                     if int(age.split(' ')[0])> 4 and int(age.split(' ')[0])<8:
                            self.AgeuponOutcome = 1
                     if int(age.split(' ')[0])<=  4 :
                            self.AgeuponOutcome = 3
                     if int(age.split(' ')[0])> 8 :
                            self.AgeuponOutcome = -1

       def chooseSex(self, sex):
              if 'Intact' in sex:
                     self.SexuponOutcome = 0
              if 'Unknown' in sex:
                     self.SexuponOutcome = 1
              else:
                     self.SexuponOutcome = 2

       def chooseClass(self, altClass):
              if self.classVar == altClass:
                     return 1
              else:
                     return 0
              
       def listVars(self):
              outPut = []
              outPut.append(self.kind)
              outPut.append(self.name)
              outPut.append(self.breed)
              outPut.append(self.AgeuponOutcome)
              outPut.append(self.SexuponOutcome)
              return outPut

       def dictVars(self):
              outPut = {}
              outPut[kind] = (self.kind)
              outPut[name] = (self.name)
              outPut[breed] = (self.breed)
              outPut[AgeuponOutcome] = (self.AgeuponOutcome)
              outPut[SexuponOutcome] = self.SexuponOutcome           
              return outPut
##
##       def getVal(string):
##              
##                     
##



# gain ration implementation
# = delta I / -sumOfAll[1-k]( 1/k)log2(1/k)



class Tree:
       """Decision tree """

##       def createNode(self, observation):

##       def testNode(observation, layer):
##              if layer in self.nodeDict:
##                     if observation in nodeDict[layer]:
##                            print 'out'
       def testNode(self, observation, Layer, parent ):
              exists = False
              for element in Layer:
                     if observation in element.Contains and parent in element.Parents:
                            exists = True
              return exists
              
       def addNode(self, observation, layerNumber, parent, child):
              Layer = self.nodeDict[layerNumber]
              exists = self.testNode(observation, Layer,parent)
              if exists == False:
                     newNode = Node(layerNumber,observation,parent,child)
                     Layer.append(newNode)
              if exists == True:
                     for element in Layer:
                            if observation in element.Contains and parent in element.Parents:
                                   if not child in element.Children:
                                          element.Children.append(child)


              return Layer


##       def calcGini(total, classModel):
              # GINI = 1-(sumAll[classes] (sqrt(fractionOfRecordsInClass))         

       def addLayer(self):
              
              layer = len(self.nodeDict) 
              self.nodeDict[layer] = []
              self.layers +=1
              return layer
              
##       def addNode(self):
##       def findBestSplit(ParentNode, newObservation):
            
       def __init__(self):
              self.layers = 0
              self.nodes = 0
              self.nodeDict = {}
              self.score = 0
              



# starting in first row,  create a tree.
# add 1st node to tree, 


with open('../../ANimalShelterExcercise/train.csv','r') as in_raw,  open('../../ANimalShelterExcercise/DogBreeds.tsv' ,'r') as breedRaw:
       infile = csv.reader(in_raw, delimiter = ',')
       infile.next()
       # need access to input data twice, so store it in dicitonary
       inDict = {}
       LabelDict = {}
       LabelList = []
       DecTree = Tree()

       Ident = 0

       breedFile = csv.reader(breedRaw, delimiter = '\t')
       breedDict = populateBreedDict(breedFile)

       



       
       for row in infile:

              
              obs = observation(row[0])
              obs.classVar = row[3]
              obs.sybClassVar = row[4]
              obs.animalKind(row[5])
              obs.animalBreed(row[8],breedDict)
              obs.AnimalID = row[0]
              obs.hasName(row[1])                     
              obs.chooseAge(row[7])
              obs.chooseSex(row[6])
              

              LabelList.append(obs)

              
##              inDict[Ident] = [row[0],row[1],row[2],row[3],row[4]]
##              LabelDict[row[0]] = row[5]
              Ident +=1


       # generate the tree:

              
       
       #ranking = dictLayers(inDict)
       ranking = obsLayers(LabelList)


        

       # ranking is    kind name sex age breed
       ranking[0] = 'kind'
       ranking[1] = 'name'
       ranking[2] = 'SexuponOutcome'
       ranking[3] = 'AgeuponOutcome'
       ranking[4] = 'breed'
#ranking.append(-1)


       for number in range(0,len(ranking)):
              layer = DecTree.addLayer()
       

##       using an observationList here

       # lets start making layers...

       print 'Building Big tree'

       # follow least variable to most variable approach for now


       # populate outside the main loop
       


       
       for key in LabelList:
              rank = 0
              
              
              for number in ranking:
                     
                     # load parent and child if applicable,  if not pass -1
                     if rank > 0 and rank < len(ranking)-1 :
                            print rank
                            parent = ranking[rank-1]
                            child = ranking[rank+1]
                     elif rank == 0:
                            parent = -1
                            child = ranking[rank+1]
                     elif rank == len(ranking)-1:
                            parent = ranking[rank-1]
                            child = -1

                     

                     value = vars(key)[number]     
                     parent = vars(key)[parent]  if parent != -1  else  'Root'
                     child  = vars(key)[child]  if child != -1   else key.classVar

                     # add node here
                     DecTree.addNode(value, rank, parent, child)
                     
                     rank+=1


       print 'Pruning tree'


       # impurity measures are consistent, more or less equal in performance,  so I'm implementing GINI
       # GINI = 1-(sumAll[classes] (sqrt(fractionOfRecordsInClass))

       # get weighted average for any two nodes 

       for key, values in DecTree.nodeDict.items():
              for value in values:
                     print value.Layer,value.Parents, value.Contains, value.Children




       
                     
              
              
