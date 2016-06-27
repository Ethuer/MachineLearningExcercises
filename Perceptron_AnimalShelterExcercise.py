import csv
from numpy import array, dot, random
from random import choice
import numpy as np
import math

unitStep = lambda x: 0 if x < 0 else 1

def sigmoidStep(z):
    #s = 1.0 / (1.0 + np.exp(-1.0 * z))
    s = 1.0 / (1.0 + math.exp(-1.0 * z))
    return s


n = 5000000
alpha = 0.000005


# 4 outcome types:  'Return_to_owner', 'Euthanasia', 'Adoption', 'Transfer', 'Died'
# each gets a perceptron



def formatE(packList):
       outlist = []
       for element in packList:
              if element > 0.001:
                     outlist.append(element)
              else:
                     outlist.append(0)
       return outlist
       


def findMax(ListIn):
       sort = sorted(ListIn)
       maxim = sort[4]
       second = sort[3]
       third = sort[2]
       
       maxi = float(maxim) * 3

       fragment = 1/( float(maxi) + float(second) + float(third) )

       maxi = float(maxi) * fragment
       seco = float(second) * fragment
       thir = float(third) * fragment
       listDict = {}
       diCount = 0
       for element in ListIn:
           listDict[diCount] = element
           diCount += 1

        
       outList = []

       for element in ListIn:
              if float(element) == float(sort[4]):
                     outList.append(maxi)
              if float(element) == float(sort[3]):
                     outList.append(seco)
              if float(element) == float(sort[2]):
                     outList.append(thir)
              if float(element) == float(sort[1]):
                     outList.append(0)
              if float(element) == float(sort[0]):
                     outList.append(0)
                     

       return outList








def populateBreedDict(breedFile):
       breedDict = {}
       for row in breedFile:
              breedDict[row[0]] = row[1]
       return breedDict

def bayesCorrect(score,secndscore, amount, total):
       try:
              amount = float(amount)
              total = float(total)

              return (score*(amount/total))/(float(score*(amount/total))+ float(secndscore*((total-amount)/total)))
       except:
              print 'failed classification in bayes' ,amount, total

def classVarToList(classVar):
        outList = [0,0,0,0,0]
        if classVar == 'Adoption':
              outList[0] = 1
        if classVar == 'Return_to_owner':
              outList[1] = 1
        if classVar == 'Euthanasia':
              outList[2] = 1
        if classVar == 'Died':
              outList[3] = 1
        if classVar == 'Transfer':
              outList[4] = 1

        return outList
       

def compareLists(predList, RealList):

       maxim = max(predList)
       
       count = 0
       results = 0
       precise = 0
       for element in RealList:
              #print element,predList[count] 
##              if element == predList[count]:
##                     precise +=1
                     
              if  element == 1 and predList[count] ==  maxim:
                     results = 1
                     
                     # predict is correct
              count += 1
       return results, precise
              

       

class Perceptron:
       """ Store all the variable in an object"""
       # static variables
       def __init__ (self, className):
              self.classVar = className
              self.name = 0.5
              self.kind = 0.5
              self.SexuponOutcome = 0.5
              self.AgeuponOutcome = 0.5
              self.breed = 0.5
              self.Color = ''


       def classify(self, prediction, observe,outname,outkind,outSexuponOutcome,outAgeuponOutcome, outbreed ):
              self.name = self.adjustweight(self.name, alpha , prediction, observe, outname )
              self.kind = self.adjustweight(self.kind, alpha , prediction, observe, outkind )
              self.SexuponOutcome = self.adjustweight(self.SexuponOutcome, alpha , prediction,observe, outSexuponOutcome )
              self.AgeuponOutcome = self.adjustweight(self.AgeuponOutcome, alpha , prediction, observe, outAgeuponOutcome )
              self.breed = self.adjustweight(self.breed, alpha , prediction, observe, outbreed )


       def predict(self, newAgeuponOutcome , newSexuponOutcome, newbreed, newname, newkind):
              a = [float(self.AgeuponOutcome),float(self.SexuponOutcome),float(self.breed),float(self.name), float(self.kind)]
              b = [float(newAgeuponOutcome),float(newSexuponOutcome),float(newbreed),float(newname), float(newkind)]

