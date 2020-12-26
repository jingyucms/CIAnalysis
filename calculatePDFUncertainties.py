from ROOT import kBlack, kBlue, kRed, kOrange, TCanvas, gStyle, TPad, TLegend, TH1F, TGraph, TFile
import ROOT
from array import array
from setTDRStyle import setTDRStyle
from array import array
from copy import deepcopy
import lhapdf

def CalculateLHAPDFWeight(pdf, Q, x1, x2, f1, f2):
	return pdf.xfxQ(f1, x1, Q) * pdf.xfxQ(f2, x2, Q)

xsecs = {
"CITo2Mu_Lam100kTeVConLL_M1300to2000" : 0.001605,
"CITo2Mu_Lam100kTeVConLR_M1300to2000" : 0.001602,
"CITo2Mu_Lam100kTeVConRR_M1300to2000" : 0.001603,
"CITo2Mu_Lam100kTeVDesLL_M1300to2000" : 0.001599,
"CITo2Mu_Lam100kTeVDesLR_M1300to2000" : 0.001593,
"CITo2Mu_Lam100kTeVDesRR_M1300to2000" : 0.001603,
"CITo2Mu_Lam16TeVConLL_M1300to2000" : 0.003378,
"CITo2Mu_Lam16TeVConLR_M1300to2000" : 0.004508,
"CITo2Mu_Lam16TeVConRR_M1300to2000" : 0.003386,
"CITo2Mu_Lam16TeVDesLL_M1300to2000" : 0.001968,
"CITo2Mu_Lam16TeVDesLR_M1300to2000" : 0.003012,
"CITo2Mu_Lam16TeVDesRR_M1300to2000" : 0.001976,
"CITo2Mu_Lam24TeVConLL_M1300to2000" : 0.002126,
"CITo2Mu_Lam24TeVConLR_M1300to2000" : 0.002351,
"CITo2Mu_Lam24TeVConRR_M1300to2000" : 0.002124,
"CITo2Mu_Lam24TeVDesLL_M1300to2000" : 0.001497,
"CITo2Mu_Lam24TeVDesLR_M1300to2000" : 0.001698,
"CITo2Mu_Lam24TeVDesRR_M1300to2000" : 0.001504,
"CITo2Mu_Lam32TeVConLL_M1300to2000" : 0.001845,
"CITo2Mu_Lam32TeVConLR_M1300to2000" : 0.001922,
"CITo2Mu_Lam32TeVConRR_M1300to2000" : 0.001844,
"CITo2Mu_Lam32TeVDesLL_M1300to2000" : 0.001499,
"CITo2Mu_Lam32TeVDesLR_M1300to2000" : 0.001554,
"CITo2Mu_Lam32TeVDesRR_M1300to2000" : 0.001494,
"CITo2Mu_Lam40TeVConLL_M1300to2000" : 0.001740,
"CITo2Mu_Lam40TeVConLR_M1300to2000" : 0.001768,
"CITo2Mu_Lam40TeVConRR_M1300to2000" : 0.001738,
"CITo2Mu_Lam40TeVDesLL_M1300to2000" : 0.001522,
"CITo2Mu_Lam40TeVDesLR_M1300to2000" : 0.001538,
"CITo2Mu_Lam40TeVDesRR_M1300to2000" : 0.001515,
"CITo2Mu_Lam100kTeVConLL_M2000toInf" : 0.000169,
"CITo2Mu_Lam100kTeVConLR_M2000toInf" : 0.000170,
"CITo2Mu_Lam100kTeVConRR_M2000toInf" : 0.000169,
"CITo2Mu_Lam100kTeVDesLL_M2000toInf" : 0.000170,
"CITo2Mu_Lam100kTeVDesLR_M2000toInf" : 0.000169,
"CITo2Mu_Lam100kTeVDesRR_M2000toInf" : 0.000170,
"CITo2Mu_Lam16TeVConLL_M2000toInf" : 0.001072,
"CITo2Mu_Lam16TeVConLR_M2000toInf" : 0.001774,
"CITo2Mu_Lam16TeVConRR_M2000toInf" : 0.001062,
"CITo2Mu_Lam16TeVDesLL_M2000toInf" : 0.000675,
"CITo2Mu_Lam16TeVDesLR_M2000toInf" : 0.001383,
"CITo2Mu_Lam16TeVDesRR_M2000toInf" : 0.000680,
"CITo2Mu_Lam24TeVConLL_M2000toInf" : 0.000398,
"CITo2Mu_Lam24TeVConLR_M2000toInf" : 0.000533,
"CITo2Mu_Lam24TeVConRR_M2000toInf" : 0.000390,
"CITo2Mu_Lam24TeVDesLL_M2000toInf" : 0.000218,
"CITo2Mu_Lam24TeVDesLR_M2000toInf" : 0.000361,
"CITo2Mu_Lam24TeVDesRR_M2000toInf" : 0.000224,
"CITo2Mu_Lam32TeVConLL_M2000toInf" : 0.000262,
"CITo2Mu_Lam32TeVConLR_M2000toInf" : 0.000306,
"CITo2Mu_Lam32TeVConRR_M2000toInf" : 0.000261,
"CITo2Mu_Lam32TeVDesLL_M2000toInf" : 0.000163,
"CITo2Mu_Lam32TeVDesLR_M2000toInf" : 0.000208,
"CITo2Mu_Lam32TeVDesRR_M2000toInf" : 0.000165,
"CITo2Mu_Lam40TeVConLL_M2000toInf" : 0.000218,
"CITo2Mu_Lam40TeVConLR_M2000toInf" : 0.000236,
"CITo2Mu_Lam40TeVConRR_M2000toInf" : 0.000217,
"CITo2Mu_Lam40TeVDesLL_M2000toInf" : 0.000155,
"CITo2Mu_Lam40TeVDesLR_M2000toInf" : 0.000174,
"CITo2Mu_Lam40TeVDesRR_M2000toInf" : 0.000156,
"CITo2Mu_Lam100kTeVConLL_M300to800" : 0.637000,
"CITo2Mu_Lam100kTeVConLR_M300to800" : 0.636400,
"CITo2Mu_Lam100kTeVConRR_M300to800" : 0.636900,
"CITo2Mu_Lam100kTeVDesLL_M300to800" : 0.633900,
"CITo2Mu_Lam100kTeVDesLR_M300to800" : 0.637000,
"CITo2Mu_Lam100kTeVDesRR_M300to800" : 0.639400,
"CITo2Mu_Lam16TeVConLL_M300to800" : 0.656100,
"CITo2Mu_Lam16TeVConLR_M300to800" : 0.657500,
"CITo2Mu_Lam16TeVConRR_M300to800" : 0.655300,
"CITo2Mu_Lam16TeVDesLL_M300to800" : 0.626900,
"CITo2Mu_Lam16TeVDesLR_M300to800" : 0.622500,
"CITo2Mu_Lam16TeVDesRR_M300to800" : 0.620600,
"CITo2Mu_Lam24TeVConLL_M300to800" : 0.642400,
"CITo2Mu_Lam24TeVConLR_M300to800" : 0.645800,
"CITo2Mu_Lam24TeVConRR_M300to800" : 0.645600,
"CITo2Mu_Lam24TeVDesLL_M300to800" : 0.630000,
"CITo2Mu_Lam24TeVDesLR_M300to800" : 0.628400,
"CITo2Mu_Lam24TeVDesRR_M300to800" : 0.628300,
"CITo2Mu_Lam32TeVConLL_M300to800" : 0.639300,
"CITo2Mu_Lam32TeVConLR_M300to800" : 0.641300,
"CITo2Mu_Lam32TeVConRR_M300to800" : 0.638800,
"CITo2Mu_Lam32TeVDesLL_M300to800" : 0.631200,
"CITo2Mu_Lam32TeVDesLR_M300to800" : 0.631000,
"CITo2Mu_Lam32TeVDesRR_M300to800" : 0.630700,
"CITo2Mu_Lam40TeVConLL_M300to800" : 0.639700,
"CITo2Mu_Lam40TeVConLR_M300to800" : 0.636500,
"CITo2Mu_Lam40TeVDesLL_M300to800" : 0.633500,
"CITo2Mu_Lam40TeVDesLR_M300to800" : 0.632900,
"CITo2Mu_Lam40TeVDesRR_M300to800" : 0.631700,
"CITo2Mu_Lam100kTeVConLR_M800to1300" : 0.014090,
"CITo2Mu_Lam100kTeVConRR_M800to1300" : 0.01400,
"CITo2Mu_Lam100kTeVDesLL_M800to1300" : 0.014130,
"CITo2Mu_Lam100kTeVDesLR_M800to1300" : 0.014100,
"CITo2Mu_Lam100kTeVDesRR_M800to1300" : 0.014100,
"CITo2Mu_Lam16TeVConLL_M800to1300" : 0.017830,
"CITo2Mu_Lam16TeVConLR_M800to1300" : 0.019920,
"CITo2Mu_Lam16TeVConRR_M800to1300" : 0.018050,
"CITo2Mu_Lam16TeVDesLL_M800to1300" : 0.013410,
"CITo2Mu_Lam16TeVDesLR_M800to1300" : 0.014610,
"CITo2Mu_Lam16TeVDesRR_M800to1300" : 0.014610,
"CITo2Mu_Lam24TeVConLL_M800to1300" : 0.014610,
"CITo2Mu_Lam24TeVConLR_M800to1300" : 0.015840,
"CITo2Mu_Lam24TeVConRR_M800to1300" : 0.015480,
"CITo2Mu_Lam24TeVDesLL_M800to1300" : 0.013470,
"CITo2Mu_Lam24TeVDesLR_M800to1300" : 0.013600,
"CITo2Mu_Lam24TeVDesRR_M800to1300" : 0.013420,
"CITo2Mu_Lam32TeVConLL_M800to1300" : 0.014810,
"CITo2Mu_Lam32TeVConLR_M800to1300" : 0.014930,
"CITo2Mu_Lam32TeVConRR_M800to1300" : 0.014750,
"CITo2Mu_Lam32TeVDesLL_M800to1300" : 0.013670,
"CITo2Mu_Lam32TeVDesLR_M800to1300" : 0.013630,
"CITo2Mu_Lam32TeVDesRR_M800to1300" : 0.013650,
"CITo2Mu_Lam40TeVConLL_M800to1300" : 0.014510,
"CITo2Mu_Lam40TeVConLR_M800to1300" : 0.014520,
"CITo2Mu_Lam40TeVConRR_M800to1300" : 0.014540,
"CITo2Mu_Lam40TeVDesLL_M800to1300" : 0.013790,
"CITo2Mu_Lam40TeVDesLR_M800to1300" : 0.013730,
"CITo2Mu_Lam40TeVDesRR_M800to1300" : 0.013750,

'2016_CITo2Mu_Lam16TeVDesRR_M300':0.550000,
'2016_CITo2Mu_Lam16TeVDesRR_M800':0.013670,
'2016_CITo2Mu_Lam16TeVDesRR_M1300':0.002403,
'2016_CITo2Mu_Lam16TeVConRR_M300':0.583500,
'2016_CITo2Mu_Lam16TeVConRR_M800':0.019120,
'2016_CITo2Mu_Lam16TeVConRR_M1300':0.003939,
}

