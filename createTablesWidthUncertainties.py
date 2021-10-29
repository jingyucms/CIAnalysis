from ROOT import TCanvas, TPad, TLegend, kWhite, kRed, kBlue, kGreen, kOrange, TGraph, kMagenta, kBlack, kCyan
from numpy import array as ar
from array import array
from setTDRStyle import setTDRStyle
from copy import deepcopy
import ratios
from helpers import *
from defs import getPlot, Backgrounds, Backgrounds2016, Backgrounds2018, Signals, Data, zScale2016, zScale2018, Data2016, Data2018

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
# ~ intfs=["Con","Des"]
print (path)
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


antypes=[
	# ["E","e","Ele","/store/user/sturdy/ZprimeAnalysis/histosHLTWeighted"],
	# ["Mu","mu","Mu","/store/user/sturdy/ZprimeAnalysis/histosCutHLT"]
	["E","e","Ele"],
	["Mu","mu","Mu"]
	]

	
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


def getLine(i,massLow,massHigh,hists,uncHists):
	# ~ line = "%d - %d & %d & %.1f \\pm %.1f & %.1f \\pm %.1f & %.1f \\pm %.1f & %.1f \\pm %.1f \\hline"
	line = "%d - %d & %d & %.2f $\\pm$ %.2f & %.2f $\\pm$ %.2f & %.2f $\\pm$ %.2f & %.2f $\\pm$ %.2f \\\ "
	
	data = hists[0].GetBinContent(i)
	dyErr = (hists[1].GetBinError(i)**2 + (hists[1].GetBinContent(i)*uncHists[0].GetBinContent(i))**2)**0.5
	dy = hists[1].GetBinContent(i)
	otherErr = (hists[2].GetBinError(i)**2 + (hists[2].GetBinContent(i)*uncHists[1].GetBinContent(i))**2)**0.5
	other = hists[2].GetBinContent(i)
	jets = hists[3].GetBinContent(i)
	jetsErr = 0.5*jets
	
	return line%(massLow,massHigh,data,(dy+max(0,other)+jets),(dyErr+otherErr+jetsErr),abs(dy),abs(dyErr),abs(other),abs(otherErr),jets,jetsErr)



def getTable(massBins,hists,uncHists):

	tableCI = '''Mass range & data & total bkg & $\\gamma^*/\\mathrm{Z}\\rightarrow$ ee & $t\\bar{t}$ and $t\\bar{t}$-like bkg & Jets \\\ 
\\hline
%s
%s
%s
%s
%s
%s
'''
	tableADD = '''Mass range & data & total bkg & $\\gamma^*/\\mathrm{Z}\\rightarrow$ ee & $t\\bar{t}$ and $t\\bar{t}$-like bkg & Jets\\\ 
\\hline
%s
%s
%s
%s
%s
'''
	lines = []
	for i in range(1,hists[0].GetNbinsX()+1):
			lines.append(getLine(i,massBins[i-1],massBins[i],hists,uncHists))
	
	
	if len(massBins) == 7: 		
		return tableCI%(lines[0],lines[1],lines[2],lines[3],lines[4],lines[5])		
	else: 		
		return tableADD%(lines[0],lines[1],lines[2],lines[3],lines[4])		



