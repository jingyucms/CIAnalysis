from ROOT import gROOT, TFile
from numpy import array as ar
from array import array
from copy import deepcopy
import pickle



def main():
	gROOT.SetBatch(True)

	
	histos = ["BB","BE"]
	#labels = ["dielectron_2016","dimuon_2016","dimuon_2017","dielectron_2017","dimuon_2018","dielectron_2018"]
	labels = ["dielectron_2016", "dimuon_2016"]
	suffixesMu = ["nominal","scaledown", "smeared","muonid"]
	suffixesEle = ["nominal","scaledown","scaleup","pileup","piledown"]
	css = ["inc","cspos","csneg"]
	lambdas = [3500+i*500 for i in range(12)]; lambdas.append(10000)
	interferences = [""]

	#massBins = [400,500,700,1100,1900,3500]
	massBins = [2000, 2200, 2600, 3000, 3400]
	signalYields = {}
	
	
	for label in labels:
		if "dimuon" in label:
			suffixes = suffixesMu
		else:
			suffixes = suffixesEle
		for suffix in suffixes:
			for cs in css:
				for histo in histos:
					for interference in interferences:			
						#model = "_"
						if "dimuon" in label:
							name = "addto2mu"
						else:			#~ print signalYields

							name = "addto2e"	
						if "2016" in label:
							fitFile = TFile("fitPlots/%s_%s_%s_%s_parametrization_fixinf_2016.root"%(name,suffix,histo.lower(),cs),"READ")
							print fitFile
						#elif "2018" in label:
						#	fitFile = TFile("%s_%s_%s_%s_parametrization_fixdes_fixinf_limitp0_limitp1_limitp2_2018.root"%(name,suffix,histo.lower(),cs),"READ")
						#else:	
						#	fitFile = TFile("%s_%s_%s_%s_parametrization_fixdes_fixinf_limitp0_limitp1_limitp2.root"%(name,suffix,histo.lower(),cs),"READ")
						for l in lambdas:
							if "dimuon" in label:
								name = "ADDGravTo2Mu_Lam%d"%l
							else:	
								name = "ADDGravTo2E_Lam%d"%l
							if not cs == "inc":
								name += "_%s"%cs
							signalYields["%s_%s_%s"%(name,label,histo)] = {}
							l = l * 0.001 # in fitFiles, the lvals = 3.5, 4.0, 4.5...
							for index, massBin in enumerate(massBins):
								#print l, massBin
								function = fitFile.Get("fn_m%d_"%(massBin))
								fitR = fitFile.Get("fitR_m%d_"%(massBin))
								#fitR.Print()
								pars = fitR.GetParams()
								errs = fitR.Errors()
								function.SetParameter(0,pars[0])
								function.SetParameter(1,pars[1])
								function.SetParameter(2,pars[2])
								function.SetParameter(3,pars[3])
								function.SetParError(0,errs[0])
								function.SetParError(1,errs[1])
								function.SetParError(2,errs[2])
								function.SetParError(3,errs[3])
								functionUnc = fitFile.Get("fn_unc_m%d_"%(massBin))
								uncert = (abs((functionUnc.Eval(l)/function.Eval(l))**2 + (functionUnc.Eval(100000)/function.Eval(100000))))**0.5	
								signalYields["%s_%s_%s"%(name,label,histo)][str(index)] = [(function.Eval(l)-function.Eval(100000)),uncert]

					'''for l in lambdas:			
						if "dimuon" in label:
							name = "ADDGravTo2Mu_Lam%d"%l
							#nameCon = "ADDGravTo2Mu_Lam%dTeV%s"%(l,"Con"+hel)
							#nameDes = "CITo2Mu_Lam%dTeV%s"%(l,"Des"+hel)
						else:	
							name = "ADDGravTo2E_Lam%d"%l
							#nameCon = "CITo2E_Lam%dTeV%s"%(l,"Con"+hel)
							#nameDes = "CITo2E_Lam%dTeV%s"%(l,"Des"+hel)
						signalYields["%s_%s_%s"%(name,label,histo)] = {}	
						for index, massBin in enumerate(massBins):
							signalYields["%s_%s_%s"%(name,label,histo)][str(index)] = [(signalYields["%s_%s_%s"%(nameCon,label,histo)][str(index)][0] + signalYields["%s_%s_%s"%(nameDes,label,histo)][str(index)][0])/2,((signalYields["%s_%s_%s"%(nameCon,label,histo)][str(index)][1]**2 + signalYields["%s_%s_%s"%(nameDes,label,histo)][str(index)][1]**2))**0.5]
					'''


			if "dimuon" in label:
				fileName = "ADDsignalYields"
			else:
				fileName = "ADDsignalYieldsEle"
			
			if suffix == "nominal":
				otherSuffix = "default"
			elif suffix == "scaledown":
				otherSuffix = "scaleDown"
			elif suffix == "scaleup":
				otherSuffix = "scaleUp"
			elif suffix == "smeared":
				otherSuffix = "resolution"
			elif suffix == "muonid":
				otherSuffix = "ID"
			elif suffix == "pileup":
				otherSuffix = "pileup"
			elif suffix == "piledown":
				otherSuffix = "piledown"
			else:
				print (suffix)
			outFilePkl = open("ADDpkl/%s_%s.pkl"%(fileName,otherSuffix),"wb")
			pickle.dump(signalYields, outFilePkl, protocol=2)
			outFilePkl.close()		
	
	
			
							
main()
