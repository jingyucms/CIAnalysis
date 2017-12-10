from ROOT import * 
from numpy import array as ar
from array import array
from setTDRStyle import setTDRStyle
from copy import deepcopy
import ratios
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
	massPlotWeighted = getPlot("massPlotWeighted")



	for i, histo in enumerate(histos):
		label = labels[i]
		
		drellyan = Process(getattr(Backgrounds,"DrellYan"))

		dyHist = deepcopy(drellyan.loadHistogramProjected(massPlot, bins[i]))
		print dyHist.Integral()
		dyHistSmear = deepcopy(drellyan.loadHistogramProjected(massPlotSmeared, bins[i]))
		dyHistScaleUp = deepcopy(drellyan.loadHistogramProjected(massPlotUp, bins[i]))
		dyHistScaleDown = deepcopy(drellyan.loadHistogramProjected(massPlotDown, bins[i]))
		dyHistWeighted = deepcopy(drellyan.loadHistogramProjected(massPlotWeighted, bins[i]))
		if "_BE" in label:
			dyHist.Add(deepcopy(drellyan.loadHistogramProjected(massPlot, 10)))
			dyHistSmear.Add(deepcopy(drellyan.loadHistogramProjected(massPlotSmeared, 10)))
			dyHistScaleUp.Add(deepcopy(drellyan.loadHistogramProjected(massPlotUp, 10)))
			dyHistScaleDown.Add(deepcopy(drellyan.loadHistogramProjected(massPlotDown, 10)))
			dyHistWeighted.Add(deepcopy(drellyan.loadHistogramProjected(massPlotWeighted, 10)))
			
		dyHist.Rebin(160)
		dyHistSmear.Rebin(160)
		dyHistScaleDown.Rebin(160)
		dyHistWeighted.Rebin(160)
		hCanvas = TCanvas("hCanvas", "Distribution", 800,800)
	
		plotPad = ROOT.TPad("plotPad","plotPad",0,0.3,1,1)
		ratioPad = ROOT.TPad("ratioPad","ratioPad",0,0.,1,0.3)
		setTDRStyle()		
		plotPad.UseCurrentStyle()
		ratioPad.UseCurrentStyle()
		plotPad.Draw()	
		ratioPad.Draw()	
		plotPad.cd()
		
		plotPad.DrawFrame(400,0,3500,2000,"; dimuon mass [GeV]; Events / 20 GeV")
		
		dyHist.Draw("samehist")
		dyHist.SetFillColor(kWhite)
		dyHistSmear.SetFillColor(kWhite)
		dyHistScaleDown.SetFillColor(kWhite)
		dyHistWeighted.SetFillColor(kWhite)
		dyHistSmear.SetLineColor(kRed)
		dyHistScaleDown.SetLineColor(kBlue)
		dyHistWeighted.SetLineColor(kGreen+2)
		dyHistSmear.Draw("samehist")
		dyHistScaleDown.Draw("samehist")
		dyHistWeighted.Draw("samehist")
		
		legend = TLegend(0.375, 0.6, 0.925, 0.925)
		legend.SetFillStyle(0)
		legend.SetBorderSize(0)
		legend.SetTextFont(42)		
		legend.AddEntry(dyHist,"Default","l")	
		legend.AddEntry(dyHistSmear,"Resolution Uncertainty","l")	
		legend.AddEntry(dyHistScaleDown,"Scale Uncertainty","l")	
		legend.AddEntry(dyHistWeighted,"ID Uncertainty","l")	
		legend.Draw()
		
		ratioPad.cd()
		xMin = 400
		xMax = 3500
		ratioGraphs =  ratios.RatioGraph(dyHist,dyHistSmear, xMin=xMin, xMax=xMax,title="Default / Uncert",yMin=0.8,yMax=1.3,ndivisions=10,color=kRed,adaptiveBinning=10000)
		ratioGraphs.draw(ROOT.gPad,True,False,True,chi2Pos=0.8)		
		ratioGraphs2 =  ratios.RatioGraph(dyHist,dyHistScaleDown, xMin=xMin, xMax=xMax,title="Default / Uncert",yMin=0.8,yMax=1.3,ndivisions=10,color=kBlue,adaptiveBinning=10000)
		ratioGraphs2.draw(ROOT.gPad,False,False,True,chi2Pos=0.8)
		ratioGraphs3 =  ratios.RatioGraph(dyHist,dyHistWeighted, xMin=xMin, xMax=xMax,title="Default / Uncert",yMin=0.8,yMax=1.3,ndivisions=10,color=kGreen+2,adaptiveBinning=10000)
		ratioGraphs3.draw(ROOT.gPad,False,False,True,chi2Pos=0.8)		
		
		hCanvas.Print("uncertainties_%s.pdf"%label)
		
main()
