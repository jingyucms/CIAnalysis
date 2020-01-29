#!/bin/env python

import sys, os
import argparse
parser = argparse.ArgumentParser()
#parser.add_argument("-inFile", help="Input file", type=str)
parser.add_argument("-flav", help="Lepton flavor", type=str)
parser.add_argument("-unc",  help="Uncertainty: 'nominal'*, 'scaleup', 'scaledown', 'muonid', 'smeared'", type=str, default="nominal")
parser.add_argument("-cs",   help="CS bin: 'inc', 'cspos', 'csneg'", type=str, default="inc")
parser.add_argument("-d",    help="debug", action='store_true')
parser.add_argument("-do2016", help="do 2016", action='store_true')
parser.add_argument("-do2018", help="do 2018", action='store_true')
parser.add_argument("-add", help="add", action="store_true")

args = parser.parse_args()

import ROOT as r
import numpy as np
#~ from nesteddict import nesteddict as ndict
import json
from copy import copy

from defs import getPlot, Backgrounds, Signals, Data, path, Signals2016, Signals2016ADD, SignalsADD, Signals2018, Signals2018ADD, zScale2016, zScale2018
from helpers import *

from setTDRStyle import setTDRStyle
setTDRStyle()


def applyPDFCorrection(hist):
	
	for i in range(0,hist.GetNbinsX()+1):
		binCenter = hist.GetBinCenter(i)
		scaleFac = 0.86 - 3.72e-05 * binCenter + 2.72e-08 * binCenter **2
		hist.SetBinContent(i,hist.GetBinContent(i)*scaleFac)
		
	return copy(hist)
antypes=[
	# ["E","e","Ele","/store/user/sturdy/ZprimeAnalysis/histosHLTWeighted"],
	# ["Mu","mu","Mu","/store/user/sturdy/ZprimeAnalysis/histosCutHLT"]
	["E","e","Ele"],
	["Mu","mu","Mu"]
	]

r.gROOT.SetBatch(True)

lvals=["16", "24", "32", "40", "100k"]
if args.do2016:
	lvals=["1", "10", "16", "22", "28", "34", "100k"]
helis=["LL","LR","RL","RR"]
intfs=["Con","Des"]
supers = [400,500,700,1100,1900,3500,10000]
extrabins = [1000+i for i in range(0, 2500, 200)]

if not os.path.exists('fitPlots'):
	os.mkdir('fitPlots')

if args.add:
	if args.do2016:
		lvals = ["%.1f"%(3.5+i*0.5) for i in range(12)]
		lvals.append("10")
		helis = [""]
		intfs = [""]
		supers = [2000, 2200, 2600, 3000, 3400, 10000]
		extrabins = [1900+i for i in range(0, 1500, 200)]
	else:
		lvals = ["%.1f"%(4+i*1) for i in range(9)]
		lvals.append("100")
		helis = [""]
		intfs = [""]
		supers = [400, 700, 1500, 2500, 3500, 10000]
		extrabins = [1900+i for i in range(0, 1500, 200)]

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
	
