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
	
	lambdas = [10,16,22,28,34,40]
	models = ["ConLL","ConLR","ConRR","DesLL","DesLR","DesRR"]
	bins = [4,7]

	massPlot = getPlot("massPlotForLimit")
	massPlotSmeared = getPlot("massPlotSmeared")
	massPlotUp = getPlot("massPlotUp")
	massPlotDown = getPlot("massPlotDown")



	for i, histo in enumerate(histos):
		label = labels[i]

		for model in models:
			for l in lambdas:
				data = Process(Data)
				drellyan = Process(getattr(Backgrounds,"DrellYan"))
				other = Process(getattr(Backgrounds,"Other"))				
				#~ name = "CITo2E_Lam%dTeV%s"%(l,model)
				#~ signal = Process(getattr(Signals,name))
			#~ 
				#~ name = "CITo2E_Lam100kTeV%s"%(model)
				#~ signalDY = Process(getattr(Signals,name))
			
				fResult = TFile("inputsCI_%s_%dTeV_%s.root"%(label,l,model),"RECREATE")	
				
				#~ sigHist = deepcopy(signal.loadHistogramProjected(massPlot, bins[i]))
				#~ sigHistSmear = deepcopy(signal.loadHistogramProjected(massPlotSmeared, bins[i]))
				#~ sigHistScaleUp = deepcopy(signal.loadHistogramProjected(massPlotUp, bins[i]))
				#~ sigHistScaleDown = deepcopy(signal.loadHistogramProjected(massPlotDown, bins[i]))
				#~ if "_BE" in label:
					#~ sigHist.Add(deepcopy(signal.loadHistogramProjected(massPlot, 10)))
					#~ sigHistSmear.Add(deepcopy(signal.loadHistogramProjected(massPlotSmeared, 10)))
					#~ sigHistScaleUp.Add(deepcopy(signal.loadHistogramProjected(massPlotUp, 10)))
					#~ sigHistScaleDown.Add(deepcopy(signal.loadHistogramProjected(massPlotDown, 10)))
				
				
					
				#~ sigHistDY = deepcopy(signalDY.loadHistogramProjected(massPlot, bins[i]))
				#~ sigHistSmearDY = deepcopy(signalDY.loadHistogramProjected(massPlotSmeared, bins[i]))
				#~ sigHistScaleUpDY = deepcopy(signalDY.loadHistogramProjected(massPlotUp, bins[i]))
				#~ sigHistScaleDownDY = deepcopy(signalDY.loadHistogramProjected(massPlotDown, bins[i]))
				#~ if "_BE" in label:
					#~ sigHistDY.Add(deepcopy(signalDY.loadHistogramProjected(massPlot, 10)))
					#~ sigHistSmearDY.Add(deepcopy(signalDY.loadHistogramProjected(massPlotSmeared, 10)))
					#~ sigHistScaleUpDY.Add(deepcopy(signalDY.loadHistogramProjected(massPlotUp, 10)))
					#~ sigHistScaleDownDY.Add(deepcopy(signalDY.loadHistogramProjected(massPlotDown, 10)))
	
				#~ sigHist.Add(sigHistDY,-1)
				#~ sigHistSmear.Add(sigHistSmearDY,-1)
				#~ sigHistScaleUp.Add(sigHistScaleUpDY,-1)
				#~ sigHistScaleDown.Add(sigHistScaleDownDY,-1)
	
				hist = data.loadHistogramProjected(massPlot, bins[i])
				#~ if "_BE" in label:
					#~ hist.Add(deepcopy(data.loadHistogramProjected(massPlot, 10)))				
				hist.SetName("dataHist_%s" %label)

				dyHist = deepcopy(drellyan.loadHistogramProjected(massPlot, bins[i]))
				#~ print dyHist.Integral()
				dyHistSmear = deepcopy(drellyan.loadHistogramProjected(massPlotSmeared, bins[i]))
				dyHistScaleUp = deepcopy(drellyan.loadHistogramProjected(massPlotUp, bins[i]))
				dyHistScaleDown = deepcopy(drellyan.loadHistogramProjected(massPlotDown, bins[i]))
				#~ if "_BE" in label:
					#~ dyHist.Add(deepcopy(drellyan.loadHistogramProjected(massPlot, 10)))
					#~ dyHistSmear.Add(deepcopy(drellyan.loadHistogramProjected(massPlotSmeared, 10)))
					#~ dyHistScaleUp.Add(deepcopy(drellyan.loadHistogramProjected(massPlotUp, 10)))
					#~ dyHistScaleDown.Add(deepcopy(drellyan.loadHistogramProjected(massPlotDown, 10)))

				otherHist = deepcopy(other.loadHistogramProjected(massPlot, bins[i]))
				otherHistSmear = deepcopy(other.loadHistogramProjected(massPlotSmeared, bins[i]))
				otherHistScaleUp = deepcopy(other.loadHistogramProjected(massPlotUp, bins[i]))
				otherHistScaleDown = deepcopy(other.loadHistogramProjected(massPlotDown, bins[i]))
				#~ if "_BE" in label:
					#~ otherHist.Add(deepcopy(other.loadHistogramProjected(massPlot, 10)))
					#~ otherHistSmear.Add(deepcopy(other.loadHistogramProjected(massPlotSmeared, 10)))
					#~ otherHistScaleUp.Add(deepcopy(other.loadHistogramProjected(massPlotUp, 10)))
					#~ otherHistScaleDown.Add(deepcopy(other.loadHistogramProjected(massPlotDown, 10)))
	
				
				#~ sigHist.SetName("sigHist_%s"%label)
				#~ sigHistSmear.SetName("sigHistSmeared_%s"%label)
				#~ sigHistScaleUp.SetName("sigHistScaleUp_%s"%label)
				#~ sigHistScaleDown.SetName("sigHistScaleDown_%s"%label)
								
				dyHist.SetName("bkgHistDY_%s"%label)
				dyHistSmear.SetName("bkgHistDYSmeared_%s"%label)
				dyHistScaleUp.SetName("bkgHistDYScaleUp_%s"%label)
				dyHistScaleDown.SetName("bkgHistDYScaleDown_%s"%label)				
				otherHist.SetName("bkgHistOther_%s"%label)
				otherHistSmear.SetName("bkgHistOtherSmeared_%s"%label)
				otherHistScaleUp.SetName("bkgHistOtherScaleUp_%s"%label)
				otherHistScaleDown.SetName("bkgHistOtherScaleDown_%s"%label)				

				#~ if "_BB" in label:
				fJets = TFile("fixFilesEle/hist_jets.root","OPEN")	
				#~ print fJets.ls()
				#~ else:	
					#~ fJets = TFile("fixFilesEle/Heep-FR-Data-total-jets-BarrelEndCaps.root","OPEN")	

				if "BB" in label:
					jetHist = fJets.Get("h_mee_BB_usual")
				else:	
					jetHist = fJets.Get("h_mee_BE_usual")
				jetHist.SetName("bkgHistJets_%s"%label)				
				jetHist.SetDirectory(fResult)				
				
				print hist.Integral(hist.FindBin(400),hist.FindBin(500-0.01))
				print dyHist.Integral(dyHist.FindBin(400),dyHist.FindBin(500-0.01)) + otherHist.Integral(otherHist.FindBin(400),otherHist.FindBin(500-0.01)) + jetHist.Integral(jetHist.FindBin(400),jetHist.FindBin(500-0.01))
				print dyHist.Integral(dyHist.FindBin(400),dyHist.FindBin(500-0.01)) 
				print otherHist.Integral(otherHist.FindBin(400),otherHist.FindBin(500-0.01)) 
				print jetHist.Integral(jetHist.FindBin(400),jetHist.FindBin(500-0.01))		


#~ 
				#~ sigHist.SetDirectory(fResult)
				#~ sigHistSmear.SetDirectory(fResult)
				#~ sigHistScaleUp.SetDirectory(fResult)
				#~ sigHistScaleDown.SetDirectory(fResult)
				dyHist.SetDirectory(fResult)
				dyHistSmear.SetDirectory(fResult)
				dyHistScaleUp.SetDirectory(fResult)
				dyHistScaleDown.SetDirectory(fResult)
				otherHist.SetDirectory(fResult)
				otherHistSmear.SetDirectory(fResult)
				otherHistScaleUp.SetDirectory(fResult)
				otherHistScaleDown.SetDirectory(fResult)
				hist.SetDirectory(fResult)

				print hist.Integral(hist.FindBin(400),hist.GetNbinsX()), dyHist.Integral(hist.FindBin(400),hist.GetNbinsX())+otherHist.Integral(hist.FindBin(400),hist.GetNbinsX())+jetHist.Integral(hist.FindBin(400),hist.GetNbinsX())
									
				fResult.Write()
				fResult.Close()

		
		
main()
