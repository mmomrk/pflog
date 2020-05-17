#!/usr/bin/env python3

import collections
import sys

levels = ['TRACE', 'DEBUG', 'INFO', 'WARNING', 'ERROR', 'CRITICAL', 'NONE']
# Not sure if I need to code this further before I find out the right lib for this
errfile = sys.stderr
critfile = errfile
loglevel = 'TRACE'


def tprint(*args, **kwargs):
    if levels.index(loglevel) < 1:
        print("TRACE: ", *args, **kwargs)


def dprint(*args, **kwargs):
    if levels.index(loglevel) < 2:
        print("DEBUG: ", *args, **kwargs)


def iprint(*args, **kwargs):
    if levels.index(loglevel) < 3:
        print("INFO: ", *args, **kwargs)


def wprint(*args, **kwargs):
    if levels.index(loglevel) < 4:
        print("WARNING: ", *args, **kwargs)


def eprint(*args, **kwargs):
    if levels.index(loglevel) < 5:
        print("ERROR: ", *args, **kwargs, file=sys.stderr)


def cprint(*args, **kwargs):
    if levels.index(loglevel) < 6:
        print("CRITICAL: ", *args, **kwargs, file=critfile)


def nprint(*args, **kwargs):
    # We are listening to you and will make everything possible to solve the issue
    pass


class Pflog():
    def __init__(self, fname):
        self.fname = fname
        self.buf = {}
        self.names = collections.OrderedDict()
        self.firstLoop = True
        self.newlineName = ""
        self.capacity = 0
        self.finalNameOrder = []
        self.ofle = None

    @staticmethod
    def swap(ilist, pair):
        print(ilist)
        ilist[pair[0]], ilist[pair[1]] = ilist[pair[1]], ilist[pair[0]]
        print(ilist)
        return ilist

    @staticmethod
    def toWrStr(inames, idict):
        # Expects input ordered names and dictionary with fresh values. Will write values from dictionary getting it by keys in the order from inames
        buf = [idict[name] for name in inames]
        return "\t".join([str(x) for x in buf])+"\n"

    @staticmethod
    def rearrange(inamesDict):
        iarr = inamesDict.keys()
        ipos = inamesDict.values()
        # current positions
        n = len(iarr)
        curs = list(range(n))
        # counters of currently vacant position
        negC = -1
        posC = 1
        ret = [""]*n
        # requests = sorted(inamesDict.items(), key=lambda t : t[1])
        # print ("Sorted requests are", requests)
        # for cand in requests:
        #print("Ginput:", inamesDict)
        fillers = []
        for cand in inamesDict.items():
            # print(cand)
            # print(ret)
            r = cand[1]
            name = cand[0]
            if r == 0:
                fillers.append(name)
                continue
            # 0 is default and means no priority:
            if r > 0:
                r = r-1
            if r < -n:
                r = -n
            # r is used as index in the array now:
            if r > n - 1:
                r = n - 1
            if ret[r] == "":
                ret[r] = name
            else:
                if r >= 0:
                    for r1 in range(r+1, n):
                        #print("trying ", r1)
                        if ret[r1] == "":
                            ret[r1] = name
                            break
                    else:
                        print("WARNING: could not resolve conflict with " +
                              name+". Will put it to a free unclaimed column")
                        fillers.append(name)
                else:  # r is < 0 for sure
                    #print("Running now on ", list(range(n+r-1, -1, -1)))
                    for r1 in range(n+r-1, -1, -1):
                        #print("trying ", r1)
                        if ret[r1] == "":
                            ret[r1] = name
                            break
                    else:
                        print("WARNING: could not resolve conflict with " +
                              name+". Will put it to a free unclaimed column")
                        fillers.append(name)
        fj = 0
        for i, n in enumerate(ret):
            if n == "":
                ret[i] = fillers[fj]
                fj += 1
        #print("Compiled ret:", ret)
        return ret

    def asd(self, val, nam, ind=0):
        # 'asd' is a shorter version of 'add'
        assert nam != "", "Empty name is not allowed"
        # print ("adding",val,nam)

        if nam in self.names.keys() and self.firstLoop:
            self.firstLoop = False

            self.newlineName = self.prevName
            # print("rearrange")
            self.finalNameOrder = Pflog.rearrange(self.names)
            self.ofle = open(self.fname, 'w')
            self.ofle.write(Pflog.toWrStr(self.finalNameOrder, {
                            nam: nam for nam in self.names.keys()}))
            self.ofle.write(Pflog.toWrStr(self.finalNameOrder, self.buf))
            self.capacity = len(self.buf)
            assert self.capacity == len(
                self.names), "Bad init. Different name and val sizes"
            # print("DEBUG: set lap")
            # print ("DEBUG: newline name is ", self.newlineName)
            self.buf = {}
            self.asd(val, nam)
            return

        if self.firstLoop:
            self.names[nam] = ind
            self.prevName = nam
        self.buf[nam] = val

        if nam == self.newlineName:
            assert len(
                self.buf) == self.capacity, "Bad write with incomplete buf"+str(self.buf)+self.capacity
            ostr = Pflog.toWrStr(self.finalNameOrder, self.buf)
            # print ("DEBUG: writing to file", ostr)
            self.ofle.write(ostr)
            self.buf = {}
        # print (self.buf)
        # print (self.names)

    def close(self):
        if self.ofle:
            self.ofle.close()
