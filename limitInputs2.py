from ROOT import * 
from numpy import array as ar
from array import array
from setTDRStyle import setTDRStyle
from copy import deepcopy

from helpers import *
from defs import getPlot, Backgrounds, Signals, Data

def main():
	### for data

	
	histos = ["BBCSPos","BBCSNeg","BECSPos","BECSNeg"]
	labels = ["dimuon_BBCSPos","dimuon_BBCSNeg","dimuon_BECSPos","dimuon_BECSNeg"]
	
	lambdas = [10,16,22,28,34]
	models = ["ConLL","ConLR","ConRR","DesLL","DesLR","DesRR"]
	bins = [6,5,9,8]

	massPlot = getPlot("massPlotForLimit")
	massPlotSmeared = getPlot("massPlotSmeared")
	massPlotUp = getPlot("massPlotUp")
	massPlotDown = getPlot("massPlotDown")
	massPlotWeighted = getPlot("massPlotWeighted")



	for i, histo in enumerate(histos):
		label = labels[i]

		for model in models:
			for l in lambdas:
				data = Process(Data)
				drellyan = Process(getattr(Backgrounds,"DrellYan"))
				other = Process(getattr(Backgrounds,"Other"))				
				name = "CITo2Mu_Lam%dTeV%s"%(l,model)
				signal = Process(getattr(Signals,name))
			
				name = "CITo2Mu_Lam100kTeV%s"%(model)
				signalDY = Process(getattr(Signals,name))
			
				fResult = TFile("inputsCI_%s_%dTeV_%s.root"%(label,l,model),"RECREATE")	
				
				sigHist = deepcopy(signal.loadHistogramProjected(massPlot, bins[i]))
				sigHistSmear = deepcopy(signal.loadHistogramProjected(massPlotSmeared, bins[i]))
				sigHistScaleUp = deepcopy(signal.loadHistogramProjected(massPlotUp, bins[i]))
				sigHistScaleDown = deepcopy(signal.loadHistogramProjected(massPlotDown, bins[i]))
				sigHistWeighted = deepcopy(signal.loadHistogramProjected(massPlotWeighted, bins[i]))
				if "_BECSPos" in label:
					sigHist.Add(deepcopy(signal.loadHistogramProjected(massPlot, 12)))
					sigHistSmear.Add(deepcopy(signal.loadHistogramProjected(massPlotSmeared, 12)))
					sigHistScaleUp.Add(deepcopy(signal.loadHistogramProjected(massPlotUp, 12)))
					sigHistScaleDown.Add(deepcopy(signal.loadHistogramProjected(massPlotDown, 12)))
					sigHistWeighted.Add(deepcopy(signal.loadHistogramProjected(massPlotWeighted, 12)))
				
				if "_BECSNeg" in label:
					sigHist.Add(deepcopy(signal.loadHistogramProjected(massPlot, 11)))
					sigHistSmear.Add(deepcopy(signal.loadHistogramProjected(massPlotSmeared, 11)))
					sigHistScaleUp.Add(deepcopy(signal.loadHistogramProjected(massPlotUp, 11)))
					sigHistScaleDown.Add(deepcopy(signal.loadHistogramProjected(massPlotDown, 11)))
					sigHistWeighted.Add(deepcopy(signal.loadHistogramProjected(massPlotWeighted, 11)))
				
					
				sigHistDY = deepcopy(signalDY.loadHistogramProjected(massPlot, bins[i]))
				sigHistSmearDY = deepcopy(signalDY.loadHistogramProjected(massPlotSmeared, bins[i]))
				sigHistScaleUpDY = deepcopy(signalDY.loadHistogramProjected(massPlotUp, bins[i]))
				sigHistScaleDownDY = deepcopy(signalDY.loadHistogramProjected(massPlotDown, bins[i]))
				sigHistWeightedDY = deepcopy(signalDY.loadHistogramProjected(massPlotWeighted, bins[i]))
				if "_BECSPos" in label:
					sigHistDY.Add(deepcopy(signalDY.loadHistogramProjected(massPlot, 12)))
					sigHistSmearDY.Add(deepcopy(signalDY.loadHistogramProjected(massPlotSmeared, 12)))
					sigHistScaleUpDY.Add(deepcopy(signalDY.loadHistogramProjected(massPlotUp, 12)))
					sigHistScaleDownDY.Add(deepcopy(signalDY.loadHistogramProjected(massPlotDown, 12)))
					sigHistWeightedDY.Add(deepcopy(signalDY.loadHistogramProjected(massPlotWeighted, 12)))
				if "_BECSNeg" in label:
					sigHistDY.Add(deepcopy(signalDY.loadHistogramProjected(massPlot, 11)))
					sigHistSmearDY.Add(deepcopy(signalDY.loadHistogramProjected(massPlotSmeared, 11)))
					sigHistScaleUpDY.Add(deepcopy(signalDY.loadHistogramProjected(massPlotUp, 11)))
					sigHistScaleDownDY.Add(deepcopy(signalDY.loadHistogramProjected(massPlotDown, 11)))
					sigHistWeightedDY.Add(deepcopy(signalDY.loadHistogramProjected(massPlotWeighted, 11)))
	
				sigHist.Add(sigHistDY,-1)
				sigHistSmear.Add(sigHistSmearDY,-1)
				sigHistScaleUp.Add(sigHistScaleUpDY,-1)
				sigHistScaleDown.Add(sigHistScaleDownDY,-1)
				sigHistWeighted.Add(sigHistWeightedDY,-1)
	
				hist = data.loadHistogramProjected(massPlot, bins[i])
				if "_BECSPos" in label:
					hist.Add(deepcopy(data.loadHistogramProjected(massPlot, 12)))				
				if "_BECSNeg" in label:
					hist.Add(deepcopy(data.loadHistogramProjected(massPlot, 11)))				
				hist.SetName("dataHist_%s" %label)

				dyHist = deepcopy(drellyan.loadHistogramProjected(massPlot, bins[i]))
				dyHistSmear = deepcopy(drellyan.loadHistogramProjected(massPlotSmeared, bins[i]))
				dyHistScaleUp = deepcopy(drellyan.loadHistogramProjected(massPlotUp, bins[i]))
				dyHistScaleDown = deepcopy(drellyan.loadHistogramProjected(massPlotDown, bins[i]))
				dyHistWeighted = deepcopy(drellyan.loadHistogramProjected(massPlotWeighted, bins[i]))
				if "_BECSPos" in label:
					dyHist.Add(deepcopy(drellyan.loadHistogramProjected(massPlot, 12)))
					dyHistSmear.Add(deepcopy(drellyan.loadHistogramProjected(massPlotSmeared,12)))
					dyHistScaleUp.Add(deepcopy(drellyan.loadHistogramProjected(massPlotUp, 12)))
					dyHistScaleDown.Add(deepcopy(drellyan.loadHistogramProjected(massPlotDown, 12)))
					dyHistWeighted.Add(deepcopy(drellyan.loadHistogramProjected(massPlotWeighted, 12)))
				if "_BECSNeg" in label:
					dyHist.Add(deepcopy(drellyan.loadHistogramProjected(massPlot, 11)))
					dyHistSmear.Add(deepcopy(drellyan.loadHistogramProjected(massPlotSmeared,11)))
					dyHistScaleUp.Add(deepcopy(drellyan.loadHistogramProjected(massPlotUp, 11)))
					dyHistScaleDown.Add(deepcopy(drellyan.loadHistogramProjected(massPlotDown, 11)))
					dyHistWeighted.Add(deepcopy(drellyan.loadHistogramProjected(massPlotWeighted, 11)))


				otherHist = deepcopy(other.loadHistogramProjected(massPlot, bins[i]))
				otherHistSmear = deepcopy(other.loadHistogramProjected(massPlotSmeared, bins[i]))
				otherHistScaleUp = deepcopy(other.loadHistogramProjected(massPlotUp, bins[i]))
				otherHistScaleDown = deepcopy(other.loadHistogramProjected(massPlotDown, bins[i]))
				otherHistWeighted = deepcopy(other.loadHistogramProjected(massPlotWeighted, bins[i]))
				if "_BECSPos" in label:
					otherHist.Add(deepcopy(other.loadHistogramProjected(massPlot, 12)))
					otherHistSmear.Add(deepcopy(other.loadHistogramProjected(massPlotSmeared, 12)))
					otherHistScaleUp.Add(deepcopy(other.loadHistogramProjected(massPlotUp, 12)))
					otherHistScaleDown.Add(deepcopy(other.loadHistogramProjected(massPlotDown, 12)))
					otherHistWeighted.Add(deepcopy(other.loadHistogramProjected(massPlotWeighted, 12)))
				if "_BECSNeg" in label:
					otherHist.Add(deepcopy(other.loadHistogramProjected(massPlot, 11)))
					otherHistSmear.Add(deepcopy(other.loadHistogramProjected(massPlotSmeared, 11)))
					otherHistScaleUp.Add(deepcopy(other.loadHistogramProjected(massPlotUp, 11)))
					otherHistScaleDown.Add(deepcopy(other.loadHistogramProjected(massPlotDown, 11)))
					otherHistWeighted.Add(deepcopy(other.loadHistogramProjected(massPlotWeighted, 11)))
	
				
				sigHist.SetName("sigHist_%s"%label)
				sigHistSmear.SetName("sigHistSmeared_%s"%label)
				sigHistScaleUp.SetName("sigHistScaleUp_%s"%label)
				sigHistScaleDown.SetName("sigHistScaleDown_%s"%label)
				sigHistWeighted.SetName("sigHistWeighted_%s"%label)
								
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
					fJets = TFile("files/Data-total-jets-BB.root","OPEN")	
				else:	
					fJets = TFile("files/Data-total-jets-BEEE.root","OPEN")	

				jetHist = fJets.Get("TotalJets")
				jetHist.SetName("bkgHistJets_%s"%label)				
				jetHist.SetDirectory(fResult)				
				

				sigHist.SetDirectory(fResult)
				sigHistSmear.SetDirectory(fResult)
				sigHistScaleUp.SetDirectory(fResult)
				sigHistScaleDown.SetDirectory(fResult)
				sigHistWeighted.SetDirectory(fResult)
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
