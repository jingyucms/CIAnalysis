#!/bin/env python

import sys, os
import argparse
from scipy.optimize import curve_fit

def par_list(value):
	values = value.split()
	if len(values) != 3:
		raise argparse.ArgumentError
	values = map(float, values)
	return values

parser = argparse.ArgumentParser()
#parser.add_argument("-inFile", help="Input file", type=str)
parser.add_argument("-flav", help="Lepton flavor", type=str)
parser.add_argument("-unc",  help="Uncertainty", type=str, default="nominal")
parser.add_argument("-cs",   help="CS bin", type=str, default="inc")
parser.add_argument("-d","--debug", dest="debug", help="debug", action='store_true')
parser.add_argument("-do2016","--do2016", dest="do2016", help="do2016", action='store_true')
parser.add_argument("-do2018","--do2018", dest="do2018", help="do2018", action='store_true')
## need options and flags here :)
# parser.add_argument('--constraint', help="constraint for paramter (par up down)", nargs=3, action='append', type=float)
parser.add_argument('--constraint', help="constraint for paramter (par up down)", action='append', type=par_list)
parser.add_argument('--fitrange',   help="fit range (low, high)", nargs=2, type=float,default=(0.5,125000.))
parser.add_argument("--fixdes",     help="fix destructive fit parameters based on constructive", action='store_true')
parser.add_argument("--fixinf",     help="fix infinity fit parameter", action='store_true')
# fix 2nd parameter for destructive fits
#   with and without constraint
# fix constant term parameter with constraint
# emutype

args        = parser.parse_args()
debug       = args.debug
constraints = {"p{0:d}".format(int(key)): None for key in range(3)}

if args.constraint:
	constraints = {"p{0:d}".format(int(key)): (low,high) for [key,low,high] in args.constraint}
print(constraints)

from ADDfitUtils import doFitOnGraph

import ROOT as r
import numpy as np
#~ from nesteddict import nesteddict as ndict
import json

from setTDRStyle import setTDRStyle
setTDRStyle()

r.gROOT.SetBatch(True)
r.gErrorIgnoreLevel = r.kWarning

if args.do2016:
	lvals = [3.5 +i *0.5 for i in range(12)]
	lvals.append(10)
	#lvals.append(100000)
else:
	lvals = [5+i for i in range(8)]
	#lvals.append(100000)

lerrs = [0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1]
bvals = [i for i in range(len(lvals))]
#helis = ["LL","LR","RR"]
intfs = [""]
#supers      = [400,500,700,1100,1900,3500,10000]
#grbins      = [400,500,700,1100,1900,3500]
#grcols      = [r.kBlack,r.kRed,r.kBlue,r.kYellow,r.kViolet,r.kGreen]
helis = [""]
supers = [2000, 2200, 2600, 3000, 3400, 10000]
grbins = [2000, 2200, 2600, 3000, 3400]
grcols = [r.kBlack, r.kRed, r.kBlue, r.kYellow, r.kViolet, r.kOrange, r.kCyan, r.kGreen, r.kAzure, r.kTeal, r.kPink]
extragrbins = [1900+x for x in range(0,1500,200)]

uncertainties = [
	"nominal",
	"scaleup",
	"scaledown",
	## ele only
	"pileup",
	"piledown",
	## muon only
	"smeared",
	"muonid",
	]
etabins = ["bb","be"]
#             0    1    2    3
csbins = ["inc","cspos","csneg"]
#            0     1     2

csbin  = args.cs
unc    = args.unc
if args.do2016:
	filefmt  = "2{0:s}_{1:s}_{2:s}_{3:s}_{4:s}_{5:s}{6:s}_2016"
elif args.do2018:
	filefmt  = "2{0:s}_{1:s}_{2:s}_{3:s}_{4:s}_{5:s}{6:s}_2018"
else:	
	filefmt  = "2{0:s}_{1:s}_{2:s}_{3:s}_{4:s}_{5:s}{6:s}_2017"
modifier = ""
if args.fixdes:
	modifier += "_fixdes"
	pass
if args.fixinf:
	modifier += "_fixinf"
	pass
if constraints["p0"]:
	modifier += "_limitp0"
	pass
if constraints["p1"]:
	modifier += "_limitp1"
	pass
if constraints["p2"]:
	modifier += "_limitp2"
	pass

if csbin not in csbins:
	print("CS bin '{0}' not in:".format(csbin),csbins)
	exit(1)
if unc not in uncertainties:
	print("Plot type '{0}' not in:".format(unc),uncertainties)
	exit(1)