pdfsetRef = lhapdf.getPDFSet("NNPDF31_nnlo_as_0118")
pdfset31LO = lhapdf.getPDFSet("NNPDF31_lo_as_0118")
pdfset31LO13 = lhapdf.getPDFSet("NNPDF31_lo_as_0130")
pdfset30NNLO = lhapdf.getPDFSet("NNPDF30_nnlo_as_0118")
pdfset30LO = lhapdf.getPDFSet("NNPDF30_lo_as_0118")
pdfset30LO13 = lhapdf.getPDFSet("NNPDF30_lo_as_0130")
pdfset23LO = lhapdf.getPDFSet("NNPDF23_lo_as_0130_qed")
# ~ print (pdfset.description)
pdfReplicasRef = pdfsetRef.mkPDFs()
pdfReplicas31LO = pdfset31LO.mkPDFs()
pdfReplicas31LO13 = pdfset31LO13.mkPDFs()
pdfReplicas30LO = pdfset30LO.mkPDFs()
pdfReplicas30LO13 = pdfset30LO13.mkPDFs()
pdfReplicas30NNLO = pdfset30NNLO.mkPDFs()
pdfReplicas23LO = pdfset23LO.mkPDFs()

def getWeight(pdfName, event, index, scale = 0, x1 = 0, x2 = 0, pdf1 = 0, pdf2 = 0):
	

	if pdfName == "NNPDF30":
		return event.pdfWeightsNNPDF30[index]
		
	if pdfName == "NNPDF30v2":
		return CalculateLHAPDFWeight(pdfReplicas30LO[index], scale, x1, x2, pdf1, pdf2)

	if pdfName == "NNPDF31":
		return event.pdfWeightsNNPDF31[index]

	if pdfName == "NNPDF23":
		return CalculateLHAPDFWeight(pdfReplicas23LO[index], scale, x1, x2, pdf1, pdf2)
		
	if pdfName == "NNPDF31v2":
		return CalculateLHAPDFWeight(pdfReplicasRef[index], scale, x1, x2, pdf1, pdf2)

	if pdfName == "NNPDF23v2":
		return event.pdfWeightsNNPDF23[index]


