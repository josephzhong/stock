# -*- coding:utf-8 -*-  
import tushare as ts
from datetime import date, timedelta
import numpy as np
import json
from os.path import exists, join
from string import split
import threading
import Queue, math
from multiprocessing.dummy import Pool as ThreadPool

class Stock:
    def __init__(self):
        self.changePrices = []
        self.dates = []
        self.openPrices = []
        self.closePrices = []
        self.v_ma5 = []
        self.volume = []
    def dict2obj(self, dict):
        #"""
        #summary:
        #将object转换成dict类型
        memberlist = [m for m in dir(self)]
        for m in memberlist:
            if m[0] != "_" and not callable(getattr(self,m)):
                setattr(self, m, dict[m])
    def obj2dict(self):
        #"""
        #summary:
        #将object转换成dict类型
        memberlist = [m for m in dir(self)]
        _dict = {}
        for m in memberlist:
            if m[0] != "_" and not callable(getattr(self,m)):
                _dict[m] = getattr(self,m)
        return _dict
    def PChange(self):
        for idx, openPrice in enumerate(self.openPrices):
            if (openPrice==0):
                self.changePrices.append(openPrice)
            else:
                self.changePrices.append((self.closePrices[idx]- openPrice)/openPrice)
    
    def indexof(self, day):
        for idx, d in enumerate(self.dates):
            if(d == day.isoformat()):
                return idx
        return -1
    def bollMd(self, day):
        result = 0
        indexend = self.indexof(day)
        if(indexend > -1):
            indexstart = indexend - 20
            if (indexstart < 0):
                indexstart = 0
            result = np.mean(self.closePrices[indexstart:indexend])
        return result
    def bollUp(self, day):
        result = 0
        indexend = self.indexof(day)
        if(indexend > -1):
            indexstart = indexend - 20
            if (indexstart < 0):
                indexstart = 0
            std = np.std(self.closePrices[indexstart:indexend])
            result = self.bollMd(day) + 2*std
        return result
    def bollDn(self, day):
        result = 0
        indexend = self.indexof(day)
        if(indexend > -1):
            indexstart = indexend - 20
            if (indexstart < 0):
                indexstart = 0
            std = np.std(self.closePrices[indexstart:indexend])
            result = self.bollMd(day) - 2*std
        return result
    def v_b(self, v_5, v_today):
        if (v_5 == 0):
            return 0
        else:
            return v_today/v_5

def fetchDataOneThread(prefix):
    today = date.today()
    startday = today - timedelta(days=90)
    data = []
    for index in range(pow(10,(6-len(prefix)))):
        suffix = str(index).zfill(6-len(prefix))
        stockId = prefix + suffix
        try:    
            result = ts.get_hist_data(stockId, start=startday.isoformat(),end=today.isoformat())
            stock = Stock()
            stock.id = stockId
            stock.dates = result.index.tolist()
            stock.openPrices = result.open.values.tolist()
            stock.closePrices = result.close.values.tolist()
            stock.v_ma5 = result.v_ma5.values.tolist()
            stock.volume = result.volume.tolist()
            stock.PChange()
            data.append(stock)
        except Exception, e:
            print e
            if(str(e).find("list index out of range") > -1):
                print str(e)
            print stockId + " is not a valid stock.\n"
    return data

def fetchData(dataPrefix):
    path = "d:\\work\\doors\\project\\cd7\\stock"
    data = []
    today = date.today()
    startday = today - timedelta(days=90)
    dataLastDateStr = today
    filepath = join(path, "stock.dat")
    if(exists(filepath)):
        try:
            dataFile = open(filepath)
            dataLoad = json.load(dataFile)
            dataLastDateStr = dataLoad["LastUpdateDate"]
            dataLoadDicts = dataLoad["data"]
            for dict in dataLoadDicts:
                stk = Stock()
                stk.dict2obj(dict)
                data.append(stk)
            dataFile.close()
            if(dataLastDateStr == today.isoformat()):
                return data
            ymd = split(dataLastDateStr, ",")
            startday = date(ymd[0],ymd[1],ymd[2]) + timedelta(days=1)
        except Exception, e:
            print e
    pool = ThreadPool(len(dataPrefix))
    results = pool.map(fetchDataOneThread, dataPrefix)
    pool.close()
    pool.join()
    for result in results:
        data.extend(result)
    #dataFile = open(filepath,"w")
    #datadicts = []
    #for dta in data:
    #    datadicts.append(dta.obj2dict())
    #dataStore = {"LastUpdateDate" : today.isoformat(), "data" : datadicts}
    #dataJsonString = json.dump(dataStore, dataFile)
    #dataFile.close()
    return data

def filterStock(samples, conditionday):
    result = []
    for sample in samples:
        try:
            bMd = sample.bollMd(conditionday)
            bDn = sample.bollDn(conditionday)
            bUp = sample.bollUp(conditionday)
            yesterdayindex = sample.indexof(conditionday + timedelta(days=-1))
            todayindex = sample.indexof(conditionday)
            if(yesterdayindex == -1 or todayindex == -1):
                yesterdayindex = sample.indexof(conditionday + timedelta(days=-2))
                todayindex = sample.indexof(conditionday + timedelta(days=-1))
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
                                if(thisV_b > 1.4):
                                    result.append(sample)
        except Exception, e:
            print e
    return result

def checkTPFP(positives, conditionday, thres):
    tpositives = 0
    for positive in positives:
        index = positive.indexof(conditionday)
        if(index > -1 and positive.changePrices[index + 1] >= Threshold):
            tpositives += 1
    if (len(positives)==0):
        return [0.0, 1.0]
    else:
        return [float(tpositives)/len(positives), float(len(positives)-tpositives)/len(positives)]
    
def averageTPFP(targets, filter, conditionday, thres):
    verifydays = [conditionday+timedelta(days=-10), conditionday+timedelta(days=-20), conditionday+timedelta(days=-30)]
    sum = [0.0, 0.0]
    for day in verifydays:
        filteredstocks = filter(targets, day)
        tpfp = checkTPFP(filteredstocks, day, thres)
        print day.isoformat() + " TP/FP: " + str(tpfp[0]) + "/" + str(tpfp[1]) + "\n"
        sum[0] += tpfp[0]
        sum[1] += tpfp[1]
    return [sum[0]/len(verifydays), sum[1]/len(verifydays)]
        
stocks = []
goodstocks = []

prefixes = ['6000','6001','6002','6003','6004','6005','6006','6007','6008','6009', '6010', '6011', '6012', '6013', '6014', '6015', '6016', '6017',  '6018', '6019', '6030', '6031', '6032', '6033', '6034', '6035', '6036', '6037', '6038', '6039', '0020','0021','0022','0023','0024','0025','0026','0027','0028','0029']
#prefixes = ['6000','6001','6002','6003']
Threshold = 0    
stocks = fetchData(prefixes)
today = date.today()
goodstocks = filterStock(stocks, today)
print "Good stocks: "
if (len(goodstocks) == 0):
    print "No good stock found.\n"
for stock in goodstocks:
    print stock.id + "\n"

verify = averageTPFP(stocks, filterStock, today, Threshold)
print "Average TP/FP: " + str(verify[0]) + "/" + str(verify[1]) + "\n"


