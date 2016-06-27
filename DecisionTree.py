import csv
import operator

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

       
                     
              

class Observation:
       """ individual observation, feeds nodes """


       def __init__(self, ident):
              self.id = ident
              self.classVar = ''
              self.age = 0
              self.Type = ''
              self.subType = ''



class Node:
       """Define a node """


       
       def __init__(self, Layer,Contains,Parent,Child):
              self.Layer = Layer
              self.Parents = [Parent]
              self.Children = [Child]
              self.Contains = [Contains]
              
              


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


with open('../DecionTreetestset.txt','r') as in_raw:
       infile = csv.reader(in_raw, delimiter = '\t')
       infile.next()
       # need access to input data twice, so store it in dicitonary
       inDict = {}
       LabelDict = {}
       DecTree = Tree()

       Ident = 0
       for row in infile:
              inDict[Ident] = [row[0],row[1],row[2],row[3],row[4]]
              LabelDict[Ident] = row[5]
              Ident +=1


       # generate the tree:
       ranking = dictLayers(inDict)

       # lets start making layers...

       print 'Building Big tree'

       # follow least variable to most variable approach for now


       # populate outside the main loop
       ranking.append(-1)
       for number in range(0,len(ranking)):
              layer = DecTree.addLayer()


       
       for key in range(0,len(inDict)):
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

                     value = inDict[key][number]
                     parent = inDict[key][parent] if parent != -1  else  'Root'
                     child  = inDict[key][child] if child != -1   else LabelDict[key]

                     # add node here
                     DecTree.addNode(value, rank, parent, child)
                     
                     rank+=1


       print 'Pruning tree'


       for key, values in DecTree.nodeDict.items():
              for value in values:
                     print value.Layer,value.Parents, value.Contains, value.Children




       
                     
              
              
