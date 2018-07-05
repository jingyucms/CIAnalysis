from math import sqrt
import ROOT
from ROOT import TMath
import sys
import copy


#path = "root://cmseos.fnal.gov///store/user/jschulte/ZprimeAnalysis/histos/histosZprimeMuMu/"
path = "filesPU/"

fileNames = {

"CITo2Mu_100kTeV_ConLL_M1300":"output_CITo2Mu_M1300_CUETP8M1_Lam100kTeVConLL_13TeV_Pythia8_Corrected-v4_ntuple.root",
"CITo2Mu_100kTeV_ConLR_M1300":"output_CITo2Mu_M1300_CUETP8M1_Lam100kTeVConLR_13TeV_Pythia8_Corrected-v4_ntuple.root",
"CITo2Mu_100kTeV_ConRR_M1300":"output_CITo2Mu_M1300_CUETP8M1_Lam100kTeVConRR_13TeV_Pythia8_Corrected-v4_ntuple.root",
"CITo2Mu_100kTeV_DesLL_M1300":"output_CITo2Mu_M1300_CUETP8M1_Lam100kTeVDesLL_13TeV_Pythia8_Corrected-v4_ntuple.root",
"CITo2Mu_100kTeV_DesLR_M1300":"output_CITo2Mu_M1300_CUETP8M1_Lam100kTeVDesLR_13TeV_Pythia8_Corrected-v4_ntuple.root",
"CITo2Mu_100kTeV_DesRR_M1300":"output_CITo2Mu_M1300_CUETP8M1_Lam100kTeVDesRR_13TeV_Pythia8_Corrected-v4_ntuple.root",

"CITo2Mu_10TeV_ConLL_M1300":"output_CITo2Mu_M1300_CUETP8M1_Lam10TeVConLL_13TeV_Pythia8_Corrected-v4_ntuple.root",
"CITo2Mu_10TeV_ConLR_M1300":"output_CITo2Mu_M1300_CUETP8M1_Lam10TeVConLR_13TeV_Pythia8_Corrected-v4_ntuple.root",
"CITo2Mu_10TeV_ConRR_M1300":"output_CITo2Mu_M1300_CUETP8M1_Lam10TeVConRR_13TeV_Pythia8_Corrected-v4_ntuple.root",
"CITo2Mu_10TeV_DesLL_M1300":"output_CITo2Mu_M1300_CUETP8M1_Lam10TeVDesLL_13TeV_Pythia8_Corrected-v4_ntuple.root",
"CITo2Mu_10TeV_DesLR_M1300":"output_CITo2Mu_M1300_CUETP8M1_Lam10TeVDesLR_13TeV_Pythia8_Corrected-v4_ntuple.root",
"CITo2Mu_10TeV_DesRR_M1300":"output_CITo2Mu_M1300_CUETP8M1_Lam10TeVDesRR_13TeV_Pythia8_Corrected-v4_ntuple.root",

"CITo2Mu_16TeV_ConLL_M1300":"output_CITo2Mu_M1300_CUETP8M1_Lam16TeVConLL_13TeV_Pythia8_Corrected-v4_ntuple.root",
"CITo2Mu_16TeV_ConLR_M1300":"output_CITo2Mu_M1300_CUETP8M1_Lam16TeVConLR_13TeV_Pythia8_Corrected-v4_ntuple.root",
"CITo2Mu_16TeV_ConRR_M1300":"output_CITo2Mu_M1300_CUETP8M1_Lam16TeVConRR_13TeV_Pythia8_Corrected-v4_ntuple.root",
"CITo2Mu_16TeV_DesLL_M1300":"output_CITo2Mu_M1300_CUETP8M1_Lam16TeVDesLL_13TeV_Pythia8_Corrected-v4_ntuple.root",
"CITo2Mu_16TeV_DesLR_M1300":"output_CITo2Mu_M1300_CUETP8M1_Lam16TeVDesLR_13TeV_Pythia8_Corrected-v4_ntuple.root",
"CITo2Mu_16TeV_DesRR_M1300":"output_CITo2Mu_M1300_CUETP8M1_Lam16TeVDesRR_13TeV_Pythia8_Corrected-v4_ntuple.root",

"CITo2Mu_1TeV_ConLL_M1300":"output_CITo2Mu_M1300_CUETP8M1_Lam1TeVConLL_13TeV_Pythia8_Corrected-v4_ntuple.root",
"CITo2Mu_1TeV_ConLR_M1300":"output_CITo2Mu_M1300_CUETP8M1_Lam1TeVConLR_13TeV_Pythia8_Corrected-v4_ntuple.root",
"CITo2Mu_1TeV_ConRR_M1300":"output_CITo2Mu_M1300_CUETP8M1_Lam1TeVConRR_13TeV_Pythia8_Corrected-v4_ntuple.root",
"CITo2Mu_1TeV_DesLL_M1300":"output_CITo2Mu_M1300_CUETP8M1_Lam1TeVDesLL_13TeV_Pythia8_Corrected-v4_ntuple.root",
"CITo2Mu_1TeV_DesLR_M1300":"output_CITo2Mu_M1300_CUETP8M1_Lam1TeVDesLR_13TeV_Pythia8_Corrected-v4_ntuple.root",
"CITo2Mu_1TeV_DesRR_M1300":"output_CITo2Mu_M1300_CUETP8M1_Lam1TeVDesRR_13TeV_Pythia8_Corrected-v4_ntuple.root",

"CITo2Mu_22TeV_ConLL_M1300":"output_CITo2Mu_M1300_CUETP8M1_Lam22TeVConLL_13TeV_Pythia8_Corrected-v4_ntuple.root",
"CITo2Mu_22TeV_ConLR_M1300":"output_CITo2Mu_M1300_CUETP8M1_Lam22TeVConLR_13TeV_Pythia8_Corrected-v4_ntuple.root",
"CITo2Mu_22TeV_ConRR_M1300":"output_CITo2Mu_M1300_CUETP8M1_Lam22TeVConRR_13TeV_Pythia8_Corrected-v4_ntuple.root",
"CITo2Mu_22TeV_DesLL_M1300":"output_CITo2Mu_M1300_CUETP8M1_Lam22TeVDesLL_13TeV_Pythia8_Corrected-v4_ntuple.root",
"CITo2Mu_22TeV_DesLR_M1300":"output_CITo2Mu_M1300_CUETP8M1_Lam22TeVDesLR_13TeV_Pythia8_Corrected-v4_ntuple.root",
"CITo2Mu_22TeV_DesRR_M1300":"output_CITo2Mu_M1300_CUETP8M1_Lam22TeVDesRR_13TeV_Pythia8_Corrected-v4_ntuple.root",

"CITo2Mu_28TeV_ConLL_M1300":"output_CITo2Mu_M1300_CUETP8M1_Lam28TeVConLL_13TeV_Pythia8_Corrected-v4_ntuple.root",
"CITo2Mu_28TeV_ConLR_M1300":"output_CITo2Mu_M1300_CUETP8M1_Lam28TeVConLR_13TeV_Pythia8_Corrected-v4_ntuple.root",
"CITo2Mu_28TeV_ConRR_M1300":"output_CITo2Mu_M1300_CUETP8M1_Lam28TeVConRR_13TeV_Pythia8_Corrected-v4_ntuple.root",
"CITo2Mu_28TeV_DesLL_M1300":"output_CITo2Mu_M1300_CUETP8M1_Lam28TeVDesLL_13TeV_Pythia8_Corrected-v4_ntuple.root",
"CITo2Mu_28TeV_DesLR_M1300":"output_CITo2Mu_M1300_CUETP8M1_Lam28TeVDesLR_13TeV_Pythia8_Corrected-v4_ntuple.root",
"CITo2Mu_28TeV_DesRR_M1300":"output_CITo2Mu_M1300_CUETP8M1_Lam28TeVDesRR_13TeV_Pythia8_Corrected-v4_ntuple.root",

"CITo2Mu_34TeV_ConLL_M1300":"output_CITo2Mu_M1300_CUETP8M1_Lam34TeVConLL_13TeV_Pythia8_Corrected-v4_ntuple.root",
"CITo2Mu_34TeV_ConLR_M1300":"output_CITo2Mu_M1300_CUETP8M1_Lam34TeVConLR_13TeV_Pythia8_Corrected-v4_ntuple.root",
"CITo2Mu_34TeV_ConRR_M1300":"output_CITo2Mu_M1300_CUETP8M1_Lam34TeVConRR_13TeV_Pythia8_Corrected-v4_ntuple.root",
"CITo2Mu_34TeV_DesLL_M1300":"output_CITo2Mu_M1300_CUETP8M1_Lam34TeVDesLL_13TeV_Pythia8_Corrected-v4_ntuple.root",
"CITo2Mu_34TeV_DesLR_M1300":"output_CITo2Mu_M1300_CUETP8M1_Lam34TeVDesLR_13TeV_Pythia8_Corrected-v4_ntuple.root",
"CITo2Mu_34TeV_DesRR_M1300":"output_CITo2Mu_M1300_CUETP8M1_Lam34TeVDesRR_13TeV_Pythia8_Corrected-v4_ntuple.root",

"CITo2Mu_100kTeV_ConLL_M2000":"output_CITo2Mu_M2000_CUETP8M1_Lam100kTeVConLL_13TeV_Pythia8_Corrected-v4_ntuple.root",
"CITo2Mu_10TeV_ConLL_M2000":"output_CITo2Mu_M2000_CUETP8M1_Lam10TeVConLL_13TeV_Pythia8_Corrected-v4_ntuple.root",
"CITo2Mu_16TeV_ConLL_M2000":"output_CITo2Mu_M2000_CUETP8M1_Lam16TeVConLL_13TeV_Pythia8_Corrected-v4_ntuple.root",
"CITo2Mu_1TeV_ConLL_M2000":"output_CITo2Mu_M2000_CUETP8M1_Lam1TeVConLL_13TeV_Pythia8_Corrected-v4_ntuple.root",
"CITo2Mu_22TeV_ConLL_M2000":"output_CITo2Mu_M2000_CUETP8M1_Lam22TeVConLL_13TeV_Pythia8_Corrected-v4_ntuple.root",
"CITo2Mu_28TeV_ConLL_M2000":"output_CITo2Mu_M2000_CUETP8M1_Lam28TeVConLL_13TeV_Pythia8_Corrected-v4_ntuple.root",
"CITo2Mu_34TeV_ConLL_M2000":"output_CITo2Mu_M2000_CUETP8M1_Lam34TeVConLL_13TeV_Pythia8_Corrected-v4_ntuple.root",

"CITo2Mu_100kTeV_ConLL_M300":"output_CITo2Mu_M300_CUETP8M1_Lam100kTeVConLL_13TeV_Pythia8_Corrected-v4_ntuple.root",
"CITo2Mu_100kTeV_ConLR_M300":"output_CITo2Mu_M300_CUETP8M1_Lam100kTeVConLR_13TeV_Pythia8_Corrected-v4_ntuple.root",
"CITo2Mu_100kTeV_ConRR_M300":"output_CITo2Mu_M300_CUETP8M1_Lam100kTeVConRR_13TeV_Pythia8_Corrected-v4_ntuple.root",
"CITo2Mu_100kTeV_DesLL_M300":"output_CITo2Mu_M300_CUETP8M1_Lam100kTeVDesLL_13TeV_Pythia8_Corrected-v4_ntuple.root",
"CITo2Mu_100kTeV_DesLR_M300":"output_CITo2Mu_M300_CUETP8M1_Lam100kTeVDesLR_13TeV_Pythia8_Corrected-v4_ntuple.root",
"CITo2Mu_100kTeV_DesRR_M300":"output_CITo2Mu_M300_CUETP8M1_Lam100kTeVDesRR_13TeV_Pythia8_Corrected-v4_ntuple.root",

"CITo2Mu_10TeV_ConLL_M300":"output_CITo2Mu_M300_CUETP8M1_Lam10TeVConLL_13TeV_Pythia8_Corrected-v4_ntuple.root",
"CITo2Mu_10TeV_ConLR_M300":"output_CITo2Mu_M300_CUETP8M1_Lam10TeVConLR_13TeV_Pythia8_Corrected-v4_ntuple.root",
"CITo2Mu_10TeV_ConRR_M300":"output_CITo2Mu_M300_CUETP8M1_Lam10TeVConRR_13TeV_Pythia8_Corrected-v4_ntuple.root",
"CITo2Mu_10TeV_DesLL_M300":"output_CITo2Mu_M300_CUETP8M1_Lam10TeVDesLL_13TeV_Pythia8_Corrected-v4_ntuple.root",
"CITo2Mu_10TeV_DesLR_M300":"output_CITo2Mu_M300_CUETP8M1_Lam10TeVDesLR_13TeV_Pythia8_Corrected-v4_ntuple.root",
"CITo2Mu_10TeV_DesRR_M300":"output_CITo2Mu_M300_CUETP8M1_Lam10TeVDesRR_13TeV_Pythia8_Corrected-v4_ntuple.root",

"CITo2Mu_16TeV_ConLL_M300":"output_CITo2Mu_M300_CUETP8M1_Lam16TeVConLL_13TeV_Pythia8_Corrected-v4_ntuple.root",
"CITo2Mu_16TeV_ConLR_M300":"output_CITo2Mu_M300_CUETP8M1_Lam16TeVConLR_13TeV_Pythia8_Corrected-v4_ntuple.root",
"CITo2Mu_16TeV_ConRR_M300":"output_CITo2Mu_M300_CUETP8M1_Lam16TeVConRR_13TeV_Pythia8_Corrected-v4_ntuple.root",
"CITo2Mu_16TeV_DesLL_M300":"output_CITo2Mu_M300_CUETP8M1_Lam16TeVDesLL_13TeV_Pythia8_Corrected-v4_ntuple.root",
"CITo2Mu_16TeV_DesLR_M300":"output_CITo2Mu_M300_CUETP8M1_Lam16TeVDesLR_13TeV_Pythia8_Corrected-v4_ntuple.root",
"CITo2Mu_16TeV_DesRR_M300":"output_CITo2Mu_M300_CUETP8M1_Lam16TeVDesRR_13TeV_Pythia8_Corrected-v4_ntuple.root",

"CITo2Mu_1TeV_ConLL_M300":"output_CITo2Mu_M300_CUETP8M1_Lam1TeVConLL_13TeV_Pythia8_Corrected-v4_ntuple.root",
"CITo2Mu_1TeV_ConLR_M300":"output_CITo2Mu_M300_CUETP8M1_Lam1TeVConLR_13TeV_Pythia8_Corrected-v4_ntuple.root",
"CITo2Mu_1TeV_ConRR_M300":"output_CITo2Mu_M300_CUETP8M1_Lam1TeVConRR_13TeV_Pythia8_Corrected-v4_ntuple.root",
"CITo2Mu_1TeV_DesLL_M300":"output_CITo2Mu_M300_CUETP8M1_Lam1TeVDesLL_13TeV_Pythia8_Corrected-v4_ntuple.root",
"CITo2Mu_1TeV_DesLR_M300":"output_CITo2Mu_M300_CUETP8M1_Lam1TeVDesLR_13TeV_Pythia8_Corrected-v4_ntuple.root",
"CITo2Mu_1TeV_DesRR_M300":"output_CITo2Mu_M300_CUETP8M1_Lam1TeVDesRR_13TeV_Pythia8_Corrected-v4_ntuple.root",

"CITo2Mu_22TeV_ConLL_M300":"output_CITo2Mu_M300_CUETP8M1_Lam22TeVConLL_13TeV_Pythia8_Corrected-v4_ntuple.root",
"CITo2Mu_22TeV_ConLR_M300":"output_CITo2Mu_M300_CUETP8M1_Lam22TeVConLR_13TeV_Pythia8_Corrected-v4_ntuple.root",
"CITo2Mu_22TeV_ConRR_M300":"output_CITo2Mu_M300_CUETP8M1_Lam22TeVConRR_13TeV_Pythia8_Corrected-v4_ntuple.root",
"CITo2Mu_22TeV_DesLL_M300":"output_CITo2Mu_M300_CUETP8M1_Lam22TeVDesLL_13TeV_Pythia8_Corrected-v4_ntuple.root",
"CITo2Mu_22TeV_DesLR_M300":"output_CITo2Mu_M300_CUETP8M1_Lam22TeVDesLR_13TeV_Pythia8_Corrected-v4_ntuple.root",
"CITo2Mu_22TeV_DesRR_M300":"output_CITo2Mu_M300_CUETP8M1_Lam22TeVDesRR_13TeV_Pythia8_Corrected-v4_ntuple.root",

"CITo2Mu_28TeV_ConLL_M300":"output_CITo2Mu_M300_CUETP8M1_Lam28TeVConLL_13TeV_Pythia8_Corrected-v4_ntuple.root",
"CITo2Mu_28TeV_ConLR_M300":"output_CITo2Mu_M300_CUETP8M1_Lam28TeVConLR_13TeV_Pythia8_Corrected-v4_ntuple.root",
"CITo2Mu_28TeV_ConRR_M300":"output_CITo2Mu_M300_CUETP8M1_Lam28TeVConRR_13TeV_Pythia8_Corrected-v4_ntuple.root",
"CITo2Mu_28TeV_DesLL_M300":"output_CITo2Mu_M300_CUETP8M1_Lam28TeVDesLL_13TeV_Pythia8_Corrected-v4_ntuple.root",
"CITo2Mu_28TeV_DesLR_M300":"output_CITo2Mu_M300_CUETP8M1_Lam28TeVDesLR_13TeV_Pythia8_Corrected-v4_ntuple.root",
"CITo2Mu_28TeV_DesRR_M300":"output_CITo2Mu_M300_CUETP8M1_Lam28TeVDesRR_13TeV_Pythia8_Corrected-v4_ntuple.root",

"CITo2Mu_34TeV_ConLL_M300":"output_CITo2Mu_M300_CUETP8M1_Lam34TeVConLL_13TeV_Pythia8_Corrected-v4_ntuple.root",
"CITo2Mu_34TeV_ConLR_M300":"output_CITo2Mu_M300_CUETP8M1_Lam34TeVConLR_13TeV_Pythia8_Corrected-v4_ntuple.root",
"CITo2Mu_34TeV_ConRR_M300":"output_CITo2Mu_M300_CUETP8M1_Lam34TeVConRR_13TeV_Pythia8_Corrected-v4_ntuple.root",
"CITo2Mu_34TeV_DesLL_M300":"output_CITo2Mu_M300_CUETP8M1_Lam34TeVDesLL_13TeV_Pythia8_Corrected-v4_ntuple.root",
"CITo2Mu_34TeV_DesLR_M300":"output_CITo2Mu_M300_CUETP8M1_Lam34TeVDesLR_13TeV_Pythia8_Corrected-v4_ntuple.root",
"CITo2Mu_34TeV_DesRR_M300":"output_CITo2Mu_M300_CUETP8M1_Lam34TeVDesRR_13TeV_Pythia8_Corrected-v4_ntuple.root",

"CITo2Mu_100kTeV_ConLL_M800":"output_CITo2Mu_M800_CUETP8M1_Lam100kTeVConLL_13TeV_Pythia8_Corrected-v4_ntuple.root",
"CITo2Mu_100kTeV_ConLR_M800":"output_CITo2Mu_M800_CUETP8M1_Lam100kTeVConLR_13TeV_Pythia8_Corrected-v4_ntuple.root",
"CITo2Mu_100kTeV_ConRR_M800":"output_CITo2Mu_M800_CUETP8M1_Lam100kTeVConRR_13TeV_Pythia8_Corrected-v4_ntuple.root",
"CITo2Mu_100kTeV_DesLL_M800":"output_CITo2Mu_M800_CUETP8M1_Lam100kTeVDesLL_13TeV_Pythia8_Corrected-v4_ntuple.root",
"CITo2Mu_100kTeV_DesLR_M800":"output_CITo2Mu_M800_CUETP8M1_Lam100kTeVDesLR_13TeV_Pythia8_Corrected-v4_ntuple.root",
"CITo2Mu_100kTeV_DesRR_M800":"output_CITo2Mu_M800_CUETP8M1_Lam100kTeVDesRR_13TeV_Pythia8_Corrected-v4_ntuple.root",

"CITo2Mu_10TeV_ConLL_M800":"output_CITo2Mu_M800_CUETP8M1_Lam10TeVConLL_13TeV_Pythia8_Corrected-v4_ntuple.root",
"CITo2Mu_10TeV_ConLR_M800":"output_CITo2Mu_M800_CUETP8M1_Lam10TeVConLR_13TeV_Pythia8_Corrected-v4_ntuple.root",
"CITo2Mu_10TeV_ConRR_M800":"output_CITo2Mu_M800_CUETP8M1_Lam10TeVConRR_13TeV_Pythia8_Corrected-v4_ntuple.root",
"CITo2Mu_10TeV_DesLL_M800":"output_CITo2Mu_M800_CUETP8M1_Lam10TeVDesLL_13TeV_Pythia8_Corrected-v4_ntuple.root",
"CITo2Mu_10TeV_DesLR_M800":"output_CITo2Mu_M800_CUETP8M1_Lam10TeVDesLR_13TeV_Pythia8_Corrected-v4_ntuple.root",
"CITo2Mu_10TeV_DesRR_M800":"output_CITo2Mu_M800_CUETP8M1_Lam10TeVDesRR_13TeV_Pythia8_Corrected-v4_ntuple.root",

"CITo2Mu_16TeV_ConLL_M800":"output_CITo2Mu_M800_CUETP8M1_Lam16TeVConLL_13TeV_Pythia8_Corrected-v4_ntuple.root",
"CITo2Mu_16TeV_ConLR_M800":"output_CITo2Mu_M800_CUETP8M1_Lam16TeVConLR_13TeV_Pythia8_Corrected-v4_ntuple.root",
"CITo2Mu_16TeV_ConRR_M800":"output_CITo2Mu_M800_CUETP8M1_Lam16TeVConRR_13TeV_Pythia8_Corrected-v4_ntuple.root",
"CITo2Mu_16TeV_DesLL_M800":"output_CITo2Mu_M800_CUETP8M1_Lam16TeVDesLL_13TeV_Pythia8_Corrected-v4_ntuple.root",
"CITo2Mu_16TeV_DesLR_M800":"output_CITo2Mu_M800_CUETP8M1_Lam16TeVDesLR_13TeV_Pythia8_Corrected-v4_ntuple.root",
"CITo2Mu_16TeV_DesRR_M800":"output_CITo2Mu_M800_CUETP8M1_Lam16TeVDesRR_13TeV_Pythia8_Corrected-v4_ntuple.root",

"CITo2Mu_1TeV_ConLL_M800":"output_CITo2Mu_M800_CUETP8M1_Lam1TeVConLL_13TeV_Pythia8_Corrected-v4_ntuple.root",
"CITo2Mu_1TeV_ConLR_M800":"output_CITo2Mu_M800_CUETP8M1_Lam1TeVConLR_13TeV_Pythia8_Corrected-v4_ntuple.root",
"CITo2Mu_1TeV_ConRR_M800":"output_CITo2Mu_M800_CUETP8M1_Lam1TeVConRR_13TeV_Pythia8_Corrected-v4_ntuple.root",
"CITo2Mu_1TeV_DesLL_M800":"output_CITo2Mu_M800_CUETP8M1_Lam1TeVDesLL_13TeV_Pythia8_Corrected-v4_ntuple.root",
"CITo2Mu_1TeV_DesLR_M800":"output_CITo2Mu_M800_CUETP8M1_Lam1TeVDesLR_13TeV_Pythia8_Corrected-v4_ntuple.root",
"CITo2Mu_1TeV_DesRR_M800":"output_CITo2Mu_M800_CUETP8M1_Lam1TeVDesRR_13TeV_Pythia8_Corrected-v4_ntuple.root",

"CITo2Mu_22TeV_ConLL_M800":"output_CITo2Mu_M800_CUETP8M1_Lam22TeVConLL_13TeV_Pythia8_Corrected-v4_ntuple.root",
"CITo2Mu_22TeV_ConLR_M800":"output_CITo2Mu_M800_CUETP8M1_Lam22TeVConLR_13TeV_Pythia8_Corrected-v4_ntuple.root",
"CITo2Mu_22TeV_ConRR_M800":"output_CITo2Mu_M800_CUETP8M1_Lam22TeVConRR_13TeV_Pythia8_Corrected-v4_ntuple.root",
"CITo2Mu_22TeV_DesLL_M800":"output_CITo2Mu_M800_CUETP8M1_Lam22TeVDesLL_13TeV_Pythia8_Corrected-v4_ntuple.root",
"CITo2Mu_22TeV_DesLR_M800":"output_CITo2Mu_M800_CUETP8M1_Lam22TeVDesLR_13TeV_Pythia8_Corrected-v4_ntuple.root",
"CITo2Mu_22TeV_DesRR_M800":"output_CITo2Mu_M800_CUETP8M1_Lam22TeVDesRR_13TeV_Pythia8_Corrected-v4_ntuple.root",

"CITo2Mu_28TeV_ConLL_M800":"output_CITo2Mu_M800_CUETP8M1_Lam28TeVConLL_13TeV_Pythia8_Corrected-v4_ntuple.root",
"CITo2Mu_28TeV_ConLR_M800":"output_CITo2Mu_M800_CUETP8M1_Lam28TeVConLR_13TeV_Pythia8_Corrected-v4_ntuple.root",
"CITo2Mu_28TeV_ConRR_M800":"output_CITo2Mu_M800_CUETP8M1_Lam28TeVConRR_13TeV_Pythia8_Corrected-v4_ntuple.root",
"CITo2Mu_28TeV_DesLL_M800":"output_CITo2Mu_M800_CUETP8M1_Lam28TeVDesLL_13TeV_Pythia8_Corrected-v4_ntuple.root",
"CITo2Mu_28TeV_DesLR_M800":"output_CITo2Mu_M800_CUETP8M1_Lam28TeVDesLR_13TeV_Pythia8_Corrected-v4_ntuple.root",
"CITo2Mu_28TeV_DesRR_M800":"output_CITo2Mu_M800_CUETP8M1_Lam28TeVDesRR_13TeV_Pythia8_Corrected-v4_ntuple.root",

"CITo2Mu_34TeV_ConLL_M800":"output_CITo2Mu_M800_CUETP8M1_Lam34TeVConLL_13TeV_Pythia8_Corrected-v4_ntuple.root",
"CITo2Mu_34TeV_ConLR_M800":"output_CITo2Mu_M800_CUETP8M1_Lam34TeVConLR_13TeV_Pythia8_Corrected-v4_ntuple.root",
"CITo2Mu_34TeV_ConRR_M800":"output_CITo2Mu_M800_CUETP8M1_Lam34TeVConRR_13TeV_Pythia8_Corrected-v4_ntuple.root",
"CITo2Mu_34TeV_DesLL_M800":"output_CITo2Mu_M800_CUETP8M1_Lam34TeVDesLL_13TeV_Pythia8_Corrected-v4_ntuple.root",
"CITo2Mu_34TeV_DesLR_M800":"output_CITo2Mu_M800_CUETP8M1_Lam34TeVDesLR_13TeV_Pythia8_Corrected-v4_ntuple.root",
"CITo2Mu_34TeV_DesRR_M800":"output_CITo2Mu_M800_CUETP8M1_Lam34TeVDesRR_13TeV_Pythia8_Corrected-v4_ntuple.root",

"Data_RunB":"output_SingleMuon_DataB_tree.root",
"Data_RunC":"output_SingleMuon_DataC_tree.root",
"Data_RunD":"output_SingleMuon_DataD_tree.root",
"Data_RunE":"output_SingleMuon_DataE_tree.root",
"Data_RunF":"output_SingleMuon_DataF_tree.root",
"Data_RunG":"output_SingleMuon_DataG_tree.root",
"Data_RunH2":"output_SingleMuon_DataH2_tree.root",
"Data_RunH3":"output_SingleMuon_DataH3_tree.root",

"ST_tW_antitop":"output_ST_tW_antitop_5f_inclusiveDecays_13TeV-powheg-pythia8_TuneCUETP8M1_Moriond17_tree.root",
"ST_tW_top":"output_ST_tW_top_5f_inclusiveDecays_13TeV-powheg-pythia8_TuneCUETP8M1_Moriond17_tree.root",
"TTTo2L2Nu":"output_TTTo2L2Nu_TuneCUETP8M2_ttHtranche3_13TeV-powheg-pythia8_Moriond17_tree.root",
"TTTo2L2Nu_M1200To1800":"output_TTToLL_MLL_1200To1800_TuneCUETP8M1_13TeV-powheg-pythia8_Moriond17_tree.root",
"TTTo2L2Nu_M1800ToInf":"output_TTToLL_MLL_1800ToInf_TuneCUETP8M1_13TeV-powheg-pythia8_Moriond17_tree.root",
"TTTo2L2Nu_M500To800":"output_TTToLL_MLL_500To800_TuneCUETP8M1_13TeV-powheg-pythia8_Moriond17_tree.root",
"TTTo2L2Nu_M800To1200":"output_TTToLL_MLL_800To1200_TuneCUETP8M1_13TeV-powheg-pythia8_Moriond17_tree.root",
"WWTo2L2Nu":"output_WWTo2L2Nu_13TeV-powheg_Moriond17_tree.root",
"WWTo2L2Nu_M1200To2500":"output_WWTo2L2Nu_Mll_1200To2500_13TeV-powheg_Moriond17_tree.root",
"WWTo2L2Nu_M2500ToInf":"output_WWTo2L2Nu_Mll_2500ToInf_13TeV-powheg_Moriond17_tree.root",
"WWTo2L2Nu_M600To1200":"output_WWTo2L2Nu_Mll_600To1200_13TeV-powheg_Moriond17_tree.root",
"WZ":"output_WZ_TuneCUETP8M1_13TeV-pythia8_Moriond17_tree.root",
"ZToMuMu_M120To200":"output_ZToMuMu_NNPDF30_13TeV-powheg_M_120_200_Moriond17_tree.root",
"ZToMuMu_M1400To2300":"output_ZToMuMu_NNPDF30_13TeV-powheg_M_1400_2300_Moriond17_tree.root",
"ZToMuMu_M200To400":"output_ZToMuMu_NNPDF30_13TeV-powheg_M_200_400_Moriond17_tree.root",
"ZToMuMu_M2300To3500":"output_ZToMuMu_NNPDF30_13TeV-powheg_M_2300_3500_Moriond17_tree.root",
"ZToMuMu_M3500To4500":"output_ZToMuMu_NNPDF30_13TeV-powheg_M_3500_4500_Moriond17_tree.root",
"ZToMuMu_M400To800":"output_ZToMuMu_NNPDF30_13TeV-powheg_M_400_800_Moriond17_tree.root",
"ZToMuMu_M4500To6000":"output_ZToMuMu_NNPDF30_13TeV-powheg_M_4500_6000_Moriond17_tree.root",
"ZToMuMu_M50To120":"output_ZToMuMu_NNPDF30_13TeV-powheg_M_50_120_Moriond17_tree.root",
"ZToMuMu_M800To1400":"output_ZToMuMu_NNPDF30_13TeV-powheg_M_800_1400_Moriond17_tree.root",
"ZZ":"output_ZZ_TuneCUETP8M1_13TeV-pythia8_Moriond17_tree.root",


#~ "JetsFromDataBB":"Data-total-jets-BB.root",
"JetsFromData":"Data-total-jets-BBBEEE.root",



}
	
	
class Signals:
	


		
	class CITo2Mu_Lam1TeVConLL:
		subprocesses = ["CITo2Mu_1TeV_ConLL_M300","CITo2Mu_1TeV_ConLL_M800","CITo2Mu_1TeV_ConLL_M1300","CITo2Mu_1TeV_ConLL_M2000"]
		label = "CITo2Mu_Lam1TeVConLL"		#"CI #rightarrow #mu^{+}#mu^{-} #Lambda 22 TeV - Con LL"
		fillcolor = ROOT.kWhite
		fillstyle = 0
		linecolor = ROOT.kBlack
		uncertainty = 0.0
		scaleFac     = 1.	
		additionalSelection = None
	class CITo2Mu_Lam1TeVConLR:
		subprocesses = ["CITo2Mu_1TeV_ConLR_M300","CITo2Mu_1TeV_ConLR_M800","CITo2Mu_1TeV_ConLR_M1300"]
		label = "CITo2Mu_Lam1TeVConLR"		#"CI #rightarrow #mu^{+}#mu^{-} #Lambda 22 TeV - Con LR"
		fillcolor = ROOT.kWhite
		fillstyle = 0
		linecolor = ROOT.kRed-4
		uncertainty = 0.0
		scaleFac     = 1.	
		additionalSelection = None
	class CITo2Mu_Lam1TeVConRR:
		subprocesses = ["CITo2Mu_1TeV_ConRR_M300","CITo2Mu_1TeV_ConRR_M800","CITo2Mu_1TeV_ConRR_M1300"]
		label = "CITo2Mu_Lam1TeVConRR"		#"CI #rightarrow #mu^{+}#mu^{-} #Lambda 22 TeV - Con RR"
		fillcolor = ROOT.kWhite
		fillstyle = 0
		linecolor = ROOT.kYellow
		uncertainty = 0.0
		scaleFac     = 1.	
		additionalSelection = None
	class CITo2Mu_Lam1TeVDesLL:
		subprocesses = ["CITo2Mu_1TeV_DesLL_M300","CITo2Mu_1TeV_DesLL_M800","CITo2Mu_1TeV_DesLL_M1300"]
		label = "CITo2Mu_Lam1TeVDesLL"		#"CI #rightarrow #mu^{+}#mu^{-} #Lambda 22 TeV - Des LL"
		fillcolor = ROOT.kWhite
		fillstyle = 0
		linecolor = ROOT.kBlue+1
		uncertainty = 0.0
		scaleFac     = 1.	
		additionalSelection = None
	class CITo2Mu_Lam1TeVDesLR:
		subprocesses = ["CITo2Mu_1TeV_DesLR_M300","CITo2Mu_1TeV_DesLR_M800","CITo2Mu_1TeV_DesLR_M1300"]
		label = "CITo2Mu_Lam1TeVDesLR"		#"CI #rightarrow #mu^{+}#mu^{-} #Lambda 22 TeV - Des LR"
		fillcolor = ROOT.kWhite
		fillstyle = 0
		linecolor = ROOT.kGreen+1
		uncertainty = 0.0
		scaleFac     = 1.	
		additionalSelection = None
	class CITo2Mu_Lam1TeVDesRR:
		subprocesses = ["CITo2Mu_1TeV_DesRR_M300","CITo2Mu_1TeV_DesRR_M800","CITo2Mu_1TeV_DesRR_M1300"]
		label = "CITo2Mu_Lam1TeVDesRR"		#"CI #rightarrow #mu^{+}#mu^{-} #Lambda 22 TeV - Des RR"
		fillcolor = ROOT.kWhite
		fillstyle = 0
		linecolor = ROOT.kMagenta+1
		uncertainty = 0.0
		scaleFac     = 1.	
		additionalSelection = None
		
	class CITo2Mu_Lam10TeVConLL:
		subprocesses = ["CITo2Mu_10TeV_ConLL_M300","CITo2Mu_10TeV_ConLL_M800","CITo2Mu_10TeV_ConLL_M1300","CITo2Mu_10TeV_ConLL_M2000"]
		label = "CITo2Mu_Lam10TeVConLL"		#"CI #rightarrow #mu^{+}#mu^{-} #Lambda 22 TeV - Con LL"
		fillcolor = ROOT.kWhite
		fillstyle = 0
		linecolor = ROOT.kRed
		uncertainty = 0.0
		scaleFac     = 1.	
		additionalSelection = None
	class CITo2Mu_Lam10TeVConLR:
		subprocesses = ["CITo2Mu_10TeV_ConLR_M300","CITo2Mu_10TeV_ConLR_M800","CITo2Mu_10TeV_ConLR_M1300"]
		label = "CITo2Mu_Lam10TeVConLR"		#"CI #rightarrow #mu^{+}#mu^{-} #Lambda 22 TeV - Con LR"
		fillcolor = ROOT.kWhite
		fillstyle = 0
		linecolor = ROOT.kRed-4
		uncertainty = 0.0
		scaleFac     = 1.	
		additionalSelection = None
	class CITo2Mu_Lam10TeVConRR:
		subprocesses = ["CITo2Mu_10TeV_ConRR_M300","CITo2Mu_10TeV_ConRR_M800","CITo2Mu_10TeV_ConRR_M1300"]
		label = "CITo2Mu_Lam10TeVConRR"		#"CI #rightarrow #mu^{+}#mu^{-} #Lambda 10 TeV - Con RR"
		fillcolor = ROOT.kWhite
		fillstyle = 0
		linecolor = ROOT.kYellow
		uncertainty = 0.0
		scaleFac     = 1.	
		additionalSelection = None
	class CITo2Mu_Lam10TeVDesLL:
		subprocesses = ["CITo2Mu_10TeV_DesLL_M300","CITo2Mu_10TeV_DesLL_M800","CITo2Mu_10TeV_DesLL_M1300"]
		label = "CITo2Mu_Lam10TeVDesLL"		#"CI #rightarrow #mu^{+}#mu^{-} #Lambda 10 TeV - Des LL"
		fillcolor = ROOT.kWhite
		fillstyle = 0
		linecolor = ROOT.kBlue+1
		uncertainty = 0.0
		scaleFac     = 1.	
		additionalSelection = None
	class CITo2Mu_Lam10TeVDesLR:
		subprocesses = ["CITo2Mu_10TeV_DesLR_M300","CITo2Mu_10TeV_DesLR_M800","CITo2Mu_10TeV_DesLR_M1300"]
		label = "CITo2Mu_Lam10TeVDesLR"		#"CI #rightarrow #mu^{+}#mu^{-} #Lambda 10 TeV - Des LR"
		fillcolor = ROOT.kWhite
		fillstyle = 0
		linecolor = ROOT.kGreen+1
		uncertainty = 0.0
		scaleFac     = 1.	
		additionalSelection = None
	class CITo2Mu_Lam10TeVDesRR:
		subprocesses = ["CITo2Mu_10TeV_DesRR_M300","CITo2Mu_10TeV_DesRR_M800","CITo2Mu_10TeV_DesRR_M1300"]
		label = "CITo2Mu_Lam10TeVDesRR"		#"CI #rightarrow #mu^{+}#mu^{-} #Lambda 10 TeV - Des RR"
		fillcolor = ROOT.kWhite
		fillstyle = 0
		linecolor = ROOT.kMagenta+1
		uncertainty = 0.0
		scaleFac     = 1.	
		additionalSelection = None
		
	class CITo2Mu_Lam16TeVConLL:
		subprocesses = ["CITo2Mu_16TeV_ConLL_M300","CITo2Mu_16TeV_ConLL_M800","CITo2Mu_16TeV_ConLL_M1300","CITo2Mu_16TeV_ConLL_M2000"]
		label = "CITo2Mu_Lam16TeVConLL"		#"CI #rightarrow #mu^{+}#mu^{-} #Lambda 22 TeV - Con LL"
		fillcolor = ROOT.kWhite
		fillstyle = 0
		linecolor = ROOT.kRed
		uncertainty = 0.
		scaleFac     = 1.	
		additionalSelection = None
	class CITo2Mu_Lam16TeVConLR:
		subprocesses = ["CITo2Mu_16TeV_ConLR_M300","CITo2Mu_16TeV_ConLR_M800","CITo2Mu_16TeV_ConLR_M1300"]
		label = "CITo2Mu_Lam16TeVConLR"		#"CI #rightarrow #mu^{+}#mu^{-} #Lambda 22 TeV - Con LR"
		fillcolor = ROOT.kWhite
		fillstyle = 0
		linecolor = ROOT.kRed-4
		uncertainty = 0.0
		scaleFac     = 1.	
		additionalSelection = None
	class CITo2Mu_Lam16TeVConRR:
		subprocesses = ["CITo2Mu_16TeV_ConRR_M300","CITo2Mu_16TeV_ConRR_M800","CITo2Mu_16TeV_ConRR_M1300"]
		label = "CITo2Mu_Lam16TeVConRR"		#"CI #rightarrow #mu^{+}#mu^{-} #Lambda 16 TeV - Con RR"
		fillcolor = ROOT.kWhite
		fillstyle = 0
		linecolor = ROOT.kYellow
		uncertainty = 0.0
		scaleFac     = 1.	
		additionalSelection = None
	class CITo2Mu_Lam16TeVDesLL:
		subprocesses = ["CITo2Mu_16TeV_DesLL_M300","CITo2Mu_16TeV_DesLL_M800","CITo2Mu_16TeV_DesLL_M1300"]
		label = "CITo2Mu_Lam16TeVDesLL"		#"CI #rightarrow #mu^{+}#mu^{-} #Lambda 16 TeV - Des LL"
		fillcolor = ROOT.kWhite
		fillstyle = 0
		linecolor = ROOT.kBlue+1
		uncertainty = 0.0
		scaleFac     = 1.	
		additionalSelection = None
	class CITo2Mu_Lam16TeVDesLR:
		subprocesses = ["CITo2Mu_16TeV_DesLR_M300","CITo2Mu_16TeV_DesLR_M800","CITo2Mu_16TeV_DesLR_M1300"]
		label = "CITo2Mu_Lam16TeVDesLR"		#"CI #rightarrow #mu^{+}#mu^{-} #Lambda 16 TeV - Des LR"
		fillcolor = ROOT.kWhite
		fillstyle = 0
		linecolor = ROOT.kGreen+1
		uncertainty = 0.0
		scaleFac     = 1.	
		additionalSelection = None
	class CITo2Mu_Lam16TeVDesRR:
		subprocesses = ["CITo2Mu_16TeV_DesRR_M300","CITo2Mu_16TeV_DesRR_M800","CITo2Mu_16TeV_DesRR_M1300"]
		label = "CITo2Mu_Lam16TeVDesRR"		#"CI #rightarrow #mu^{+}#mu^{-} #Lambda 16 TeV - Des RR"
		fillcolor = ROOT.kWhite
		fillstyle = 0
		linecolor = ROOT.kMagenta+1
		uncertainty = 0.0
		scaleFac     = 1.	
		additionalSelection = None

	class CITo2Mu_Lam22TeVConLL:
		subprocesses = ["CITo2Mu_22TeV_ConLL_M300","CITo2Mu_22TeV_ConLL_M800","CITo2Mu_22TeV_ConLL_M1300","CITo2Mu_22TeV_ConLL_M2000"]
		label = "CITo2Mu_Lam22TeVConLL"		#"CI #rightarrow #mu^{+}#mu^{-} #Lambda 22 TeV - Con LL"
		fillcolor = ROOT.kWhite
		fillstyle = 0
		linecolor = ROOT.kRed
		uncertainty = 0.0
		scaleFac     = 1.	
		additionalSelection = None
	class CITo2Mu_Lam22TeVConLR:
		subprocesses = ["CITo2Mu_22TeV_ConLR_M300","CITo2Mu_22TeV_ConLR_M800","CITo2Mu_22TeV_ConLR_M1300"]
		label = "CITo2Mu_Lam22TeVConLR"		#"CI #rightarrow #mu^{+}#mu^{-} #Lambda 22 TeV - Con LR"
		fillcolor = ROOT.kWhite
		fillstyle = 0
		linecolor = ROOT.kRed-4
		uncertainty = 0.0
		scaleFac     = 1.	
		additionalSelection = None
	class CITo2Mu_Lam22TeVConRR:
		subprocesses = ["CITo2Mu_22TeV_ConRR_M300","CITo2Mu_22TeV_ConRR_M800","CITo2Mu_22TeV_ConRR_M1300"]
		label = "CITo2Mu_Lam22TeVConRR"		#"CI #rightarrow #mu^{+}#mu^{-} #Lambda 22 TeV - Con RR"
		fillcolor = ROOT.kWhite
		fillstyle = 0
		linecolor = ROOT.kYellow
		uncertainty = 0.0
		scaleFac     = 1.	
		additionalSelection = None
	class CITo2Mu_Lam22TeVDesLL:
		subprocesses = ["CITo2Mu_22TeV_DesLL_M300","CITo2Mu_22TeV_DesLL_M800","CITo2Mu_22TeV_DesLL_M1300"]
		label = "CITo2Mu_Lam22TeVDesLL"		#"CI #rightarrow #mu^{+}#mu^{-} #Lambda 22 TeV - Des LL"
		fillcolor = ROOT.kWhite
		fillstyle = 0
		linecolor = ROOT.kBlue+1
		uncertainty = 0.0
		scaleFac     = 1.	
		additionalSelection = None
	class CITo2Mu_Lam22TeVDesLR:
		subprocesses = ["CITo2Mu_22TeV_DesLR_M300","CITo2Mu_22TeV_DesLR_M800","CITo2Mu_22TeV_DesLR_M1300"]
		label = "CITo2Mu_Lam22TeVDesLR"		#"CI #rightarrow #mu^{+}#mu^{-} #Lambda 22 TeV - Des LR"
		fillcolor = ROOT.kWhite
		fillstyle = 0
		linecolor = ROOT.kGreen+1
		uncertainty = 0.0
		scaleFac     = 1.	
		additionalSelection = None
	class CITo2Mu_Lam22TeVDesRR:
		subprocesses = ["CITo2Mu_22TeV_DesRR_M300","CITo2Mu_22TeV_DesRR_M800","CITo2Mu_22TeV_DesRR_M1300"]
		label = "CITo2Mu_Lam22TeVDesRR"		#"CI #rightarrow #mu^{+}#mu^{-} #Lambda 22 TeV - Des RR"
		fillcolor = ROOT.kWhite
		fillstyle = 0
		linecolor = ROOT.kMagenta+1
		uncertainty = 0.0
		scaleFac     = 1.	
		additionalSelection = None
		
	class CITo2Mu_Lam28TeVConLL:
		subprocesses = ["CITo2Mu_28TeV_ConLL_M300","CITo2Mu_28TeV_ConLL_M800","CITo2Mu_28TeV_ConLL_M1300","CITo2Mu_28TeV_ConLL_M2000"]
		label = "CITo2Mu_Lam28TeVConLL"		#"CI #rightarrow #mu^{+}#mu^{-} #Lambda 28 TeV - Con LL"
		fillcolor = ROOT.kWhite
		fillstyle = 0
		linecolor = ROOT.kRed
		uncertainty = 0.0
		scaleFac     = 1.	
		additionalSelection = None
	class CITo2Mu_Lam28TeVConLR:
		subprocesses = ["CITo2Mu_28TeV_ConLR_M300","CITo2Mu_28TeV_ConLR_M800","CITo2Mu_28TeV_ConLR_M1300"]
		label = "CITo2Mu_Lam28TeVConLR"		#"CI #rightarrow #mu^{+}#mu^{-} #Lambda 28 TeV - Con LR"
		fillcolor = ROOT.kWhite
		fillstyle = 0
		linecolor = ROOT.kRed-4
		uncertainty = 0.0
		scaleFac     = 1.	
		additionalSelection = None
	class CITo2Mu_Lam28TeVConRR:
		subprocesses = ["CITo2Mu_28TeV_ConRR_M300","CITo2Mu_28TeV_ConRR_M800","CITo2Mu_28TeV_ConRR_M1300"]
		label = "CITo2Mu_Lam28TeVConRR"		#"CI #rightarrow #mu^{+}#mu^{-} #Lambda 28 TeV - Con RR"
		fillcolor = ROOT.kWhite
		fillstyle = 0
		linecolor = ROOT.kYellow
		uncertainty = 0.0
		scaleFac     = 1.	
		additionalSelection = None
	class CITo2Mu_Lam28TeVDesLL:
		subprocesses = ["CITo2Mu_28TeV_DesLL_M300","CITo2Mu_28TeV_DesLL_M800","CITo2Mu_28TeV_DesLL_M1300"]
		label = "CITo2Mu_Lam28TeVDesLL"		#"CI #rightarrow #mu^{+}#mu^{-} #Lambda 28 TeV - Des LL"
		fillcolor = ROOT.kWhite
		fillstyle = 0
		linecolor = ROOT.kBlue+1
		uncertainty = 0.0
		scaleFac     = 1.	
		additionalSelection = None
	class CITo2Mu_Lam28TeVDesLR:
		subprocesses = ["CITo2Mu_28TeV_DesLR_M300","CITo2Mu_28TeV_DesLR_M800","CITo2Mu_28TeV_DesLR_M1300"]
		label = "CITo2Mu_Lam28TeVDesLR"		#"CI #rightarrow #mu^{+}#mu^{-} #Lambda 28 TeV - Des LR"
		fillcolor = ROOT.kWhite
		fillstyle = 0
		linecolor = ROOT.kGreen+1
		uncertainty = 0.0
		scaleFac     = 1.	
		additionalSelection = None
	class CITo2Mu_Lam28TeVDesRR:
		subprocesses = ["CITo2Mu_28TeV_DesRR_M300","CITo2Mu_28TeV_DesRR_M800","CITo2Mu_28TeV_DesRR_M1300"]
		label = "CITo2Mu_Lam28TeVDesRR"		#"CI #rightarrow #mu^{+}#mu^{-} #Lambda 22 TeV - Des RR"
		fillcolor = ROOT.kWhite
		fillstyle = 0
		linecolor = ROOT.kMagenta+1
		uncertainty = 0.0
		scaleFac     = 1.	
		additionalSelection = None
		
	class CITo2Mu_Lam34TeVConLL:
		subprocesses = ["CITo2Mu_34TeV_ConLL_M300","CITo2Mu_34TeV_ConLL_M800","CITo2Mu_34TeV_ConLL_M1300","CITo2Mu_34TeV_ConLL_M2000"]
		label = "CITo2Mu_Lam34TeVConLL"		#"CI #rightarrow #mu^{+}#mu^{-} #Lambda 34 TeV - Con LL"
		fillcolor = ROOT.kWhite
		fillstyle = 0
		linecolor = ROOT.kRed
		uncertainty = 0.0
		scaleFac     = 1.	
		additionalSelection = None
	class CITo2Mu_Lam34TeVConLR:
		subprocesses = ["CITo2Mu_34TeV_ConLR_M300","CITo2Mu_34TeV_ConLR_M800","CITo2Mu_34TeV_ConLR_M1300"]
		label = "CITo2Mu_Lam34TeVConLR"		#"CI #rightarrow #mu^{+}#mu^{-} #Lambda 34 TeV - Con LR"
		fillcolor = ROOT.kWhite
		fillstyle = 0
		linecolor = ROOT.kRed-4
		uncertainty = 0.0
		scaleFac     = 1.	
		additionalSelection = None
	class CITo2Mu_Lam34TeVConRR:
		subprocesses = ["CITo2Mu_34TeV_ConRR_M300","CITo2Mu_34TeV_ConRR_M800","CITo2Mu_34TeV_ConRR_M1300"]
		label = "CITo2Mu_Lam34TeVConRR"		#"CI #rightarrow #mu^{+}#mu^{-} #Lambda 34 TeV - Con RR"
		fillcolor = ROOT.kWhite
		fillstyle = 0
		linecolor = ROOT.kYellow
		uncertainty = 0.0
		scaleFac     = 1.	
		additionalSelection = None
	class CITo2Mu_Lam34TeVDesLL:
		subprocesses = ["CITo2Mu_34TeV_DesLL_M300","CITo2Mu_34TeV_DesLL_M800","CITo2Mu_34TeV_DesLL_M1300"]
		label = "CITo2Mu_Lam34TeVDesLL"		#"CI #rightarrow #mu^{+}#mu^{-} #Lambda 34 TeV - Des LL"
		fillcolor = ROOT.kWhite
		fillstyle = 0
		linecolor = ROOT.kBlue+1
		uncertainty = 0.0
		scaleFac     = 1.	
		additionalSelection = None
	class CITo2Mu_Lam34TeVDesLR:
		subprocesses = ["CITo2Mu_34TeV_DesLR_M300","CITo2Mu_34TeV_DesLR_M800","CITo2Mu_34TeV_DesLR_M1300"]
		label = "CITo2Mu_Lam34TeVDesLR"		#"CI #rightarrow #mu^{+}#mu^{-} #Lambda 34 TeV - Des LR"
		fillcolor = ROOT.kWhite
		fillstyle = 0
		linecolor = ROOT.kGreen+1
		uncertainty = 0.0
		scaleFac     = 1.	
		additionalSelection = None
	class CITo2Mu_Lam34TeVDesRR:
		subprocesses = ["CITo2Mu_34TeV_DesRR_M300","CITo2Mu_34TeV_DesRR_M800","CITo2Mu_34TeV_DesRR_M1300"]
		label = "CITo2Mu_Lam34TeVDesRR"		#"CI #rightarrow #mu^{+}#mu^{-} #Lambda 22 TeV - Des RR"
		fillcolor = ROOT.kWhite
		fillstyle = 0
		linecolor = ROOT.kMagenta+1
		uncertainty = 0.0
		scaleFac     = 1.	
		additionalSelection = None
				
		
	class CITo2Mu_Lam100kTeVConLL:
		subprocesses = ["CITo2Mu_100kTeV_ConLL_M300","CITo2Mu_100kTeV_ConLL_M800","CITo2Mu_100kTeV_ConLL_M1300","CITo2Mu_100kTeV_ConLL_M2000"]
		label = "CITo2Mu_Lam100kTeVConLL"		#"CI #rightarrow #mu^{+}#mu^{-} #Lambda 100k TeV - Con LL"
		fillcolor = ROOT.kWhite
		fillstyle = 0
		linecolor = ROOT.kBlack
		uncertainty = 0.0
		scaleFac     = 1.	
		additionalSelection = None
	class CITo2Mu_Lam100kTeVConLR:
		subprocesses = ["CITo2Mu_100kTeV_ConLR_M300","CITo2Mu_100kTeV_ConLR_M800","CITo2Mu_100kTeV_ConLR_M1300"]
		label = "CITo2Mu_Lam100kTeVConLR"		#"CI #rightarrow #mu^{+}#mu^{-} #Lambda 100k TeV - Con LR"
		fillcolor = ROOT.kWhite
		fillstyle = 0
		linecolor = ROOT.kRed-4
		uncertainty = 0.0
		scaleFac     = 1.	
		additionalSelection = None
	class CITo2Mu_Lam100kTeVConRR:
		subprocesses = ["CITo2Mu_100kTeV_ConRR_M300","CITo2Mu_100kTeV_ConRR_M800","CITo2Mu_100kTeV_ConRR_M1300"]
		label = "CITo2Mu_Lam100kTeVConRR"		#"CI #rightarrow #mu^{+}#mu^{-} #Lambda 100k TeV - Con RR"
		fillcolor = ROOT.kWhite
		fillstyle = 0
		linecolor = ROOT.kYellow
		uncertainty = 0.0
		scaleFac     = 1.	
		additionalSelection = None
	class CITo2Mu_Lam100kTeVDesLL:
		subprocesses = ["CITo2Mu_100kTeV_DesLL_M300","CITo2Mu_100kTeV_DesLL_M800","CITo2Mu_100kTeV_DesLL_M1300"]
		label = "CITo2Mu_Lam100kTeVDesLL"		#"CI #rightarrow #mu^{+}#mu^{-} #Lambda 100k TeV - Des LL"
		fillcolor = ROOT.kWhite
		fillstyle = 0
		linecolor = ROOT.kBlue+1
		uncertainty = 0.0
		scaleFac     = 1.	
		additionalSelection = None
	class CITo2Mu_Lam100kTeVDesLR:
		subprocesses = ["CITo2Mu_100kTeV_ConLR_M300","CITo2Mu_100kTeV_ConLR_M800","CITo2Mu_100kTeV_ConLR_M1300"]
		label = "CITo2Mu_Lam100kTeVDesLR"		#"CI #rightarrow #mu^{+}#mu^{-} #Lambda 100k TeV - Des LR"
		fillcolor = ROOT.kWhite
		fillstyle = 0
		linecolor = ROOT.kGreen+1
		uncertainty = 0.0
		scaleFac     = 1.	
		additionalSelection = None
	class CITo2Mu_Lam100kTeVDesRR:
		subprocesses = ["CITo2Mu_100kTeV_ConRR_M300","CITo2Mu_100kTeV_ConRR_M800","CITo2Mu_100kTeV_ConRR_M1300"]
		label = "CITo2Mu_Lam100kTeVDesRR"		#"CI #rightarrow #mu^{+}#mu^{-} #Lambda 22 TeV - Des RR"
		fillcolor = ROOT.kWhite
		fillstyle = 0
		linecolor = ROOT.kMagenta+1
		uncertainty = 0.0
		scaleFac     = 1.	
		additionalSelection = None
				
		
		
