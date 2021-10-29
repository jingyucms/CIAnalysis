import ROOT
import gc
from array import array
from ROOT import TCanvas, TPad, TH1F, TH2F, TH1I, THStack, TLegend, TMath
from math import sqrt
from defs import defineMyColors, myColors, fileNames, fileNamesEle, path, crossSections, zScale, zScale2016
from copy import deepcopy
import math, uuid

	
	
def totalNumberOfGeneratedEvents(path,muon=True,genMass=False):
	"""
	path: path to directory containing all sample files

	returns dict samples names -> number of simulated events in source sample
	"""
	from ROOT import TFile
	result = {}

	for sampleName, filePath in getFilePathsAndSampleNames(path,muon).items():
			if genMass:
				if "CI" in filePath or "ADD" in filePath or "2018" in filePath or "2016" in filePath: continue
				filePath = filePath.replace("dileptonAna_muons","dileptonAna_genMassOther")
				filePath = filePath.replace("dileptonAna_electrons","dileptonAna_genMassOther_electrons")
			rootFile = TFile(filePath, "read")
			result[sampleName] = rootFile.FindObjectAny("Events").GetBinContent(1)				
	return result
	
def negWeightFractions(path,muon=True,genMass=False):
	"""
	path: path to directory containing all sample files

	returns dict samples names -> fraction of events wiBackgrounds2016th negative weights in source sample
	"""
	from ROOT import TFile
	result = {}

	for sampleName, filePath in getFilePathsAndSampleNames(path,muon).items():
			if genMass:
				if "CI" in filePath or "ADD" in filePath or "2018" in filePath or "2016" in filePath: continue
				
				filePath = filePath.replace("dileptonAna_muons","dileptonAna_genMassOther")
				filePath = filePath.replace("dileptonAna_electrons","dileptonAna_genMassOther_electrons")		
			rootFile = TFile(filePath, "read")
			result[sampleName] = rootFile.FindObjectAny("weights").GetBinContent(1)/(rootFile.FindObjectAny("weights").GetBinContent(1)+rootFile.FindObjectAny("weights").GetBinContent(2))				
	return result


def binning(channel='muon'):
	if channel == 'muon':
		
		return [60., 65.43046396, 71.3524269, 77.81037328, 84.85281374, 92.53264952,  100.90756983,  110.04048518,  120., 129.95474058, 140.73528833, 152.41014904, 165.0535115, 178.74571891, 193.57377942, 209.63191906,  227.02218049,  245.85507143,  266.2502669,   288.3373697, 
		312.25673399,  338.16035716,  366.21284574,  396.59246138,  429.49225362, 465.12128666,  503.70596789,  545.49148654,  590.74337185,  639.74918031, 692.82032303,  750.29404456,  812.53556599,  879.94040575,  952.93689296, 
		1031.98888927, 1117.59873655, 1210.310449,   1310.71317017, 1419.4449167,
		1537.19663264, 1664.71658012, 1802.81509423, 1952.36973236, 2114.3308507, 2289.72764334, 2479.6746824,  2685.37900061, 2908.14776151, 3149.39656595, 3410.65844758, 3693.59361467, 4000.,4500,5200,6000,7000,8000]
	if channel == 'electron':
		# ~ return ([j for j in range(50, 120, 5)] +
				# ~ [j for j in range(120, 150, 5)] +
				# ~ [j for j in range(150, 200, 10)] +
				# ~ [j for j in range(200, 600, 20)]+
				# ~ [j for j in range(600, 900, 30) ]+
				# ~ [j for j in range(900, 1250, 50)] +
				# ~ [j for j in range(1250, 1600, 60) ] +
				# ~ [j for j in range(1600, 1900, 70) ] +
				# ~ [j for j in range(1900, 4000, 80) ] +
				# ~ [j for j in range(4000, 5000, 100) ] +
				# ~ [5000])
		return ([j for j in range(50, 120, 5)] +
				[j for j in range(120, 150, 5)] +
				[j for j in range(150, 200, 10)] +
				[j for j in range(200, 600, 20)]+
				[j for j in range(600, 900, 30) ]+
				[j for j in range(900, 1250, 50)] +
				[j for j in range(1250, 1610, 60) ] +
				[j for j in range(1610, 1890, 70) ] +
				[j for j in range(1890, 3970, 80) ] +
				[j for j in range(3970, 6070, 100) ] +
				[6070])
	# Calculate logarithmic bins
	# ~ width = (math.log(m_max) - math.log(m_min)) / nbins
	# ~ logbins = []	# ~ # Exceed m_max to start with Z' binning, but reach 5 TeV
	# ~ for i in range(0, nbins + 8):
		# ~ logbins.append(int(math.exp(math.log(m_min) + width * i)))

	# ~ return logbins
	
