# -*- coding:utf-8 -*-  
from stockclass import Stock
from data import floatFormat
import math, random, warnings,logging, sys
from datetime import date, timedelta, datetime
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