class Data:
		subprocesses = ["Data_RunB","Data_RunC","Data_RunD","Data_RunE","Data_RunF","Data_RunG","Data_RunH2","Data_RunH3"]
		label = "Data"
		fillcolor = ROOT.kBlack
		linecolor = ROOT.kBlack	
		uncertainty = 0.0
		scaleFac     = 1.	
		additionalSelection = None
class Backgrounds:
	
	class DrellYan:
		subprocesses = ["ZToMuMu_M50To120","ZToMuMu_M120To200","ZToMuMu_M200To400","ZToMuMu_M400To800","ZToMuMu_M800To1400","ZToMuMu_M1400To2300","ZToMuMu_M2300To3500","ZToMuMu_M3500To4500","ZToMuMu_M4500To6000"]
		label = "#gamma/Z #rightarrow #mu^{+}#mu^{-}"
		fillcolor = ROOT.kAzure+1
		linecolor = ROOT.kBlack	
		uncertainty = 0.04
		scaleFac     = 1.	
		additionalSelection = None
	class Top:
		subprocesses = ["ST_tW_antitop","ST_tW_top","TTTo2L2Nu","TTTo2L2Nu_M500To800","TTTo2L2Nu_M800To1200","TTTo2L2Nu_M1200To1800","TTTo2L2Nu_M1800ToInf"]
		label = "t#bar{t}, tW, #bar{t}W"
		fillcolor = ROOT.kRed-4
		linecolor = ROOT.kBlack	
		uncertainty = 0.04
		scaleFac     = 1.	
		additionalSelection = None
	class Diboson:
		subprocesses = ["ZZ","WZ","WWTo2L2Nu","WWTo2L2Nu_M600To1200","WWTo2L2Nu_M1200To2500","WWTo2L2Nu_M2500ToInf"]
		label = "WW, WZ, ZZ"
		fillcolor = ROOT.kGreen+3
		linecolor = ROOT.kBlack	
		uncertainty = 0.04
		scaleFac     = 1.	
		additionalSelection = None
	
	class Other:
		subprocesses = ["ST_tW_antitop","ST_tW_top","TTTo2L2Nu","TTTo2L2Nu_M500To800","TTTo2L2Nu_M800To1200","TTTo2L2Nu_M1200To1800","TTTo2L2Nu_M1800ToInf","ZZ","WZ","WWTo2L2Nu","WWTo2L2Nu_M600To1200","WWTo2L2Nu_M1200To2500","WWTo2L2Nu_M2500ToInf"]
		label = "Other"
		fillcolor = ROOT.kRed-4
		linecolor = ROOT.kBlack	
		uncertainty = 0.04
		scaleFac     = 1.	
		additionalSelection = None

	class Jets:
		subprocesses = ["JetsFromData"]
		label = "Jets"
		fillcolor = ROOT.kYellow
		linecolor = ROOT.kBlack	
		uncertainty = 0.04
		scaleFac     = 1.	
		additionalSelection = None



