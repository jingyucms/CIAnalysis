import argparse
import subprocess
import time
import os
import sys
##Data card for Zprime -> ll analysis, created on %(date)s at %(time)s using revision %(hash)s of the package

simpleTemplate='''
# Simple counting experiment, with one signal and one background process 
imax 1  number of channels
jmax 1  number of backgrounds
kmax 2  number of nuisance parameters (sources of systematical uncertainties)
------------
# we have just one channel, in which we observe 0 events
bin 1
observation %(data)s
------------
# now we list the expected events for signal and all backgrounds in that bin
# the second 'process' line must have a positive number for backgrounds, and 0 for signal
# then we list the independent sources of uncertainties, and give their effect (syst. error)
# on each process and bin
bin          1            1   
process     signal   background
process      0	          1 
rate       %(nSig)s    %(nBkg)s
------------
lumi lnN       1.04     1.04    
bgkg lnN         -    %(uncert)s  
'''



def writeCard(card,fileName):

	text_file = open("%s.txt" % (fileName), "w")
	text_file.write(card)
	text_file.close()
	

def main():

	nSig = 10
	nBkg = 100
	
	bkgUncert = 1. +  nBkg**0.5/nBkg
	data = nSig + nBkg

	inputs = {"data":data,"nBkg":nBkg,"uncert":bkgUncert,"nSig":nSig}


	dataCard = simpleTemplate%inputs

	writeCard(dataCard,"testCard")	

main()
