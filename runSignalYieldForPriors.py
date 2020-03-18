#!/bin/env python

import sys, os
import argparse
parser = argparse.ArgumentParser()
parser.add_argument("-add", help="add", action="store_true")
args = parser.parse_args()

# ~ csbins = ["inc", "cspos", "csneg"]
# ~ programs = ["makeFit.py", "makeGraph.py"]
programs = ["produceHistogramsForPriorFits.py"]
uncertainties = ["nominal","scaleup","scaledown","pileup","piledown","smeared","muonid","pdfWeightsUp","pdfWeightsDown",'prefireup','prefiredown']
# ~ uncertainties = ["pdfWeightsUp","pdfWeightsDown"]

for unc in uncertainties:

	
	cmd = "python produceHistogramsForPriorFits.py --suffix %s"%unc
	if args.add:
		cmd += " -add"
	print (cmd)
	os.system(cmd)
