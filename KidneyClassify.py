import csv
from numpy import array, dot, random
from random import choice


unitStep = lambda x: 0 if x < 0 else 1

n = 18500
alpha = 0.01


class AllVariables:
       """ Store all the variable in an object"""
       # static variables
       classVar = 0.5
       age = 0.5
       pressure = 0.5
       sugar = 0.5
       anemia = 0.5

       def predict(self, newAge,newPres,newSug,newAnemia):
              a = [float(self.age),float(self.pressure),float(self.sugar),float(self.anemia)]
              b = [float(newAge),float(newPres),float(newSug),float(newAnemia)]
              return  unitStep(dot(a,b))

                        
       def adjustweight(self, oldWeight, alpha,predict, observed, rating ):
              #print (oldWeight)
              try:
                     oldWeight = float(oldWeight)
                     observed = float(observed)
                     predict = float(predict)
                     rating = float(rating)
              except:
                     return 0

              #print alpha,predict, observed, rating

              #print  oldWeight, alpha,predict, observed, rating
##              try:
##                     print 'Result' , (((alpha *((observed - predict))*rating)))
##              except:
##                     print 'Failure',type(alpha), type(observed),  type(predict), type(rating)
##                     return 0
              
              return (oldWeight + ((alpha*(observed - predict))*rating))


##
##
##class VariableInfluence:
##       
##       """ each observed variable has its own influence"""
##
##       def __init__(self, name):
##              # initialize the weight uninformative prior
##              self.weight = 0.5
##              self.name = name
##       
##
##       
##       def adjustweight(self,alpha,predict, observed, rating ):
##              self.weight = (self.weight + ((alpha*(observed-predict))*rating))
##              
##

       

class observation:

       """ Observation class to store values """

       classifier = 0

       def classifyVarCheck(self,classVar):
              if classVar == 'ckd':
                     classVar = 1
              if classVar == 'notckd':
                     classVar = 0
              self.classVar = classVar
              

       def classifyAnemia(self,anemia):
              if anemia == 'yes':
                     anemia = 1
              if anemia == 'no':
                     anemia = 0
              if anemia == '?':
                     anemia = 0.5
              self.anemia = anemia
                     
       def chooseAge(self,age):
              if age == '?':
                     age = 0.5 ####
              float(age) = float(age)/100
##              if int(age) <= 50:
##                     age = 0
##              if int(age) > 65:
##                     age = 1
              self.age = age

       def choosePressure(self,pres):
              if pres == '?':
                     pres = 75
              pres = (pres / 100)
##              if int(pres) <= 80:
##                     pres = 0
##              if int(pres) > 80:
##                     pres = 1
              self.pressure = pres

       def chooseSugar(self,sug):
              if sug == '?':
                     sug = 0
              self.sugar = sug

                     
       def __init__(self):
              self.classVar = 0
              self.age = 0
              self.pressure = 0
              self.sugar = 0
              self.anemia = 0


       # reset age



       
                            
       
def adjustweight(oldWeight, alpha,predict, observed, rating ):
       newWeight = (oldWeight + ((alpha*(observed-predict))*rating))
       return newWeight



# training algorythm
#  w(t+1) = w(t) + a(di - yi)xi,j
def adjustweight(oldWeight, alpha,predict, observed, rating ):
       newWeight = (oldWeight + ((alpha*(observed-predict))*rating))
       return newWeight

       

# needs global priors,  lets use 0.5 as priors for all.

w = random.rand(5)

testvalues = {} 


# population look

with open('chronic_kidney_disease.arff','r') as in_raw:
       infile = csv.reader(in_raw, delimiter = ',')

       trainingList = []
       testList = []

       count = 0
       
       for row in infile:
              if row and not '@' in row[0]:

                     classification = row[24]
                     anemia = row[23]
                     age = row[0]
                     pressure = row[1]
                     sugar = row[4]
                     
                     obs = observation()
                     obs.classifyVarCheck(classification)
                     obs.chooseAge(age)
                     obs.classifyAnemia(anemia)
                     obs.chooseSugar(sugar)
                     obs.choosePressure(pressure)


                     if random.randint(1, 20) == 7:
                          testList.append(obs)
                     else: 
                            trainingList.append(obs)
                     
##                     print obs.age, obs.sugar, obs.pressure, obs.anemia,obs.classVar
                     
                     count +=1
             
                     
print count , len(trainingList), len(testList)

varObject = AllVariables()

print varObject.anemia

## weighting loop
for element in xrange(n):
       tempObj = random.choice(trainingList)

       prediction = varObject.predict(tempObj.age,tempObj.pressure,tempObj.sugar,tempObj.anemia)
       varObject.anemia = varObject.adjustweight(varObject.anemia, alpha , prediction, tempObj.classVar, tempObj.anemia )    
       varObject.age = varObject.adjustweight(varObject.age, alpha , prediction, tempObj.classVar, tempObj.age )
       varObject.pressure = varObject.adjustweight(varObject.pressure, alpha , prediction, tempObj.classVar, tempObj.pressure )
       varObject.sugar = varObject.adjustweight(varObject.sugar, alpha , prediction, tempObj.classVar, tempObj.sugar )
       


total = 0
true = 0
for element in testList:
       
       prediction = varObject.predict(element.age,element.pressure,element.sugar,element.anemia)
       reality = element.classVar
       total +=1
       if reality == prediction:
              true +=1
              
print vars(varObject)
print true, total, (float(true)/float(total))


       