plots = {

	"Mubbnominal": "massPlotBBNoLog",
	"Mubenominal": "massPlotBENoLog",
	"Elebbnominal": "massPlotEleBBNoLog",
	"Elebenominal": "massPlotEleBENoLog",
	"Mubbscaleup": "massPlotBBScaleUpNoLog",
	"Mubescaleup": "massPlotBEScaleUpNoLog",
	"Elebbscaleup": "massPlotEleBBScaleUpNoLog",
	"Elebescaleup": "massPlotEleBEScaleUpNoLog",
	"Mubbscaledown": "massPlotBBScaleDownNoLog",
	"Mubescaledown": "massPlotBEScaleDownNoLog",
	"Elebbscaledown": "massPlotEleBBScaleDownNoLog",
	"Elebescaledown": "massPlotEleBEScaleDownNoLog",

	"Elebbpileup": "massPlotEleBBPUScaleUpNoLog",
	"Elebepileup": "massPlotEleBEPUScaleUpNoLog",
	"Elebbpiledown": "massPlotEleBBPUScaleDownNoLog",
	"Elebepiledown": "massPlotEleBEPUScaleDownNoLog",
	
	"Mubbsmeared": "massPlotBBSmearNoLog",
	"Mubesmeared": "massPlotBESmearNoLog",	
	"Mubbmuonid": "massPlotBBMuonIDNoLog",
	"Mubemuonid": "massPlotBEMuonIDNoLog",	

	"Mubbnominalcspos": "massPlotBBCSPosNoLog",
	"Mubenominalcspos": "massPlotBECSPosNoLog",
	"Elebbnominalcspos": "massPlotEleBBCSPosNoLog",
	"Elebenominalcspos": "massPlotEleBECSPosNoLog",
	"Mubbscaleupcspos": "massPlotBBScaleUpCSPosNoLog",
	"Mubescaleupcspos": "massPlotBEScaleUpCSPosNoLog",
	"Elebbscaleupcspos": "massPlotEleBBScaleUpCSPosNoLog",
	"Elebescaleupcspos": "massPlotEleBEScaleUpCSPosNoLog",
	"Mubbscaledowncspos": "massPlotBBScaleDownCSPosNoLog",
	"Mubescaledowncspos": "massPlotBEScaleDownCSPosNoLog",
	"Elebbscaledowncspos": "massPlotEleBBScaleDownCSPosNoLog",
	"Elebescaledowncspos": "massPlotEleBEScaleDownCSPosNoLog",

	"Elebbpileupcspos": "massPlotEleBBPUScaleUpCSPosNoLog",
	"Elebepileupcspos": "massPlotEleBEPUScaleUpCSPosNoLog",
	"Elebbpiledowncspos": "massPlotEleBBPUScaleDownCSPosNoLog",
	"Elebepiledowncspos": "massPlotEleBEPUScaleDownCSPosNoLog",
	
	"Mubbsmearedcspos": "massPlotBBSmearCSPosNoLog",
	"Mubesmearedcspos": "massPlotBESmearCSPosNoLog",	
	"Mubbmuonidcspos": "massPlotBBMuonIDCSPosNoLog",
	"Mubemuonidcspos": "massPlotBEMuonIDCSPosNoLog",	
	
	"Mubbnominalcsneg": "massPlotBBCSNegNoLog",
	"Mubenominalcsneg": "massPlotBECSNegNoLog",
	"Elebbnominalcsneg": "massPlotEleBBCSNegNoLog",
	"Elebenominalcsneg": "massPlotEleBECSNegNoLog",
	"Mubbscaleupcsneg": "massPlotBBScaleUpCSNegNoLog",
	"Mubescaleupcsneg": "massPlotBEScaleUpCSNegNoLog",
	"Elebbscaleupcsneg": "massPlotEleBBScaleUpCSNegNoLog",
	"Elebescaleupcsneg": "massPlotEleBEScaleUpCSNegNoLog",
	"Mubbscaledowncsneg": "massPlotBBScaleDownCSNegNoLog",
	"Mubescaledowncsneg": "massPlotBEScaleDownCSNegNoLog",
	"Elebbscaledowncsneg": "massPlotEleBBScaleDownCSNegNoLog",
	"Elebescaledowncsneg": "massPlotEleBEScaleDownCSNegNoLog",

	"Elebbpileupcsneg": "massPlotEleBBPUScaleUpCSNegNoLog",
	"Elebepileupcsneg": "massPlotEleBEPUScaleUpCSNegNoLog",
	"Elebbpiledowncsneg": "massPlotEleBBPUScaleDownCSNegNoLog",
	"Elebepiledowncsneg": "massPlotEleBEPUScaleDownCSNegNoLog",
	
	"Mubbsmearedcsneg": "massPlotBBSmearCSNegNoLog",
	"Mubesmearedcsneg": "massPlotBESmearCSNegNoLog",	
	"Mubbmuonidcsneg": "massPlotBBMuonIDCSNegNoLog",
	"Mubemuonidcsneg": "massPlotBEMuonIDCSNegNoLog",	
	
}

lumis = {

	"Mu": 42.1,
	"Ele": 41.5

} 
if args.do2016:
	lumis = {"Mu":36.3, "Ele":35.9}   
	
etabins = ["bb","be"]
#             0    1    2    3
csbins = ["inc","csneg","cspos"]
#            0     1     2

csbin  = args.cs
unc    = args.unc
debug = args.d

if csbin not in csbins:
	print("CS bin '{0}' not in:".format(csbin),csbins)
	exit(1)
if unc not in uncertainties:
	print("Plot type '{0}' not in:".format(unc),uncertainties)
	exit(1)