# Color definition
#==================
defineMyColors = {
        'Black' : (0, 0, 0),
        'White' : (255, 255, 255),
        'Red' : (255, 0, 0),
        'DarkRed' : (128, 0, 0),
        'Green' : (0, 255, 0),
        'Blue' : (0, 0, 255),
        'Yellow' : (255, 255, 0),
        'Orange' : (255, 128, 0),
        'DarkOrange' : (255, 64, 0),
        'Magenta' : (255, 0, 255),
        'KDEBlue' : (64, 137, 210),
        'Grey' : (128, 128, 128),
        'DarkGreen' : (0, 128, 0),
        'DarkSlateBlue' : (72, 61, 139),
        'Brown' : (70, 35, 10),

        'MyBlue' : (36, 72, 206),
        'MyDarkBlue' : (18, 36, 103),
        'MyGreen' : (70, 164, 60),
        'AnnBlueTitle' : (29, 47, 126),
        'AnnBlue' : (55, 100, 255),
#        'W11AnnBlue' : (0, 68, 204),
#        'W11AnnBlue' : (63, 122, 240),
    }


myColors = {
            'W11ttbar':  855,
            'W11singlet':  854,
            'W11ZLightJets':  401,
            'W11ZbJets':  400,
            'W11WJets':  842,
            'W11Diboson':  920,
            'W11AnnBlue': 856,
            'W11Rare':  630,
            }


