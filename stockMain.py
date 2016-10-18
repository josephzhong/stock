# -*- coding:utf-8 -*-
import threading
# from tree import tree1
# from tree2007 import tree1filter
from stockclass import Stock
from data import *
from filter import *
from verify import *
from _datetime import timedelta

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
        if yesterdayindex > -1 and nextdayindex < len(sample.dates) and yesterdayindex > 20 and todayindex > 20:
            bMd = sample.bollMd(conditionday)
            bUp = sample.bollUp(conditionday)
            lastClose = sample.closePrices[yesterdayindex]
            lastOpen = sample.openPrices[yesterdayindex]
            thisChange = sample.changePrices[todayindex]
            thisOpen = sample.openPrices[todayindex]
            thisClose = sample.closePrices[todayindex]
            thisV_b = sample.v_b(sample.v_ma5[todayindex], sample.volume[todayindex])
            if bMd == 0.0 or bUp == 0.0:
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
            if sample.changePrices[nextdayindex] > 0.05:
                self.result = "High"
            else:
                if sample.changePrices[nextdayindex] >=0 and sample.changePrices[nextdayindex] <= 0.05:
                    self.result = "Low"
                else:
                    if sample.changePrices[nextdayindex] < 0 and sample.changePrices[nextdayindex] >= -0.05:
                        self.result = "MinusLow"
                    else:
                        self.result = "MinusHigh"
            return self
        else:
            return None
    

def printGoodStock(stocks, filter, day):
    goodstocks = []
    today = day
    goodstocks = filter(stocks, today)
    logging.info(filter.__name__ + " Good stocks: ")
    if len(goodstocks) == 0:
        logging.info("No good stock found.")
    for idx1, data1 in enumerate(goodstocks):
        if idx1 < len(goodstocks) - 1:
            for idx2, data2 in enumerate(goodstocks[idx1:]):
                if idx2 < len(goodstocks) - 1:
                    if goodstocks[idx2].score < goodstocks[idx2 + 1].score:
                        temp = goodstocks[idx2]
                        goodstocks[idx2] = goodstocks[idx2 + 1]
                        goodstocks[idx2 + 1] = temp
    for stock in goodstocks:
        logging.info("{0}\t{1}\t{2}\tlast day of data on {3}".format(stock.id, stock.name, stock.score, stock.dates[len(stock.dates) - 1]))

# run the model to print the good stocks for next day and verify the model. threshold is 0.0 by default
def subprocessfunc(data, day):
    # from tree2007 import tree1filter
    from tree7y600pre import tree7y600prefilter
    printGoodStock(data, tree7y600prefilter, day)
    verify(data, tree7y600prefilter, day, 0.0)

#To predict the result of some specific stock given in datas
def subprocessPredictfunc(datas, day):
    # from tree2007 import tree1filter
    from tree7y600pre import tree7y600prePrediction
    for data in datas:
        score = tree7y600prePrediction(data, day)
        logging.info("Stock {1} - High: {0[0]}, Low: {0[1]}, MinusLow: {0[2]}, MinusHigh: {0[3]}".format(score, data.id))
    
#main
#prefixes = ['60050']

prefixes = []
prefs = ['600','601', '603']
for pref in prefs:
    for i in range(10):
        prefixes.append(pref + str(i).zfill(1))

logging.basicConfig(filename= datetime.now().strftime("%Y_%m_%d_%H_%M_%S")+ '.log',level=logging.DEBUG)


# if(sys.getrecursionlimit() < 4000):
#    sys.setrecursionlimit(4000)
# logging.info("Current stack limit: {0}".format(sys.getrecursionlimit()))

startday = datetime.strptime("2015-07-01", '%Y-%m-%d').date()
endday = datetime.strptime("2015-10-16", '%Y-%m-%d').date()
stocks = fetchData_mongo(prefixes, startday, endday)
# writeToArffFile(stocks,"stock_7year.arff")

threading.stack_size(231072000)
subthread = threading.Thread(target=subprocessfunc, args=(stocks, endday))
# subthread = threading.Thread(target=subprocessPredictfunc, args=(stocks, endday))
logging.info("subthread started.")
subthread.start()
subthread.join()

# printGoodStock(stocks, tree1filter)
# verify(stocks, tree1filter, date.today(), 0.0)
logging.shutdown()
print ("Script ends.")
