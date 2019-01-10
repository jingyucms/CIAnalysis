from ROOT import gROOT, TFile
from numpy import array as ar
from array import array
from copy import deepcopy
import pickle



def main():
	gROOT.SetBatch(True)

	
	histos = ["BB","BE"]
	labels = ["dielectron_2016","dimuon_2016","dimuon_2017","dielectron_2017","dimuon_2018","dielectron_2018"]
	suffixesMu = ["nominal","scaledown","smeared","muonid"]
	suffixesEle = ["nominal","scaledown","scaleup","pileup","piledown"]
	css = ["inc","cspos","csneg"]
	lambdas = [10,16,22,28,34,40,46]
	interferences = ["Con","Des"]
	hels = ["LL","LR","RR"]

	massBins = [400,500,700,1100,1900,3500]
	signalYields = {}
	
	
	for label in labels:
		if "dimuon" in label:
			suffixes = suffixesMu
		else:
			suffixes = suffixesEle
		for suffix in suffixes:
			for cs in css:
				for histo in histos:
					for hel in hels:
						for interference in interferences:			
							model = interference+hel
							if "dimuon" in label:
								name = "cito2mu"
							else:			#~ print signalYields

								name = "cito2e"	
							if "2016" in label:
								fitFile = TFile("%s_%s_%s_%s_parametrization_fixdes_fixinf_limitp0_limitp1_limitp2_2016.root"%(name,suffix,histo.lower(),cs),"READ")
							else:	
								fitFile = TFile("%s_%s_%s_%s_parametrization_fixdes_fixinf_limitp0_limitp1_limitp2.root"%(name,suffix,histo.lower(),cs),"READ")
							for l in lambdas:
								if "dimuon" in label:
									name = "CITo2Mu_Lam%dTeV%s"%(l,model)
								else:	
									name = "CITo2E_Lam%dTeV%s"%(l,model)
								if not cs == "inc":
									name += "_%s"%cs
								signalYields["%s_%s_%s"%(name,label,histo)] = {}
								for index, massBin in enumerate(massBins):
									function = fitFile.Get("fn_m%d_%s"%(massBin,model))
									fitR = fitFile.Get("fitR_m%d_%s"%(massBin,model))
									pars = fitR.GetParams()
									errs = fitR.Errors()
									function.SetParameter(0,pars[0])
									function.SetParameter(1,pars[1])
									function.SetParameter(2,pars[2])
									function.SetParError(0,errs[0])
									function.SetParError(1,errs[1])
									function.SetParError(2,errs[2])
									functionUnc = fitFile.Get("fn_unc_m%d_%s"%(massBin,model))
									uncert = (abs((functionUnc.Eval(l)/function.Eval(l))**2 + (functionUnc.Eval(100000)/function.Eval(100000))))**0.5	
									signalYields["%s_%s_%s"%(name,label,histo)][str(index)] = [(function.Eval(l)-function.Eval(100000)),uncert]

						for l in lambdas:			
							if "dimuon" in label:
								name = "CITo2Mu_Lam%dTeV%s"%(l,hel)
								nameCon = "CITo2Mu_Lam%dTeV%s"%(l,"Con"+hel)
								nameDes = "CITo2Mu_Lam%dTeV%s"%(l,"Des"+hel)
							else:	
								name = "CITo2E_Lam%dTeV%s"%(l,hel)
								nameCon = "CITo2E_Lam%dTeV%s"%(l,"Con"+hel)
								nameDes = "CITo2E_Lam%dTeV%s"%(l,"Des"+hel)
							signalYields["%s_%s_%s"%(name,label,histo)] = {}	
							for index, massBin in enumerate(massBins):
								signalYields["%s_%s_%s"%(name,label,histo)][str(index)] = [(signalYields["%s_%s_%s"%(nameCon,label,histo)][str(index)][0] + signalYields["%s_%s_%s"%(nameDes,label,histo)][str(index)][0])/2,((signalYields["%s_%s_%s"%(nameCon,label,histo)][str(index)][1]**2 + signalYields["%s_%s_%s"%(nameDes,label,histo)][str(index)][1]**2))**0.5]
					


			if "dimuon" in label:
				fileName = "signalYields"
			else:
				fileName = "signalYieldsEle"
			
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
			outFilePkl = open("%s_%s.pkl"%(fileName,otherSuffix),"wb")
			pickle.dump(signalYields, outFilePkl, protocol=2)
			outFilePkl.close()		
	
	
			
							
main()