def getPlot(name):
	from defs import plots
	if not name in dir(plots):
		print "unknown plot '%s, exiting'"%name
		sys.exit()
	else:
		return copy.copy(getattr(plots, name))
	
		
class Plot:
	
	histName = "none"
	plotName = "none"
	xaxis   = "none"
	yaxis	= "none"
	cut = ""
	variable = ""
	xMin = 0
	xMax = 0
	nBins = 0
	binning = []
	yMin 	= 0
	yMax	= 0 
	rebin = 1
	fileName = "none.pdf"
	log = False
	useJets = False
	
	def __init__(self,histName,plotName, yRange = None, xRange = None, nBins = 0, xLabel = "", yLabel = "",log=False,rebin = None, binning = [], useJets=False,plot2D=False):
		self.histName=histName
		self.xaxis=xLabel
		self.yaxis=yLabel
		self.nBins = nBins
		self.binning = binning
		self.xMin= None
		self.xMax= None
		self.yMin= None
		self.yMax= None
		self.plotName = plotName
		self.fileName= plotName
		self.useJets = useJets
		self.plot2D = plot2D
		if rebin != None:
			self.rebin = rebin
		if log:
			self.fileName+"_log" 
		self.log = log

		if yRange != None:
			self.yMin = yRange[0]
			self.yMax = yRange[1]
		if xRange != None:
			self.xMin = xRange[0]
			self.xMax = xRange[1]


