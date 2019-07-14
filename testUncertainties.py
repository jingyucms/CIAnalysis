from ROOT import TCanvas, TPad, TLegend, kWhite, kRed, kBlue, kGreen, kOrange
from numpy import array as ar
from array import array
from setTDRStyle import setTDRStyle
from copy import deepcopy
import ratios
from helpers import *
from defs import getPlot, Backgrounds, Backgrounds2016, Backgrounds2018, Signals, Data, zScale2016, zScale2018

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


for etabin in etabins:

	for antype in antypes:
		addLabel = ""
		if args.do2016:
			addLabel="_2016"
		elif args.do2018:
			addLabel="_2018"
		# ~ for intfe in intfs:
			# ~ for heli in helis:
		plotName = antype[2]+etabin+'nominal'
		plotNameScaleUp = antype[2]+etabin+'scaleup'
		plotNameScaleDown = antype[2]+etabin+'scaledown'
		if antype[2] == 'Ele':
			plotNamePUUp = antype[2]+etabin+'pileup'
			plotNamePUDown = antype[2]+etabin+'piledown'
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
		if antype[2] == 'Mu':
			plotWeigthed = getPlot(plots[plotNameWeighted])
			plotSmeared = getPlot(plots[plotNameSmear])

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
				zScaleFac = zScale2016["electrons"]
		elif args.do2018:		
			zScaleFac = zScale2018["muons"]
			if not plot.muon:
				zScaleFac = zScale2018["electrons"]
		else:
			zScaleFac = zScale["muons"]
			if not plot.muon:
				zScaleFac = zScale["electrons"]							          
		# list for 2016

		if args.do2016:	
			drellyan = Process(getattr(Backgrounds2016,"DrellYan"),eventCounts,negWeights)
			other = Process(getattr(Backgrounds2016,"Other"),eventCounts,negWeights)
		elif args.do2018:
			drellyan = Process(getattr(Backgrounds2018,"DrellYan"),eventCounts,negWeights)
			other = Process(getattr(Backgrounds2018,"Other"),eventCounts,negWeights)
		else:
			drellyan = Process(getattr(Backgrounds,"DrellYan"),eventCounts,negWeights)
			other = Process(getattr(Backgrounds,"Other"),eventCounts,negWeights)
		

		dyHist = deepcopy(drellyan.loadHistogram(plot,lumi,zScaleFac))
		dyHistScaleUp = deepcopy(drellyan.loadHistogram(plotScaleUp,lumi,zScaleFac))
		dyHistScaleDown = deepcopy(drellyan.loadHistogram(plotScaleDown,lumi,zScaleFac))
		if antype[2] == 'Ele':
			dyHistPUUp = deepcopy(drellyan.loadHistogram(plotPUUp,lumi,zScaleFac))
			dyHistPUDown = deepcopy(drellyan.loadHistogram(plotPUDown,lumi,zScaleFac))
		if antype[2] == 'Mu':
			dyHistWeighted = deepcopy(drellyan.loadHistogram(plotWeigthed,lumi,zScaleFac))
			dyHistSmear = deepcopy(drellyan.loadHistogram(plotSmeared,lumi,zScaleFac))
		

		dyHist.Add(deepcopy(other.loadHistogram(plot,lumi,zScaleFac)))
		dyHistScaleUp.Add(deepcopy(other.loadHistogram(plotScaleUp,lumi,zScaleFac)))
		dyHistScaleDown.Add(deepcopy(other.loadHistogram(plotScaleDown,lumi,zScaleFac)))
		if antype[2] == 'Ele':	
			dyHistPUUp.Add(deepcopy(other.loadHistogram(plotPUUp,lumi,zScaleFac)))
			dyHistPUDown.Add(deepcopy(other.loadHistogram(plotPUDown,lumi,zScaleFac)))
		if antype[2] == 'Mu':		
			dyHistWeighted.Add(deepcopy(other.loadHistogram(plotWeigthed,lumi,zScaleFac)))
			dyHistSmear.Add(deepcopy(other.loadHistogram(plotSmeared,lumi,zScaleFac)))
		
		rebin = 20
		dyHist.Rebin(rebin)
		
		if antype[2] == 'Ele':
			dyHistPUUp.Rebin(rebin)
			dyHistPUDown.Rebin(rebin)
		dyHistScaleUp.Rebin(rebin)
		dyHistScaleDown.Rebin(rebin)
		if antype[2] == 'Mu':
			dyHistWeighted.Rebin(rebin)
			dyHistSmear.Rebin(rebin)
		hCanvas = TCanvas("hCanvas", "Distribution", 800,800)
	
		plotPad = ROOT.TPad("plotPad","plotPad",0,0.3,1,1)
		ratioPad = ROOT.TPad("ratioPad","ratioPad",0,0.,1,0.3)
		setTDRStyle()		
		plotPad.UseCurrentStyle()
		ratioPad.UseCurrentStyle()
		plotPad.Draw()	
		ratioPad.Draw()	
		plotPad.cd()
		
		plotPad.DrawFrame(0,0.000001,5000,500000,"; dimuon mass [GeV]; Events / 20 GeV")
		plotPad.SetLogy()
		dyHist.Draw("samehist")
		dyHist.SetFillColor(kWhite)
		dyHistScaleDown.SetFillColor(kWhite)
		dyHistScaleDown.SetLineColor(kBlue)
		dyHistScaleDown.Draw("samehist")
		if antype[2] == 'Ele':
			dyHistPUUp.SetFillColor(kWhite)
			dyHistPUDown.SetFillColor(kWhite)
			dyHistPUUp.SetLineColor(kOrange+2)		
			dyHistPUUp.Draw("samehist")
		if antype[2] == 'Mu':
			dyHistSmear.SetFillColor(kWhite)
			dyHistSmear.SetLineColor(kRed)
			dyHistWeighted.SetFillColor(kWhite)
			dyHistWeighted.SetLineColor(kGreen+2)
			dyHistWeighted.Draw("samehist")
			dyHistSmear.Draw("samehist")
		
		legend = TLegend(0.375, 0.6, 0.925, 0.925)
		legend.SetFillStyle(0)
		legend.SetBorderSize(0)
		legend.SetTextFont(42)		
		legend.AddEntry(dyHist,"Default","l")	
		legend.AddEntry(dyHistScaleDown,"Scale Uncertainty","l")	
		if antype[2] == 'Mu':
			legend.AddEntry(dyHistSmear,"Resolution Uncertainty","l")	
			legend.AddEntry(dyHistWeighted,"ID Uncertainty","l")	
		if antype[2] == 'Ele':
			legend.AddEntry(dyHistPUUp,"PU Uncertainty","l")	
		legend.Draw()

		latex = ROOT.TLatex()
		latex.SetTextFont(42)
		latex.SetTextAlign(31)
		latex.SetTextSize(0.04)
		latex.SetNDC(True)
		latexCMS = ROOT.TLatex()
		latexCMS.SetTextFont(61)
		latexCMS.SetTextSize(0.06)
		latexCMS.SetNDC(True)
		latexCMSExtra = ROOT.TLatex()
		latexCMSExtra.SetTextFont(52)
		latexCMSExtra.SetTextSize(0.045)
		latexCMSExtra.SetNDC(True)
	
		latex.DrawLatex(0.95, 0.96, "%.1f fb^{-1} (13 TeV)"%(float(lumi)/1000,))
		cmsExtra = "#splitline{Preliminary}{Simulation}"
		yLabelPos = 0.82	
		latexCMS.DrawLatex(0.19,0.89,"CMS")
		latexCMSExtra.DrawLatex(0.19,yLabelPos,"%s"%(cmsExtra))	
		
		ratioPad.cd()
		xMin = 0
		xMax = 5000
		yMax = 1.1
		yMin = 0.9
		# ~ if "BE" in label:
			# ~ yMax = 1.2
			# ~ yMin = 0.8
		ratioGraphs2 =  ratios.RatioGraph(dyHist,dyHistScaleDown, xMin=xMin, xMax=xMax,title="Default / Uncert",yMin=0.8,yMax=1.3,ndivisions=10,color=kBlue,adaptiveBinning=10000)
		ratioGraphs2.draw(ROOT.gPad,True,False,True,chi2Pos=0.8)		
		if antype[2] == 'Mu':	
			ratioGraphs3 =  ratios.RatioGraph(dyHist,dyHistWeighted, xMin=xMin, xMax=xMax,title="Default / Uncert",yMin=0.8,yMax=1.3,ndivisions=10,color=kGreen+2,adaptiveBinning=10000)
			ratioGraphs3.draw(ROOT.gPad,False,False,True,chi2Pos=0.8)					
			ratioGraphs =  ratios.RatioGraph(dyHist,dyHistSmear, xMin=xMin, xMax=xMax,title="Default / Uncert",yMin=yMin,yMax=yMax,ndivisions=10,color=kRed,adaptiveBinning=10000)
			ratioGraphs.draw(ROOT.gPad,False,False,True,chi2Pos=0.8)		
		if antype[2] == 'Ele':	
			ratioGraphs4 =  ratios.RatioGraph(dyHist,dyHistPUUp, xMin=xMin, xMax=xMax,title="Default / Uncert",yMin=0.8,yMax=1.3,ndivisions=10,color=kOrange+2,adaptiveBinning=10000)	
			ratioGraphs4.draw(ROOT.gPad,False,False,True,chi2Pos=0.8)		
		
		hCanvas.Print("uncertainties_%s%s.pdf"%(plotName,addLabel))


