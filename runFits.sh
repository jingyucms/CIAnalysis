python makeFit.py 
python makeFit.py -unc scaleup
python makeFit.py -unc scaledown
python makeFit.py -unc muonid
python makeFit.py -unc smeared
python makeFit.py -unc pileup 
python makeFit.py -unc piledown
python makeGraph.py --fixinf --fixdes --constraint '0 0 1e4' --constraint '1 0 1e9' --constraint '2 0 1e9'
python makeGraph.py --fixinf --fixdes --constraint '0 0 1e4' --constraint '1 0 1e9' --constraint '2 0 1e9' -unc scaleup 
python makeGraph.py --fixinf --fixdes --constraint '0 0 1e4' --constraint '1 0 1e9' --constraint '2 0 1e9' -unc scaledown
python makeGraph.py --fixinf --fixdes --constraint '0 0 1e4' --constraint '1 0 1e9' --constraint '2 0 1e9' -unc muonid
python makeGraph.py --fixinf --fixdes --constraint '0 0 1e4' --constraint '1 0 1e9' --constraint '2 0 1e9' -unc smeared
python makeGraph.py --fixinf --fixdes --constraint '0 0 1e4' --constraint '1 0 1e9' --constraint '2 0 1e9' -unc pileup
python makeGraph.py --fixinf --fixdes --constraint '0 0 1e4' --constraint '1 0 1e9' --constraint '2 0 1e9' -unc piledown
python makeFit.py -cs cspos
python makeFit.py -unc scaleup -cs cspos
python makeFit.py -unc scaledown -cs cspos
python makeFit.py -unc muonid -cs cspos
python makeFit.py -unc smeared -cs cspos
python makeFit.py -unc pileup -cs cspos
python makeFit.py -unc piledown -cs cspos
python makeGraph.py --fixinf --fixdes --constraint '0 0 1e4' --constraint '1 0 1e9' --constraint '2 0 1e9' -cs cspos
python makeGraph.py --fixinf --fixdes --constraint '0 0 1e4' --constraint '1 0 1e9' --constraint '2 0 1e9' -unc scaleup  -cs cspos
python makeGraph.py --fixinf --fixdes --constraint '0 0 1e4' --constraint '1 0 1e9' --constraint '2 0 1e9' -unc scaledown -cs cspos
python makeGraph.py --fixinf --fixdes --constraint '0 0 1e4' --constraint '1 0 1e9' --constraint '2 0 1e9' -unc muonid -cs cspos
python makeGraph.py --fixinf --fixdes --constraint '0 0 1e4' --constraint '1 0 1e9' --constraint '2 0 1e9' -unc smeared -cs cspos
python makeGraph.py --fixinf --fixdes --constraint '0 0 1e4' --constraint '1 0 1e9' --constraint '2 0 1e9' -unc pileup -cs cspos
python makeGraph.py --fixinf --fixdes --constraint '0 0 1e4' --constraint '1 0 1e9' --constraint '2 0 1e9' -unc piledown -cs cspos
python makeFit.py -cs csneg
python makeFit.py -unc scaleup -cs csneg
python makeFit.py -unc scaledown -cs csneg
python makeFit.py -unc muonid -cs csneg
python makeFit.py -unc smeared -cs csneg
python makeFit.py -unc pileup -cs csneg
python makeFit.py -unc piledown -cs csneg
python makeGraph.py --fixinf --fixdes --constraint '0 0 1e4' --constraint '1 0 1e9' --constraint '2 0 1e9' -cs csneg
python makeGraph.py --fixinf --fixdes --constraint '0 0 1e4' --constraint '1 0 1e9' --constraint '2 0 1e9' -unc scaleup  -cs csneg
python makeGraph.py --fixinf --fixdes --constraint '0 0 1e4' --constraint '1 0 1e9' --constraint '2 0 1e9' -unc scaledown -cs csneg
python makeGraph.py --fixinf --fixdes --constraint '0 0 1e4' --constraint '1 0 1e9' --constraint '2 0 1e9' -unc muonid -cs csneg
python makeGraph.py --fixinf --fixdes --constraint '0 0 1e4' --constraint '1 0 1e9' --constraint '2 0 1e9' -unc smeared -cs csneg
python makeGraph.py --fixinf --fixdes --constraint '0 0 1e4' --constraint '1 0 1e9' --constraint '2 0 1e9' -unc pileup -cs csneg
python makeGraph.py --fixinf --fixdes --constraint '0 0 1e4' --constraint '1 0 1e9' --constraint '2 0 1e9' -unc piledown -cs csneg
