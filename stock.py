# -*- coding:utf-8 -*-  
import tushare as ts
from datetime import date, timedelta
import numpy as np
import json
from os.path import exists, join
from string import split
import threading
import Queue, math, random
from multiprocessing.dummy import Pool as ThreadPool

class Stock:
    def __init__(self):
        self.changePrices = []
        self.dates = []
        self.openPrices = []
        self.closePrices = []
        self.v_ma5 = []
        self.volume = []
        self.name = u""
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
        for idx, closePrice in enumerate(self.closePrices):
            if (idx < 1 or self.openPrices[idx]==0):
                self.changePrices.append(0.0)
            else:
                self.changePrices.append((self.closePrices[idx] - self.openPrices[idx])/self.openPrices[idx])
    
    def indexof(self, day):
        for idx, d in enumerate(self.dates):
            if(d == day.isoformat()):
                return idx
        #today没有数据就往前推一天，最多往前推3天
        yesterday = day + timedelta(days=-1)
        for idx, d in enumerate(self.dates):
            if(d == yesterday.isoformat()):
                return idx
        daybeforeyesterday = yesterday + timedelta(days=-1)
        for idx, d in enumerate(self.dates):
            if(d == daybeforeyesterday.isoformat()):
                return idx
        beforedaybeforeyesterday = daybeforeyesterday + timedelta(days=-1)
        for idx, d in enumerate(self.dates):
            if(d == beforedaybeforeyesterday.isoformat()):
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
    def checkIfHengPan(self, currentday):
        period = 20
        uplimit = 0.3
        downlimit = -0.3
        idxend = self.indexof(currentday)
        idxstart = idxend - period
        if(idxend > -1 and idxstart > -1):
            for idxday in range(idxstart, idxend):
                delta = (self.closePrices[idxday] - self.openPrices[idxstart])/self.openPrices[idxstart]
                if ( delta > uplimit or delta < downlimit):
                    return False
            return True
        return False

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

def fetchToday(stocks):
    today = date.today()
    stocksnow = ts.get_today_all()
    codes = stocksnow.code.tolist()
    for stock in stocks:
        stockidx = -1
        for codeidx, code in enumerate(codes):
            if(stock.id == code):
                stockidx = codeidx
                break
        if(stockidx > -1):
            stock.name = stocksnow.name.tolist()[stockidx]
            if(len(stock.dates) - 1 < 0):
                continue
            if(today.isoformat() != stock.dates[len(stock.dates) - 1]):
                if(len(stock.closePrices) - 1 < 0):
                    continue
                stock.dates.append(today)
                stock.openPrices.append(stocksnow.open.tolist()[stockidx])
                stock.closePrices.append(stocksnow.trade.tolist()[stockidx])
                if(stocksnow.open.tolist()[stockidx] == 0.0):
                    stock.changePrices.append(0.0)
                else:
                    stock.changePrices.append((stocksnow.trade.tolist()[stockidx] - stocksnow.open.tolist()[stockidx])/stocksnow.open.tolist()[stockidx])
                stock.volume.append(stocksnow.volume.tolist()[stockidx])
                idx = stock.indexof(today)
                if(idx >= 4):
                    stock.v_ma5.append((stock.volume[idx] + stock.volume[idx - 1] + stock.volume[idx - 2] + stock.volume[idx - 3] + stock.volume[idx - 4])/5)
                else:
                    total = 0
                    i = 0
                    while(i<=idx):
                        total += stock.volume[idx - i]
                        i += 1
                    stock.v_ma5.append(total/(idx + 1))
                    
def fetchData(dataPrefix):
    path = "d:\\work\\doors\\project\\cd7\\stock"
    data = []
    pool = ThreadPool(len(dataPrefix))
    results = pool.map(fetchDataOneThread, dataPrefix)
    pool.close()
    pool.join()
    for result in results:
        data.extend(result)
    #fetchToday(data)
    return data

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
        except Exception, e:
            print e
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
    verifytimes = len(verifydays)
    for day in verifydays:
        filteredstocks = filter(targets, day)
        tpfp = checkTPFP(filteredstocks, day, thres)
        print "{0} TP/FP: {1[0]:.2%}/{1[1]:.2%}\n".format(day.isoformat(), tpfp)
        sum[0] += tpfp[0]
        sum[1] += tpfp[1]
        if(tpfp[0] == 0.0 and tpfp[1] == 0.0):
            verifytimes = verifytimes - 1
    if(verifytimes == 0):
        return [0.0, 0.0]
    return [sum[0]/verifytimes, sum[1]/verifytimes]
        
stocks = []
goodstocks = []

prefixes = ['6000','6001','6002','6003','6004','6005','6006','6007','6008','6009', '6010', '6011', '6012', '6013', '6014', '6015', '6016', '6017',  '6018', '6019', '6030', '6031', '6032', '6033', '6034', '6035', '6036', '6037', '6038', '6039', '0020','0021','0022','0023','0024','0025','0026','0027','0028','0029']
#prefixes = ['6003']
Threshold = 0
stocks = fetchData(prefixes)
today = date.today()
goodstocks = filterStock(stocks, today)
print "Good stocks: "
if (len(goodstocks) == 0):
    print "No good stock found.\n"
for stock in goodstocks:
    print u"{0}\t{1}\tlast day of data on {2}\n".format(stock.id, stock.name, stock.dates[len(stock.dates) - 1])

verify = averageTPFP(stocks, filterStock, today, Threshold)
print "Average TP/FP: {0[0]:.2%} / {0[1]:.2%}\n".format(verify)


