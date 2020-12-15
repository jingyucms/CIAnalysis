from ROOT import TFile

from setTDRStyle import setTDRStyle

dyFile = TFile("drellyan.root","OPEN")	
dyHist = dyFile.Get("h1_dimuo_m")
dyHistPDF = dyFile.Get("h1_dimuo_m_pdf_total")


otherFile = TFile("other.root","OPEN")	
otherHist = otherFile.Get("h1_dimuo_m")
otherHistPDF = otherFile.Get("h1_dimuo_m_pdf_total")

from setTDRStyle import setTDRStyle

xMin = 1000
xMax = 60000

defaultDY =  dyHist.Integral(dyHist.FindBin(xMin),dyHist.FindBin(xMax-0.01))
pdfDY     =  dyHistPDF.Integral(dyHistPDF.FindBin(xMin),dyHistPDF.FindBin(xMax-0.01))

defaultOther =  otherHist.Integral(otherHist.FindBin(xMin),otherHist.FindBin(xMax-0.01))
pdfOther     =  otherHistPDF.Integral(otherHistPDF.FindBin(xMin),otherHistPDF.FindBin(xMax-0.01))

print ("DY PDF: ", abs(1 - (pdfDY)/(defaultDY)))
print ("Other PDF: ", abs(1 - (pdfOther)/(defaultOther)))

xMin = 3000
xMax = 60000

defaultDY =  dyHist.Integral(dyHist.FindBin(xMin),dyHist.FindBin(xMax-0.01))
pdfDY     =  dyHistPDF.Integral(dyHistPDF.FindBin(xMin),dyHistPDF.FindBin(xMax-0.01))

defaultOther =  otherHist.Integral(otherHist.FindBin(xMin),otherHist.FindBin(xMax-0.01))
pdfOther     =  otherHistPDF.Integral(otherHistPDF.FindBin(xMin),otherHistPDF.FindBin(xMax-0.01))

print ("DY PDF: ", abs(1 - (pdfDY)/(defaultDY)))
print ("Other PDF: ", abs(1 - (pdfOther)/(defaultOther)))

# ~ massBins = [400,500,700,1100,1900,3500,6000,7000,10000]
# ~ massBins = [1800,2200,2600,3000,3400,10000]
# ~ massBins = [60., 65.43046396, 71.3524269, 77.81037328, 84.85281374, 92.53264952,  100.90756983,  110.04048518,  120., 129.95474058, 140.73528833, 152.41014904, 165.0535115, 178.74571891, 193.57377942, 209.63191906,  227.02218049,  245.85507143,  266.2502669,   288.3373697, 
		# ~ 312.25673399,  338.16035716,  366.21284574,  396.59246138,  429.49225362, 465.12128666,  503.70596789,  545.49148654,  590.74337185,  639.74918031, 692.82032303,  750.29404456,  812.53556599,  879.94040575,  952.93689296, 
		# ~ 1031.98888927, 1117.59873655, 1210.310449,   1310.71317017, 1419.4449167,
		# ~ 1537.19663264, 1664.71658012, 1802.81509423, 1952.36973236, 2114.3308507, 2289.72764334, 2479.6746824,  2685.37900061, 2908.14776151, 3149.39656595, 3410.65844758, 3693.59361467, 4000.,4500,5200,6000,7000,8000]

massBins = [j for j in range(50, 120, 5)] + [j for j in range(120, 150, 5)] + [j for j in range(150, 200, 10)] + [j for j in range(200, 600, 20)]+ [j for j in range(600, 900, 30) ]+ [j for j in range(900, 1250, 50)] + [j for j in range(1250, 1610, 60) ] + [j for j in range(1610, 1890, 70) ] + [j for j in range(1890, 3970, 80) ] + [j for j in range(3970, 6070, 100) ] + [6070]

pdfUncertDY = []
pdfUncertOther = []
for i in range(0,len(massBins)-1):
	xMin = massBins[i]
	xMax = massBins[i+1]
	print (xMin, xMax)
	defaultDY =  dyHist.Integral(dyHist.FindBin(xMin),dyHist.FindBin(xMax-0.01))
	pdfDY     =  dyHistPDF.Integral(dyHistPDF.FindBin(xMin),dyHistPDF.FindBin(xMax-0.01))
	print (defaultDY, pdfDY)
	defaultOther =  otherHist.Integral(otherHist.FindBin(xMin),otherHist.FindBin(xMax-0.01))
	pdfOther     =  otherHistPDF.Integral(otherHistPDF.FindBin(xMin),otherHistPDF.FindBin(xMax-0.01))

	pdfUncertDY.append(1+abs(1 - pdfDY/defaultDY))
	if defaultOther > 0:
		pdfUncertOther.append(1+abs(1 - pdfOther/defaultOther))
	else:	
		pdfUncertOther.append(0)
	
print 	(pdfUncertDY)
print  (pdfUncertOther)


hCanvas = TCanvas("hCanvas", "Distribution", 800,400)

plotPad = TPad("plotPad","plotPad",0,0,1,1)
setTDRStyle()		
plotPad.UseCurrentStyle()
plotPad.Draw()	
plotPad.cd()


dyHist.Rebin(500)
dyHistPDF.Rebin(500)
otherHist.Rebin(500)
otherHistPDF.Rebin(500)
#~ 
#~ 
dyHistPDF.Divide(dyHist)
otherHistPDF.Divide(otherHist)


plotPad.DrawFrame(0,0.95,5000,1.5,"; dilepton mass [GeV]; PDF uncertainty")

dyHistPDF.SetLineColor(kGreen+2)
otherHistPDF.SetLineColor(kRed)
dyHist.GetXaxis().SetRangeUser(0,2000)
dyHistPDF.Draw("samehist")
#~ dyHistPDF.Draw("samepe")
otherHistPDF.Draw("samehist")

legend = TLegend(0.2, 0.7, 0.5, 0.925)
legend.SetFillStyle(0)
legend.SetBorderSize(0)
legend.SetTextFont(42)		
legend.AddEntry(dyHistPDF,"Drell-Yan","l")		
legend.AddEntry(otherHistPDF,"Other Backgrounds","l")		
legend.Draw()



	
hCanvas.Print("pdfUncert.pdf")