for etabin in etabins:

	for antype in antypes:
		muonlyuncs = ["muonid", "smeared"]
		eleonlyuncs = ["piledown", "pileup"]
		if unc in muonlyuncs and antype[2] == "Ele":
			print("Not processing uncertainty '{0:s}' for lepton flavour '{1:s}'".format(unc,antype[2]))
			continue
		if unc in eleonlyuncs and antype[2] == "Mu":
			print("Not processing uncertainty '{0:s}' for lepton flavour '{1:s}'".format(unc,antype[2]))
			continue
		params = {}
		addLabel = ""
		if args.do2016:
			addLabel="_2016"
		elif args.do2018:
			addLabel="_2018"
		model = "CI"
		if args.add: model = "ADD"
		with open("{0:s}parametrization_2{1:s}_{2:s}_{3:s}_{4:s}{5:s}.json".format(model,antype[1],unc,etabin,csbin,addLabel),"w") as js:
			with open("{0:s}counts_2{1:s}_{2:s}_{3:s}_{4:s}{5:s}.txt".format(model,antype[1],unc,etabin,csbin,addLabel),"w") as out:
				for intf in intfs:
					for heli in helis:
						files=[]
						for point in supers[:-1]:
							# params["{0:s}{1:s}_{2:d}GeV".format(intf,heli,point)] = np.zeros(len(lvals),'float64')
							params["{0:s}{1:s}_{2:d}GeV".format(intf,heli,point)]     = [0. for j in range(len(lvals))]
							params["{0:s}{1:s}_{2:d}GeV_err".format(intf,heli,point)] = [0. for j in range(len(lvals))]
							pass
						for point in extrabins:
							params["{0:s}{1:s}_{2:d}GeV".format(intf,heli,point)]     = [0. for j in range(len(lvals))]
							params["{0:s}{1:s}_{2:d}GeV_err".format(intf,heli,point)] = [0. for j in range(len(lvals))]
							pass
						for i,lval in enumerate(lvals):
							hist = None
							can   = r.TCanvas("can","",800,800)
							stack = r.THStack("stack","")
							plotName = antype[2]+etabin+unc
							if not csbin == "inc":
								plotName = antype[2]+etabin+unc+csbin
							plot = getPlot(plots[plotName])

	 
							eventCounts = totalNumberOfGeneratedEvents(path,plot.muon)  
							negWeights = negWeightFractions(path,plot.muon)     
							if args.do2016:	
								lumi = 35.9*1000
								if plot.muon:
									lumi = 36.3*1000
							elif args.do2018:	
								lumi = 59.4*1000
								if plot.muon:
									lumi = 61.3*1000
							else:
								lumi = 41.529*1000
								if plot.muon:
									lumi = 42.135*1000
							if args.do2016:		
								zScaleFac = zScale2016["muons"]
								if not plot.muon:
									if "bbbe" in plot.histName:
										zScaleFac = zScale2016["electrons"][0]
									elif "bb" in plot.histName:
										zScaleFac = zScale2016["electrons"][1]
									elif "be" in plot.histName:
										zScaleFac = zScale2016["electrons"][2]
									else:
										zScaleFac = zScale2016["electrons"][0]
							elif args.do2018:		
								zScaleFac = zScale2018["muons"]
								if not plot.muon:
									if "bbbe" in plot.histName:
										zScaleFac = zScale2018["electrons"][0]
									elif "bb" in plot.histName:
										zScaleFac = zScale2018["electrons"][1]
									elif "be" in plot.histName:
										zScaleFac = zScale2018["electrons"][2]
									else:
										zScaleFac = zScale2018["electrons"][0]

							else:
								zScaleFac = zScale["muons"]
								if not plot.muon:
									if "bbbe" in plot.histName:
										zScaleFac = zScale["electrons"][0]
									elif "bb" in plot.histName:
										zScaleFac = zScale["electrons"][1]
									elif "be" in plot.histName:
										zScaleFac = zScale["electrons"][2]
									else:
										zScaleFac = zScale["electrons"][0]							          
							signal = "%sTo2%s_Lam%sTeV%s%s"%(model,antype[0],lval,intf,heli)
							if args.add:
								signal = "ADDGravTo2%s_Lam%s"%(antype[0],str(int(float(lval)*1000)))
							if signal == "CITo2E_Lam40TeVDesRR" or signal == "CITo2Mu_Lam40TeVConRR":
							# ~ if signal == "CITo2E_Lam40TeVConLR" or signal == "CITo2E_Lam32TeVConRR" or signal == "CITo2Mu_Lam40TeVConLR" or signal == "CITo2Mu_Lam24TeVDesRR" or signal == "CITo2Mu_Lam32TeVDesRR":
								# list for 2017
								continue
							if signal == 'CITo2E_Lam100kTeVDesRR':
								signal = 'CITo2E_Lam100kTeVDesLL'	
							if signal == "CITo2Mu_Lam10TeVConRL" or signal == "CITo2Mu_Lam10TeVConLR":
								# list for 2016
								continue
							if args.do2016 and not args.add:	
								Signal = Process(getattr(Signals2016,signal),eventCounts,negWeights) 
							elif args.do2018 and not args.add:	
								Signal = Process(getattr(Signals2018,signal),eventCounts,negWeights) 
							elif args.add and args.do2016:
								Signal = Process(getattr(Signals2016ADD, signal),eventCounts,negWeights)
							elif args.add and args.do2018:
								Signal = Process(getattr(Signals2018ADD, signal),eventCounts,negWeights)
							elif args.add:
								Signal = Process(getattr(SignalsADD, signal),eventCounts,negWeights)
							else:	
								Signal = Process(getattr(Signals,signal),eventCounts,negWeights)                        
							
							signalhist = Signal.loadHistogram(plot,lumi,zScaleFac)
							signalHistBefore = signalhist.Clone()
							if not args.do2016:
								signalhist = applyPDFCorrection(signalhist)
							signalhist.SetMinimum(0.8*signalhist.GetMinimum(0.001))
							signalhist.SetMaximum(1.25*signalhist.GetMaximum())
							signalhist.Draw("hist")
							signalHistBefore.SetLineStyle(ROOT.kDashed)
							signalHistBefore.SetLineColor(ROOT.kRed)
							signalHistBefore.Draw("samehist")
							signalhist.GetXaxis().SetRangeUser(0,5000)
							signalhist.GetXaxis().SetNdivisions(505)
							r.gPad.SetLogy(True)
							
							latex = ROOT.TLatex()
							latex.SetTextFont(42)
							latex.SetTextAlign(31)
							latex.SetTextSize(0.04)
							latex.SetNDC(True)						

							latex.DrawLatex(0.95, 0.96, "%.1f fb^{-1} (13 TeV)"%(lumis[antype[2]],))
							
							
							latex.DrawLatex(0.85, 0.8, "%s"%(signal))

							
							can.Update()
							# raw_input()
							for ftype in ["png","C","pdf","eps"]:
								if args.do2016:
									can.SaveAs("fitPlots/{8:s}to2{1:s}_{2:s}{3:s}{4:s}_{5:s}_{6:s}_{7:s}_2016.{0:s}".format(ftype,antype[1],lval,intf,heli,unc,etabin,csbin,model))									
								elif args.do2018:
									can.SaveAs("fitPlots/{8:s}to2{1:s}_{2:s}{3:s}{4:s}_{5:s}_{6:s}_{7:s}_2018.{0:s}".format(ftype,antype[1],lval,intf,heli,unc,etabin,csbin,model))									
								else:	
									can.SaveAs("fitPlots/{8:s}to2{1:s}_{2:s}{3:s}{4:s}_{5:s}_{6:s}_{7:s}.{0:s}".format(ftype,antype[1],lval,intf,heli,unc,etabin,csbin,model))
							# raw_input("enter to continue")
							for p,point in enumerate(supers[:-1]):
								bval  = signalhist.FindBin(point)
								upval = signalhist.FindBin(supers[p+1]-0.05)
								val   = signalhist.Integral(bval,upval)
								err   = r.Double(0)
								val   = signalhist.Integral(bval,upval)
								val2  = signalhist.IntegralAndError(bval,upval,err)
								out.write("{0:s} {1:d} {2:d} {3:d} {4:2.4f} {5:2.4f}\n".format(lval,point,bval,upval,val,err))
								params["{0:s}{1:s}_{2:d}GeV".format(intf,heli,point)][i] = val
								params["{0:s}{1:s}_{2:d}GeV_err".format(intf,heli,point)][i] = err
								pass

							# Mass bin scan above 1 TeV
							for point in extrabins:
								bval  = signalhist.FindBin(point)
								upval = signalhist.FindBin(100000000)
								val   = signalhist.Integral(bval,upval)
								err   = r.Double(0)
								val   = signalhist.Integral(bval,upval)
								val2  = signalhist.IntegralAndError(bval,upval,err)
								out.write("{0:s} {1:d} {2:d} {3:d} {4:2.4f} {5:2.4f}\n".format(lval,point,bval,upval,val,err))
								params["{0:s}{1:s}_{2:d}GeV".format(intf,heli,point)][i]     = val
								params["{0:s}{1:s}_{2:d}GeV_err".format(intf,heli,point)][i] = err
								pass
							pass
						pass
					pass
				pass
			json.dump(params,js)
			pass
		pass
	pass