##              print a, b, dot(a,b)

              # print unitStep(dot(a,b)),dot(a,b) ,  sigmoidStep(dot(a,b))
              return   sigmoidStep(dot(a,b)),dot(a,b)

                        
       def adjustweight(self, oldWeight, alpha,predict, observed, rating ):
              oldWeight = float(oldWeight)
              observed = float(observed)
              predict = float(predict)
              rating = float(rating)
              return (oldWeight + ((alpha*(observed - predict))*rating))


##class Layer:
##
##       def __init__ (self):
##              self.adopt = Perceptron('Adoption')
##              self.retur = Perceptron('Return_to_owner')
##              self.eutha = Perceptron('Euthanasia')
##              self.died_ = Perceptron('Died')
##              self.trans = Perceptron('Transfer')


class observation:

       """ Observation class to store values """

       classifier = 0

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
                            self.breed = 0
                     else:
                            self.breed = 4
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


       # reset age

                    
  

# needs global priors,  lets use 0.5 as priors for all.



# population loop

with open('train.csv','r') as in_raw, open('DogBreeds.tsv' ,'r') as breedRaw:
       infile = csv.reader(in_raw, delimiter = ',')
       infile.next()
       breedFile = csv.reader(breedRaw, delimiter = '\t')

       trainingList = []
       testList = []

       count = 0

       breedDict = populateBreedDict(breedFile)
       print len(breedDict)
       
       for row in infile:
              if row and not '@' in row[0]:

                     obs = observation(row[0])

                     
                     ID = row[0]
                     name = row[1]
                     classification = row[3]
                     subClass = row[4]
                     
                     obs.classVar = row[3]
                     obs.sybClassVar = row[4]
                     obs.animalKind(row[5])
                     obs.animalBreed(row[8],breedDict)
                     obs.AnimalID = row[0]
                     obs.hasName(row[1])                     
                     obs.chooseAge(row[7])
                     obs.chooseSex(row[6])

                     # print obs.AgeuponOutcome , obs.SexuponOutcome, obs.breed, obs.name, obs.kind
 

                     if random.randint(1, 30000) == 7:
                          testList.append(obs)
                     else: 
                            trainingList.append(obs)
                     
##                     print obs.age, obs.sugar, obs.pressure, obs.anemia,obs.classVar
                     

             
                     
print count , len(trainingList), len(testList)

#varObject = Percep()
adopt = Perceptron('Adoption')
retur = Perceptron('Return_to_owner')
eutha = Perceptron('Euthanasia')
died_ = Perceptron('Died')
trans = Perceptron('Transfer')

varObject = adopt

died_.kind = -3
died_.breed = -10
died_.name = -12

##print died_.predict(1,1,-1,-1,-1)
##print eutha.predict(1,1,-1,-1,-1)
####
##print died_.classVar, eutha.classVar , eutha.kind, died_.kind

#print varObject.anemia
##
#### weighting loop





print 'Starting the learning process,  resembles first layer perceptron'  

predCount = 0

for element in xrange(n):
       
       tempObj = random.choice(trainingList)

       predAdopt, score1 = adopt.predict(tempObj.AgeuponOutcome , tempObj.SexuponOutcome, tempObj.breed, tempObj.name, tempObj.kind)
       predRetur, score2 = retur.predict(tempObj.AgeuponOutcome , tempObj.SexuponOutcome, tempObj.breed, tempObj.name, tempObj.kind)
       predEutha, score3 = eutha.predict(tempObj.AgeuponOutcome , tempObj.SexuponOutcome, tempObj.breed, tempObj.name, tempObj.kind)
       predDied_, score4 = died_.predict(tempObj.AgeuponOutcome , tempObj.SexuponOutcome, tempObj.breed, tempObj.name, tempObj.kind)
       predTrans, score5 = trans.predict(tempObj.AgeuponOutcome , tempObj.SexuponOutcome, tempObj.breed, tempObj.name, tempObj.kind)
