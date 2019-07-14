#!/bin/env python

import sys, os
import argparse
parser = argparse.ArgumentParser()
parser.add_argument("-do2016", help="do 2016", action='store_true')
parser.add_argument("-do2018", help="do 2018", action='store_true')
parser.add_argument("-add", help="add", action="store_true")
args = parser.parse_args()

# ~ csbins = ["inc", "cspos", "csneg"]
# ~ programs = ["makeFit.py", "makeGraph.py"]
programs = ["makeGraph.py"]
uncertainties = ["nominal","scaleup","scaledown","pileup","piledown","smeared","muonid"]

for unc in uncertainties:
	cmd = "python signalYields.py -s %s"%unc
	
	print (cmd)
	os.system(cmd)
