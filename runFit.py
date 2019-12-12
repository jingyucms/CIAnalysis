#!/bin/env python

import sys, os
import argparse
parser = argparse.ArgumentParser()
parser.add_argument("-do2016", help="do 2016", action='store_true')
parser.add_argument("-do2018", help="do 2018", action='store_true')
parser.add_argument("-add", help="add", action="store_true")
args = parser.parse_args()

csbins = ["inc", "cspos", "csneg"]
programs = ["makeFit.py", "makeGraph.py"]
# ~ programs = ["makeGraph.py"]
# ~ uncertainties = ["","scaleup","scaledown","pileup","piledown","smeared","muonid"]
uncertainties = ["","scaleup","scaledown","pileup","piledown","smeared","muonid"]

for cs in csbins:
	for program in programs:
		for unc in uncertainties:
			cmd = "python %s"%program
			if args.add:
				cmd = cmd + " -add"
			if args.do2016:
				cmd = cmd + " -do2016"
			elif args.do2018:
				cmd = cmd + " -do2018"
			if cs != "inc":
				cmd = cmd + " -cs %s"%cs
			if unc != "":
				cmd = cmd + " -unc %s"%unc
			if args.add and "Graph" in program:
				cmd = cmd + " --fixinf" 
				if args.do2016:
					cmd = cmd + " --fitrange 3 11" 
				else:	
					cmd = cmd + " --fitrange 3.5 110" 
			if not args.add and "Graph" in program:
				cmd = cmd + " --fixinf --fixdes --constraint '0 0 1e4' --constraint '1 0 1e9' --constraint '2 0 1e9'"
			print (cmd)
			os.system(cmd)
