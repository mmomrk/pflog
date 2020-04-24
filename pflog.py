#!/usr/bin/env python3


class Pflog():
    def __init__(self, fname):
        self.fname = fname
        self.buf = {}
        self.names = {}
        self.firstLoop = True
        self.newlineName = ""
        self.capacity = 0

    @staticmethod
    def swap(ilist, pair):
        print (ilist)
        ilist[pair[0]], ilist[pair[1]] = ilist[pair[1]], ilist[pair[0]]
        print (ilist)
        return ilist

    @staticmethod
    def toWrStr(inames,idict):
        buf = [ idict[name] for name in inames]
        return "\t".join([str(x) for x in buf])+"\n"

    @staticmethod
    def rearrange(iarr, ipos):
        curs =list( range(len(iarr)))
        from collections import defaultdict as dedi
        accums = dedi(lambda : 0)
        for x in ipos:
            accums[x] += 1
        print("Acums:",accums)
        #for 
        print ("TODO FINISHED HERE !!!")
        return iarr

        
        

    def asd(self, val, nam, index = 0):
        # 'asd' is a shorter version of 'add'
        assert nam != "", "Empty name is not allowed"
        #print ("adding",val,nam)

        if nam in self.names.keys and self.firstLoop:
            self.firstLoop = False
            self.newlineName = self.names[-1]
            self.names = rearrange(self.names.keys, self.names.values)
            self.ofle = open(self.fname, 'w')
            self.ofle.write(Pflog.toWrStr(self.names.keys, {nam:nam for nam in self.names.keys}))
            self.ofle.write(Pflog.toWrStr(self.names.keys,self.buf))
            self.capacity = len(self.buf)
            assert self.capacity == len(
                self.names), "Bad init. Different name and val sizes"
            #print("DEBUG: set lap")
            #print ("DEBUG: newline name is ", self.newlineName)
            self.buf = {}
            self.asd(val, nam)
            return

        if self.firstLoop:
            self.names[nam] = index
        self.buf[nam] =  val

        if nam == self.newlineName:
            assert len(
                self.buf) == self.capacity, "Bad write with incomplete buf"+str(self.buf)+self.capacity
            ostr = Pflog.toWrStr(self.names.keys,self.buf)
            #print ("DEBUG: writing to file", ostr)
            self.ofle.write(ostr)
            self.buf = {}
        #print (self.buf)
        #print (self.names)

    def close(self):
        self.ofle.close()
