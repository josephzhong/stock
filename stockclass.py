# -*- coding:utf-8 -*-  
import numpy as np
from datetime import timedelta
import math


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
        member_list = [m for m in dir(self)]
        for m in member_list:
            if m[0] != "_" and not callable(getattr(self,m)):
                setattr(self, m, dict[m])

    def obj2dict(self):
        member_list = [m for m in dir(self)]
        _dict = {}
        for m in member_list:
            if m[0] != "_" and not callable(getattr(self,m)):
                _dict[m] = getattr(self,m)
        return _dict

    def PChange(self):
        for idx, closePrice in enumerate(self.closePrices):
            if idx < 1 or self.openPrices[idx] == 0:
                self.changePrices.append(0.0)
            else:
                self.changePrices.append((self.closePrices[idx] - self.openPrices[idx])/self.openPrices[idx])

    def calc_v_ma5(self):

        for idx, date in enumerate(self.dates):
            vma5 = 0.0
            if idx >= 5 and len(self.volume[0:idx]) > 0:
                vma5 = np.nanmean(self.volume[idx-5:idx])
            else:
                if len(self.volume[0:idx]) == 0:
                    vma5 = self.volume[0]
                else:
                    vma5 = np.nanmean(self.volume[0:idx])
            if math.isnan(vma5):
                vma5 = 0.0
            self.v_ma5.append(vma5)

    def indexof(self, day):
        for idx, d in enumerate(self.dates):
            if d == day.isoformat():
                return idx
        yesterday = day + timedelta(days=-1)
        for idx, d in enumerate(self.dates):
            if d == yesterday.isoformat():
                return idx
        day_before_yesterday = yesterday + timedelta(days=-1)
        for idx, d in enumerate(self.dates):
            if d == day_before_yesterday.isoformat():
                return idx
        before_day_before_yesterday = day_before_yesterday + timedelta(days=-1)
        for idx, d in enumerate(self.dates):
            if d == before_day_before_yesterday.isoformat():
                return idx
        return -1

    def bollMd(self, day):
        result = 0.0
        index_end = self.indexof(day)
        if index_end > -1:
            index_start = index_end - 20
            if index_start < 0:
                index_start = 0
            if len(self.closePrices[index_start:index_end]) == 0:
                result = self.closePrices[index_end]
            else:
                result = np.nanmean(self.closePrices[index_start:index_end])
            if math.isnan(result):
                result = 0.0
        return result

    def bollUp(self, day):
        result = 0.0
        index_end = self.indexof(day)
        if index_end > -1:
            index_start = index_end - 20
            if index_start < 0:
                index_start = 0
            std = 0.0
            if len(self.closePrices[index_start:index_end]) > 0:
                std = np.std(self.closePrices[index_start:index_end])
            if math.isnan(std):
                std = 0.0
            result = self.bollMd(day) + 2*std
        return result

    def bollDn(self, day):
        result = 0.0
        index_end = self.indexof(day)
        if index_end > -1:
            index_start = index_end - 20
            if index_start < 0:
                index_start = 0
            std = 0.0
            if len(self.closePrices[index_start:index_end]) > 0:
                std = np.std(self.closePrices[index_start:index_end])
            if math.isnan(std):
                std = 0.0
            result = self.bollMd(day) - 2*std
        return result

    def v_b(self, v_5, v_today):
        if v_5 == 0.0:
            return 0.0
        else:
            return v_today/v_5

    def checkIfHengPan(self, current_day):
        period = 20
        up_limit = 0.3
        down_limit = -0.3
        idx_end = self.indexof(current_day)
        idx_start = idx_end - period
        if idx_end > -1 and idx_start > -1:
            for idx_day in range(idx_start, idx_end):
                delta = (self.closePrices[idx_day] - self.openPrices[idx_start])/self.openPrices[idx_start]
                if delta > up_limit or delta < down_limit:
                    return False
            return True
        return False
