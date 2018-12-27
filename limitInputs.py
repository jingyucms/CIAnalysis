from ROOT import * 
from numpy import array as ar
from array import array
from setTDRStyle import setTDRStyle
from copy import deepcopy

from helpers import *
from defs import getPlot, Backgrounds, Signals, Data



def main():
	### for data

	
	histos = ["BB","BE"]
	labels = ["dimuon_Moriond2017_BB","dimuon_Moriond2017_BE"]

	bins = [4,7]


	massPlot = getPlot("massPlotForLimit")
	massPlotSmeared = getPlot("massPlotSmeared")
	massPlotUp = getPlot("massPlotUp")
	massPlotDown = getPlot("massPlotDown")
	massPlotPUUp = getPlot("massPlotPUUp")
	massPlotPUDown = getPlot("massPlotPUDown")
	massPlotWeighted = getPlot("massPlotWeighted")


	for i, histo in enumerate(histos):
		label = labels[i]

		data = Process(Data)
		drellyan = Process(getattr(Backgrounds,"DrellYan"))
		other = Process(getattr(Backgrounds,"Other"))				
	
		fResult = TFile("inputsCI_%s.root"%(label),"RECREATE")	


		hist = deepcopy(data.loadHistogramProjected(massPlot, bins[i]))
		if "_BE" in label:
			hist.Add(deepcopy(data.loadHistogramProjected(massPlot, 10)))				
		hist.SetName("dataHist_%s" %label)

		dyHist = deepcopy(drellyan.loadHistogramProjected(massPlot, bins[i]))
		dyHistSmear = deepcopy(drellyan.loadHistogramProjected(massPlotSmeared, bins[i]))
		dyHistScaleUp = deepcopy(drellyan.loadHistogramProjected(massPlotUp, bins[i]))
		dyHistScaleDown = deepcopy(drellyan.loadHistogramProjected(massPlotDown, bins[i]))
		dyHistPUUp = deepcopy(drellyan.loadHistogramProjected(massPlotPUUp, bins[i]))
		dyHistPUDown = deepcopy(drellyan.loadHistogramProjected(massPlotPUDown, bins[i]))
		dyHistWeighted = deepcopy(drellyan.loadHistogramProjected(massPlotWeighted, bins[i]))
		if "_BE" in label:
			dyHist.Add(deepcopy(drellyan.loadHistogramProjected(massPlot, 10)))
			dyHistSmear.Add(deepcopy(drellyan.loadHistogramProjected(massPlotSmeared, 10)))
			dyHistScaleUp.Add(deepcopy(drellyan.loadHistogramProjected(massPlotUp, 10)))
			dyHistScaleDown.Add(deepcopy(drellyan.loadHistogramProjected(massPlotDown, 10)))
			dyHistPUUp.Add(deepcopy(drellyan.loadHistogramProjected(massPlotPUUp, 10)))
			dyHistPUDown.Add(deepcopy(drellyan.loadHistogramProjected(massPlotPUDown, 10)))
			dyHistWeighted.Add(deepcopy(drellyan.loadHistogramProjected(massPlotWeighted, 10)))

		otherHist = deepcopy(other.loadHistogramProjected(massPlot, bins[i]))
		otherHistSmear = deepcopy(other.loadHistogramProjected(massPlotSmeared, bins[i]))
		otherHistScaleUp = deepcopy(other.loadHistogramProjected(massPlotUp, bins[i]))
		otherHistScaleDown = deepcopy(other.loadHistogramProjected(massPlotDown, bins[i]))
		otherHistPUUp = deepcopy(other.loadHistogramProjected(massPlotPUUp, bins[i]))
		otherHistPUDown = deepcopy(other.loadHistogramProjected(massPlotPUDown, bins[i]))
		otherHistWeighted = deepcopy(other.loadHistogramProjected(massPlotWeighted, bins[i]))
		if "_BE" in label:
			otherHist.Add(deepcopy(other.loadHistogramProjected(massPlot, 10)))
			otherHistSmear.Add(deepcopy(other.loadHistogramProjected(massPlotSmeared, 10)))
			otherHistScaleUp.Add(deepcopy(other.loadHistogramProjected(massPlotUp, 10)))
			otherHistScaleDown.Add(deepcopy(other.loadHistogramProjected(massPlotDown, 10)))
			otherHistPUUp.Add(deepcopy(other.loadHistogramProjected(massPlotPUUp, 10)))
			otherHistPUDown.Add(deepcopy(other.loadHistogramProjected(massPlotPUDown, 10)))
			otherHistWeighted.Add(deepcopy(other.loadHistogramProjected(massPlotWeighted, 10)))

						
		dyHist.SetName("bkgHistDY_%s"%label)
		dyHistSmear.SetName("bkgHistDYSmeared_%s"%label)
		dyHistScaleUp.SetName("bkgHistDYScaleUp_%s"%label)
		dyHistScaleDown.SetName("bkgHistDYScaleDown_%s"%label)				
		dyHistPUUp.SetName("bkgHistDYPUUp_%s"%label)
		dyHistPUDown.SetName("bkgHistDYPUDown_%s"%label)				
		dyHistWeighted.SetName("bkgHistDYWeighted_%s"%label)				
		otherHist.SetName("bkgHistOther_%s"%label)
		otherHistSmear.SetName("bkgHistOtherSmeared_%s"%label)
		otherHistScaleUp.SetName("bkgHistOtherScaleUp_%s"%label)
		otherHistScaleDown.SetName("bkgHistOtherScaleDown_%s"%label)				
		otherHistPUUp.SetName("bkgHistOtherPUUp_%s"%label)
		otherHistPUDown.SetName("bkgHistOtherPUDown_%s"%label)				
		otherHistWeighted.SetName("bkgHistOtherWeighted_%s"%label)				

		if "_BB" in label:
			fJets = TFile("filesPU/Data-total-jets-BB.root","OPEN")	
		else:	
			fJets = TFile("filesPU/Data-total-jets-BEEE.root","OPEN")	

		jetHist = fJets.Get("TotalJets")
		jetHist.SetName("bkgHistJets_%s"%label)				
		jetHist.SetDirectory(fResult)				



		dyHistSmear.Scale(1.0113457140805746)
		otherHistSmear.Scale(1.0113457140805746)
		dyHistWeighted.Scale(1.0016195696993435)
		otherHistWeighted.Scale(1.0016195696993435)
		dyHistScaleUp.Scale(1.0079267396624512)
		dyHistScaleDown.Scale(1.0079267396624512)
		otherHistScaleUp.Scale(1.0079267396624512)
		otherHistScaleDown.Scale(1.0079267396624512)


		dyHist.SetDirectory(fResult)
		dyHistSmear.SetDirectory(fResult)
		dyHistScaleUp.SetDirectory(fResult)
		dyHistScaleDown.SetDirectory(fResult)
		dyHistPUUp.SetDirectory(fResult)
		dyHistPUDown.SetDirectory(fResult)
		dyHistWeighted.SetDirectory(fResult)
		otherHist.SetDirectory(fResult)
		otherHistSmear.SetDirectory(fResult)
		otherHistScaleUp.SetDirectory(fResult)
		otherHistScaleDown.SetDirectory(fResult)
		otherHistPUUp.SetDirectory(fResult)
		otherHistPUDown.SetDirectory(fResult)
		otherHistWeighted.SetDirectory(fResult)
		hist.SetDirectory(fResult)

		fResult.Write()
		fResult.Close()

		#~ xMin = 2000
		#~ xMax = 60000
		#~ print "Uncertainties:"
		#~ default =  dyHist.Integral(hist.FindBin(xMin),hist.FindBin(xMax-0.01)) + otherHist.Integral(hist.FindBin(xMin),hist.FindBin(xMax-0.01)) + jetHist.Integral(jetHist.FindBin(xMin),jetHist.FindBin(xMax-0.01))
		#~ 
		#~ errDY = ROOT.Double()
		#~ errOther = ROOT.Double()
		#~ 
		#~ default2 = dyHist.IntegralAndError(hist.FindBin(xMin),hist.FindBin(xMax-0.01),errDY) + otherHist.IntegralAndError(hist.FindBin(xMin),hist.FindBin(xMax-0.01),errOther) + jetHist.Integral(jetHist.FindBin(xMin),jetHist.FindBin(xMax-0.01))
		#~ err = errDY+errOther
		#~ print errDY, errOther
		#~ jetsDown =  dyHist.Integral(hist.FindBin(xMin),hist.FindBin(xMax-0.01)) + otherHist.Integral(hist.FindBin(xMin),hist.FindBin(xMax-0.01)) + jetHist.Integral(jetHist.FindBin(xMin),jetHist.FindBin(xMax-0.01)) *0.5
		#~ jetsUp =  dyHist.Integral(hist.FindBin(xMin),hist.FindBin(xMax-0.01)) + otherHist.Integral(hist.FindBin(xMin),hist.FindBin(xMax-0.01)) + jetHist.Integral(jetHist.FindBin(xMin),jetHist.FindBin(xMax-0.01)) *1.5
		#~ smear =  dyHistSmear.Integral(hist.FindBin(xMin),hist.FindBin(xMax-0.01)) + otherHistSmear.Integral(hist.FindBin(xMin),hist.FindBin(xMax-0.01)) + jetHist.Integral(jetHist.FindBin(xMin),jetHist.FindBin(xMax-0.01))
		#~ scaleUp =  dyHistScaleUp.Integral(hist.FindBin(xMin),hist.FindBin(xMax-0.01)) + otherHistScaleUp.Integral(hist.FindBin(xMin),hist.FindBin(xMax-0.01)) + jetHist.Integral(jetHist.FindBin(xMin),jetHist.FindBin(xMax-0.01))
		#~ PUDown =  dyHistPUDown.Integral(hist.FindBin(xMin),hist.FindBin(xMax-0.01)) + otherHistPUDown.Integral(hist.FindBin(xMin),hist.FindBin(xMax-0.01))	+ jetHist.Integral(jetHist.FindBin(xMin),jetHist.FindBin(xMax-0.01))			
		#~ PUUp =  dyHistPUUp.Integral(hist.FindBin(xMin),hist.FindBin(xMax-0.01)) + otherHistPUUp.Integral(hist.FindBin(xMin),hist.FindBin(xMax-0.01)) + jetHist.Integral(jetHist.FindBin(xMin),jetHist.FindBin(xMax-0.01))
		#~ scaleDown =  dyHistScaleDown.Integral(hist.FindBin(xMin),hist.FindBin(xMax-0.01)) + otherHistScaleDown.Integral(hist.FindBin(xMin),hist.FindBin(xMax-0.01)) + jetHist.Integral(jetHist.FindBin(xMin),jetHist.FindBin(xMax-0.01))		 		
		#~ ID =  dyHistWeighted.Integral(hist.FindBin(xMin),hist.FindBin(xMax-0.01)) + otherHistWeighted.Integral(hist.FindBin(xMin),hist.FindBin(xMax-0.01)) + jetHist.Integral(jetHist.FindBin(xMin),jetHist.FindBin(xMax-0.01))
		#~ 
		#~ print "Res: ", abs(1 - smear/default)
		#~ print "ScaleUp: ", abs(1 - scaleUp/default)
		#~ print "ScaleDown: ", abs(1 - scaleDown/default)
		#~ print "PU: ", max(abs(1 - PUDown/default),abs(1 - PUUp/default))
		#~ print "Jets: ", max(abs(1 - jetsDown/default),abs(1 - jetsUp/default))
		#~ print "ID: ", abs(1 - ID/default)
		#~ print "MC stats: ", abs(err/default2)
		#~ 


main()
