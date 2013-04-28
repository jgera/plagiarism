#! /usr/bin/env python3
# -*- coding: utf-8 -*-

import math

class SSK:
    def __init__(self, s, t, l = 0.5):
        self.s = s
        self.t = t
        self.l = l
    
    def __solve(self, s, t, p):
        result = [0.0 for x in range(0, p)]
        
        n = len(s)
        m = len(t)
        
        if p > max(n, m):
            return result
        
        d10 = [[0.0 for x in range(0, m + 1)] for x in range(0, n + 1)]
        d20 = [[0.0 for x in range(0, m + 1)] for x in range(0, n + 1)]
        d11 = [[0.0 for x in range(0, m + 1)] for x in range(0, n + 1)]
        d21 = [[0.0 for x in range(0, m + 1)] for x in range(0, n + 1)]
        d0 = [0.0 for x in range(0, n + 1)]
        
        for i in range(0, n + 1):
            for j in range(0, m + 1):
                d10[i][j] = 1.0
        
        l = self.l
        l2 = l * l
        d0[0] = 0
        
        for i in range(1, n + 1):
            d0[i] = d0[i - 1]
            for j in range(0, m):
                if t[j] == s[i - 1]:
                    d0[i] += d10[i - 1][j] * l2
        
        result[0] = d0[n]
        
        for k in range(1, p):
            for j in range(0, m + 1):
                d21[k - 1][j] = 0.0
            for i in range(k, n + 1):
                for j in range(0, k):
                    d21[i][j] = 0.0
                for j in range(k, m + 1):
                    if s[i - 1] == t[j - 1]:
                        d21[i][j] = l * (d21[i][j - 1] + l * d10[i - 1][j - 1])
                    else:
                        d21[i][j] = l * (d21[i][j - 1])
            
            for j in range(0, m + 1):
                d11[k - 1][j] = 0.0
            for i in range(k, n + 1):
                for j in range(0, k):
                    d11[i][j] = 0.0
                for j in range(k, m + 1):
                    d11[i][j] = l * d11[i - 1][j] + d21[i][j]
            
            d11, d10 = d10, d11
            d21, d20 = d20, d21
            
            for i in range(0, n + 1):
                d0[i] = 0.0
            for i in range(k + 1, n + 1):
                d0[i] = d0[i - 1]
                for j in range(0, m):
                    if t[j] == s[i - 1]:
                        d0[i] += d10[i - 1][j] * l2
            result[k] = d0[n]
        
        return result
    
    def solve(self, p):
        st = self.__solve(self.s, self.t, p)
        ss = self.__solve(self.s, self.s, p)
        tt = self.__solve(self.t, self.t, p)
        try:
            return st[p-1] / math.sqrt(ss[p-1] * tt[p-1])
        except ZeroDivisionError:
            pass
            return 0.0