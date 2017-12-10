import ROOT
import gc
from array import array
from ROOT import TCanvas, TPad, TH1F, TH2F, TH1I, THStack, TLegend, TMath
from ConfigParser import ConfigParser
from math import sqrt
from defs import defineMyColors, myColors, fileNames, path
from copy import deepcopy
config = ConfigParser()



	
def totalNumberOfGeneratedEvents(path):
	"""
	path: path to directory containing all sample files

	returns dict samples names -> number of simulated events in source sample
	"""
	from ROOT import TFile
	result = {}
	#~ print path

	for sampleName, filePath in getFilePathsAndSampleNames(path).iteritems():
			print sampleName
			rootFile = TFile(filePath, "read")
			result[sampleName] = rootFile.FindObjectAny("Events").GetBinContent(1)				
	return result
	
def loadHistoFromFile(fileName,histName,rebin):
	"""
	returns histogram from file
	"""
	from ROOT import TFile, TH1F
	rootFile = TFile(path+fileName, "read")
	if "jets" in fileName:
		tmpResult = rootFile.Get("TotalJets")
		result = TH1F("jets","jets",10000,0,10000)
		for i in range(0,tmpResult.GetNbinsX()):
			result.SetBinContent(i,tmpResult.GetBinContent(i))
		
	else:	
		result = rootFile.Get(histName)
	result.Rebin(rebin)
	result.SetDirectory(0)	
	return deepcopy(result)

def loadHistoFromFileProjected(fileName,histName,rebin,binNumber):
	"""
	returns histogram from file
	"""
	
	from random import randint
	from sys import maxint
	name = "%x"%(randint(0, maxint))	
	from ROOT import TFile, TH1F
	rootFile = TFile(path+fileName, "read")
	print histName, fileName
	result = rootFile.Get(histName).ProjectionX(name,binNumber,binNumber)
	#~ print rootFile.Get(histName).GetYaxis().GetBinLabel(binNumber)
	#~ result.Rebin(rebin)
	#~ result.Sumw2()
	result.SetDirectory(0)	
	return result




def getFilePathsAndSampleNames(path):
	"""
	helper function
	path: path to directory containing all sample files

	returns: dict of smaple names -> path of .root file (for all samples in path)
	"""
	result = []
	from glob import glob
	from re import match
	result = {}

	for filePath in glob("%s/*.root"%(path)):
		if "ana_datamc" in filePath and not "SingleMuon" in filePath:
			sampleName = filePath.split("/")[-1].split("ana_datamc_")[-1].split(".root")[0]
			result[sampleName] = filePath
	return result


def getHistoFromTree(tree,plot,nEvents = -1):

	from ROOT import TH1F
	from random import randint
	from sys import maxint
	if nEvents < 0:
		nEvents = maxint
	#make a random name you could give something meaningfull here,
	#but that would make this less readable

	

	name = "%x"%(randint(0, maxint))
	if plot.binning == []:
		result = TH1F(name, "", plot.nBins, plot.xMin, plot.xMax)
	else:
		result = TH1F(name, "", len(plot.binning)-1, array("f",plot.binning))
		
	result.Sumw2()
	tree.Draw("%s>>%s"%(plot.variable, name), plot.cut, "goff", nEvents)
	
	result.SetBinContent(plot.nBins,result.GetBinContent(plot.nBins)+result.GetBinContent(plot.nBins+1))
	if result.GetBinContent(plot.nBins) >= 0.:
		result.SetBinError(plot.nBins,sqrt(result.GetBinContent(plot.nBins)))
	else:
		result.SetBinError(plot.nBins,0)

	return result

	

def createMyColors():
    iIndex = 2000

    containerMyColors = []
    for color in defineMyColors.keys():
        tempColor = ROOT.TColor(iIndex,
            float(defineMyColors[color][0]) / 255, float(defineMyColors[color][1]) / 255, float(defineMyColors[color][2]) / 255)
        containerMyColors.append(tempColor)

        myColors.update({ color: iIndex })
        iIndex += 1

    return containerMyColors
	
class Process:
	samples = []
	label = ""
	theColor = 0
	theLineColor = 0 
	histo = None
	uncertainty = 0.
	scaleFac = 1.
	
	def __init__(self, process, normalized = True):
		self.samples = process.subprocesses
		self.label = process.label
		self.theColor = process.fillcolor
		self.theLineColor = process.linecolor
		self.normalized = normalized

		
	def loadHistogram(self,plot):
		
		for index, sample in enumerate(self.samples):
			tempHist = loadHistoFromFile(fileNames[sample],plot.histName,plot.rebin)
			###tempHist.Scale(lumi*self.xsecs[index]/self.nEvents[index]) #histograms are already scaled to lumi
			if self.histo == None:
				self.histo = tempHist.Clone()
			else:	
				self.histo.Add(tempHist.Clone())
		self.histo.SetFillColor(self.theColor)
		self.histo.SetLineColor(self.theLineColor)
		self.histo.GetXaxis().SetTitle(plot.xaxis) 
		self.histo.GetYaxis().SetTitle(plot.yaxis)	
		if "CI" in self.label:
			self.histo.Scale(1.3)				
		return self.histo
	def loadHistogramProjected(self,plot,binNumber):
		histo = None
		for index, sample in enumerate(self.samples):
			tempHist = loadHistoFromFileProjected(fileNames[sample],plot.histName,plot.rebin,binNumber)
			###tempHist.Scale(lumi*self.xsecs[index]/self.nEvents[index]) #histograms are already scaled to lumi
			if histo == None:
				histo = tempHist.Clone()
			else:	
				histo.Add(tempHist.Clone())
		histo.SetFillColor(self.theColor)
		histo.SetLineColor(self.theLineColor)
		histo.GetXaxis().SetTitle(plot.xaxis) 
		histo.GetYaxis().SetTitle(plot.yaxis)	
		return histo

	
class TheStack:
	from ROOT import THStack
	theStack = THStack()	
	theHistogram = None	
	def  __init__(self,processes,plot):
		self.theStack = THStack()
			
		for process in processes:
			temphist = process.loadHistogram(plot)

			self.theStack.Add(temphist.Clone())
			if self.theHistogram == None:
				self.theHistogram = temphist.Clone()
			else:	
				self.theHistogram.Add(temphist.Clone())

def getDataHist(plot,files,fromTree=False):
	if not fromTree:
		histo = loadHistoFromFile(files["data"], plot.histName,plot.rebin)
	else:
		histo = getHistoFromTree(files["data"], plot)
	return histo	




