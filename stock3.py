# -*- coding:utf-8 -*-  
from os.path import exists, join
import threading
import math, random, warnings,logging, sys
#from tree import tree1
#from tree2007 import tree1filter
from stockclass import Stock
from data import *

class stockView:
    def __init__(self):
        self.lastClose_bMd = 0.0
        self.lastOpen_bMd = 0.0
        self.lastClose_bUp = 0.0
        self.lastOpen_bUp = 0.0
        self.thisChange = 0.0
        self.thisOpen_bUp = 0.0
        self.thisClose_bUp = 0.0
        self.thisV_b = 0.0
        self.ifHengPan = 0
        self.result = "GoDown"
    def fromStock(self, sample, conditionday):
        todayindex = sample.indexof(conditionday)
        yesterdayindex = todayindex - 1
        nextdayindex = todayindex + 1
        if(yesterdayindex > -1 and nextdayindex < len(sample.dates) and yesterdayindex > 20 and todayindex > 20):
            bMd = sample.bollMd(conditionday)
            bUp = sample.bollUp(conditionday)
            lastClose = sample.closePrices[yesterdayindex]
            lastOpen = sample.openPrices[yesterdayindex]
            thisChange = sample.changePrices[todayindex]
            thisOpen = sample.openPrices[todayindex]
            thisClose = sample.closePrices[todayindex]
            thisV_b = sample.v_b(sample.v_ma5[todayindex], sample.volume[todayindex])
            if(bMd == 0.0 or bUp == 0.0):
                return None
            self.lastClose_bMd = floatFormat((lastClose-bMd)/bMd)
            self.lastOpen_bMd = floatFormat((lastOpen-bMd)/bMd)
            self.lastClose_bUp = floatFormat((lastClose-bUp)/bUp)
            self.lastOpen_bUp = floatFormat((lastOpen-bUp)/bUp)
            self.thisChange = floatFormat(sample.changePrices[todayindex])
            self.thisOpen_bUp = floatFormat((thisOpen-bUp)/bUp)
            self.thisClose_bUp = floatFormat((thisClose-bUp)/bUp)
            self.thisV_b = floatFormat(sample.v_b(sample.v_ma5[todayindex], sample.volume[todayindex]))
            self.ifHengPan = boolToInt(sample.checkIfHengPan(conditionday))
            if(sample.changePrices[nextdayindex] > 0.05):
                self.result = "High"
            else:
                if(sample.changePrices[nextdayindex] >=0 and sample.changePrices[nextdayindex] <= 0.05):
                    self.result = "Low"
                else:
                    if(sample.changePrices[nextdayindex] < 0 and sample.changePrices[nextdayindex] >= -0.05):
                        self.result = "MinusLow"
                    else:
                        self.result = "MinusHigh"
            return self
        else:
            return None
    

#base on human experience
def filterStock(samples, conditionday):
    result = []
    for sample in samples:
        try:
            bMd = sample.bollMd(conditionday)
            bDn = sample.bollDn(conditionday)
            bUp = sample.bollUp(conditionday)
            todayindex = sample.indexof(conditionday)
            yesterdayindex = todayindex - 1
            if(yesterdayindex > -1 and todayindex > -1):
                lastClose = sample.closePrices[yesterdayindex]
                lastOpen = sample.openPrices[yesterdayindex]
                thisChange = sample.changePrices[todayindex]
                thisOpen = sample.openPrices[todayindex]
                thisClose = sample.closePrices[todayindex]
                thisV_b = sample.v_b(sample.v_ma5[todayindex], sample.volume[todayindex])
                #1.前一天股价（开盘收盘价）在BOLL上线以下并且在BOLL中线以上。
                if(lastClose < bUp and lastClose > bMd and lastOpen < bUp and lastOpen > bMd):
                #2.当天K线为阳线
                    if(thisChange > 0):
                #3.当天开盘价在BOLL上线以下
                        if(thisOpen < bUp):
                #4.当天收盘价在BOLL上线以上
                            if(thisClose > bUp):
                #5.当天量比为1.4倍以上     视为突破
                                if(thisV_b > 1.6):
                #6.之前长时间横盘
                                    if(sample.checkIfHengPan(conditionday)):
                                        result.append(sample)
        except Exception as e:
            logging.warning("filterStock function: "  + str(e))
    return result
