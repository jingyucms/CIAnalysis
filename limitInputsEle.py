from ROOT import * 
from numpy import array as ar
from array import array
from setTDRStyle import setTDRStyle
from copy import deepcopy

from helpersEle import *
from defsEle import getPlot, Backgrounds, Signals, Data

def main():
	### for data

	
	histos = ["BB","BE"]
	labels = ["dielectron_Moriond2017_BB","dielectron_Moriond2017_BE"]

	bins = [4,7]

	massPlot = getPlot("massPlotForLimit")
	massPlotSmeared = getPlot("massPlotSmeared")
	massPlotUp = getPlot("massPlotUp")
	massPlotDown = getPlot("massPlotDown")
	massPlotPUUp = getPlot("massPlotPUUp")
	massPlotPUDown = getPlot("massPlotPUDown")



	for i, histo in enumerate(histos):
		label = labels[i]


		data = Process(Data)
		drellyan = Process(getattr(Backgrounds,"DrellYan"))
		other = Process(getattr(Backgrounds,"Other"))				
	
		fResult = TFile("inputsCI_%s.root"%(label),"RECREATE")	
		

		hist = data.loadHistogramProjected(massPlot, bins[i])
			
		hist.SetName("dataHist_%s" %label)

		dyHist = deepcopy(drellyan.loadHistogramProjected(massPlot, bins[i]))
		dyHistSmear = deepcopy(drellyan.loadHistogramProjected(massPlotSmeared, bins[i]))
		dyHistScaleUp = deepcopy(drellyan.loadHistogramProjected(massPlotUp, bins[i]))
		dyHistScaleDown = deepcopy(drellyan.loadHistogramProjected(massPlotDown, bins[i]))
		dyHistPUUp = deepcopy(drellyan.loadHistogramProjected(massPlotPUUp, bins[i]))
		dyHistPUDown = deepcopy(drellyan.loadHistogramProjected(massPlotPUDown, bins[i]))


		otherHist = deepcopy(other.loadHistogramProjected(massPlot, bins[i]))
		otherHistSmear = deepcopy(other.loadHistogramProjected(massPlotSmeared, bins[i]))
		otherHistScaleUp = deepcopy(other.loadHistogramProjected(massPlotUp, bins[i]))
		otherHistScaleDown = deepcopy(other.loadHistogramProjected(massPlotDown, bins[i]))
		otherHistPUUp = deepcopy(other.loadHistogramProjected(massPlotPUUp, bins[i]))
		otherHistPUDown = deepcopy(other.loadHistogramProjected(massPlotPUDown, bins[i]))
						
		dyHist.SetName("bkgHistDY_%s"%label)
		dyHistSmear.SetName("bkgHistDYSmeared_%s"%label)
		dyHistScaleUp.SetName("bkgHistDYScaleUp_%s"%label)
		dyHistScaleDown.SetName("bkgHistDYScaleDown_%s"%label)				
		dyHistPUUp.SetName("bkgHistDYPUUp_%s"%label)
		dyHistPUDown.SetName("bkgHistDYPUDown_%s"%label)				
		otherHist.SetName("bkgHistOther_%s"%label)
		otherHistSmear.SetName("bkgHistOtherSmeared_%s"%label)
		otherHistScaleUp.SetName("bkgHistOtherScaleUp_%s"%label)
		otherHistScaleDown.SetName("bkgHistOtherScaleDown_%s"%label)				
		otherHistPUUp.SetName("bkgHistOtherPUUp_%s"%label)
		otherHistPUDown.SetName("bkgHistOtherPUDown_%s"%label)				

		fJets = TFile("filesElePU/hist_jets.root","OPEN")	

		if "BB" in label:
			jetHist = fJets.Get("h_mee_BB_usual")
		else:	
			jetHist = fJets.Get("h_mee_BE_usual")
		jetHist.SetName("bkgHistJets_%s"%label)				
		jetHist.SetDirectory(fResult)				

		dyHist.SetDirectory(fResult)
		dyHistSmear.SetDirectory(fResult)
		dyHistScaleUp.SetDirectory(fResult)
		dyHistScaleDown.SetDirectory(fResult)
		dyHistPUUp.SetDirectory(fResult)
		dyHistPUDown.SetDirectory(fResult)
		otherHist.SetDirectory(fResult)
		otherHistSmear.SetDirectory(fResult)
		otherHistScaleUp.SetDirectory(fResult)
		otherHistScaleDown.SetDirectory(fResult)
		otherHistPUUp.SetDirectory(fResult)
		otherHistPUDown.SetDirectory(fResult)
		hist.SetDirectory(fResult)

							
		fResult.Write()
		fResult.Close()


		
		### To print uncertainty values

		#~ xMin = 2000
		#~ xMax = 60000
		#~ 
