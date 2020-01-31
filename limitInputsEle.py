from ROOT import TFile 
from numpy import array as ar
from array import array
from setTDRStyle import setTDRStyle
from copy import deepcopy

from helpers import *
from defs import getPlot, Backgrounds, Signals, Data, Data2016, Data2018, zScale, zScale2018, zScale2016, Backgrounds2016, Backgrounds2018

def main():
	### for data

	
	histos = ["BB","BE","BB","BE","BB","BE"]
	labels = ["dielectron_2016_BB","dielectron_2016_BE","dielectron_2017_BB","dielectron_2017_BE","dielectron_2018_BB","dielectron_2018_BE"]

	css = ["inc","cspos","csneg"]
	for cs in css:
		for i, histo in enumerate(histos):
			label = labels[i]
			if cs == "cspos":
				massPlot = getPlot("massPlotEle%sCSPosNoLog"%histo)
				massPlotUp = getPlot("massPlotEle%sScaleUpCSPosNoLog"%histo)
				massPlotDown = getPlot("massPlotEle%sScaleDownCSPosNoLog"%histo)
				massPlotPUUp = getPlot("massPlotEle%sPUScaleUpCSPosNoLog"%histo)
				massPlotPUDown = getPlot("massPlotEle%sPUScaleDownCSPosNoLog"%histo)
			if cs == "csneg":
				massPlot = getPlot("massPlotEle%sCSNegNoLog"%histo)
				massPlotUp = getPlot("massPlotEle%sScaleUpCSNegNoLog"%histo)
				massPlotDown = getPlot("massPlotEle%sScaleDownCSNegNoLog"%histo)
				massPlotPUUp = getPlot("massPlotEle%sPUScaleUpCSNegNoLog"%histo)
				massPlotPUDown = getPlot("massPlotEle%sPUScaleDownCSNegNoLog"%histo)
			else:
				massPlot = getPlot("massPlotEle%sNoLog"%histo)
				massPlotUp = getPlot("massPlotEle%sScaleUpNoLog"%histo)
				massPlotDown = getPlot("massPlotEle%sScaleDownNoLog"%histo)
				massPlotPUUp = getPlot("massPlotEle%sPUScaleUpNoLog"%histo)
				massPlotPUDown = getPlot("massPlotEle%sPUScaleDownNoLog"%histo)

			eventCounts = totalNumberOfGeneratedEvents(path,massPlot.muon)	
			negWeights = negWeightFractions(path,massPlot.muon)

			if "2016" in label:
				data = Process(Data2016, normalized=True)
				drellyan = Process(getattr(Backgrounds2016,"DrellYan"),eventCounts,negWeights)
				other = Process(getattr(Backgrounds2016,"Other"),eventCounts,negWeights)				
				jets = Process(getattr(Backgrounds2016,"Jets"),eventCounts,negWeights, normalized = True)				
			elif "2018" in label:
				data = Process(Data2018, normalized=True)
				drellyan = Process(getattr(Backgrounds2018,"DrellYan"),eventCounts,negWeights)
				other = Process(getattr(Backgrounds2018,"Other"),eventCounts,negWeights)				
				jets = Process(getattr(Backgrounds2018,"Jets"),eventCounts,negWeights, normalized = True)				
			else:
				data = Process(Data, normalized=True)
				drellyan = Process(getattr(Backgrounds,"DrellYan"),eventCounts,negWeights)
				other = Process(getattr(Backgrounds,"Other"),eventCounts,negWeights)	
				jets = Process(getattr(Backgrounds,"Jets"),eventCounts,negWeights, normalized = True)	
				
			if cs == "inc":
				fResult = TFile("inputsCI_%s.root"%(label),"RECREATE")	
			else:
				fResult = TFile("inputsCI_%s_%s.root"%(cs,label),"RECREATE")


			if "2016" in label:	
					lumi = 35.9*1000
					if "bbbe" in massPlot.histName:
						zScaleFac = zScale2016["electrons"][0]
					elif "bb" in massPlot.histName:
						zScaleFac = zScale2016["electrons"][1]
					elif "be" in massPlot.histName:
						zScaleFac = zScale2016["electrons"][2]
					else:
						zScaleFac = zScale2016["electrons"][0]

			elif "2018" in label:
					lumi = 59.97*1000
					if "bbbe" in massPlot.histName:
						zScaleFac = zScale2018["electrons"][0]
					elif "bb" in massPlot.histName:
						zScaleFac = zScale2018["electrons"][1]
					elif "be" in massPlot.histName:
						zScaleFac = zScale2018["electrons"][2]
					else:
						zScaleFac = zScale2018["electrons"][0]
			else:
					lumi = 41.529*1000
					if "bbbe" in massPlot.histName:
						zScaleFac = zScale["electrons"][0]
					elif "bb" in massPlot.histName:
						zScaleFac = zScale["electrons"][1]
					elif "be" in massPlot.histName:
						zScaleFac = zScale["electrons"][2]
					else:
						zScaleFac = zScale["electrons"][0]
		
			
			jetHist = deepcopy(jets.loadHistogram(massPlot,lumi,zScaleFac))
			hist = data.loadHistogram(massPlot, lumi, zScaleFac)
			if cs == "inc":	
				hist.SetName("dataHist_%s" %(label))
			else:	
				hist.SetName("dataHist_%s_%s" %(cs,label))

			dyHist = deepcopy(drellyan.loadHistogram(massPlot, lumi, zScaleFac))
			dyHistScaleUp = deepcopy(drellyan.loadHistogram(massPlotUp, lumi, zScaleFac))
			dyHistScaleDown = deepcopy(drellyan.loadHistogram(massPlotDown, lumi, zScaleFac))
			dyHistPUUp = deepcopy(drellyan.loadHistogram(massPlotPUUp, lumi, zScaleFac))
			dyHistPUDown = deepcopy(drellyan.loadHistogram(massPlotPUDown, lumi, zScaleFac))


			otherHist = deepcopy(other.loadHistogram(massPlot, lumi, zScaleFac))
			otherHistScaleUp = deepcopy(other.loadHistogram(massPlotUp, lumi, zScaleFac))
			otherHistScaleDown = deepcopy(other.loadHistogram(massPlotDown, lumi, zScaleFac))
			otherHistPUUp = deepcopy(other.loadHistogram(massPlotPUUp, lumi, zScaleFac))
			otherHistPUDown = deepcopy(other.loadHistogram(massPlotPUDown, lumi, zScaleFac))
			if cs == "inc":
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
			else:
				dyHist.SetName("bkgHistDY_%s_%s"%(cs,label))
				dyHistScaleUp.SetName("bkgHistDYScaleUp_%s_%s"%(cs,label))
				dyHistScaleDown.SetName("bkgHistDYScaleDown_%s_%s"%(cs,label))				
				dyHistPUUp.SetName("bkgHistDYPUUp_%s_%s"%(cs,label))
				dyHistPUDown.SetName("bkgHistDYPUDown_%s_%s"%(cs,label))				
				otherHist.SetName("bkgHistOther_%s_%s"%(cs,label))
				otherHistScaleUp.SetName("bkgHistOtherScaleUp_%s_%s"%(cs,label))
				otherHistScaleDown.SetName("bkgHistOtherScaleDown_%s_%s"%(cs,label))				
				otherHistPUUp.SetName("bkgHistOtherPUUp_%s_%s"%(cs,label))
				otherHistPUDown.SetName("bkgHistOtherPUDown_%s_%s"%(cs,label))				

			if not cs == "inc":
				jetHist.SetName("bkgHistJets_%s_%s"%(cs,label))				
			else:	
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