#base on machine learning
def filterStock2(samples, conditionday):
    result = []
    for sample in samples:
        try:
            todayindex = sample.indexof(conditionday)
            yesterdayindex = todayindex - 1
            if(yesterdayindex > -1 and yesterdayindex > 20 and todayindex > 20 and todayindex < len(sample.dates)):
                bMd = sample.bollMd(conditionday)
                bUp = sample.bollUp(conditionday)
                lastClose = sample.closePrices[yesterdayindex]
                lastOpen = sample.openPrices[yesterdayindex]
                thisChange = sample.changePrices[todayindex]
                thisOpen = sample.openPrices[todayindex]
                thisClose = sample.closePrices[todayindex]
                thisV_b = sample.v_b(sample.v_ma5[todayindex], sample.volume[todayindex])
                if(bMd == 0.0 or bUp == 0.0):
                    continue
                lastClose_bMd = floatFormat((lastClose-bMd)/bMd)
                lastOpen_bMd = floatFormat((lastOpen-bMd)/bMd)
                lastClose_bUp = floatFormat((lastClose-bUp)/bUp)
                lastOpen_bUp = floatFormat((lastOpen-bUp)/bUp)
                thisChange = floatFormat(sample.changePrices[todayindex])
                thisOpen_bUp = floatFormat((thisOpen-bUp)/bUp)
                thisClose_bUp = floatFormat((thisClose-bUp)/bUp)
                thisV_b = floatFormat(sample.v_b(sample.v_ma5[todayindex], sample.volume[todayindex]))
                ifHengPan = sample.checkIfHengPan(conditionday)
                if(lastClose_bUp=="BelowZero" and lastClose_bMd=="BelowZero" and lastOpen_bUp=="AboveZero" and lastOpen_bMd=="AboveZero" and thisChange=="AboveZero" and thisClose_bUp=="AboveZero" and thisV_b=="BelowZero" and ifHengPan==True):
                    result.append(sample)
                    continue
                if(lastClose_bUp=="AboveZero" and lastOpen_bUp=="AboveZero" and thisChange=="AboveZero" and thisClose_bUp=="BelowZero" and thisV_b=="AboveZero" and ifHengPan==True):
                    result.append(sample)
                    continue
        except Exception as e:
                logging.warning("filterStock2 function: "  + str(e))
    return result

def filterStock3(samples, conditionday):
    result = []
    for sample in samples:
        try:
            todayindex = sample.indexof(conditionday)
            yesterdayindex = todayindex - 1
            if(yesterdayindex > -1 and yesterdayindex > 20 and todayindex > 20 and todayindex < len(sample.dates)):
                bMd = sample.bollMd(conditionday)
                bUp = sample.bollUp(conditionday)
                lastClose = sample.closePrices[yesterdayindex]
                lastOpen = sample.openPrices[yesterdayindex]
                thisChange = sample.changePrices[todayindex]
                thisOpen = sample.openPrices[todayindex]
                thisClose = sample.closePrices[todayindex]
                thisV_b = sample.v_b(sample.v_ma5[todayindex], sample.volume[todayindex])
                if(bMd == 0.0 or bUp == 0.0):
                    continue
                lastClose_bMd = floatFormat((lastClose-bMd)/bMd)
                lastOpen_bMd = floatFormat((lastOpen-bMd)/bMd)
                lastClose_bUp = floatFormat((lastClose-bUp)/bUp)
                lastOpen_bUp = floatFormat((lastOpen-bUp)/bUp)
                thisChange = floatFormat(sample.changePrices[todayindex])
                thisOpen_bUp = floatFormat((thisOpen-bUp)/bUp)
                thisClose_bUp = floatFormat((thisClose-bUp)/bUp)
                thisV_b = floatFormat(sample.v_b(sample.v_ma5[todayindex], sample.volume[todayindex]))
                ifHengPan = sample.checkIfHengPan(conditionday)
                if(thisOpen_bUp=="BelowZero" and lastOpen_bUp=="BelowZero" and lastClose_bMd=="AboveZero" and lastOpen_bMd=="BelowZero" and thisClose_bUp=="AboveZero" and ifHengPan==True and lastClose_bUp=="AboveZero" and thisV_b=="AboveZero"):
                    result.append(sample)
                    continue
                if(thisOpen_bUp=="BelowZero" and lastOpen_bUp=="AboveZero" and thisChange=="BelowZero" and lastClose_bMd=="AboveZero" and thisV_b=="AboveZero" and ifHengPan==True and lastClose_bUp=="BelowZero"):
                    result.append(sample)
                    continue
                if(thisOpen_bUp=="BelowZero" and lastOpen_bUp=="AboveZero" and thisChange=="AboveZero" and thisClose_bUp=="BelowZero" and lastClose_bUp=="AboveZero" and thisV_b=="AboveZero" and ifHengPan==True):
                    result.append(sample)
                    continue
                if(thisOpen_bUp=="BelowZero" and lastOpen_bUp=="AboveZero" and thisChange=="AboveZero" and thisClose_bUp=="AboveZero" and thisV_b=="BelowZero" and ifHengPan==True and lastClose_bMd=="BelowZero"):
                    result.append(sample)
                    continue
                if(thisOpen_bUp=="AboveZero" and thisV_b=="AboveZero" and ifHengPan==True and thisChange=="BelowZero" and lastClose_bUp=="BelowZero" and lastOpen_bUp=="BelowZero" and lastClose_bMd=="AboveZero" and lastOpen_bMd=="BelowZero" and thisClose_bUp=="BelowZero"):
                    result.append(sample)
                    continue
                if(thisOpen_bUp=="AboveZero" and thisV_b=="AboveZero" and ifHengPan==True and thisChange=="BelowZero" and lastClose_bUp=="BelowZero" and lastOpen_bUp=="AboveZero"):
                    result.append(sample)
        except Exception as e:
                logging.warning("filterStock3 function: "  + str(e))
    return result
