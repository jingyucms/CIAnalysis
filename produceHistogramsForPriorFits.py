from ROOT import gROOT, TFile, TGraphErrors, TCanvas
from numpy import array as ar
from array import array
import argparse
from copy import deepcopy
import pickle

from defs import getPlot, Backgrounds, Signals, Data, path, Signals2016, Signals2016ADD, SignalsADD, Signals2018, Signals2018ADD, zScale2016, zScale2018, Backgrounds, Backgrounds2016, Backgrounds2018
from helpers import *

plots = {

	"Mubbnominal": "massPlotBBNoLog",
	"Mubenominal": "massPlotBENoLog",
	"Elebbnominal": "massPlotEleBBNoLog",
	"Elebenominal": "massPlotEleBENoLog",
	"MubbpdfWeightsUp": "massPlotBBNoLog",
	"MubepdfWeightsUp": "massPlotBENoLog",
	"ElebbpdfWeightsUp": "massPlotEleBBNoLog",
	"ElebepdfWeightsUp": "massPlotEleBENoLog",
	"MubbpdfWeightsDown": "massPlotBBNoLog",
	"MubepdfWeightsDown": "massPlotBENoLog",
	"ElebbpdfWeightsDown": "massPlotEleBBNoLog",
	"ElebepdfWeightsDown": "massPlotEleBENoLog",
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
	"Elebbprefireup": "massPlotEleBBPrefireUpNoLog",
	"Elebeprefireup": "massPlotEleBEPrefireUpNoLog",
	"Elebbprefiredown": "massPlotEleBBPrefireDownNoLog",
	"Elebeprefiredown": "massPlotEleBEPrefireDownNoLog",
	
	"Mubbsmeared": "massPlotBBSmearNoLog",
	"Mubesmeared": "massPlotBESmearNoLog",	
	"Mubbmuonid": "massPlotBBMuonIDNoLog",
	"Mubemuonid": "massPlotBEMuonIDNoLog",	

	"Mubbnominalcspos": "massPlotBBCSPosNoLog",
	"Mubenominalcspos": "massPlotBECSPosNoLog",
	"Elebbnominalcspos": "massPlotEleBBCSPosNoLog",
	"Elebenominalcspos": "massPlotEleBECSPosNoLog",

	"MubbpdfWeightsUpcspos": "massPlotBBCSPosNoLog",
	"MubepdfWeightsUpcspos": "massPlotBECSPosNoLog",
	"ElebbpdfWeightsUpcspos": "massPlotEleBBCSPosNoLog",
	"ElebepdfWeightsUpcspos": "massPlotEleBECSPosNoLog",

	"MubbpdfWeightsDowncspos": "massPlotBBCSPosNoLog",
	"MubepdfWeightsDowncspos": "massPlotBECSPosNoLog",
	"ElebbpdfWeightsDowncspos": "massPlotEleBBCSPosNoLog",
	"ElebepdfWeightsDowncspos": "massPlotEleBECSPosNoLog",
	
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

	"Elebbprefireupcspos": "massPlotEleBBPrefireUpCSPosNoLog",
	"Elebeprefireupcspos": "massPlotEleBEPrefireUpCSPosNoLog",
	"Elebbprefiredowncspos": "massPlotEleBBPrefireDownCSPosNoLog",
	"Elebeprefiredowncspos": "massPlotEleBEPrefireDownCSPosNoLog",
	
	"Mubbsmearedcspos": "massPlotBBSmearCSPosNoLog",
	"Mubesmearedcspos": "massPlotBESmearCSPosNoLog",	
	"Mubbmuonidcspos": "massPlotBBMuonIDCSPosNoLog",
	"Mubemuonidcspos": "massPlotBEMuonIDCSPosNoLog",	
	
	"Mubbnominalcsneg": "massPlotBBCSNegNoLog",
	"Mubenominalcsneg": "massPlotBECSNegNoLog",
	"Elebbnominalcsneg": "massPlotEleBBCSNegNoLog",
	"Elebenominalcsneg": "massPlotEleBECSNegNoLog",
	"MubbpdfWeightsUpcsneg": "massPlotBBCSNegNoLog",
	"MubepdfWeightsUpcsneg": "massPlotBECSNegNoLog",
	"ElebbpdfWeightsUpcsneg": "massPlotEleBBCSNegNoLog",
	"ElebepdfWeightsUpcsneg": "massPlotEleBECSNegNoLog",
	"MubbpdfWeightsDowncsneg": "massPlotBBCSNegNoLog",
	"MubepdfWeightsDowncsneg": "massPlotBECSNegNoLog",
	"ElebbpdfWeightsDowncsneg": "massPlotEleBBCSNegNoLog",
	"ElebepdfWeightsDowncsneg": "massPlotEleBECSNegNoLog",
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
	"Elebbprefireupcsneg": "massPlotEleBBPrefireUpCSNegNoLog",
	"Elebeprefireupcsneg": "massPlotEleBEPrefireUpCSNegNoLog",
	"Elebbprefiredowncsneg": "massPlotEleBBPrefireDownCSNegNoLog",
	"Elebeprefiredowncsneg": "massPlotEleBEPrefireDownCSNegNoLog",
	
	"Mubbsmearedcsneg": "massPlotBBSmearCSNegNoLog",
	"Mubesmearedcsneg": "massPlotBESmearCSNegNoLog",	
	"Mubbmuonidcsneg": "massPlotBBMuonIDCSNegNoLog",
	"Mubemuonidcsneg": "massPlotBEMuonIDCSNegNoLog",	
	
}


