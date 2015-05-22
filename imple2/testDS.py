'''Created on May02, 2014
Decision Tree algorithm
@author: Aidan
'''
from numpy import *
from object_json import *
from trees import *
import pdb


def DSTest():
    with open('lenses.txt','r') as fr:
        lenses = [line.strip().split('\t') for line in fr]
    lensesLabels = ['age', 'prescript', 'astigmatic', 'tearRate']

    classifierDS = decisionTree()
    
    #classifierDS.trainDS(lenses[:-1], lensesLabels, modelType = 'ID3')
    #classifierDS.trainDS(lenses[:-1], lensesLabels, modelType = 'C45')
    classifierDS.trainDS(lenses, lensesLabels, modelType = 'ID3')
    classifierDS.trainDS(lenses, lensesLabels, modelType = 'C45')

    predictClass_ID3 = []
    predictClass_C45 = []
    lenses.extend([['presbyopic','myope','yes','normal','hard'],
                   ['presbyopic','myope','yes','reduced','no lenses'],
                  ])
    for item in lenses:
        predictClass_ID3.append(classifierDS.classifyDS(item, modelType = 'ID3'))
        predictClass_C45.append(classifierDS.classifyDS(item, modelType = 'C45')) 
    print 'predictClass_ID3:\n ', predictClass_ID3
    print 'predictClass_C45:\n ', predictClass_C45

    classifierDS.treePlot(modelType = 'C45')
    classifierDS.treePlot(modelType = 'ID3')
if __name__ == '__main__':
    
    DSTest()