def loadHistoFromFile(fileName,histName,rebin,muon=True,logBins=False,genMass=False,CIBins=False):
	"""
	returns histogram from file
	"""
	
	if "2016" in fileName and "Our2018" in histName:
		histName = histName.replace("2018","2016")
	if "2016" in fileName and "Our2017" in histName:
		histName = histName.replace("2017","2016")
	if "2018" in fileName and "Our2017" in histName:
		histName = histName.replace("2017","2018")
		
	if genMass:
		histName = "genMass/GenMass"
		fileName = fileName.replace("dileptonAna_muons","dileptonAna_genMassOther")
		fileName = fileName.replace("dileptonAna_electrons","dileptonAna_genMassOther_electrons")
		
	from ROOT import TFile, TH1F
	rootFile = TFile(path+fileName, "read")
	if "saved_hist_for_combine" in fileName or "jets_muons" in fileName or "hist_jets" in fileName or 'Result_' in fileName or "combined_jet" in fileName:
		if muon:
			if 	"combined_jet" in fileName:
				if "be" in histName:
					if "2018" in fileName:
						actualRootFile = TFile(path+"combined_jet_log_BE_2018_binWidth.root", "read")
					else:	
						actualRootFile = TFile(path+"combined_jet_log_BE_binWidth.root", "read")
					tmpResult = actualRootFile.Get("DATA_mass_log_BE")
				elif "bb" in histName:
					tmpResult = rootFile.Get("DATA_mass_log_BB")
				else:
					if "2018" in fileName:
						actualRootFile = TFile(path+"combined_jet_log_inclusive_2018_binWidth.root", "read")
					else:	
						actualRootFile = TFile(path+"combined_jet_log_inclusive_binWidth.root", "read")
					tmpResult = actualRootFile.Get("DATA_mass_log_BB")
				if "2018" in fileName:
					tmpResult.Scale(0.5885366095313584)
				else:	
					tmpResult.Scale(0.4114633904686416)
				bng = binning("muon")

				tmpResult2 = TH1F("intermediate","intermediate",len(bng) - 1, array('d', bng))
				for i in range(0,tmpResult.GetNbinsX()):
					tmpResult2.SetBinContent(i,tmpResult.GetBinContent(i))
				tmpResult = tmpResult2	
			else:		
				if "be" in histName:
					tmpResult = rootFile.Get("jetsBE")
				elif "bb" in histName:
					tmpResult = rootFile.Get("jetsBB")
				else:
					tmpResult = rootFile.Get("jets")
				
				# ~ bng = binning("muon")
				# ~ tmpResult2 = TH1F("intermediate","intermediate",len(bng) - 1, array('d', bng))
				# ~ for i in range(0,tmpResult.GetNbinsX()):
					# ~ tmpResult2.SetBinContent(i,tmpResult.GetBinContent(i))
				# ~ tmpResult = tmpResult2						
		else:
			if fileName == "hist_jets.root":
				if "bbbe" in histName:
					tmpResult = rootFile.Get("h_mee_all")
				elif "bb" in histName:
					tmpResult = rootFile.Get("h_mee_all_BB")
				else:
					tmpResult = rootFile.Get("h_mee_all_BE")
			else:
				if "bbbe" in histName:
					tmpResult = rootFile.Get("jets_h_mee_all")
				elif "bb" in histName:
					tmpResult = rootFile.Get("jets_h_mee_all_BB")
				else:
					tmpResult = rootFile.Get("jets_h_mee_all_BE")
				# ~ for i in range(0,tmpResult.GetNbinsX()):
					# ~ tmpResult.SetBinContent(i,tmpResult.GetBinContent(i)*tmpResult.GetBinWidth(i))
					# ~ tmpResult.SetBinError(i,tmpResult.GetBinError(i)*tmpResult.GetBinWidth(i))
		result = tmpResult.Clone("jets")
		if '_CSPos' in histName or '_CSNeg' in histName:
			result.Scale(0.5)
		
	else:	
		if '2016' in fileName and 'muon' in fileName:
			histName2 = histName.replace('Our2017','Our2016')
			result = rootFile.Get(histName2)
		else:	
			result = rootFile.Get(histName)

	print (fileName)		
	if logBins and not CIBins:
		if ( "Mass" in histName and not ("saved_hist_for_combine" in fileName or "hist_jets" in fileName or "Result_" in fileName or "combined_jet" in fileName)):
			if not muon:
				bng = binning("electron")
			else:
				bng = binning("muon")

			# ~ result = result.Rebin(len(bng) - 1, 'hist_' + uuid.uuid4().hex, array('d', bng))
			
			for i in range(0,result.GetNbinsX()):
				result.SetBinContent(i,result.GetBinContent(i)/result.GetBinWidth(i))
				result.SetBinError(i,result.GetBinError(i)/result.GetBinWidth(i))
			result.SetBinContent(result.GetNbinsX()+1,0)
	elif CIBins:
		if ( "Mass" in histName ):
			if not muon:
				bng = [400,500,700,1100,1900,3500,6000,6500,7000,10000]
			else:
				bng = [400,500,700,1100,1900,3500,6000,6500,7000,10000]

			if ("saved_hist_for_combine" in fileName or "hist_jets" in fileName or "Result_" in fileName or "combined_jet" in fileName):
				for i in range(0,result.GetNbinsX()):
					result.SetBinContent(i,result.GetBinContent(i)*result.GetBinWidth(i))
					result.SetBinError(i,result.GetBinError(i)*result.GetBinWidth(i))
					
			result = result.Rebin(len(bng) - 1, 'hist_' + uuid.uuid4().hex, array('d', bng))
			
			for i in range(0,result.GetNbinsX()):
				result.SetBinContent(i,result.GetBinContent(i)/result.GetBinWidth(i))
				result.SetBinError(i,result.GetBinError(i)/result.GetBinWidth(i))
			result.SetBinContent(result.GetNbinsX()+1,0)
	else:
		if not ("saved_hist_for_combine" in fileName or "hist_jets" in fileName or "Result_" in fileName or "combined_jet" in fileName):
			result.Rebin(rebin)

	result.SetDirectory(0)
	return deepcopy(result)
	