# if __name__ == "__main__":
for etabin in etabins:
	for emutype in ["e","mu"]:
		muonlyuncs = ["muonid", "smeared"]
		eleonlyuncs = ["pileup", "piledown"]
		if unc in muonlyuncs and emutype == "e":
			print("Not processing uncertainty '{0:s}' for leptonn flavour '{1:s}'".format(unc,emutype))
			continue
		if unc in eleonlyuncs and emutype == "mu":
			print("Not processing uncertainty '{0:s}' for leptonn flavour '{1:s}'".format(unc,emutype))
			continue
		# xvals=np.zeros(len(lvals),'float64')
		xvals=np.array(lvals,dtype='float64')
		xerrs=np.array(lerrs,dtype='float64')
		# emutype = "mu"
		addLabel = ""
		if args.do2016:
			addLabel = "_2016"
		elif args.do2018:
			addLabel = "_2018"
		with open("fitFiles/addparametrization_2{0:s}_{1:s}_{2:s}_{3:s}{4:s}.json".format(emutype,unc,etabin,csbin,addLabel),"r") as js:
			print("fitFiles/addto2{0:s}_{1:s}_{2:s}_{3:s}_parametrization{4:s}{5:s}.root".format(emutype,unc,etabin,csbin,modifier,addLabel))
			params = json.load(js)
			outf = r.TFile("fitPlots/addto2{0:s}_{1:s}_{2:s}_{3:s}_parametrization{4:s}{5:s}.root".format(emutype,unc,etabin,csbin,modifier,addLabel), "recreate")
			for heli in helis:
				conFitPar = []
				for intf in intfs:
					print("Fitting primary bins for the limits")
					for i,point in enumerate(supers[:-1]):
						doFitOnGraph(params, lvals, xvals, xerrs,
									 intf, heli, i, point, outf, conFitPar,
									 args.fixinf, args.fixdes, constraints, args.fitrange)
						pass
					print("Fitting extra bins for the mass scan")
					for i,point in enumerate(extragrbins):
						doFitOnGraph(params, lvals, xvals, xerrs,
									 intf, heli, 1, point, outf, conFitPar,
									 args.fixinf, args.fixdes, constraints, args.fitrange)
						pass
					# raw_input("continue")
					pass
				pass
			outf.Write()

			for heli in helis:
				conFitPar = []
				for intf in intfs:
					can = r.TCanvas("can","",800,800)
					r.gStyle.SetOptStat(0)
					r.gStyle.SetOptFit(0)
					grMass = {}
					fMass  = {}
					leg = r.TLegend(0.5,0.7,0.95,0.9)
					for grbin in grbins:
						grMass[grbin] = outf.Get("gr_{0:s}{1:s}_m{2:d}".format(intf,heli,grbin))
						#fMass[grbin]  = outf.Get("fn_m{2:d}_{0:s}{1:s}".format(intf,heli,grbin)).GetChisquare()
						fMass[grbin]  = outf.Get("fitR_m{2:d}_{0:s}{1:s}".format(intf,heli,grbin)).Chi2()
						ndf = outf.Get("fitR_m{2:d}_{0:s}{1:s}".format(intf,heli,grbin)).Ndf()
	
						if grbin == grbins[0]: #400 for CI
							grMass[grbin].Draw("ap")
							r.gStyle.SetOptStat(0)
							r.gStyle.SetOptFit(0)
							r.gPad.SetLogy(r.kTRUE)
							r.gPad.SetLogx(r.kTRUE)
						else:
							grMass[grbin].Draw("psame")
							pass
						grMass[grbin].GetYaxis().SetRangeUser(1,1e7)
						grMass[grbin].SetMinimum(0.001)
						grMass[grbin].SetMaximum(1e7)
						grMass[grbin].SetMarkerColor(grcols[grbins.index(grbin)])
						if debug:
							print("Finding {0:d} in supers".format(grbin),supers)
							pass
						suIdx = supers.index(grbin)
						leg.AddEntry(grMass[grbin], "{0:d} < M_{{ll}} [GeV] < {1:d}, #chi^{{2}}/NDF = {2:2.2f}/{3:d}".format(supers[suIdx], supers[suIdx+1], fMass[grbin], ndf), "p")
						r.gPad.Update()
						pass
					leg.Draw("")
					can.Modified()
					can.Update()
					r.gPad.Update()

					#for ftype in ["png","C","pdf","eps"]:
					for ftype in ["pdf"]:
						can.SaveAs("fitPlots/params_{1:s}.{0:s}".format(ftype,filefmt.format(emutype,intf,heli,unc,etabin,csbin,modifier)))
						pass
					can.Clear()
					can.Update()

					leg = r.TLegend(0.5,0.7,0.95,0.9)
					for extrabin in extragrbins:
						grMass[extrabin] = outf.Get("gr_{0:s}{1:s}_m{2:d}".format(intf,heli,extrabin))
						# fMass[extrabin]  = outf.Get("fn_m{2:d}_{0:s}{1:s}".format(intf,heli,extrabin)).GetChisquare()
						fMass[extrabin]  = outf.Get("fitR_m{2:d}_{0:s}{1:s}".format(intf,heli,extrabin)).Chi2()
						ndf = outf.Get("fitR_m{2:d}_{0:s}{1:s}".format(intf,heli,extrabin)).Ndf()
	
						if extragrbins.index(extrabin) == 0:
							grMass[extrabin].Draw("ap")
							r.gStyle.SetOptStat(0)
							r.gStyle.SetOptFit(0)
							r.gPad.SetLogy(r.kTRUE)
							r.gPad.SetLogx(r.kTRUE)
						else:
							grMass[extrabin].Draw("psame")
							pass
						grMass[extrabin].GetYaxis().SetRangeUser(1,1e7)
						grMass[extrabin].SetMinimum(0.001)
						grMass[extrabin].SetMaximum(1e7)
						grMass[extrabin].SetMarkerColor(r.kOrange+extragrbins.index(extrabin))
						leg.AddEntry(grMass[extrabin], "{0:d} < M_{{ll}} [GeV], #chi^{{2}}/NDF = {1:2.2f}/{2:d}".format(extrabin, fMass[extrabin], ndf), "p")
						r.gPad.Update()
						pass
					leg.Draw("")
					can.Modified()
					can.Update()
					r.gPad.Update()

					# raw_input("continue")
					#for ftype in ["png","C","pdf","eps"]:
					for ftype in ["pdf"]:
						can.SaveAs("fitPlots/scanmass_{1:s}.{0:s}".format(ftype,filefmt.format(emutype,intf,heli,unc,etabin,csbin,modifier)))
						pass
					pass
				pass
			outf.Close()
			pass
		pass