def main():


	pdfs = ["NNPDF23"]
	path = "files/"
	files = [path+"dileptonAna_pdf_CITo2Mu_Lam16TeVConLL_M300to800.root",path+"dileptonAna_pdf_CITo2Mu_Lam16TeVConLL_M800to1300.root",path+"dileptonAna_pdf_CITo2Mu_Lam16TeVConLL_M1300to2000.root",path+"dileptonAna_pdf_CITo2Mu_Lam16TeVConLL_M2000toInf.root"]


	for pdf in pdfs:

		canv = TCanvas("c1","c1",800,800)	
		plotPad = TPad("plotPad","plotPad",0,0,1,1)
		style = setTDRStyle()
		gStyle.SetOptStat(0)
		plotPad.UseCurrentStyle()
		plotPad.Draw()
		plotPad.cd()
		
		leg = TLegend(0.52, 0.71, 0.89, 0.92,"","brNDC")
		leg.SetFillColor(10)
		leg.SetFillStyle(0)
		leg.SetLineColor(10)
		leg.SetShadowColor(0)
		leg.SetBorderSize(1)	
			
		leg2 = TLegend(0.52, 0.71, 0.89, 0.92,"","brNDC")
		leg2.SetFillColor(10)
		leg2.SetFillStyle(0)
		leg2.SetLineColor(10)
		leg2.SetShadowColor(0)
		leg2.SetBorderSize(1)		


		
		binning = [400,500,700,1100,1900,3500,13000]
		hists = []
		for i in range(0,100):
			weightSums.append(0)
			hists.append(TH1F("hist_%s_%d"%(pdf,i),"hist_%s_%d"%(pdf,i),len(binning)-1,array('f',binning)))
		
		nnn = len(files)
		for index, fileName in enumerate(files):
			
			f = TFile(fileName,"OPEN")
			tree = f.Get("pdfTree")
			xsec = xsecs[fileName.split("dileptonAna_pdf_")[-1].split(".root")[0]]
			print ("processing sample %d / %d"%(index+1,nnn))
			sampleWeight = xsec/tree.GetEntries()
			for ev in tree:
				if ev.recoMass < 0: continue
				genMass = tree.GetLeaf("pdfInfo/scale").GetValue()
				central_value = getWeight(pdf, ev, 0, tree.GetLeaf("pdfInfo/scale").GetValue(), tree.GetLeaf("pdfInfo/x1").GetValue(), tree.GetLeaf("pdfInfo/x2").GetValue(), tree.GetLeaf("pdfInfo/pdf1").GetValue(), tree.GetLeaf("pdfInfo/pdf2").GetValue())
				hists[0].Fill(genMass,sampleWeight)
				for i in range(1,100):
					localValue = 1. # replace this with the PDF weight calculation for the individial replicaes
					if  localValue/central_value > 10 or localValue/central_value < 0.1 : continue 
					hists[i].Fill(genMass,1)#replace the 1 with the event weight that you obtain by first removing the central value PDF weight and then applying the PDF weight for this replica
		hists[0].SetMarkerColor(ROOT.kRed)			
		for i in range(0,100):
			if i == 0: hists[0].Draw()
			else: hists[i].Draw("samehist")
		hists[0].Draw("same")	
		hists[0].GetXaxis().SetTitle("generated mass [GeV]")	
		hists[0].GetYaxis().SetTitle("N Events")	
		leg2.AddEntry(hists[0],"central value","p")	
		leg2.AddEntry(hists[1],"variations","l")	
		leg2.Draw()
		ROOT.gPad.SetLogy()
		canv.Print("hists_%s.pdf"%pdf)			
			
		change = []
		
		for y in range(0,hists[0].GetNbinsX()):
				change.append([])
		for i in range(0,100):
			if i > 0:
				for y in range(1,hists[0].GetNbinsX()+1):
					change[y-1].append(1) # in this loop over all the mass bins, replace the 1 with the relative change between the nominal bin content and the one for the PDF replica

		plotPad = TPad("plotPad","plotPad",0,0,1,1)			
		plotPad.UseCurrentStyle()
		plotPad.Draw()
		plotPad.cd()
		plotPad.DrawFrame(400,0,5000,0.3,";generated mass [GeV];PDF Uncert")

		masses = []
		for i in range(0,len(binning)-1):
			masses.append((binning[i]+binning[i+1])/2)
		
		graph = TGraph()
		for i in range(0,len(masses)):
			uncert = 0 # Calculate the relative PDF uncertainty as the 1 sigma envelope of the relative differences
			graph.SetPoint(i,masses[i],uncert)

		
		graph.Draw("lp")
		graphNorm.SetMarkerColor(ROOT.kRed)
		graphNorm.SetLineColor(ROOT.kRed)

		func = ROOT.TF1("f1","pol4")
		graph.Fit("f1")
		leg.AddEntry(graph,"PDF uncertainty for %s"%pdf,"pl")

		canv.Print("pdfUncertainty_%s.pdf"%pdf)
	
main()