def main():
	gROOT.SetBatch(True)
	
	parser = argparse.ArgumentParser(description='Process some integers.')
	
	parser.add_argument("-add", "--add", action="store_true", dest="useADD", default=False,
						  help="use ADD instead of CI.")
	parser.add_argument("-s", "--suffix", dest="suffix", default='nominal',
						  help="name of systematic to use")
	args = parser.parse_args()					  
	useADD = args.useADD					  
	histos = ["BB","BE"]
	labels = ["dielectron_2016","dimuon_2016","dimuon_2017","dielectron_2017","dimuon_2018","dielectron_2018"]
	suffixesMu = ["nominal","scaleup","scaledown","smeared","muonid","pdfWeightsUp","pdfWeightsDown"]
	suffixesEle = ["nominal","scaledown","scaleup","pileup","piledown","pdfWeightsUp","pdfWeightsDown",'prefireup','prefiredown']
	css = ["inc","cspos","csneg"]
	lambdas = [10,16,22,28,34,40,46]
	interferences = ["Con","Des"]
	hels = ["LL","RL","LR","RR"]
	massBins = [400,500,700,1100,1900,3500]
	if useADD:
		labels = ["dielectron_2016","dimuon_2016","dimuon_2017","dielectron_2017","dimuon_2018","dielectron_2018"]
		lambdas = [3500+i*500 for i in range(12)]; lambdas.append(10000)
		interferences = [""]
		hels = [""]
		massBins = [1800, 2200, 2600, 3000, 3400]
		
	graphs = []	
	for label in labels:
		print (label)
		if "dimuon" in label:
			suffixes = suffixesMu
		else:
			suffixes = suffixesEle
		if not args.suffix in suffixes: continue	
		suffix = args.suffix
		for cs in css:
			for histo in histos:
				for hel in hels:
					for interference in interferences:			
						model = interference+hel
						addci = "CI"
						if useADD: addci = "ADD"
						if "dimuon" in label:
							name = "%sto2mu"%addci
						else:			#~ print signalYields

							name = "%sto2e"	%addci
						if useADD:
							# ~ if not "2016" in label: massBins = [400, 700, 1500, 2500, 3500]
							# ~ else: massBins = [2000, 2200, 2600, 3000, 3400]
							if "2016" in label:
								fitFile = TFile("%s_%s_%s_%s_parametrization_fixinf_limitp0_limitp1_limitp2_2016.root"%(name,suffix,histo.lower(),cs),"READ")
							elif "2018" in label:
								fitFile = TFile("%s_%s_%s_%s_parametrization_fixinf_limitp0_limitp1_limitp2_2018.root"%(name,suffix,histo.lower(),cs),"READ")
							else:
								fitFile = TFile("%s_%s_%s_%s_parametrization_fixinf_limitp0_limitp1_limitp2.root"%(name,suffix,histo.lower(),cs),"READ")
						else:	
							if "2016" in label:
								fitFile = TFile("%s_%s_%s_%s_parametrization_fixinf_limitp0_limitp1_limitp2_2016.root"%(name,suffix,histo.lower(),cs),"READ")
							elif "2018" in label:
								fitFile = TFile("%s_%s_%s_%s_parametrization_fixinf_limitp0_limitp1_limitp2_2018.root"%(name,suffix,histo.lower(),cs),"READ")
							else:	
								fitFile = TFile("%s_%s_%s_%s_parametrization_fixinf_limitp0_limitp1_limitp2.root"%(name,suffix,histo.lower(),cs),"READ")
						# ~ print (fitFile.ls())		
						# ~ print ("%s_%s_%s_%s_parametrization_fixinf.root"%(name,suffix,histo.lower(),cs))
						
						if "dimuon" in label:
							plotName = "Mu"+histo.lower()+suffix
						else:	
							plotName = "Ele"+histo.lower()+suffix
						if not cs == "inc":
							plotName = plotName + cs	
						plot = getPlot(plots[plotName])

 
						eventCounts = totalNumberOfGeneratedEvents(path,plot.muon)  
						negWeights = negWeightFractions(path,plot.muon)
						if "2016" in label:	
							lumi = 35.9*1000
							if plot.muon:
								lumi = 36294.6
						elif "2018" in label:	
							lumi = 59.4*1000
							if plot.muon:
								lumi = 61298.775231718995
						else:
							lumi = 41.529*1000
							if plot.muon:
								lumi = 42079.880396
						if "2016" in label:		
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
						elif "2018" in label:		
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
						background = "DrellYan"
						if "2016" in label:	
							DY = Process(getattr(Backgrounds2016,background),eventCounts,negWeights) 
						elif "2018" in label:	
							DY = Process(getattr(Backgrounds2018,background),eventCounts,negWeights) 
						else:	
							DY = Process(getattr(Backgrounds,background),eventCounts,negWeights)						
						
						backgroundHist = DY.loadHistogram(plot,lumi,zScaleFac)	
						backgroundHist = backgroundHist.Rebin(len(massBins), name, array('d', massBins+[10000]))


						for index, massBin in enumerate(massBins):
							function = fitFile.Get("fn_m%d_%s"%(massBin,model))
							fitR = fitFile.Get("fitR_m%d_%s"%(massBin,model))
							pars = fitR.GetParams()
							errs = fitR.Errors()
							function.SetParameter(0,pars[0])
							function.SetParameter(1,pars[1])
							function.SetParameter(2,pars[2])
							function.SetParError(0,errs[0])
							function.SetParError(1,errs[1])
							function.SetParError(2,errs[2])
							# ~ if useADD:
								# ~ function.SetParameter(3, pars[3])
								# ~ function.SetParError(3, errs[3])
							functionUnc = fitFile.Get("fn_unc_m%d_%s"%(massBin,model))
							
							graph = TGraphErrors()
							graph.SetTitle("%s%s%s%s_M%d"%(label,histo,cs,model,massBin))
							graph.SetName("%s%s%s%s_M%d"%(label,histo,cs,model,massBin))
						
							if args.useADD:
								for indel, l in enumerate(lambdas+[100000]):
									uncert = (abs((functionUnc.Eval(l)/function.Eval(l))**2 + (functionUnc.Eval(100000)/function.Eval(100000))))**0.5
									# ~ print (function.Eval(100000) , backgroundHist.GetBinContent(index+1))	
									graph.SetPoint(indel,float(l)/1000,function.Eval(l)-function.Eval(100000) + backgroundHist.GetBinContent(index+1))
									graph.SetPointError(indel,0,(uncert**2+backgroundHist.GetBinError(index+1)**2)**0.5)
							else:		
								for indel, l in enumerate(lambdas+[100000]):
									uncert = (abs((functionUnc.Eval(l)/function.Eval(l))**2 + (functionUnc.Eval(100000)/function.Eval(100000))))**0.5
									# ~ print (function.Eval(100000) , backgroundHist.GetBinContent(index+1))	
									graph.SetPoint(indel,l,function.Eval(l)-function.Eval(100000) + backgroundHist.GetBinContent(index+1))
									graph.SetPointError(indel,0,(uncert**2+backgroundHist.GetBinError(index+1)**2)**0.5)
							
							graphs.append(deepcopy(graph))
	if args.useADD:
		suffix += "_add"
	outFile = TFile("graphsForPriors_%s.root"%suffix,"RECREATE")
	
	for graph in graphs:
		graph.Write()
	outFile.Close()						
							
main()
