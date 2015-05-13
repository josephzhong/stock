# -*- coding:utf-8 -*-  
import tushare as ts
from datetime import date, timedelta
import numpy as np

class Stock:
    changePrices = []
    dates = []
    def PChange(self, openPrices, closePrices):
        for idx, openPrice in enumerate(openPrices):
            if (openPrice==0):
                self.changePrices.append(openPrice)
            else:
                self.changePrices.append((openPrice - closePrices[idx])/openPrice)
    
    def indexof(self, day):
        for idx, d in enumerate(self.dates):
            if(d == day.isoformat()):
                return idx
        return -1
    def bollMd(self, closePrices, day):
        result = 0
        indexend = self.indexof(day)
        if(indexend > -1):
            indexstart = indexend - 20
            if (indexstart < 0):
                indexstart = 0
            result = np.mean(closePrices[indexstart:indexend])
        return result
    def bollUp(self, closePrices, day):
        result = 0
        indexend = self.indexof(day)
        if(indexend > -1):
            indexstart = indexend - 20
            if (indexstart < 0):
                indexstart = 0
            std = np.std(closePrices[indexstart:indexend])
            result = self.bollMd(closePrices, day) + 2*std
        return result
    def bollDn(self, closePrices, day):
        result = 0
        indexend = self.indexof(day)
        if(indexend > -1):
            indexstart = indexend - 20
            if (indexstart < 0):
                indexstart = 0
            std = np.std(closePrices[indexstart:indexend])
            result = self.bollMd(closePrices, day) - 2*std
        return result
    def v_b(self, v_5, v_today):
        if (v_5 == 0):
            return 0
        else:
            return v_today/v_5

def filterStock(samples, conditionday):
    result = []
    for sample in samples:
        bMd = sample.bollMd(sample.closePrices, conditionday)
        bDn = sample.bollDn(sample.closePrices, conditionday)
        bUp = sample.bollUp(sample.closePrices, conditionday)
        yesterdayindex = sample.indexof(conditionday + timedelta(days=-1))
        todayindex = yesterdayindex + 1
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
    return result

def fetchData(dataPrefix):
    data = []
    for prefix in dataPrefix:
        for index in range(100):
            suffix = str(index).zfill(2)
            stockId = prefix + suffix
            try:    
                today = date.today()
                startday = today - timedelta(days=90)
                result = ts.get_hist_data(stockId, start=startday.isoformat(),end=today.isoformat())
                stock = Stock()
                stock.id = stockId
                stock.dates = result.index.tolist()
                stock.openPrices = result.open.values.tolist()
                stock.closePrices = result.close.values.tolist()
                stock.v_ma5 = result.v_ma5.values.tolist()
                stock.volume = result.volume.tolist()
                stock.PChange(stock.openPrices,stock.closePrices)
                data.append(stock)
            except Exception, e:
                print e
                print stockId + " is not a valid stock.\n"
    return data

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
#prefixes = ['600', '601', '603', '002']
prefixes = ['6000']
Threshold = 0    
stocks = fetchData(prefixes)
today = date.today()
goodstocks = filterStock(stocks, today)
print "Good stocks: "
for stock in goodstocks:
    print stock.id + "\n"

verify = averageTPFP(stocks, filterStock, today, Threshold)
print "Average TP/FP: " + str(verify[0]) + "/" + str(verify[1]) + "\n"


