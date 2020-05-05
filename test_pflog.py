#!/usr/bin/env python3

import unittest
import pflog as pf
import sys
import os


class testPflog(unittest.TestCase):
    def testInit(self):
        fnam = "hello.delit"
        x = pf.Pflog(fnam)
        assert x is not None, "Bad init"
        assert x.buf == {} and x.names == {
        } and x.firstLoop == True and x.newlineName == "", "A very stupid test failed"
        x.asd(1, '1')
        x.asd(2, '1')
        assert x.firstLoop == False, "No first loop detection"
        x.close()
        assert os.path.isfile(fnam), "out file not created"
        fle = open(fnam, 'r')
        lines = fle.readlines()
        fle.close()
        os.remove(fnam)
        assert "1" in lines[0] and "1" in lines[1] and "2" in lines[2], "File written incorrectly"

    def testNWrites(self):
        num = 10
        names = [str(i)+".delit" for i in range(num)]
        pfls = [pf.Pflog(name) for name in names]
        for _ in range(100):
            for i, pfl in enumerate(pfls):
                for t in range(i+1):
                    pfl.asd(t, str(t)+"_"+str(t))
        for pfl in pfls:
            pfl.close()

        for name in names:
            assert os.path.isfile(name), name+" was not created in the test"
            fle = open(name, 'r')
            lines = fle.readlines()
            fle.close()
            os.remove(name)
            assert len(lines[0].split()) == int(
                name.split('.')[0])+1, "Bad number of columns"

    def testRearrange(self):
        n = int(10)
        names = [str(i) for i in range(-int(n/2), int(n/2))]
        fnam = 'hard.delit'
        ol = pf.Pflog(fnam)
        for _ in range(5):
            for val, name in zip(range(n), names):
                ol.asd(val, name, ind=int(int(name)/2))
        ol.close()

        assert os.path.isfile(fnam), name+" was not created in the test"
        fle = open(fnam, 'r')
        lines = fle.readlines()
        fle.close()
        os.remove(fnam)
        assert lines[0] == '\t'.join([str(i) for i in [2, 3, 4, -1, 0, 1, -2, -4, -5, -3]]) + \
            '\n', "Bad rearrange result. May be a consequence of changing the queueing and priorities; " + \
            lines[0]

    def testIndSame(self):
        fnam = 'ind.delit'
        ol = pf.Pflog(fnam)
        for _ in range(10):
            ol.asd(1, '1', ind=-1)
            ol.asd(2, '2', ind=-1)
            ol.asd(3, '3', ind=-1)
        ol.close()
        assert os.path.isfile(fnam), name+" was not created in the test"
        fle = open(fnam, 'r')
        lines = fle.readlines()
        fle.close()
        os.remove(fnam)
        assert lines[0] == '\t'.join(
            [str(i) for i in [3, 2, 1]]) + '\n', "Failed test of repeated ind=-1"

    def testIndOverflow(self):
        fnam = 'indof.delit'
        ol = pf.Pflog(fnam)
        for _ in range(10):
            ol.asd(1, '1', ind=11)
            ol.asd(2, '2', ind=-11)
            ol.asd(3, '3')
        ol.close()
        assert os.path.isfile(fnam), name+" was not created in the test"
        fle = open(fnam, 'r')
        lines = fle.readlines()
        fle.close()
        os.remove(fnam)
        assert lines[0] == '\t'.join(
            [str(i) for i in [2, 3, 1]]) + '\n', "Failed test of repeated ind=-1"

    def testXprint(self):
        # I don't have any idea how to write this test in a reasonable amount of time
        pass


if __name__ == "__main__":
    unittest.main()