#first filter using machine learning
def wekafilter(samples, conditionday):
    result = []
    for sample in samples:
        try:
            todayindex = sample.indexof(conditionday)
            yesterdayindex = todayindex - 1
            if(yesterdayindex > -1 and yesterdayindex > 20 and todayindex > 20 and todayindex < len(sample.dates)):
                bMd = sample.bollMd(conditionday)
                bUp = sample.bollUp(conditionday)
                lastClose = sample.closePrices[yesterdayindex]
                lastOpen = sample.openPrices[yesterdayindex]
                thisChange = sample.changePrices[todayindex]
                thisOpen = sample.openPrices[todayindex]
                thisClose = sample.closePrices[todayindex]
                thisV_b = sample.v_b(sample.v_ma5[todayindex], sample.volume[todayindex])
                if(bMd == 0.0 or bUp == 0.0):
                    continue
                lastClose_bMd = (lastClose-bMd)/bMd
                lastOpen_bMd = (lastOpen-bMd)/bMd
                lastClose_bUp = (lastClose-bUp)/bUp
                lastOpen_bUp = (lastOpen-bUp)/bUp
                thisChange = sample.changePrices[todayindex]
                thisOpen_bUp = (thisOpen-bUp)/bUp
                thisClose_bUp = (thisClose-bUp)/bUp
                thisV_b = sample.v_b(sample.v_ma5[todayindex], sample.volume[todayindex])
                ifHengPan = sample.checkIfHengPan(conditionday)
                GoUp = 0.0
                if (thisChange <= -0.038):
                    if (thisChange <= -0.07):
                        if (thisClose_bUp > -0.208):
                            if (thisClose_bUp > -0.202):
                                if (lastClose_bMd <= -0.017): 
                                    GoUp = (3.0)
                    if (thisChange > -0.07):
                        if (thisChange <= -0.063):
                            if (ifHengPan <= 0):
                                if (thisChange > -0.065):
                                    if (thisChange > -0.064):
                                        if (lastClose_bUp > -0.14): 
                                            GoUp = (2.0)
                if (thisChange > -0.038):
                    if (ifHengPan <= 0):
                        if (thisV_b > 0.973):
                            if (lastClose_bUp <= -0.662):
                                if (thisClose_bUp <= -0.669):
                                    if (lastOpen_bUp <= -0.778): 
                                        GoUp = (8.0/1.0)
                                if (thisClose_bUp > -0.669): 
                                    GoUp = (20.0/3.0)
                    if (ifHengPan > 0):
                        if (thisOpen_bUp <= -0.186):
                            if (lastOpen_bUp <= -0.206):
                                if (thisChange <= 0.01):
                                    if (thisChange <= -0.021):
                                        if (thisV_b > 0.765):
                                            if (lastOpen_bMd <= -0.094):
                                                if (thisChange <= -0.023):
                                                    if (thisChange <= -0.027):
                                                        if (thisV_b <= 1.007): 
                                                            GoUp = (5.0/1.0)
                                                if (thisChange > -0.023): 
                                                    GoUp = (3.0)
                                            if (lastOpen_bMd > -0.094): 
                                                GoUp = (4.0)
                                if (thisChange > 0.01):
                                    if (thisChange <= 0.018):
                                        if (thisOpen_bUp <= -0.224): 
                                            GoUp = (29.0/9.0)
                            if (lastOpen_bUp > -0.206):
                                if (lastOpen_bMd <= -0.06):
                                    if (lastOpen_bUp > -0.176):
                                        if (thisV_b <= 0.871):
                                            if (lastClose_bUp > -0.209):
                                                if (lastClose_bMd <= -0.091): 
                                                    GoUp = (7.0)
                                        if (thisV_b > 0.871): 
                                            GoUp = (19.0)
                                if (lastOpen_bMd > -0.06):
                                    if (lastClose_bMd > 0.124):
                                        if (thisOpen_bUp <= -0.314): 
                                            GoUp = (11.0/1.0)
                        if (thisOpen_bUp > -0.186):
                            if (lastOpen_bUp > -0.166):
                                if (thisV_b <= 1.079):
                                    if (lastClose_bMd <= -0.032):
                                        if (lastOpen_bUp <= -0.14):
                                            if (lastClose_bMd <= -0.072):
                                                if (lastOpen_bMd > -0.066): 
                                                    GoUp = (6.0/1.0)
                                    if (lastClose_bMd > -0.032): 
                                        GoUp = (3.0)
                                if (thisV_b > 1.079): 
                                    GoUp = (4.0)
                
                if (GoUp > 0.0):
                    sample.score = GoUp
                    result.append(sample)
        except Exception as e:
                logging.warning("filterStock3 function: "  + str(e))
    return result