def loadHistoFromFile2D(fileName,histName,rebin):
	"""
	returns histogram from file
	"""
	from ROOT import TFile, TH2F
	rootFile = TFile(path+fileName, "read")
	result = rootFile.Get(histName)
	result.SetDirectory(0)	
	return deepcopy(result)

def loadHistoFromFileProjected(fileName,histName,rebin,binLow,binHigh=-1):
	"""
	returns histogram from file
	"""
	from random import randint
	from sys import maxsize
	name = "%x"%(randint(0, maxsize))	
	from ROOT import TFile, TH2F
	rootFile = TFile(path+fileName, "read")
	result = rootFile.Get(histName)
	if binHigh == -1:	
		result = result.ProjectionY(name,int(binLow/100),binHigh)
	else:	
		result = result.ProjectionY(name,result.GetXaxis().FindBin(binLow),result.GetXaxis().FindBin(binHigh-0.001))
	result.Rebin(rebin)
	result.SetDirectory(0)	

	return result




def getFilePathsAndSampleNames(path,muon=True):
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
		
		if muon:
			if "dileptonAna_muons" in filePath and not "SingleMuon" in filePath:
				sampleName = filePath.split("/")[-1].split("dileptonAna_muons_")[-1].split(".root")[0]
				if "2016_" in sampleName:
					if "CI" in sampleName:
						sampleName = sampleName.replace("2016_","")
					elif "ADD" in sampleName:
						sampleName = sampleName.replace("2016_", "")
						sampleName = sampleName.replace("LambdaT", "Lam")
					else:	
						sampleName = sampleName.replace("2016_","")+"_2016"
				if "2018_" in sampleName:
					if "CI" in sampleName:
						sampleName = sampleName.replace("2018_","") + "_2018"
					elif "ADD" in sampleName:
						sampleName = sampleName.replace("2018_", "")
						sampleName = sampleName.replace("LambdaT", "Lam")
					else:	
						sampleName = sampleName.replace("2018_","")+"_2018"
				result[sampleName] = filePath
		else:
			if "dileptonAna_electrons" in filePath and not "DoubleElectron" in filePath:
				sampleName = filePath.split("/")[-1].split("dileptonAna_electrons_")[-1].split(".root")[0]
				if "2016_" in sampleName:
					if "CI" in sampleName:
						sampleName = sampleName.replace("2016_","")
					elif "ADD" in sampleName:
                                                sampleName = sampleName.replace("2016_", "")
                                                sampleName = sampleName.replace("LambdaT", "Lam")
					else:	
						sampleName = sampleName.replace("2016_","")+"_2016"
				if "2018_" in sampleName:
					if "CI" in sampleName:
						sampleName = sampleName.replace("2018_","") + '_2018'
					elif "ADD" in sampleName:
                                                sampleName = sampleName.replace("2018_", "")
                                                sampleName = sampleName.replace("LambdaT", "Lam")
					else:	
						sampleName = sampleName.replace("2018_","")+"_2018"
				result[sampleName] = filePath
				
	return result