for etabin in etabins:

	for antype in antypes:
		addLabel = ""
		if args.do2016:
			addLabel="_2016"
		elif args.do2018:
			addLabel="_2018"
		if args.add:
			addLabel += "_ADD"	
		# ~ for intfe in intfs:
			# ~ for heli in helis:
		plotName = antype[2]+etabin+'nominal'
		plotNameScaleUp = antype[2]+etabin+'scaleup'
		plotNameScaleDown = antype[2]+etabin+'scaledown'
		if antype[2] == 'Ele':
			plotNamePUUp = antype[2]+etabin+'pileup'
			plotNamePUDown = antype[2]+etabin+'piledown'
			plotNamePrefireUp = antype[2]+etabin+'prefireup'
			plotNamePrefireDown = antype[2]+etabin+'prefiredown'
		if antype[2] == 'Mu':
			plotNameSmear = antype[2]+etabin+'smeared'
			plotNameWeighted = antype[2]+etabin+'muonid'
		if not csbin == "inc":
			plotName = antype[2]+etabin+unc+csbin
		plot = getPlot(plots[plotName])

		plotScaleUp = getPlot(plots[plotNameScaleUp])
		plotScaleDown = getPlot(plots[plotNameScaleDown])
		if antype[2] == 'Ele':
			plotPUUp = getPlot(plots[plotNamePUUp])
			plotPUDown = getPlot(plots[plotNamePUDown])
			plotPrefireUp = getPlot(plots[plotNamePrefireUp])
			plotPrefireDown = getPlot(plots[plotNamePrefireDown])
		if antype[2] == 'Mu':
			plotWeigthed = getPlot(plots[plotNameWeighted])
			plotSmeared = getPlot(plots[plotNameSmear])

		eventCounts = totalNumberOfGeneratedEvents(path,plot.muon)  
		negWeights = negWeightFractions(path,plot.muon)     
		if "2016" in addLabel:	
				lumi = 35.9*1000
				if "bbbe" in plot.histName:
					zScaleFac = zScale2016["electrons"][0]
				elif "bb" in plot.histName:
					zScaleFac = zScale2016["electrons"][1]
				elif "be" in plot.histName:
					zScaleFac = zScale2016["electrons"][2]
				if plot.muon:
					zScaleFac = zScale2016["muons"]

		elif "2018" in addLabel:
				lumi = 59.97*1000
				if "bbbe" in plot.histName:
					zScaleFac = zScale2018["electrons"][0]
				elif "bb" in plot.histName:
					zScaleFac = zScale2018["electrons"][1]
				elif "be" in plot.histName:
					zScaleFac = zScale2018["electrons"][2]
				if plot.muon:
					zScaleFac = zScale2018["muons"]
		else:
				lumi = 41.529*1000
				if "bbbe" in plot.histName:
					zScaleFac = zScale["electrons"][0]
				elif "bb" in plot.histName:
					zScaleFac = zScale["electrons"][1]
				elif "be" in plot.histName:
					zScaleFac = zScale["electrons"][2]
				if plot.muon:
					zScaleFac = zScale["muons"]						          
		# list for 2016

		if "2016" in addLabel:	
			data = Process(Data2016, normalized=True)
			drellyan = Process(getattr(Backgrounds2016,"DrellYan"),eventCounts,negWeights)
			jets = Process(getattr(Backgrounds2016,"Jets"),eventCounts,negWeights,normalized=True)
			if antype[2] == 'Ele':
				other = Process(getattr(Backgrounds2016,"OtherEle"),eventCounts,negWeights)
			else:
				other = Process(getattr(Backgrounds2016,"Other"),eventCounts,negWeights)
		elif "2018" in addLabel:
			data = Process(Data2018, normalized=True)			
			drellyan = Process(getattr(Backgrounds2018,"DrellYan"),eventCounts,negWeights)
			other = Process(getattr(Backgrounds2018,"Other"),eventCounts,negWeights)
			jets = Process(getattr(Backgrounds2018,"Jets"),eventCounts,negWeights,normalized=True)
			
		else:
			data = Process(Data, normalized=True)			
			drellyan = Process(getattr(Backgrounds,"DrellYan"),eventCounts,negWeights)
			other = Process(getattr(Backgrounds,"Other"),eventCounts,negWeights)
			jets = Process(getattr(Backgrounds,"Jets"),eventCounts,negWeights,normalized=True)
		
		dataHist = data.loadHistogram(plot,lumi,zScaleFac)
		

		dyHist = deepcopy(drellyan.loadHistogram(plot,lumi,zScaleFac))
		dyHistPDF = dyHist.Clone("dyPDF")
		dyHistScaleUp = deepcopy(drellyan.loadHistogram(plotScaleUp,lumi,zScaleFac))
		dyHistScaleDown = deepcopy(drellyan.loadHistogram(plotScaleDown,lumi,zScaleFac))
		if antype[2] == 'Ele':
			dyHistPUUp = deepcopy(drellyan.loadHistogram(plotPUUp,lumi,zScaleFac))
			dyHistPUDown = deepcopy(drellyan.loadHistogram(plotPUDown,lumi,zScaleFac))
			dyHistPrefireUp = deepcopy(drellyan.loadHistogram(plotPrefireUp,lumi,zScaleFac))
			dyHistPrefireDown = deepcopy(drellyan.loadHistogram(plotPrefireDown,lumi,zScaleFac))
		if antype[2] == 'Mu':
			dyHistWeighted = deepcopy(drellyan.loadHistogram(plotWeigthed,lumi,zScaleFac))
			dyHistSmear = deepcopy(drellyan.loadHistogram(plotSmeared,lumi,zScaleFac))
		
		otherHist = other.loadHistogram(plot,lumi,zScaleFac)
		otherHistPDF = otherHist.Clone("otherPDF")
		
		otherHistXSec = otherHist.Clone("otherHistXSec")
		# ~ dyHistXSec = dyHist.Clone("dyHistXSec")
		otherHistXSec.Scale(1.07)	
		# ~ dyHistXSec.Add(otherHistXSec)		

		otherHistRest = otherHist.Clone("otherHistRest")
		dyHistRest = dyHist.Clone("dyHistRest")
		# ~ dyHistRest.Add(otherHistRest)
		
		if args.do2016:
			if antype[2] == 'Ele':
				if etabin == "bb":	
					dyHistRest.Scale(1+(0.01**2+0.06**2)**0.5)	
					otherHistRest.Scale(1+(0.01**2+0.06**2)**0.5)	
				else:	
					dyHistRest.Scale(1+(0.01**2+0.08**2)**0.5)	
					otherHistRest.Scale(1+(0.01**2+0.08**2)**0.5)	
			elif antype[2] == 'Mu':
				if etabin == "bb":	
					dyHistRest.Scale(1+(0.003**2+0.05**2)**0.5)	
					otherHistRest.Scale(1+(0.003**2+0.05**2)**0.5)	
				else:	
					dyHistRest.Scale(1+(0.007**2+0.05**2)**0.5)	
					otherHistRest.Scale(1+(0.007**2+0.05**2)**0.5)	
		if args.do2018:
			if antype[2] == 'Ele':
				if etabin == "bb":	
					dyHistRest.Scale(1+(0.02**2+0.06**2)**0.5)	
					otherHistRest.Scale(1+(0.02**2+0.06**2)**0.5)	
				else:	
					dyHistRest.Scale(1+(0.04**2+0.08**2)**0.5)	
					otherHistRest.Scale(1+(0.04**2+0.08**2)**0.5)	
			elif antype[2] == 'Mu':
				if etabin == "bb":	
					dyHistRest.Scale(1+(0.01**2+0.05**2)**0.5)	
					otherHistRest.Scale(1+(0.01**2+0.05**2)**0.5)	
				else:	
					dyHistRest.Scale(1+(0.01**2+0.05**2)**0.5)	
					otherHistRest.Scale(1+(0.01**2+0.05**2)**0.5)	
		else:
			if antype[2] == 'Ele':
				if etabin == "bb":	
					dyHistRest.Scale(1+(0.02**2+0.06**2)**0.5)	
					otherHistRest.Scale(1+(0.02**2+0.06**2)**0.5)	
				else:	
					dyHistRest.Scale(1+(0.04**2+0.08**2)**0.5)	
					otherHistRest.Scale(1+(0.04**2+0.08**2)**0.5)	
			elif antype[2] == 'Mu':
				if etabin == "bb":	
					dyHistRest.Scale(1+(0.01**2+0.05**2)**0.5)	
					otherHistRest.Scale(1+(0.01**2+0.05**2)**0.5)	
				else:	
					dyHistRest.Scale(1+(0.01**2+0.05**2)**0.5)	
					otherHistRest.Scale(1+(0.01**2+0.05**2)**0.5)	
		
		# ~ dyHist.Add(deepcopy(otherHist))
		otherHistScaleUp = deepcopy(other.loadHistogram(plotScaleUp,lumi,zScaleFac))
		otherHistScaleDown = deepcopy(other.loadHistogram(plotScaleDown,lumi,zScaleFac))
		if antype[2] == 'Ele':	
			otherHistPUUp = deepcopy(other.loadHistogram(plotPUUp,lumi,zScaleFac))
			otherHistPUDown = deepcopy(other.loadHistogram(plotPUDown,lumi,zScaleFac))
			otherHistPrefireUp = deepcopy(other.loadHistogram(plotPrefireUp,lumi,zScaleFac))
			otherHistPrefireDown = deepcopy(other.loadHistogram(plotPrefireDown,lumi,zScaleFac))
		if antype[2] == 'Mu':		
			otherHistWeighted = deepcopy(other.loadHistogram(plotWeigthed,lumi,zScaleFac))
			otherHistSmear = deepcopy(other.loadHistogram(plotSmeared,lumi,zScaleFac))
		
		if args.add:
			if args.do2016:
				massBins = [1900,2200,2600,3000,3400,10000]
			else:	
				massBins = [1800,2200,2600,3000,3400,10000]
		else:	
			massBins =  [400,500,700,1100,1900,3500,10000]
		massBins =  [120,400,600,900,1300,1800,10000]

		jetHist = TheStack([jets],lumi,plot,zScaleFac).theHistogram
	
		jetHist = jetHist.Rebin(len(massBins) - 1, 'hist_' + uuid.uuid4().hex, array('d', massBins))
		dataHist = dataHist.Rebin(len(massBins) - 1, 'hist_' + uuid.uuid4().hex, array('d', massBins))

		dyHist = dyHist.Rebin(len(massBins) - 1, 'hist_' + uuid.uuid4().hex, array('d', massBins))
		dyHistPDF = dyHistPDF.Rebin(len(massBins) - 1, 'hist_' + uuid.uuid4().hex, array('d', massBins))
		dyHistRest = dyHistRest.Rebin(len(massBins) - 1, 'hist_' + uuid.uuid4().hex, array('d', massBins))
		if antype[2] == 'Ele':
			dyHistPUUp = dyHistPUUp.Rebin(len(massBins) - 1, 'hist_' + uuid.uuid4().hex, array('d', massBins))
			dyHistPUDown = dyHistPUDown.Rebin(len(massBins) - 1, 'hist_' + uuid.uuid4().hex, array('d', massBins))
			dyHistPrefireUp = dyHistPrefireUp.Rebin(len(massBins) - 1, 'hist_' + uuid.uuid4().hex, array('d', massBins))
			dyHistPrefireDown = dyHistPrefireDown.Rebin(len(massBins) - 1, 'hist_' + uuid.uuid4().hex, array('d', massBins))
		dyHistScaleUp = dyHistScaleUp.Rebin(len(massBins) - 1, 'hist_' + uuid.uuid4().hex, array('d', massBins))
		dyHistScaleDown  = dyHistScaleDown.Rebin(len(massBins) - 1, 'hist_' + uuid.uuid4().hex, array('d', massBins))
		if antype[2] == 'Mu':
			dyHistWeighted = dyHistWeighted.Rebin(len(massBins) - 1, 'hist_' + uuid.uuid4().hex, array('d', massBins))
			dyHistSmear = dyHistSmear.Rebin(len(massBins) - 1, 'hist_' + uuid.uuid4().hex, array('d', massBins))
			
		otherHist = otherHist.Rebin(len(massBins) - 1, 'hist_' + uuid.uuid4().hex, array('d', massBins))
		otherHistPDF = otherHistPDF.Rebin(len(massBins) - 1, 'hist_' + uuid.uuid4().hex, array('d', massBins))
		otherHistXSec = otherHistXSec.Rebin(len(massBins) - 1, 'hist_' + uuid.uuid4().hex, array('d', massBins))
		otherHistRest = otherHistRest.Rebin(len(massBins) - 1, 'hist_' + uuid.uuid4().hex, array('d', massBins))
		if antype[2] == 'Ele':
			otherHistPUUp = otherHistPUUp.Rebin(len(massBins) - 1, 'hist_' + uuid.uuid4().hex, array('d', massBins))
			otherHistPUDown = otherHistPUDown.Rebin(len(massBins) - 1, 'hist_' + uuid.uuid4().hex, array('d', massBins))
			otherHistPrefireUp = otherHistPrefireUp.Rebin(len(massBins) - 1, 'hist_' + uuid.uuid4().hex, array('d', massBins))
			otherHistPrefireDown = otherHistPrefireDown.Rebin(len(massBins) - 1, 'hist_' + uuid.uuid4().hex, array('d', massBins))
		otherHistScaleUp = otherHistScaleUp.Rebin(len(massBins) - 1, 'hist_' + uuid.uuid4().hex, array('d', massBins))
		otherHistScaleDown = otherHistScaleDown.Rebin(len(massBins) - 1, 'hist_' + uuid.uuid4().hex, array('d', massBins))
		if antype[2] == 'Mu':
			otherHistWeighted = otherHistWeighted.Rebin(len(massBins) - 1, 'hist_' + uuid.uuid4().hex, array('d', massBins))
			otherHistSmear = otherHistSmear.Rebin(len(massBins) - 1, 'hist_' + uuid.uuid4().hex, array('d', massBins))
		
		if args.add:	
			dyPDF =	[1.0335288129164533, 1.0429886021839947, 1.047645134519074, 1.069030181137942, 1.119036982092236]
			otherPDF = [1.1655371996916466, 1.269902491201715, 1.2699234253751208, 1.2984407542188063, 1.3777961331626525]

		else:
			dyPDF =	[1.0133126577202494, 1.0147788328624159, 1.01842209757115, 1.0243644300786998, 1.039572839847093, 1.1144248733154136]
			otherPDF = [1.0358232181870253, 1.088892531404347, 1.1254268509362337, 1.1736824180528946, 1.2024257617076786, 1.3369525304968204]

		
		for i in range(0,len(dyPDF)):
			dyHistPDF.SetBinContent(i+1,dyHistPDF.GetBinContent(i+1)*dyPDF[i])
			otherHistPDF.SetBinContent(i+1,otherHistPDF.GetBinContent(i+1)*otherPDF[i])
		
		
		dyHistPDF.Divide(dyHist)
		dyHistScaleDown.Divide(dyHist)
		dyHistRest.Divide(dyHist)
		if antype[2] == 'Ele':
			dyHistPUUp.Divide(dyHist)
			dyHistPUDown.Divide(dyHist)
			dyHistPrefireUp.Divide(dyHist)
			dyHistPrefireDown.Divide(dyHist)
		if antype[2] == 'Mu':
			dyHistSmear.Divide(dyHist)
			dyHistWeighted.Divide(dyHist)
			
		otherHistPDF.Divide(otherHist)
		otherHistScaleDown.Divide(otherHist)
		otherHistRest.Divide(otherHist)
		otherHistXSec.Divide(otherHist)
		if antype[2] == 'Ele':
			otherHistPUUp.Divide(otherHist)
			otherHistPUDown.Divide(otherHist)
			otherHistPrefireUp.Divide(otherHist)
			otherHistPrefireDown.Divide(otherHist)
		if antype[2] == 'Mu':
			otherHistSmear.Divide(otherHist)
			otherHistWeighted.Divide(otherHist)
		
	
		totalHistDY = dyHistPDF.Clone("total")
		totalHistOther = otherHistPDF.Clone("total")

		

		for i in range(0,dyHist.GetNbinsX()):
			
			
			dyHistPDF.SetBinContent(i,abs(dyHistPDF.GetBinContent(i)-1))
			dyHistRest.SetBinContent(i,abs(dyHistRest.GetBinContent(i)-1))
			dyHistScaleDown.SetBinContent(i,abs(dyHistScaleDown.GetBinContent(i)-1))
			if antype[2] == 'Ele':	
				dyHistPUUp.SetBinContent(i,abs(dyHistPUUp.GetBinContent(i)-1))
				dyHistPUDown.SetBinContent(i,abs(dyHistPUDown.GetBinContent(i)-1))
				dyHistPUUp.SetLineWidth(2)
				dyHistPUDown.SetLineWidth(2)
				dyHistPrefireUp.SetBinContent(i,abs(dyHistPrefireUp.GetBinContent(i)-1))
				dyHistPrefireDown.SetBinContent(i,abs(dyHistPrefireDown.GetBinContent(i)-1))
				dyHistPrefireUp.SetLineWidth(2)
				dyHistPrefireDown.SetLineWidth(2)

			if antype[2] == 'Mu':			
				dyHistSmear.SetBinContent(i,abs(dyHistSmear.GetBinContent(i)-1))
				dyHistWeighted.SetBinContent(i,abs(dyHistWeighted.GetBinContent(i)-1))
				dyHistSmear.SetLineWidth(2)
				dyHistWeighted.SetLineWidth(2)	

			otherHistPDF.SetBinContent(i,abs(otherHistPDF.GetBinContent(i)-1))
			otherHistRest.SetBinContent(i,abs(otherHistRest.GetBinContent(i)-1))
			otherHistXSec.SetBinContent(i,abs(otherHistXSec.GetBinContent(i)-1))
			otherHistScaleDown.SetBinContent(i,abs(otherHistScaleDown.GetBinContent(i)-1))
			if antype[2] == 'Ele':	
				otherHistPUUp.SetBinContent(i,abs(otherHistPUUp.GetBinContent(i)-1))
				otherHistPUDown.SetBinContent(i,abs(otherHistPUDown.GetBinContent(i)-1))
				otherHistPUUp.SetLineWidth(2)
				otherHistPUDown.SetLineWidth(2)
				otherHistPrefireUp.SetBinContent(i,abs(otherHistPrefireUp.GetBinContent(i)-1))
				otherHistPrefireDown.SetBinContent(i,abs(otherHistPrefireDown.GetBinContent(i)-1))
				otherHistPrefireUp.SetLineWidth(2)
				otherHistPrefireDown.SetLineWidth(2)

			if antype[2] == 'Mu':			
				otherHistSmear.SetBinContent(i,abs(otherHistSmear.GetBinContent(i)-1))
				otherHistWeighted.SetBinContent(i,abs(otherHistWeighted.GetBinContent(i)-1))
				otherHistSmear.SetLineWidth(2)
				otherHistWeighted.SetLineWidth(2)	
				
		
		for i in range(0,dyHist.GetNbinsX()):
			
			if antype[2] == 'Ele':	
				totalHistDY.SetBinContent(i,(dyHistPDF.GetBinContent(i)**2 + dyHistRest.GetBinContent(i)**2 + dyHistScaleDown.GetBinContent(i)**2 + dyHistPUUp.GetBinContent(i)**2 + dyHistPrefireUp.GetBinContent(i)**2)**0.5)	

			if antype[2] == 'Mu':				
				totalHistDY.SetBinContent(i,(dyHistPDF.GetBinContent(i)**2 + dyHistRest.GetBinContent(i)**2 + dyHistScaleDown.GetBinContent(i)**2 + dyHistSmear.GetBinContent(i)**2 + dyHistWeighted.GetBinContent(i)**2)**0.5)	
				
		for i in range(0,otherHist.GetNbinsX()):
			
			if antype[2] == 'Ele':	
				totalHistOther.SetBinContent(i,(otherHistPDF.GetBinContent(i)**2 + otherHistRest.GetBinContent(i)**2 + otherHistXSec.GetBinContent(i)**2 + otherHistScaleDown.GetBinContent(i)**2 + otherHistPUUp.GetBinContent(i)**2 + otherHistPrefireUp.GetBinContent(i)**2)**0.5)	

			if antype[2] == 'Mu':				
				totalHistOther.SetBinContent(i,(otherHistPDF.GetBinContent(i)**2 + otherHistRest.GetBinContent(i)**2 + otherHistXSec.GetBinContent(i)**2 + otherHistScaleDown.GetBinContent(i)**2 + otherHistSmear.GetBinContent(i)**2 + otherHistWeighted.GetBinContent(i)**2)**0.5)	
				
		# ~ dyHistPDF.SetLineWidth(2)
		# ~ dyHistScaleDown.SetLineWidth(2)
		# ~ totalHist.SetLineWidth(2)

		
		tab = getTable(massBins,[dataHist,dyHist,otherHist,jetHist],[totalHistDY,totalHistOther])
		
		print (plotName, addLabel)
		print (tab)
		
		text_file = open("tabs/yieldTable_%s%s.txt"%(plotName,addLabel), "w")

		text_file.write(tab)

		text_file.close()