def checkTPFP(positives, conditionday, thres):
    tpositives = 0
    for positive in positives:
        index = positive.indexof(conditionday)
        if(index + 1 >= len(positive.changePrices)):
            continue
        if(index > -1 and positive.changePrices[index + 1] >= thres):
            tpositives += 1
    if (len(positives)==0):
        return [0.0, 0.0]
    else:
        return [float(tpositives)/len(positives), float(len(positives)-tpositives)/len(positives)]
    
def averageTPFP(targets, filter, conditionday, thres):
    verifydays = []
    deltadays = []
    weekday = conditionday.weekday()
    for deltaday in range(1, 35):
        if ((weekday - deltaday)%7 >= 0 and (weekday - deltaday)%7 <= 4):
            deltadays.append(deltaday)
    for deltaday in deltadays:
        verifydays.append(conditionday - timedelta(days=deltaday))
    sum = [0.0, 0.0]
    verifytimes = 0
    for day in verifydays:
        filteredstocks = filter(targets, day)
        tpfp = checkTPFP(filteredstocks, day, thres)
        logging.info("{0} TP/FP: {1[0]:.2%}/{1[1]:.2%}".format(day.isoformat(), tpfp))
        sum[0] += tpfp[0]
        sum[1] += tpfp[1]
        if(tpfp[0] != 0.0 or tpfp[1] != 0.0):
            verifytimes += 1
    if(verifytimes == 0):
        return [0.0, 0.0]
    return [sum[0]/verifytimes, sum[1]/verifytimes]

def printGoodStock(stocks, filter, day):
    goodstocks = []
    today = day
    goodstocks = filter(stocks, today)
    logging.info(filter.__name__ + " Good stocks: ")
    if (len(goodstocks) == 0):
        logging.info("No good stock found.")
    for idx1, data1 in enumerate(goodstocks):
        if(idx1 < len(goodstocks) - 1 ):
            for idx2, data2 in enumerate(goodstocks[idx1:]):
                if(idx2 < len(goodstocks) - 1):
                    if(goodstocks[idx2].score < goodstocks[idx2 + 1].score):
                        temp = goodstocks[idx2]
                        goodstocks[idx2] = goodstocks[idx2 + 1]
                        goodstocks[idx2 + 1] = temp
    for stock in goodstocks:
        logging.info("{0}\t{1}\t{2}\tlast day of data on {3}".format(stock.id, stock.name, stock.score, stock.dates[len(stock.dates) - 1]))

