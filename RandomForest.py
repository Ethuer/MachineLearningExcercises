import csv
import operator
import random
import collections
import math

compare = lambda x, y: collections.Counter(x) == collections.Counter(y)

def compareList(L1,L2):
       count = 0
       equal = True
       for element in L1:
              if element != L2[count]:
                     equal = False
              count += 1
       return equal
                     


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
              self.countObserv = 1
              self.Parents = Parent
              self.Children = [Child]
              self.Contains = [Contains]
              self.active = True
              
              


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
              if 'Neutered' or 'Spayed' in sex:
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

       def pruneTree(self):
              for key, values in self.nodeDict.items():
                     for value in values:

                            # calc gini for downstream nodes to check for current split
                            DecTree.calcGini(value)
                            
                            print 'Layer :', key, ' Node :', value.Contains,'Parent : ',value.Parents, 'Children : ', value.Children,' Count :' ,  value.countObserv


       
       def testNode(self, observation, Layer, parent ):
              exists = False
              for element in Layer:
                     if observation in element.Contains and parent == element.Parents : #cmp(parent , element.Parents) != 0 :#compareList(parent , element.Parents) == True :
                            exists = True
              return exists


       # addNode checks if node exists by having the same parent
       def addNode(self, observation, layerNumber, parent, child):
              
              Layer = self.nodeDict[layerNumber]
              exists = self.testNode(observation, Layer,parent)
              if exists == False:
                     
                     newNode = Node(layerNumber,observation,parent,child)
                     Layer.append(newNode)
                     
              if exists == True:
                     for element in Layer:
                            
                            if observation  in  element.Contains and parent ==  element.Parents:#compareList(parent , element.Parents) == True:
                                   if not child in element.Children:
                                          element.Children.append(child)
                                   element.countObserv +=1
              return nodecount


##       def combineNodes(self, node, Children ):
              
              


       def calcGini(self,node):
              ChildNodes = self.downstreamNodes(node)
              total = node.countObserv
              sumList = []
##              print len(ChildNodes)
              for child in ChildNodes:
                     residual = (total - child.countObserv)
                     arg1 = (float(child.countObserv)/float(total))* ((float(child.countObserv)/float(total)))
                     arg2 = (float(residual)/float(total))*(float(residual)/float(total))
##                     print arg1, arg2
                     Gini = 1- arg1 - arg2
                     fraction = (float(child.countObserv) / float(total))
                     print Gini
                     sumList.append((Gini*fraction))

              TotalGini = sum(sumList)

              
##                     print fraction1, fraction
                     
##                     sumList.append(fraction)
##              GiNi = 1-(sum(sumList))
                        
##              print GiNi, total
              
              return TotalGini
              # GINI = 1-(sumAll[classes] (sqrt(fractionOfRecordsInClass))         

##       def pruneNodes(self):
##
##       def joinNodes(self):
              
              

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


       def downstreamNodes(self,node):
              # finds children,  finds gini, removes Nodes
              newRoot = node.Parents
              newRoot.append(node.Contains[0])
              ChildNodes = []

##              print node.Children

              
              for key, values in self.nodeDict.items():
                     if key == node.Layer +1 :
                            for value in values:
                                   if sorted(node.Parents) == sorted(value.Parents):
##                                          print sorted(newRoot) , sorted(value.Parents)
                                          
                                          
                                          ChildNodes.append(value)
                     
              return ChildNodes
       
              



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
              

              if random.randrange(0,100) == 7:
                     LabelList.append(obs)

              
##              inDict[Ident] = [row[0],row[1],row[2],row[3],row[4]]
##              LabelDict[row[0]] = row[5]
              Ident +=1


       # generate the tree:

              
       
       #ranking = dictLayers(inDict)
       ranking = obsLayers(LabelList)


##       # create a tree
##       for element in LabelList:
##              print element.classVar
##              

##
##
##
##
##       
##
       # ranking is    kind name sex age breed
       ranking[0] = 'kind'
       ranking[1] = 'name'
       ranking[2] = 'SexuponOutcome'
       ranking[3] = 'AgeuponOutcome'
       ranking[4] = 'breed'
###ranking.append(-1)
##
##
       for number in range(0,len(ranking)):
              layer = DecTree.addLayer()
##       
##
####       using an observationList here
##
##       # lets start making layers...
##
##       print 'Building Big tree'
##
##       # follow least variable to most variable approach for now
##
##
##       # populate outside the main loop
##       
##
##
##       # lets build the biggest tree, then find the coverage per node to cut them loose
       nodecount = 0
       for key in LabelList:
              rank = 0
              
              
              for number in ranking:
                     predec = rank
                     predecessorList = []
                     predecessorList.append('Root')
                     
                     # load parent and child if applicable,  if not pass -1
                     if rank > 0 and rank < len(ranking)-1 :
                            #print rank
                            parent = ranking[rank-1]
                            child = ranking[rank+1]
                     elif rank == 0:
                            parent = -1
                            child = ranking[rank+1]
##                            predecessorList.append('Root')
                            
                     elif rank == len(ranking)-1:
                            parent = ranking[rank-1]
                            child = -1

                     while(predec > 0):
                            predec -=1
                            predecessorList.append(vars(key)[ranking[predec]])
                     


                     value = vars(key)[number]     
##                     parent = predecessorList  if parent != -1  else  ['Root']
                     child  = vars(key)[child]  if child != -1   else key.classVar

                     # add node here

##                     nodeCode = node.getNodeCode()
              
                     DecTree.addNode(value, rank,predecessorList, child)
                     
                     rank+=1
##            
##
       print 'Pruning tree'

       DecTree.pruneTree()
##       # this one is actually not too big.  I'll assign by ant crawling probabilities
##
##
##       # impurity measures are consistent, more or less equal in performance,  so I'm implementing GINI
##       # GINI = 1-(sumAll[classes] (sqrt(fractionOfRecordsInClass))
##
##       # get weighted average for any two nodes
                     
##





       
##
##
##
##
##       
                     
              
              
