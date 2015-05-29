# -*- coding:utf-8 -*-  
import numpy as np
from datetime import date, timedelta, datetime
import math, random
class Stock:
    def __init__(self):
        self.changePrices = []
        self.dates = []
        self.openPrices = []
        self.closePrices = []
        self.v_ma5 = []
        self.volume = []
        self.name = u""
        self.score = 0.0
    def dict2obj(self, dict):
        #"""
        #summary:
        #��objectת����dict����
        memberlist = [m for m in dir(self)]
        for m in memberlist:
            if m[0] != "_" and not callable(getattr(self,m)):
                setattr(self, m, dict[m])
    def obj2dict(self):
        #"""
        #summary:
        #��objectת����dict����
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
    def calc_v_ma5(self):
        for idx, date in enumerate(self.dates):
            vma5 = 0.0
            if(idx >= 5 and len(self.volume[0:idx]) > 0):
                vma5 = np.nanmean(self.volume[idx-5:idx])
            else:
                if(len(self.volume[0:idx]) == 0):
                    vma5 = self.volume[0]
                else:
                    vma5 = np.nanmean(self.volume[0:idx])
            if(math.isnan(vma5)):
                vma5 = 0.0
            self.v_ma5.append(vma5)
    def indexof(self, day):
        for idx, d in enumerate(self.dates):
            if(d == day.isoformat()):
                return idx
        #todayû�����ݾ���ǰ��һ�죬�����ǰ��3��
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
        result = 0.0
        indexend = self.indexof(day)
        if(indexend > -1):
            indexstart = indexend - 20
            if (indexstart < 0):
                indexstart = 0
            if(len(self.closePrices[indexstart:indexend]) == 0):
                result = self.closePrices[indexend]
            else:
                result = np.nanmean(self.closePrices[indexstart:indexend])
            if(math.isnan(result)):
                result = 0.0
        return result
    def bollUp(self, day):
        result = 0.0
        indexend = self.indexof(day)
        if(indexend > -1):
            indexstart = indexend - 20
            if (indexstart < 0):
                indexstart = 0
            std = 0.0
            if(len(self.closePrices[indexstart:indexend]) > 0):
                std = np.std(self.closePrices[indexstart:indexend])
            if(math.isnan(std)):
                std = 0.0
            result = self.bollMd(day) + 2*std
        return result
    def bollDn(self, day):
        result = 0.0
        indexend = self.indexof(day)
        if(indexend > -1):
            indexstart = indexend - 20
            if (indexstart < 0):
                indexstart = 0
            std = 0.0
            if(len(self.closePrices[indexstart:indexend]) > 0):
                std = np.std(self.closePrices[indexstart:indexend])
            if(math.isnan(std)):
                std = 0.0
            result = self.bollMd(day) - 2*std
        return result
    def v_b(self, v_5, v_today):
        if (v_5 == 0.0):
            return 0.0
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
    