def verify(data, func, verifyday, thres):
    verify = averageTPFP(data, func, verifyday, thres)
    logging.info(func.__name__ + " Average TP/FP: {0[0]:.2%} / {0[1]:.2%}".format(verify))

def boolToInt(bool):
    if(bool):
        return 1
    else:
        return 0
    
def floatFormat(num):
    if(math.isnan(num)):
        return 0.0
    else:
        return float(int(num*1000))/1000

def writeToJsonFileForTraining(dataArray):
    file = open("stock.json", "w")
    jsonobj = {}
    
    lastClose_bMds = []
    lastOpen_bMds = []
    lastClose_bUps = []
    lastOpen_bUps = []
    thisChanges = []
    thisOpen_bUps = []
    thisClose_bUps = []
    thisV_bs = []
    ifHengPans = []
    results = []
    
    
    for sample in dataArray:
        for day in sample.dates:
            conditionday = datetime.strptime(day, '%Y-%m-%d').date()
            todayindex = sample.indexof(conditionday)
            yesterdayindex = todayindex - 1
            nextdayindex = todayindex + 1
            if(yesterdayindex > -1 and nextdayindex < len(sample.dates) and yesterdayindex > 20 and todayindex > 20):
                bMd = sample.bollMd(conditionday)
                bUp = sample.bollUp(conditionday)
                lastClose = sample.closePrices[yesterdayindex]
                lastOpen = sample.openPrices[yesterdayindex]
                thisChange = sample.changePrices[todayindex]
                thisOpen = sample.openPrices[todayindex]
                thisClose = sample.closePrices[todayindex]
                thisV_b = sample.v_b(sample.v_ma5[todayindex], sample.volume[todayindex])
                if(bMd == 0.0 or bUp == 0.0):
                    continue
                lastClose_bMds.append(floatFormat((lastClose-bMd)/bMd))
                lastOpen_bMds.append(floatFormat((lastOpen-bMd)/bMd))
                lastClose_bUps.append(floatFormat((lastClose-bUp)/bUp))
                lastOpen_bUps.append(floatFormat((lastOpen-bUp)/bUp))
                thisChanges.append(floatFormat(sample.changePrices[todayindex]))
                thisOpen_bUps.append(floatFormat((thisOpen-bUp)/bUp))
                thisClose_bUps.append(floatFormat((thisClose-bUp)/bUp))
                thisV_bs.append(floatFormat(sample.v_b(sample.v_ma5[todayindex], sample.volume[todayindex])))
                ifHengPans.append(sample.checkIfHengPan(conditionday))
                results.append(sample.changePrices[nextdayindex] > 0.03 )
    jsonobj = {"result": results, "lastClose_bMd": lastClose_bMds, "lastOpen_bMd": lastOpen_bMds, "lastClose_bUp": lastClose_bUps, "lastOpen_bUp": lastOpen_bUps, "thisChange": thisChanges, "thisOpen_bUp": thisOpen_bUps, "thisClose_bUp": thisClose_bUps, "thisV_b": thisV_bs, "ifHengPan": ifHengPans}
    jsonstr = json.dumps(jsonobj, separators=(",", ": "))
    file.write(jsonstr)
    file.close()
    
