from ROOT import TFile
from numpy import array as ar
from array import array
from setTDRStyle import setTDRStyle
from copy import deepcopy

from helpers import *
from defs import getPlot, Backgrounds, Signals, Data



def main():
	### for data

	
	histos = ["BB","BE"]
	labels = ["dimuon_2017_BB","dimuon_2017_BE"]

	for i, histo in enumerate(histos):
		label = labels[i]

		massPlot = getPlot("massPlot%sNoLog"%histo)
		massPlotSmeared = getPlot("massPlot%sSmearNoLog"%histo)
		massPlotUp = getPlot("massPlot%sScaleUpNoLog"%histo)
		massPlotDown = getPlot("massPlot%sScaleDownNoLog"%histo)
		massPlotWeighted = getPlot("massPlot%sMuonIDNoLog"%histo)

		eventCounts = totalNumberOfGeneratedEvents(path,massPlot.muon)	
		negWeights = negWeightFractions(path,massPlot.muon)

		data = Process(Data, normalized=True)
		drellyan = Process(getattr(Backgrounds,"DrellYan"),eventCounts,negWeights)
		other = Process(getattr(Backgrounds,"Other"),eventCounts,negWeights)				
	
		fResult = TFile("inputsCI_%s.root"%(label),"RECREATE")	


		lumi = 42.135*1000

		hist = deepcopy(data.loadHistogram(massPlot,lumi))			
		hist.SetName("dataHist_%s" %label)


		dyHist = deepcopy(drellyan.loadHistogram(massPlot,lumi))
		dyHistSmear = deepcopy(drellyan.loadHistogram(massPlotSmeared,lumi))
		dyHistScaleUp = deepcopy(drellyan.loadHistogram(massPlotUp,lumi))
		dyHistScaleDown = deepcopy(drellyan.loadHistogram(massPlotDown,lumi))
		dyHistWeighted = deepcopy(drellyan.loadHistogram(massPlotWeighted,lumi))

		otherHist = deepcopy(other.loadHistogram(massPlot,lumi))
		otherHistSmear = deepcopy(other.loadHistogram(massPlotSmeared,lumi))
		otherHistScaleUp = deepcopy(other.loadHistogram(massPlotUp,lumi))
		otherHistScaleDown = deepcopy(other.loadHistogram(massPlotDown,lumi))
		otherHistWeighted = deepcopy(other.loadHistogram(massPlotWeighted,lumi))
						
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

		if "_BB" in label:
			fJets = TFile("../files/Data-total-jets-BB-pt53.root","OPEN")	
		else:	
			fJets = TFile("../files/Data-total-jets-BEEE-pt53.root","OPEN")	

		jetHist = fJets.Get("TotalJets")
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
