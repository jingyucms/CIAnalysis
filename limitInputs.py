from ROOT import TFile
from numpy import array as ar
from array import array
from setTDRStyle import setTDRStyle
from copy import deepcopy

from helpers import *
from defs import getPlot, Backgrounds, Signals, Data, Data2016, Data2018, zScale, zScale2018, zScale2016, Backgrounds2016



def main():
	### for data

	
	histos = ["BB","BE","BB","BE","BB","BE"]
	labels = ["dimuon_2016_BB","dimuon_2016_BE","dimuon_2017_BB","dimuon_2017_BE","dimuon_2018_BB","dimuon_2018_BE"]

	for i, histo in enumerate(histos):
		label = labels[i]

		massPlot = getPlot("massPlot%sNoLog"%histo)
		massPlotSmeared = getPlot("massPlot%sSmearNoLog"%histo)
		massPlotUp = getPlot("massPlot%sScaleUpNoLog"%histo)
		massPlotDown = getPlot("massPlot%sScaleDownNoLog"%histo)
		massPlotWeighted = getPlot("massPlot%sMuonIDNoLog"%histo)

		eventCounts = totalNumberOfGeneratedEvents(path,massPlot.muon)	
		negWeights = negWeightFractions(path,massPlot.muon)
		if "2016" in label:
			data = Process(Data2016, normalized=True)
			drellyan = Process(getattr(Backgrounds2016,"DrellYan"),eventCounts,negWeights)
			other = Process(getattr(Backgrounds2016,"Other"),eventCounts,negWeights)				
		elif "2018" in label:
			data = Process(Data2018, normalized=True)
			drellyan = Process(getattr(Backgrounds,"DrellYan"),eventCounts,negWeights)
			other = Process(getattr(Backgrounds,"Other"),eventCounts,negWeights)				
		else:
			data = Process(Data, normalized=True)
			drellyan = Process(getattr(Backgrounds,"DrellYan"),eventCounts,negWeights)
			other = Process(getattr(Backgrounds,"Other"),eventCounts,negWeights)				
	
		fResult = TFile("inputsCI_%s.root"%(label),"RECREATE")	


		if "2016" in label:	
				lumi = 36.3*1000
				zScaleFac = zScale2016["muons"]
		elif "2018" in label:
				lumi = 61.608*1000
				zScaleFac = zScale2018["muons"]
		else:
				lumi = 42.135*1000
				zScaleFac = zScale["muons"]

		hist = deepcopy(data.loadHistogram(massPlot,lumi,zScaleFac))			
		hist.SetName("dataHist_%s" %label)


		dyHist = deepcopy(drellyan.loadHistogram(massPlot,lumi,zScaleFac))
		dyHistSmear = deepcopy(drellyan.loadHistogram(massPlotSmeared,lumi,zScaleFac))
		dyHistScaleUp = deepcopy(drellyan.loadHistogram(massPlotUp,lumi,zScaleFac))
		dyHistScaleDown = deepcopy(drellyan.loadHistogram(massPlotDown,lumi,zScaleFac))
		dyHistWeighted = deepcopy(drellyan.loadHistogram(massPlotWeighted,lumi,zScaleFac))

		otherHist = deepcopy(other.loadHistogram(massPlot,lumi,zScaleFac))
		otherHistSmear = deepcopy(other.loadHistogram(massPlotSmeared,lumi,zScaleFac))
		otherHistScaleUp = deepcopy(other.loadHistogram(massPlotUp,lumi,zScaleFac))
		otherHistScaleDown = deepcopy(other.loadHistogram(massPlotDown,lumi,zScaleFac))
		otherHistWeighted = deepcopy(other.loadHistogram(massPlotWeighted,lumi,zScaleFac))
						
		dyHist.SetName("bkgHistDY_%s"%label)
		dyHistSmear.SetName("bkgHistDYSmeared_%s"%label)
		dyHistScaleUp.SetName("bkgHistDYScaleUp_%s"%label)
		dyHistScaleDown.SetName("bkgHistDYScaleDown_%s"%label)				
		dyHistWeighted.SetName("bkgHistDYWeighted_%s"%label)				

		otherHist.SetName("bkgHistOther_%s"%label)
		otherHistSmear.SetName("bkgHistOtherSmeared_%s"%label)
		otherHistScaleUp.SetName("bkgHistOtherScaleUp_%s"%label)
		otherHistScaleDown.SetName("bkgHistOtherScaleDown_%s"%label)				
		otherHistWeighted.SetName("bkgHistOtherWeighted_%s"%label)				
		if "2016" in label:
			if "_BB" in label:
				fJets = TFile("../files/Data-total-jets-BB-pt53.root","OPEN")	
			else:	
				fJets = TFile("../files/Data-total-jets-BEEE-pt53.root","OPEN")	
		else:
			if "_BB" in label:
				fJets = TFile("../files/Data-total-jets-BB-pt53.root","OPEN")	
			else:	
				fJets = TFile("../files/Data-total-jets-BEEE-pt53.root","OPEN")	
			
		jetHist = fJets.Get("TotalJets")
		if "2018" in label:
			jetHist.Scale(61.608/42.135)
		jetHist.SetName("bkgHistJets_%s"%label)				
		jetHist.SetDirectory(fResult)				


		dyHist.SetDirectory(fResult)
		dyHistSmear.SetDirectory(fResult)
		dyHistScaleUp.SetDirectory(fResult)
		dyHistScaleDown.SetDirectory(fResult)
		dyHistWeighted.SetDirectory(fResult)
		otherHist.SetDirectory(fResult)
		otherHistSmear.SetDirectory(fResult)
		otherHistScaleUp.SetDirectory(fResult)
		otherHistScaleDown.SetDirectory(fResult)
		otherHistWeighted.SetDirectory(fResult)
		hist.SetDirectory(fResult)

		fResult.Write()
		fResult.Close()



main()