class plots:
	
	massPlot = Plot("ZprimeRecomass","DimuonMass",xLabel="dimuon mass [GeV]",log=True,xRange=[120,3000],nBins = 100, rebin=20,yLabel="Events / 20 GeV",useJets=True)
	massPlotForLimit = Plot("CSMassBinned","DimuonMassSmeared",xLabel="dimuon mass [GeV]",log=True,xRange=[120,3000],nBins = 100, rebin=1,yLabel="Events / 20 GeV",useJets=True)
	massPlotWeighted = Plot("CSMassMuIDBinned","DimuonMassSmeared",xLabel="dimuon mass [GeV]",log=True,xRange=[120,3000],nBins = 100, rebin=1,yLabel="Events / 20 GeV",useJets=True)
	massPlotSmeared = Plot("CSSmearedMassBinned","DimuonMassSmeared",xLabel="dimuon mass [GeV]",log=True,xRange=[120,3000],nBins = 1, rebin=20,yLabel="Events / 20 GeV",useJets=True)
	massPlotUp = Plot("CSMassUpBinned","DimuonMassScaleUp",xLabel="dimuon mass [GeV]",log=True,xRange=[120,3000],nBins = 100, rebin=1,yLabel="Events / 20 GeV",useJets=True)
	massPlotDown = Plot("CSMassDownBinned","DimuonMassScaleDown",xLabel="dimuon mass [GeV]",log=True,xRange=[120,3000],nBins = 100, rebin=1,yLabel="Events / 20 GeV",useJets=True)
	massPlotPUUp = Plot("CSMassPUUpBinned","DimuonPUMassScaleUp",xLabel="dimuon mass [GeV]",log=True,xRange=[120,3000],nBins = 100, rebin=1,yLabel="Events / 20 GeV",useJets=True)
	massPlotPUDown = Plot("CSMassPUDownBinned","DimuonPUMassScaleDown",xLabel="dimuon mass [GeV]",log=True,xRange=[120,3000],nBins = 100, rebin=1,yLabel="Events / 20 GeV",useJets=True)
	
	etaPtMapGen = Plot("EtaPtMapGen","EtaPtMapGen",xLabel="lepton #eta",log=False,xRange=[-2.4,2.4],nBins = 100, rebin=1,yLabel="Events / 0.6 GeV",plot2D=True)
	etaPtMapReco = Plot("EtaPtMapReco","EtaPtMapReco",xLabel="lepton #eta",log=False,xRange=[-2.4,2.4],nBins = 100, rebin=1,yLabel="Events / 0.6 GeV",plot2D=True)
	
	csPlotM60To120 = Plot("CosAngleCollinSoperCorrect60Mass120","CosThetaStar_M60To120",xLabel="dimuon mass [GeV]",log=True,xRange=[-1,1],nBins = 100, rebin=1,yLabel="Events / 0.2")
	csPlotM120To300 = Plot("CosAngleCollinSoperCorrect120Mass300","CosThetaStar_M120To300",xLabel="dimuon mass [GeV]",log=True,xRange=[-1,1],nBins = 100, rebin=1,yLabel="Events / 0.2")
	csPlotM300To700 = Plot("CosAngleCollinSoperCorrect300Mass700","CosThetaStar_M300To700",xLabel="dimuon mass [GeV]",log=True,xRange=[-1,1],nBins = 100, rebin=1,yLabel="Events / 0.2")
	csPlotM700To3000 = Plot("CosAngleCollinSoperCorrect700Mass3000","CosThetaStar_M700To3000",xLabel="dimuon mass [GeV]",log=True,xRange=[-1,1],nBins = 100, rebin=1,yLabel="Events / 0.2")
	
	
	resPlot1 = Plot("MassResultionEBEB1","resPlot_M0To250",xLabel="(reco mass - gen mass)/gen mass",log=False,xRange=[0.5,0.5],nBins = 100, rebin=1,yLabel="Events / 0.01")
	resPlot2 = Plot("MassResultionEBEB2","resPlot_M250To750",xLabel="(reco mass - gen mass)/gen mass",log=False,xRange=[0.5,0.5],nBins = 100, rebin=1,yLabel="Events / 0.01")
	resPlot3 = Plot("MassResultionEBEB3","resPlot_M750To1250",xLabel="(reco mass - gen mass)/gen mass",log=False,xRange=[0.5,0.5],nBins = 100, rebin=1,yLabel="Events / 0.01")
	resPlot4 = Plot("MassResultionEBEB4","resPlot_M1250To1750",xLabel="(reco mass - gen mass)/gen mass",log=False,xRange=[0.5,0.5],nBins = 100, rebin=1,yLabel="Events / 0.01")
	resPlot5 = Plot("MassResultionEBEB5","resPlot_M1750To2250",xLabel="(reco mass - gen mass)/gen mass",log=False,xRange=[0.5,0.5],nBins = 100, rebin=1,yLabel="Events / 0.01")
	resPlot6 = Plot("MassResultionEBEB6","resPlot_M2000To4000",xLabel="(reco mass - gen mass)/gen mass",log=False,xRange=[0.5,0.5],nBins = 100, rebin=1,yLabel="Events / 0.01")
	resPlot7 = Plot("MassResultionEBEB7","resPlot_M4000To6000",xLabel="(reco mass - gen mass)/gen mass",log=False,xRange=[0.5,0.5],nBins = 100, rebin=1,yLabel="Events / 0.01")