##       print predAdopt, predRetur, predEutha,predDied_,predTrans, score1,score2,score3,score4,score5
##       print predAdopt, score
       
       adopt.classify(predAdopt, tempObj.chooseClass(adopt.classVar) ,tempObj.name ,tempObj.kind,tempObj.SexuponOutcome,tempObj.AgeuponOutcome, tempObj.breed )
       retur.classify(predRetur, tempObj.chooseClass(retur.classVar) ,tempObj.name ,tempObj.kind,tempObj.SexuponOutcome,tempObj.AgeuponOutcome, tempObj.breed )
       eutha.classify(predEutha, tempObj.chooseClass(eutha.classVar) ,tempObj.name ,tempObj.kind,tempObj.SexuponOutcome,tempObj.AgeuponOutcome, tempObj.breed )
       died_.classify(predDied_, tempObj.chooseClass(died_.classVar) ,tempObj.name ,tempObj.kind,tempObj.SexuponOutcome,tempObj.AgeuponOutcome, tempObj.breed )
       trans.classify(predTrans, tempObj.chooseClass(trans.classVar) ,tempObj.name ,tempObj.kind,tempObj.SexuponOutcome,tempObj.AgeuponOutcome, tempObj.breed )


       predCount +=1
       if (predCount % 10000) == 10:
              print 'count at ', predCount
              print 'Adopt', vars(adopt)
              print 'Return', vars(retur)
              print 'Euthan', vars(eutha)
              print 'Transp', vars(trans)
              print 'Died',vars(died_)


              
                            
total = 0
trueCount = 0
precise = 0
preciseCount = 0
print 'testing true positives'
print 'Adopt','returned','euthanasia','Died','Trans'

argfile = open('testResults_forLogLoss.tsv','w')
outfile = csv.writer(argfile,delimiter = '\t')
outfile.writerow(['ID' , 'Adopt','Died','Euthanasia','Return_to_owner','Transfer'])

amountDict = {'adopt':10769 ,'retur':4786,'eutha':1555,'died_':197,'trans':9422}
# Return_to_owner 4786
# Transfer 9422
# Adoption 10769
# Euthanasia 1555
# Died 197
# OutcomeType 1
# total 26730
####outfile.writerow(['Adopt' , vars(adopt)])
####outfile.writerow(['Returned' , vars(retur)])
####outfile.writerow(['Euthanized' , vars(eutha)])
####outfile.writerow(['Died' , vars(died_)])
####outfile.writerow(['Transfered' , vars(trans)])


test_raw = open('test.csv','r')
testFile = csv.reader(test_raw, delimiter = ',')
testFile.next()


printCount = 0
for row in testFile:

       element = observation(row[0])
       #.observation(row[0])
       scoreDict = {}
       #element.classVar = row[3]
       #element.sybClassVar = row[4]
       element.animalKind(row[3])
       element.animalBreed(row[6],breedDict)
       #obs.AnimalID = row[0]
       obs.hasName(row[1])                     
       obs.chooseAge(row[5])
       obs.chooseSex(row[4])

       resList = [0,0,0,0,0]
       predAdopt, score1 = adopt.predict(element.AgeuponOutcome , element.SexuponOutcome, element.breed, element.name, element.kind)
       resList[0] = predAdopt
       scoreDict['adopt'] = predAdopt
       predRetur, score2 = retur.predict(element.AgeuponOutcome , element.SexuponOutcome, element.breed, element.name, element.kind)
       resList[1] = predRetur
       scoreDict['retur'] = predRetur
       predEutha, score3 = eutha.predict(element.AgeuponOutcome , element.SexuponOutcome, element.breed, element.name, element.kind)
       resList[2] = predEutha
       scoreDict['eutha'] = predEutha
       predDied_, score5 = died_.predict(element.AgeuponOutcome , element.SexuponOutcome, element.breed, element.name, element.kind)
       resList[3] = predDied_
       scoreDict['died_'] = predDied_
       predTrans, score5 = trans.predict(element.AgeuponOutcome , element.SexuponOutcome, element.breed, element.name, element.kind)
       resList[4] = predTrans
       scoreDict['trans'] = predTrans


       total += 1

       resList = formatE(resList)
       outList = findMax(resList)
       
       
       

        
       
       #outfile.writerow([element.classVar,outList[0],outList[3],outList[2],outList[1],outList[4],"%.4f" %float(resList[0]),"%.4f" %float(resList[1]),"%.4f" %float(resList[2]),"%.4f" %float(resList[3]),"%.4f" %float(resList[4]), RealList[0], RealList[1], RealList[2], RealList[3], RealList[4]])
       outfile.writerow([element.AnimalID, outList[0],outList[3],outList[2],outList[1],outList[4]])
#ID	Adoption	Died	Euthanasia	Return_to_owner	Transfer


print 'True : ', trueCount, 'Total : ' , total, 'Exact predictions total : ', preciseCount, ' percentage of true classes', (float(trueCount)/float(total))


##

#4678 * 


# P(A|B) = P(B|A)*P(A) / P(B)

# Return_to_owner 4786
# Transfer 9422
# Adoption 10769
# Euthanasia 1555
# Died 197
# OutcomeType 1
# total 26730