def getHistoFromTree(tree,plot,nEvents = -1):

	from ROOT import TH1F
	from random import randint
	from sys import maxint
	if nEvents < 0:
		nEvents = maxint
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
	xsecs = []
	nEvents = []
	negWeightFraction = []
	
		
	
	def __init__(self, process,Counts={"none":-1},negWeights={"none":-1}, normalized = False):
		self.samples = process.subprocesses
		self.label = process.label
		self.theColor = process.fillcolor
		self.theLineColor = process.linecolor
		self.normalized = normalized
		self.xsecs = []
		self.negWeightFraction = []
		self.nEvents = []
		for sample in self.samples:
			if not "Data" in sample and not "Jets" in sample:
				if "ConRL" in sample or "DesRL" in sample:
					self.xsecs.append(crossSections[sample.replace('RL',"LR")])
				else:	
					self.xsecs.append(crossSections[sample])
				self.negWeightFraction.append(negWeights[sample])
				self.nEvents.append(Counts[sample])	
	def loadHistogram(self,plot,lumi,zScaleFac,genMass=False,CIBins=False):
		histo = None
		if plot.plot2D:
			for index, sample in enumerate(self.samples):
				
				if plot.muon:
					tempHist = loadHistoFromFile2D(fileNames[sample],plot.histName,plot.rebin)
				else:	
					tempHist = loadHistoFromFile2D(fileNamesEle[sample],plot.histName,plot.rebin)
				if not self.normalized:
					tempHist.Scale(lumi*self.xsecs[index]/self.nEvents[index]*(1-2*self.negWeightFraction[index])*zScaleFac)
				if histo == None:
					histo = tempHist.Clone()
				else:	
					histo.Add(tempHist.Clone())
			histo.SetFillColor(self.theColor)
			histo.SetLineColor(self.theLineColor)
			histo.GetXaxis().SetTitle(plot.xaxis) 
			histo.GetYaxis().SetTitle(plot.yaxis)	
		else:
			for index, sample in enumerate(self.samples):
				if plot.muon:
					tempHist = loadHistoFromFile(fileNames[sample],plot.histName,plot.rebin,plot.muon,plot.logX,genMass=genMass,CIBins=CIBins)
				else:	
					tempHist = loadHistoFromFile(fileNamesEle[sample],plot.histName,plot.rebin,plot.muon,plot.logX,genMass=genMass,CIBins=CIBins)
				if not self.normalized:
					if plot.muon:
						tempHist.Scale(lumi*self.xsecs[index]/self.nEvents[index]*(1-2*self.negWeightFraction[index])*zScaleFac)
					else:	
						tempHist.Scale(lumi*self.xsecs[index]/self.nEvents[index]*(1-2*self.negWeightFraction[index])*zScaleFac)
						
				if histo == None:
					histo = tempHist.Clone()
				else:
					histo.Add(tempHist.Clone())
			histo.SetFillColor(self.theColor)
			histo.SetLineColor(self.theLineColor)
			histo.GetXaxis().SetTitle(plot.xaxis) 
			histo.GetYaxis().SetTitle(plot.yaxis)	
				
		return histo
	def loadHistogramProjected(self,plot,lumi,zScaleFac):
		histo = None
		for index, sample in enumerate(self.samples):
			if plot.muon:
				tempHist = loadHistoFromFileProjected(fileNames[sample],plot.histName,plot.rebin,plot.projLow,plot.projHigh)
			else:
				tempHist = loadHistoFromFileProjected(fileNamesEle[sample],plot.histName,plot.rebin,plot.projLow,plot.projHigh)
				
			if len(self.xsecs) > 0:
				tempHist.Scale(lumi*self.xsecs[index]/self.nEvents[index]*(1-2*self.negWeightFraction[index])*zScaleFac)
			if histo == None:
				histo = tempHist.Clone()
			else:	
				histo.Add(tempHist.Clone())
		histo.SetFillColor(self.theColor)
		histo.SetLineColor(self.theLineColor)
		histo.GetXaxis().SetTitle(plot.xaxis) 
		histo.GetYaxis().SetTitle(plot.yaxis)	
		return histo


