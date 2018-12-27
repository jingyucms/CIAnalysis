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
	labels = ["dielectron_2017_BB","dielectron_2017_BE"]


	for i, histo in enumerate(histos):
		label = labels[i]

		massPlot = getPlot("massPlot%sNoLog"%histo)
		massPlotUp = getPlot("massPlot%sScaleUpNoLog"%histo)
		massPlotDown = getPlot("massPlot%sScaleDownNoLog"%histo)
		massPlotPUUp = getPlot("massPlotEle%sPUScaleUpNoLog"%histo)
		massPlotPUDown = getPlot("massPlotEle%sPUScaleDownNoLog"%histo)

		eventCounts = totalNumberOfGeneratedEvents(path,massPlot.muon)	
		negWeights = negWeightFractions(path,massPlot.muon)

		data = Process(Data,normalized=True)
		drellyan = Process(getattr(Backgrounds,"DrellYan"),eventCounts,negWeights)
		other = Process(getattr(Backgrounds,"Other"),eventCounts,negWeights)				
	
		fResult = TFile("inputsCI_%s.root"%(label),"RECREATE")	

		lumi = 41.529*1000
		
		hist = data.loadHistogram(massPlot, lumi)
			
		hist.SetName("dataHist_%s" %label)

		dyHist = deepcopy(drellyan.loadHistogram(massPlot, lumi))
		dyHistScaleUp = deepcopy(drellyan.loadHistogram(massPlotUp, lumi))
		dyHistScaleDown = deepcopy(drellyan.loadHistogram(massPlotDown, lumi))
		dyHistPUUp = deepcopy(drellyan.loadHistogram(massPlotPUUp, lumi))
		dyHistPUDown = deepcopy(drellyan.loadHistogram(massPlotPUDown, lumi))


		otherHist = deepcopy(other.loadHistogram(massPlot, lumi))
		otherHistScaleUp = deepcopy(other.loadHistogram(massPlotUp, lumi))
		otherHistScaleDown = deepcopy(other.loadHistogram(massPlotDown, lumi))
		otherHistPUUp = deepcopy(other.loadHistogram(massPlotPUUp, lumi))
		otherHistPUDown = deepcopy(other.loadHistogram(massPlotPUDown, lumi))
						
		dyHist.SetName("bkgHistDY_%s"%label)
		dyHistScaleUp.SetName("bkgHistDYScaleUp_%s"%label)
		dyHistScaleDown.SetName("bkgHistDYScaleDown_%s"%label)				
		dyHistPUUp.SetName("bkgHistDYPUUp_%s"%label)
		dyHistPUDown.SetName("bkgHistDYPUDown_%s"%label)				
		otherHist.SetName("bkgHistOther_%s"%label)
		otherHistScaleUp.SetName("bkgHistOtherScaleUp_%s"%label)
		otherHistScaleDown.SetName("bkgHistOtherScaleDown_%s"%label)				
		otherHistPUUp.SetName("bkgHistOtherPUUp_%s"%label)
		otherHistPUDown.SetName("bkgHistOtherPUDown_%s"%label)				

		fJets = TFile("../files/saved_hist_for_combine.root","OPEN")	

		if "BB" in label:
			jetHist = fJets.Get("Jets_h_mee_all_BB")
		else:	
			jetHist = fJets.Get("Jets_h_mee_all_BE")
		jetHist.SetName("bkgHistJets_%s"%label)				
		jetHist.SetDirectory(fResult)				

		dyHist.SetDirectory(fResult)
		dyHistScaleUp.SetDirectory(fResult)
		dyHistScaleDown.SetDirectory(fResult)
		dyHistPUUp.SetDirectory(fResult)
		dyHistPUDown.SetDirectory(fResult)
		otherHist.SetDirectory(fResult)
		otherHistScaleUp.SetDirectory(fResult)
		otherHistScaleDown.SetDirectory(fResult)
		otherHistPUUp.SetDirectory(fResult)
		otherHistPUDown.SetDirectory(fResult)
		hist.SetDirectory(fResult)

							
		fResult.Write()
		fResult.Close()
		
		
main()
