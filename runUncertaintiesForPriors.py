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
uncertainties = ["nominal","scaleup","scaledown","pileup","piledown","smeared","muonid","pdfWeightsUp","pdfWeightsDown",'prefireup','prefiredown',"pdfUncertainty"]
# ~ uncertainties = ["pdfWeightsUp","pdfWeightsDown"]

for unc in uncertainties:

	
	cmd = "python produceSystematicsForPriors.py -s %s"%unc
	if args.add:
		cmd += " -add"
	print (cmd)
	os.system(cmd)