def writeToArffFile(dataArray,filename):
    file = open(filename, "w")
    jsonobj = {}
    
    lastClose_bMds = []
    lastOpen_bMds = []
    lastClose_bUps = []
    lastOpen_bUps = []
    thisChanges = []
    thisOpen_bUps = []
    thisClose_bUps = []
    thisV_bs = []
    ifHengPans = []
    results = []
    
    file.write("@relation stock\n")
    file.write("\n")
    dataexample = stockView()
    memberlist = [m for m in dir(dataexample)]
    attrs = []
    for m in memberlist:
        if m[0] != "_" and not callable(getattr(dataexample,m)):
            attrs.append(m)
    for attr in attrs:
        if(attr != "result"):
            file.write("@attribute {0} numeric\n".format(attr))
    file.write("@attribute {0} {{High, Low, MinusHigh, MinusLow}}\n".format("result"))
    file.write("\n")
    file.write("@data\n")
    total = len(dataArray)
    prog = 0
    for idx, sample in enumerate(dataArray):
        if(int((idx+1)*100/total) > prog):
            print ("{0}\tOutput: {1}%\n".format(datetime.now().strftime("%d %b %Y %H:%M:%S"), int((idx+1)*100/total)))
            prog = (idx+1)*100/total
        for day in sample.dates:
            conditionday = datetime.strptime(day, '%Y-%m-%d').date()
            data = stockView().fromStock(sample, conditionday)
            if(data != None):
                attrvalues = []
                for attr in attrs:
                    if(attr != "result"):
                        attrvalues.append(getattr(data, attr))
                file.write("{{0 {0[0]}, 1 {0[1]}, 2 {0[2]}, 3 {0[3]}, 4 {0[4]}, 5 {0[5]}, 6 {0[6]}, 7 {0[7]}, 8 {0[8]}, 9 {1}}}\n".format(attrvalues, data.result))
    file.close()

def subprocessfunc(data, day):
    #from tree2007 import tree1filter
    from tree7y600pre import tree7y600prefilter
    printGoodStock(data, tree7y600prefilter, day)
    verify(data, tree7y600prefilter, day, 0.0)
prefixes = []
#prefixes = ['6000','6001','6002','6003','6004','6005','6006','6007','6008','6009', '6010', '6011', '6012', '6013', '6014', '6015', '6016', '6017',  '6018', '6019', '6030', '6031', '6032', '6033', '6034', '6035', '6036', '6037', '6038', '6039', '0020','0021','0022','0023','0024','0025','0026','0027','0028','0029']
#prefixes = ['60030']
#prefixes = ['6000','6001','6002','6003','6004','6005','6006','6007','6008','6009', '6010', '6011', '6012', '6013', '6014', '6015', '6016', '6017',  '6018', '6019', '6030', '6031', '6032', '6033', '6034', '6035', '6036', '6037', '6038', '6039']
prefs = ['600','601', '603', '002']
for pref in prefs:
    for i in range(10):
        prefixes.append(pref + str(i).zfill(1))

logging.basicConfig(filename= datetime.now().strftime("%Y_%m_%d_%H_%M_%S")+ '.log',level=logging.DEBUG)


#if(sys.getrecursionlimit() < 4000):
#    sys.setrecursionlimit(4000)
#logging.info("Current stack limit: {0}".format(sys.getrecursionlimit()))

startday = datetime.strptime("2015-03-18", '%Y-%m-%d').date()
endday = datetime.strptime("2015-06-18", '%Y-%m-%d').date()
stocks = fetchData_mongo(prefixes, startday, endday)
#writeToArffFile(stocks,"stock_7year.arff")

#startday = datetime.strptime("2007-01-01", '%Y-%m-%d').date()
#endday = datetime.strptime("2007-12-31", '%Y-%m-%d').date()
#stocks = fetchData(prefixes, startday, endday)
#writeToArffFile(stocks,"stock_2007.arff")
#printGoodStock(stocks, filterStock)
#verify(stocks, filterStock, date.today(), 0.0)
#printGoodStock(stocks, filterStock2)
#verify(stocks, filterStock2, date.today(), 0.0)
#printGoodStock(stocks, filterStock3)
#verify(stocks, filterStock3, date.today(), 0.0)
#writeToJsonFileForTraining(stocks)
#printGoodStock(stocks, wekafilter)
#verify(stocks, wekafilter, date.today(), 0.0)
#printGoodStock(stocks, tree1filter)
#verify(stocks, tree1filter, date.today(), 0.0)

threading.stack_size(1310720000)
subthread = threading.Thread(target=subprocessfunc, args=(stocks, endday))
logging.info("subthread started.")
subthread.start()
subthread.join()

#printGoodStock(stocks, tree1filter)
#verify(stocks, tree1filter, date.today(), 0.0)
logging.shutdown()
print ("Script ends.")
