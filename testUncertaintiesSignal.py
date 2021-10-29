from ROOT import TCanvas, TPad, TLegend, kWhite, kRed, kBlue, kGreen, kOrange, TGraph, kMagenta, kBlack, kYellow, kAzure, kCyan
from numpy import array as ar
from array import array
from setTDRStyle import setTDRStyle
from copy import deepcopy, copy
import ratios
from helpers import *
from defs import getPlot, Backgrounds, Backgrounds2016, Backgrounds2018, Signals, Data, zScale2016, zScale2018, Signals2016, Signals2018

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

def applyPDFCorrection(hist):
	
	for i in range(0,hist.GetNbinsX()+1):
		binCenter = hist.GetBinCenter(i)
		scaleFac = 0.86 - 3.72e-05 * binCenter + 2.72e-08 * binCenter **2
		hist.SetBinContent(i,hist.GetBinContent(i)*scaleFac)
		
	return copy(hist)


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
				else:
					zScaleFac = zScale2016["electrons"][0]

		elif "2018" in addLabel:
				lumi = 59.97*1000
				if "bbbe" in plot.histName:
					zScaleFac = zScale2018["electrons"][0]
				elif "bb" in plot.histName:
					zScaleFac = zScale2018["electrons"][1]
				elif "be" in plot.histName:
					zScaleFac = zScale2018["electrons"][2]
				else:
					zScaleFac = zScale2018["electrons"][0]
		else:
				lumi = 41.529*1000
				if "bbbe" in plot.histName:
					zScaleFac = zScale["electrons"][0]
				elif "bb" in plot.histName:
					zScaleFac = zScale["electrons"][1]
				elif "be" in plot.histName:
					zScaleFac = zScale["electrons"][2]
				else:
					zScaleFac = zScale["electrons"][0]						          
		# list for 2016

		if args.do2016:
			if antype[2] == 'Ele':
				drellyan = Process(getattr(Signals2016,"CITo2E_Lam16TeVConLL"),eventCounts,negWeights)
			else:	
				drellyan = Process(getattr(Signals2016,"CITo2Mu_Lam16TeVConLL"),eventCounts,negWeights)
		elif args.do2018:
			if antype[2] == 'Ele':
				drellyan = Process(getattr(Signals2018,"CITo2E_Lam16TeVConLL"),eventCounts,negWeights)
			else:	
				drellyan = Process(getattr(Signals2018,"CITo2Mu_Lam16TeVConLL"),eventCounts,negWeights)
		else:
			if antype[2] == 'Ele':
				drellyan = Process(getattr(Signals,"CITo2E_Lam16TeVConLL"),eventCounts,negWeights)
			else:	
				drellyan = Process(getattr(Signals,"CITo2Mu_Lam16TeVConLL"),eventCounts,negWeights)
		

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
		

		dyHistRest = dyHist.Clone("dyHistRest")
		
		if args.do2016:
			if antype[2] == 'Ele':
				if etabin == "bb":	
					dyHistRest.Scale(1+(0.01**2+0.06**2)**0.5)	
				else:	
					dyHistRest.Scale(1+(0.01**2+0.08**2)**0.5)	
			elif antype[2] == 'Mu':
				if etabin == "bb":	
					dyHistRest.Scale(1+(0.003**2+0.05**2)**0.5)	
				else:	
					dyHistRest.Scale(1+(0.007**2+0.05**2)**0.5)	
		if args.do2018:
			if antype[2] == 'Ele':
				if etabin == "bb":	
					dyHistRest.Scale(1+(0.02**2+0.06**2)**0.5)	
				else:	
					dyHistRest.Scale(1+(0.04**2+0.08**2)**0.5)	
			elif antype[2] == 'Mu':
				if etabin == "bb":	
					dyHistRest.Scale(1+(0.01**2+0.05**2)**0.5)	
				else:	
					dyHistRest.Scale(1+(0.01**2+0.05**2)**0.5)	
		else:
			if antype[2] == 'Ele':
				if etabin == "bb":	
					dyHistRest.Scale(1+(0.02**2+0.06**2)**0.5)	
				else:	
					dyHistRest.Scale(1+(0.04**2+0.08**2)**0.5)	
			elif antype[2] == 'Ele':
				if etabin == "bb":	
					dyHistRest.Scale(1+(0.01**2+0.05**2)**0.5)	
				else:	
					dyHistRest.Scale(1+(0.01**2+0.05**2)**0.5)	
		if not args.do2016:			
			dyHistXSec = applyPDFCorrection(dyHist.Clone("dyHistWeights"))
			dyHistXSec.SetLineColor(kAzure+1)
		else:
			dyHistXSec = dyHist.Clone("dyHistWeights")
		rebin = 500
		dyHist.Rebin(rebin)
		dyHistPDF.Rebin(rebin)
		dyHistXSec.Rebin(rebin)
		dyHistRest.Rebin(rebin)
		if antype[2] == 'Ele':
			dyHistPUUp.Rebin(rebin)
			dyHistPUDown.Rebin(rebin)
			dyHistPrefireUp.Rebin(rebin)
			dyHistPrefireDown.Rebin(rebin)
		dyHistScaleUp.Rebin(rebin)
		dyHistScaleDown.Rebin(rebin)
		if antype[2] == 'Mu':
			dyHistWeighted.Rebin(rebin)
			dyHistSmear.Rebin(rebin)

			
		dyPDF =	[1.0304566227826, 1.0552718350331, 1.100243469049, 1.138843573312, 1.174158749016, 1.209089494844, 1.23199869043, 1.254411193798, 1.276680893283, 1.298545020289]
		# ~ otherPDF = [1.0199628059050245, 1.0947822978713515, 1.1667059306633676, 1.2015510490544068, 1.1924439114319363, 1.2791537171741354, 1.3099638693824318, 1.3304365451747442, 1.3440462920421208, 1.4843342155218124]
		# ~ dyPDF = [1.0110591059033056, 1.0116390308490022, 1.0136110368833455, 1.0163549343410934, 1.0190161799320379, 1.0208608215032775, 1.0241056311080647, 1.0268799585966002, 1.0284194934661846, 1.0319438166063548, 1.0365003172410037, 1.0440534405776285, 1.0411516320347873, 1.0450996065156617, 1.0519395286390203, 1.0628252223431283, 1.079245559669309, 1.106583440995778, 1.0916382619739038, 1.105558793030756, 1.119207441948754, 1.13746974534373, 1.1660294230175545, 1.1660294230175545, 1.1660294230175545, 1.1660294230175545]
		# ~ otherPDF = [1.0184530267699423, 1.0214964429984492, 1.0484287816310063, 1.1063530964912485, 1.132790305234357, 1.1632392501943913, 1.1758782432034307, 1.193556487636365, 1.2019645329535742, 1.1560453218324351, 1.1789670634151592, 1.266484301402874, 1.2774161730695819, 1.2415610963248342, 1.3226574340755608, 1.2652759905898592, 1.3846277401882812, 1.341585680160312, 1.3801239366049678, 1.3776280394993747, 1.3874437228143155, 1.1718685925006866, 1.4843342155218124, 1.4843342155218124, 1.4843342155218124, 1.4843342155218124]	
		# ~ dyPDF = [1.0136110368833455, 1.0163549343410934, 1.0190161799320379, 1.0208608215032775, 1.0241056311080647, 1.0268799585966002, 1.0284194934661846, 1.0319438166063548, 1.0365003172410037, 1.0440534405776285, 1.0411516320347873, 1.0450996065156617, 1.0519395286390203, 1.0628252223431283, 1.079245559669309, 1.106583440995778, 1.0916382619739038, 1.105558793030756, 1.119207441948754, 1.13746974534373, 1.1660294230175545]
		# ~ otherPDF = [1.0484287816310063, 1.1063530964912485, 1.132790305234357, 1.1632392501943913, 1.1758782432034307, 1.193556487636365, 1.2019645329535742, 1.1560453218324351, 1.1789670634151592, 1.266484301402874, 1.2774161730695819, 1.2415610963248342, 1.3226574340755608, 1.2652759905898592, 1.3846277401882812, 1.341585680160312, 1.3801239366049678, 1.3776280394993747, 1.3874437228143155, 1.1718685925006866, 1.4843342155218124]	
			
		for i in range(0,len(dyPDF)):
			dyHistPDF.SetBinContent(i+1,dyHistPDF.GetBinContent(i+1)*dyPDF[i])
		
		

		
		dyHistPDF.SetLineColor(kMagenta)
		dyHistPDF.SetFillStyle(0)
		hCanvas = TCanvas("hCanvas", "Distribution", 1200,800)
	
		# ~ plotPad = ROOT.TPad("plotPad","plotPad",0,0.3,1,1)
		ratioPad = ROOT.TPad("ratioPad","ratioPad",0,0.,1,1)
		setTDRStyle()		
		# ~ plotPad.UseCurrentStyle()
		ratioPad.UseCurrentStyle()
		# ~ plotPad.Draw()	
		ratioPad.Draw()	
		ratioPad.cd()
		# ~ if antype[2] == 'Ele':	
			# ~ plotPad.DrawFrame(400,0.000001,5000,500000,"; dielectron mass [GeV]; Events / 200 GeV")
		# ~ else:	
			# ~ plotPad.DrawFrame(400,0.000001,5000,500000,"; dimuon mass [GeV]; Events / 200 GeV")
		# ~ plotPad.SetLogy()
		# ~ dyHist.Draw("samehist")
		# ~ dyHistPDF.Draw("samehist")
		dyHist.SetFillColor(kWhite)
		dyHistScaleDown.SetFillColor(kWhite)
		dyHistScaleDown.SetLineColor(kBlue)
		# ~ dyHistScaleDown.Draw("samehist")
		if antype[2] == 'Ele':
			dyHistPUUp.SetFillColor(kWhite)
			dyHistPUDown.SetFillColor(kWhite)
			dyHistPUUp.SetLineColor(kOrange+2)		
			dyHistPrefireUp.SetLineColor(kCyan)		
			dyHistPrefireUp.SetFillColor(kWhite)		
			# ~ dyHistPUUp.Draw("samehist")
		if antype[2] == 'Mu':
			dyHistSmear.SetFillColor(kWhite)
			dyHistSmear.SetLineColor(kRed)
			dyHistWeighted.SetFillColor(kWhite)
			dyHistWeighted.SetLineColor(kGreen+2)
			# ~ dyHistWeighted.Draw("samehist")e
			# ~ dyHistSmear.Draw("samehist")
		
		legend = TLegend(0.375, 0.6, 0.925, 0.925)
		legend.SetFillStyle(0)
		legend.SetBorderSize(0)
		legend.SetTextFont(42)
		# ~ legend.AddEntry(dyHist,"Default","l")	
		legend.AddEntry(dyHistPDF,"PDF Uncertainty","l")	
		if not args.do2016:
			legend.AddEntry(dyHistXSec,"PDF Reweight Uncertainty","l")	
		legend.AddEntry(dyHistScaleDown,"Scale Uncertainty","l")	
		if antype[2] == 'Mu':
			legend.AddEntry(dyHistSmear,"Resolution Uncertainty","l")	
			if args.do2016:
				legend.AddEntry(dyHistWeighted,"Reco + ID Uncertainty","l")	
			else:	
				legend.AddEntry(dyHistWeighted,"Reco Uncertainty","l")	
		if antype[2] == 'Ele':
			legend.AddEntry(dyHistPUUp,"PU Uncertainty","l")	
			legend.AddEntry(dyHistPrefireUp,"Prefire Uncertainty","l")	
		# ~ legend.Draw()

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
	
	
		dyHistPDF.Divide(dyHist)
		dyHistScaleDown.Divide(dyHist)
		dyHistRest.Divide(dyHist)
		dyHistXSec.Divide(dyHist)
		if antype[2] == 'Ele':
			dyHistPUUp.Divide(dyHist)
			dyHistPUDown.Divide(dyHist)
			dyHistPrefireUp.Divide(dyHist)
			dyHistPrefireDown.Divide(dyHist)
		if antype[2] == 'Mu':
			dyHistSmear.Divide(dyHist)
			dyHistWeighted.Divide(dyHist)

		totalHist = dyHistPDF.Clone("total")
		totalHist.SetLineColor(kBlack)
		totalHist.SetLineWidth(2)
		legend.AddEntry(totalHist,"Total Uncertainty","l")	

		

		for i in range(0,dyHist.GetNbinsX()):
			
			
			dyHistPDF.SetBinContent(i,abs(dyHistPDF.GetBinContent(i)-1))
			dyHistRest.SetBinContent(i,abs(dyHistRest.GetBinContent(i)-1))
			dyHistXSec.SetBinContent(i,abs(dyHistXSec.GetBinContent(i)-1))
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
				
		
		for i in range(0,dyHist.GetNbinsX()):
			
			if antype[2] == 'Ele':	
				totalHist.SetBinContent(i,(dyHistPDF.GetBinContent(i)**2 + dyHistRest.GetBinContent(i)**2 + dyHistXSec.GetBinContent(i)**2 + dyHistScaleDown.GetBinContent(i)**2 + dyHistPUUp.GetBinContent(i)**2 + dyHistPrefireUp.GetBinContent(i)**2)**0.5)	
				print (dyHistPDF.GetBinContent(i),dyHistRest.GetBinContent(i),dyHistXSec.GetBinContent(i),dyHistScaleDown.GetBinContent(i),dyHistPUUp.GetBinContent(i), totalHist.GetBinContent(i))

			if antype[2] == 'Mu':				
				totalHist.SetBinContent(i,(dyHistPDF.GetBinContent(i)**2 + dyHistRest.GetBinContent(i)**2 + dyHistXSec.GetBinContent(i)**2 + dyHistScaleDown.GetBinContent(i)**2 + dyHistSmear.GetBinContent(i)**2 + dyHistWeighted.GetBinContent(i)**2)**0.5)	
				
		dyHistXSec.SetLineWidth(2)
		dyHistPDF.SetLineWidth(2)
		dyHistScaleDown.SetLineWidth(2)
		totalHist.SetLineWidth(2)

	
		ratioPad.cd()
		xMin = 400
		xMax = 5000
		yMax = 1.1
		yMin = 0.9
		# ~ if "BE" in label:
			# ~ yMax = 1.2
			# ~ yMin = 0.8
		if antype[2] == 'Ele':	
			ratioPad.DrawFrame(400,0,5000,0.8,"; dielectron mass [GeV]; Systematic Uncertainty")
		else:	
			ratioPad.DrawFrame(400,0,5000,0.8,"; dimuon mass [GeV]; Systematic Uncertainty")


		dyHistPDF.Draw("samehist")
		if not args.do2016:
			dyHistXSec.Draw("samehist")
		dyHistScaleDown.Draw("samehist")
		if antype[2] == 'Ele':	
			dyHistPUUp.Draw("samehist")
			dyHistPrefireUp.Draw("samehist")
		if antype[2] == 'Mu':
			dyHistSmear.Draw("samehist")
			dyHistWeighted.Draw("samehist")
		totalHist.Draw("samehist")	
		# ~ ratioGraphs2 =  ratios.RatioGraph(dyHist,dyHistScaleDown, xMin=xMin, xMax=xMax,title="Default / Uncert",yMin=0.8,yMax=1.3,ndivisions=10,color=kBlue,adaptiveBinning=10000)
		# ~ ratioGraphs2.draw(ROOT.gPad,False,False,True,chi2Pos=0.8)		
		# ~ ratioGraphs5 =  ratios.RatioGraph(dyHist,dyHistPDF, xMin=xMin, xMax=xMax,title="Default / Uncert",yMin=0.8,yMax=1.3,ndivisions=10,color=kMagenta,adaptiveBinning=10000)
		# ~ ratioGraphs5.draw(ROOT.gPad,False,False,True,chi2Pos=0.8)		
		# ~ if antype[2] == 'Mu':	
			# ~ ratioGraphs3 =  ratios.RatioGraph(dyHist,dyHistWeighted, xMin=xMin, xMax=xMax,title="Default / Uncert",yMin=0.8,yMax=1.3,ndivisions=10,color=kGreen+2,adaptiveBinning=10000)
			# ~ ratioGraphs3.draw(ROOT.gPad,False,False,True,chi2Pos=0.8)					
			# ~ ratioGraphs =  ratios.RatioGraph(dyHist,dyHistSmear, xMin=xMin, xMax=xMax,title="Default / Uncert",yMin=yMin,yMax=yMax,ndivisions=10,color=kRed,adaptiveBinning=10000)
			# ~ ratioGraphs.draw(ROOT.gPad,False,False,True,chi2Pos=0.8)		
		# ~ if antype[2] == 'Ele':	
			# ~ ratioGraphs4 =  ratios.RatioGraph(dyHist,dyHistPUUp, xMin=xMin, xMax=xMax,title="Default / Uncert",yMin=0.8,yMax=1.3,ndivisions=10,color=kOrange+2,adaptiveBinning=10000)	
			# ~ ratioGraphs4.draw(ROOT.gPad,False,False,True,chi2Pos=0.8)		


		latex.DrawLatex(0.95, 0.96, "%.1f fb^{-1} (13 TeV)"%(float(lumi)/1000,))
		cmsExtra = "#splitline{Preliminary}{Simulation}"
		yLabelPos = 0.82	
		latexCMS.DrawLatex(0.19,0.89,"CMS")
		latexCMSExtra.DrawLatex(0.19,yLabelPos,"%s"%(cmsExtra))	
		
		
		legend.Draw("same")		
		ratioPad.RedrawAxis()
		hCanvas.Print("uncertaintiesSignal_%s%s.pdf"%(plotName,addLabel))