def makeHistoCumulative(histo):
	from ROOT import Double
	err = Double()
	for i in range(0,histo.GetNbinsX()):
		histo.SetBinContent(i+1,histo.IntegralAndError(i+1, histo.GetNbinsX()+1, err))
		histo.SetBinError(i+1,err)

	return histo
	
class TheStack:
	from ROOT import THStack
	theStack = THStack()	
	theHistogram = None	
	def  __init__(self,processes,lumi,plot,zScaleFac,genMass=False,CIBins=False,cumulative=False):
		self.theStack = THStack()
			
		for process in processes:
			temphist = process.loadHistogram(plot,lumi,zScaleFac,genMass=genMass,CIBins=CIBins)
			if cumulative:
				temphist = makeHistoCumulative(temphist)
			self.theStack.Add(temphist.Clone())
			if self.theHistogram == None:
				self.theHistogram = temphist.Clone()
			else:	
				self.theHistogram.Add(temphist.Clone())
	def Add(self,addstack):
		for h in addstack.theStack.GetHists():
			self.theStack.Add(h.Clone())
			self.theHistogram.Add(h.Clone())
							
class TheStackRun2:
	from ROOT import THStack
	theStack = THStack()	
	theHistogram = None	
	def  __init__(self,processes,lumi,plot,zScaleFac,CIBins=False,cumulative=False):
		self.theStack = THStack()
	
		for index, process in enumerate(processes[0]):
			temphist = process.loadHistogram(plot,lumi[0],zScaleFac[0],CIBins=CIBins)
			temphist.Add(processes[1][index].loadHistogram(plot,lumi[1],zScaleFac[1],CIBins=CIBins))
			temphist.Add(processes[2][index].loadHistogram(plot,lumi[2],zScaleFac[2],CIBins=CIBins))
			if cumulative:
				temphist = makeHistoCumulative(temphist)
			self.theStack.Add(temphist.Clone())
			if self.theHistogram == None:
				self.theHistogram = temphist.Clone()
			else:	
				self.theHistogram.Add(temphist.Clone())
				
class TheStack2D:
	from ROOT import THStack
	theStack = THStack()	
	theHistogram = None	
	def  __init__(self,processes,lumi,plot,zScale):
		self.theStack = THStack()
			
		for process in processes:
			temphist = process.loadHistogramProjected(plot,lumi,zScale)

			self.theStack.Add(temphist.Clone())
			if self.theHistogram == None:
				self.theHistogram = temphist.Clone()
			else:	
				self.theHistogram.Add(temphist.Clone())
class TheStack2DRun2:
	from ROOT import THStack
	theStack = THStack()	
	theHistogram = None	
	def  __init__(self,processes,lumi,plot,zScale,CIBins=False):
		self.theStack = THStack()
			
		for index, process in enumerate(processes[0]):
			temphist = process.loadHistogramProjected(plot,lumi[0],zScale[0])
			temphist.Add(processes[1][index].loadHistogramProjected(plot,lumi[1],zScale[1]))
			temphist.Add(processes[2][index].loadHistogramProjected(plot,lumi[2],zScale[2]))

			self.theStack.Add(temphist.Clone())
			if self.theHistogram == None:
				self.theHistogram = temphist.Clone()
			else:	
				self.theHistogram.Add(temphist.Clone())

def getDataHist(plot,files,fromTree=False,CIBins=False,cumulative=False):
	if not fromTree:
		histo = loadHistoFromFile(files["data"], plot.histName,plot.rebin,plot.muon,CIBins=CIBins)
	else:
		histo = getHistoFromTree(files["data"], plot)
	if cumulative:
		histo = makeHistoCumulative(histo)	
	return histo	
	
def getDataHist2D(plot,files,binLow,binHigh,fromTree=False):
	if not fromTree:
		histo = loadHistoFromFileProjected(files["data"], plot.histName,plot.rebin,binLow,binHigh)
	else:
		histo = getHistoFromTree(files["data"], plot)
	return histo	




