from stockclass import Stock
import math, random, warnings,logging, sys
from datetime import date, timedelta, datetime

    
def getnextworkingday(d):
    newday = d + timedelta(days=1)
    if(newday.weekday() > 4):
        newday = newday + timedelta(days=1)
    if(newday.weekday() > 4):
        newday = newday + timedelta(days=1)
    return newday

def checkTPFP(positives, conditionday, thres):
    tpositives = 0
    averGrowth = 0.0
    for positive in positives:
        index = positive.indexof(conditionday)
        if(index < 0):
            continue
        if(index + 1 >= len(positive.changePrices)):
            continue
        averGrowth += positive.changePrices[index + 1]
        if(index > -1 and positive.changePrices[index + 1] >= thres):
            tpositives += 1
    if (len(positives)==0):
        return [0.0, 0.0, 0.0]
    else:
        return [float(tpositives)/len(positives), float(len(positives)-tpositives)/len(positives), averGrowth/len(positives)]


def averageTPFP(targets, filter, conditionday, thres):
    verifydays = []
    deltadays = []
    weekday = conditionday.weekday()
    for deltaday in range(1, 35):
        if ((weekday - deltaday)%7 >= 0 and (weekday - deltaday)%7 <= 4):
            deltadays.append(deltaday)
    for deltaday in deltadays:
        verifydays.append(conditionday - timedelta(days=deltaday))
    sum = [0.0, 0.0, 0.0]
    verifytimes = 0
    for day in verifydays:
        filteredstocks = filter(targets, day)
        tpfp = checkTPFP(filteredstocks, day, thres)
        logging.info("{0} TP/FP: {1[0]:.2%}/{1[1]:.2%} Average Growth: {1[2]:.3%}".format(getnextworkingday(day).isoformat(), tpfp))
        sum[0] += tpfp[0]
        sum[1] += tpfp[1]
        sum[2] += tpfp[2]
        if(tpfp[0] != 0.0 or tpfp[1] != 0.0):
            verifytimes += 1
    if(verifytimes == 0):
        return [0.0, 0.0]
    return [sum[0]/verifytimes, sum[1]/verifytimes, sum[2]/verifytimes]

def verify(data, func, verifyday, thres):
    verify = averageTPFP(data, func, verifyday, thres)
    logging.info(func.__name__ + " Average TP/FP: {0[0]:.2%} / {0[1]:.2%} Average Growth: {0[2]:.3%}".format(verify))