#~ 
		#~ default =  dyHist.Integral(dyHist.FindBin(xMin),dyHist.FindBin(xMax-0.01)) + otherHist.Integral(dyHist.FindBin(xMin),dyHist.FindBin(xMax-0.01)) + jetHist.Integral(jetHist.FindBin(xMin),jetHist.FindBin(xMax-0.01))
#~ 
		#~ errDY = ROOT.Double()	
		#~ errOther = ROOT.Double()	
		#~ default2 = dyHist.IntegralAndError(hist.FindBin(xMin),hist.FindBin(xMax-0.01),errDY) + otherHist.IntegralAndError(hist.FindBin(xMin),hist.FindBin(xMax-0.01),errOther) + jetHist.Integral(jetHist.FindBin(xMin),jetHist.FindBin(xMax-0.01))
		#~ err = errDY+errOther
#~ 
		#~ jetsDown =  dyHist.Integral(dyHist.FindBin(xMin),dyHist.FindBin(xMax-0.01)) + otherHist.Integral(dyHist.FindBin(xMin),dyHist.FindBin(xMax-0.01)) + jetHist.Integral(jetHist.FindBin(xMin),jetHist.FindBin(xMax-0.01))*0.5
		#~ jetsUp =  dyHist.Integral(dyHist.FindBin(xMin),dyHist.FindBin(xMax-0.01)) + otherHist.Integral(dyHist.FindBin(xMin),dyHist.FindBin(xMax-0.01)) + jetHist.Integral(jetHist.FindBin(xMin),jetHist.FindBin(xMax-0.01))*1.5
		#~ scaleUp =  dyHistScaleUp.Integral(dyHistScaleUp.FindBin(xMin),dyHistScaleUp.FindBin(xMax-0.01)) + otherHistScaleUp.Integral(dyHistScaleUp.FindBin(xMin),dyHistScaleUp.FindBin(xMax-0.01)) + jetHist.Integral(jetHist.FindBin(xMin),jetHist.FindBin(xMax-0.01))
		#~ scaleDown =  dyHistScaleDown.Integral(dyHistScaleDown.FindBin(xMin),dyHistScaleDown.FindBin(xMax-0.01)) + otherHistScaleDown.Integral(dyHistScaleDown.FindBin(xMin),dyHistScaleDown.FindBin(xMax-0.01))	+ jetHist.Integral(jetHist.FindBin(xMin),jetHist.FindBin(xMax-0.01))			
		#~ scalePUUp =  dyHistPUUp.Integral(dyHistPUUp.FindBin(xMin),dyHistPUUp.FindBin(xMax-0.01)) + otherHistPUUp.Integral(dyHistPUUp.FindBin(xMin),dyHistPUUp.FindBin(xMax-0.01)) + jetHist.Integral(jetHist.FindBin(xMin),jetHist.FindBin(xMax-0.01))
		#~ scalePUDown =  dyHistPUDown.Integral(dyHistPUDown.FindBin(xMin),dyHistPUDown.FindBin(xMax-0.01)) + otherHistPUDown.Integral(dyHistPUDown.FindBin(xMin),dyHistPUDown.FindBin(xMax-0.01))	+ jetHist.Integral(jetHist.FindBin(xMin),jetHist.FindBin(xMax-0.01))		
		#~ 
		#~ print "Mass Scale: ", max(abs(1 - scaleUp/default),abs(1 - scaleDown/default))*100
		#~ print "PU: ", max(abs(1 - scalePUUp/default),abs(1 - scalePUDown/default))*100
		#~ print "Kets: ", max(abs(1 - jetsUp/default),abs(1 - jetsDown/default))*100
		#~ print "MC stats: ", abs(err/default2)*100
		#~ 
#~ 


		
		
main()
