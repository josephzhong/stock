'''Created on May02, 2014
Decision Tree algorithm
@author: Aidan
'''

from numpy import *
from object_json import *
from copy import *
from math import log
import pdb
import operator
import treePlotter


class decisionTree(object):
    def __init__(self,dsDict_ID3 = None,dsDict_C45 = None, features = None, **args):
        '''currently support ID3 and C4.5, the default type is C4.5, CART TBD
           
        '''
        obj_list = inspect.stack()[1][-2]
        self.__name__ = obj_list[0].split('=')[0].strip()
        self.dsDict_ID3 = dsDict_ID3
        self.dsDict_C45 = dsDict_C45
        #self.classLabel = classLabel
        self.features = features
        
    def jsonDumpsTransfer(self):
        '''essential transformation to Python basic type in order to
        store as json. dumps as objectname.json if filename missed '''
        #pdb.set_trace()

    def jsonDumps(self, filename=None):
        '''dumps to json file'''
        self.jsonDumpsTransfer()
        if not filename:
            jsonfile = self.__name__+'.json'
        else: jsonfile = filename
        objectDumps2File(self, jsonfile)
        
    def jsonLoadTransfer(self):      
        '''essential transformation to object required type, such as numpy matrix
        call this function after newobject = objectLoadFromFile(jsonfile)'''
        #pdb.set_trace()

    def calcShannonEnt(self, dataSet):
        #pdb.set_trace()
        numEntries = len(dataSet)
        labelCounts = {}
        '''
        get the label type and number, crate a dict with type as key  
        '''
        for featVec in dataSet:
            currentLabel = featVec[-1]
            labelCounts[currentLabel] = labelCounts.get(currentLabel,0)+1
        # caclulate shannonEnt
        labelNumList = labelCounts.values()
        pList = [float(item)/numEntries for item in labelNumList if item != 0]# remove zero-length items

        lList = [item*log(item,2) for item in pList]
        shannonEnt = -sum(lList)
        return shannonEnt

    def calcFeatureSplitInfo(self, featureVList):
        #pdb.set_trace()
        numEntries = len(featureVList)
        featureVauleSetList = list(set(featureVList))
        '''
        get the value type and number, crate a dict with type as key  
        '''
        valueCounts = [featureVList.count(featVec) for featVec in featureVauleSetList]
        # caclulate shannonEnt
        pList = [float(item)/numEntries for item in valueCounts ]# remove zero-length items

        lList = [item*log(item,2) for item in pList]
        splitInfo = -sum(lList)
        return splitInfo, featureVauleSetList

    def splitDataSet(self, dataSet, axis, value):
        '''return dataset satisfy condition dataSet[i][axis] == value,
        and remove dataSet[i][axis]'''
        retDataSet = []
        for featVec in dataSet:
            if featVec[axis] == value:
                reducedFeatVec = featVec[:axis]     #chop out axis used for splitting
                reducedFeatVec.extend(featVec[axis+1:])
                retDataSet.append(reducedFeatVec)
        return retDataSet

    def chooseBestFetureToSplit(self, dataSet, modelType):
        '''choose feture which has maximum info Gain if ID3
        choose feture which has maximum info Gain Ratio if C45
        for C45, support only discrete dixtribution'''
        NumofFetures = len(dataSet[0][:-1])
        
        #print 'NumofFetures',NumofFetures
        totality = len(dataSet)
        BaseEntropy = self.calcShannonEnt(dataSet)
        #dataArray = array(dataSet)
        #print 'BaseEntropy:',BaseEntropy
        ConditionEntropy = []
        slpitInfo = []#for C4.5, calculate gain ratio
        allFeatVList=[]
        for f in range(NumofFetures):
            #caculate conditionEntropy
            featList = [example[f] for example in dataSet]
            splitI, featureValueList = self.calcFeatureSplitInfo(featList)
            allFeatVList.append(featureValueList)         
            slpitInfo.append(splitI)
            
            resultGain = 0.0
            
            for value in featureValueList:
                subSet = self.splitDataSet(dataSet, f, value)
                #print subSet
                appearNum = float(len(subSet))
                subShannonEnt = self.calcShannonEnt(subSet)
                resultGain += (appearNum/totality)*subShannonEnt
            ConditionEntropy.append(resultGain)
        
        infoGainArray = BaseEntropy*ones(NumofFetures)-array(ConditionEntropy)
        infoGainRatioArray = infoGainArray/array(slpitInfo)#c4.5, info gain ratio
    
        #print 'ConditionEntropy:',ConditionEntropy
        #print 'infoGain:',infoGain
        if modelType == 'ID3':
            bestFeatureIndex =  argsort(-infoGainArray)[0]
        elif modelType == 'C45':
            bestFeatureIndex =  argsort(-infoGainRatioArray)[0]
            
        return bestFeatureIndex, allFeatVList[bestFeatureIndex]

    def majorityCnt(self, classList):
        '''calculate the majority type'''  
        classCntDict = {}
        #print 'classList',classList
        for vec in classList:
            classCntDict[vec] = classCntDict.get(vec,0) + 1
        #print  'classCntDict:',classCntDict
        sortedClassCntList = sorted(classCntDict.iteritems(), key = operator.itemgetter(1),reverse = True)
        return sortedClassCntList[0][0]

    def isLeafNode(self, dataSet):
        '''if entropy ==0 or <threshold, the dataset belong to the same class, Return True and
        class type(or the majority type), else return False'''
        isLeaf = False
        classtype = None
        classList = [example[-1] for example in dataSet]
        #pdb.set_trace()
        if classList.count(classList[0]) == len(classList): 
           isLeaf = True
           classtype = classList[0]#stop splitting when all of the classes are equal
           return isLeaf, classtype
        if len(dataSet[0]) == 1: #stop splitting when there are no more features in dataSet
           isLeaf = True
           classtype =  self.majorityCnt(classList)
        return isLeaf, classtype

    def __trainDS(self, dataSet, inLabels, modelType):
        '''create decision tree'''
        #print 'dataSet',dataSet
        labels = inLabels[:]
        isLeaf, classType = self.isLeafNode(dataSet)
        if isLeaf: return classType
        
        bestFeatureIndex, featValueList = self.chooseBestFetureToSplit(dataSet, modelType)
        #pdb.set_trace()
        bestFeature = labels[bestFeatureIndex]
        myTree = {bestFeature:{}}
        del(labels[bestFeatureIndex])

        for value in featValueList:
           subLabels = labels[:]       #copy all of labels, so trees don't mess up existing labels
           myTree[bestFeature][value] = self.__trainDS(self.splitDataSet(dataSet, bestFeatureIndex, value),subLabels, modelType)
        return myTree

    def trainDS(self, dataSet, features, modelType = 'C45'):
        ''' for C4.5, post pruning TBD'''
        self.features = features

        if modelType == 'ID3':
           self.dsDict_ID3 = self.__trainDS(dataSet, features, modelType)
        elif modelType == 'C45':
           self.dsDict_C45 = self.__trainDS(dataSet, features,modelType)
        else:
            print 'erro type, support ID3 or C45'

    def __classifier(self, vec2Classify, dsDict):
        ''' '''
        firstStr = dsDict.keys()[0]
        secondDict = dsDict[firstStr]
        featIndex = self.features.index(firstStr)
        key = vec2Classify[featIndex]
        valueOfFeat = secondDict[key]
        if isinstance(valueOfFeat, dict): 
            classLabel = self.__classifier(vec2Classify, valueOfFeat)
        else: classLabel = valueOfFeat
        return classLabel

    def classifyDS(self, vec2Classify, modelType = 'C45'):
        if modelType == 'ID3':
            classLabel = self.__classifier(vec2Classify, self.dsDict_ID3)
            return classLabel
        elif modelType == 'C45':
            classLabel = self.__classifier(vec2Classify, self.dsDict_C45)
            return classLabel
        else:
            print 'erro type, support ID3 or C45'
            #raise()
            return None

    def treePlot(self, modelType = 'C45'):
        if modelType == 'ID3':
            treePlotter.createPlot(self.dsDict_ID3)
        elif modelType == 'C45':
            treePlotter.createPlot(self.dsDict_C45)
        else:
            print 'erro type, support ID3 or C45'
        
    
if __name__ == '__main__':
    dataSet2 = [[1,1,'yes'],
               [1,1,'yes'],
               [1,0,'no'],
               [0,1,'no'],
               [0,1,'no']
              ]
    dataSet = [[1.1,1.2,'yes'],
               [0.9,1.5,'yes'],
               [0.5,0.8,'no'],
               [0.3,1.9,'no'],
               [0.1,1.7,'no']
              ]
    labels = ['no surfacing', 'flippers']
    testDS = decisionTree()
    testDS.trainDS(dataSet, labels, modelType = 'ID3')
    testDS.trainDS(dataSet, labels, modelType = 'C45')
    for (key, value) in testDS.__dict__.items():
        print key, ':\n',value

    predictClass_ID3 = []
    predictClass_C45 = []
    dataSet.append([0,0,'no'])
    for item in dataSet:
        predictClass_ID3.append( testDS.classifyDS(item, modelType = 'ID3'))
        predictClass_C45.append(testDS.classifyDS(item, modelType = 'C45')) 
    print 'predictClass_ID3 ', predictClass_ID3
    print 'predictClass_C45 ', predictClass_C45
    testDS.treePlot()
    
