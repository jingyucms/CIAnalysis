python makeFit.py -do2018
python makeFit.py -unc scaleup -do2018
python makeFit.py -unc scaledown -do2018
python makeFit.py -unc muonid -do2018
python makeFit.py -unc smeared -do2018
python makeFit.py -unc pileup -do2018
python makeFit.py -unc piledown -do2018
python makeGraph.py --fixinf --fixdes --constraint '0 0 1e4' --constraint '1 0 1e9' --constraint '2 0 1e9' -do2018
python makeGraph.py --fixinf --fixdes --constraint '0 0 1e4' --constraint '1 0 1e9' --constraint '2 0 1e9' -unc scaleup  -do2018
python makeGraph.py --fixinf --fixdes --constraint '0 0 1e4' --constraint '1 0 1e9' --constraint '2 0 1e9' -unc scaledown -do2018
python makeGraph.py --fixinf --fixdes --constraint '0 0 1e4' --constraint '1 0 1e9' --constraint '2 0 1e9' -unc muonid -do2018
python makeGraph.py --fixinf --fixdes --constraint '0 0 1e4' --constraint '1 0 1e9' --constraint '2 0 1e9' -unc smeared -do2018
python makeGraph.py --fixinf --fixdes --constraint '0 0 1e4' --constraint '1 0 1e9' --constraint '2 0 1e9' -unc pileup -do2018
python makeGraph.py --fixinf --fixdes --constraint '0 0 1e4' --constraint '1 0 1e9' --constraint '2 0 1e9' -unc piledown -do2018
python makeFit.py -cs cspos -do2018
python makeFit.py -unc scaleup -cs cspos -do2018
python makeFit.py -unc scaledown -cs cspos -do2018
python makeFit.py -unc muonid -cs cspos -do2018
python makeFit.py -unc smeared -cs cspos -do2018
python makeFit.py -unc pileup -cs cspos -do2018
python makeFit.py -unc piledown -cs cspos -do2018
python makeGraph.py --fixinf --fixdes --constraint '0 0 1e4' --constraint '1 0 1e9' --constraint '2 0 1e9' -cs cspos -do2018
python makeGraph.py --fixinf --fixdes --constraint '0 0 1e4' --constraint '1 0 1e9' --constraint '2 0 1e9' -unc scaleup  -cs cspos -do2018
python makeGraph.py --fixinf --fixdes --constraint '0 0 1e4' --constraint '1 0 1e9' --constraint '2 0 1e9' -unc scaledown -cs cspos -do2018
python makeGraph.py --fixinf --fixdes --constraint '0 0 1e4' --constraint '1 0 1e9' --constraint '2 0 1e9' -unc muonid -cs cspos -do2018
python makeGraph.py --fixinf --fixdes --constraint '0 0 1e4' --constraint '1 0 1e9' --constraint '2 0 1e9' -unc smeared -cs cspos -do2018
python makeGraph.py --fixinf --fixdes --constraint '0 0 1e4' --constraint '1 0 1e9' --constraint '2 0 1e9' -unc pileup -cs cspos -do2018
python makeGraph.py --fixinf --fixdes --constraint '0 0 1e4' --constraint '1 0 1e9' --constraint '2 0 1e9' -unc piledown -cs cspos -do2018
python makeFit.py -cs csneg -do2018
python makeFit.py -unc scaleup -cs csneg -do2018
python makeFit.py -unc scaledown -cs csneg -do2018
python makeFit.py -unc muonid -cs csneg -do2018
python makeFit.py -unc smeared -cs csneg -do2018
python makeFit.py -unc pileup -cs csneg -do2018
python makeFit.py -unc piledown -cs csneg -do2018
python makeGraph.py --fixinf --fixdes --constraint '0 0 1e4' --constraint '1 0 1e9' --constraint '2 0 1e9' -cs csneg -do2018
python makeGraph.py --fixinf --fixdes --constraint '0 0 1e4' --constraint '1 0 1e9' --constraint '2 0 1e9' -unc scaleup  -cs csneg -do2018
python makeGraph.py --fixinf --fixdes --constraint '0 0 1e4' --constraint '1 0 1e9' --constraint '2 0 1e9' -unc scaledown -cs csneg -do2018
python makeGraph.py --fixinf --fixdes --constraint '0 0 1e4' --constraint '1 0 1e9' --constraint '2 0 1e9' -unc muonid -cs csneg -do2018
python makeGraph.py --fixinf --fixdes --constraint '0 0 1e4' --constraint '1 0 1e9' --constraint '2 0 1e9' -unc smeared -cs csneg -do2018
python makeGraph.py --fixinf --fixdes --constraint '0 0 1e4' --constraint '1 0 1e9' --constraint '2 0 1e9' -unc pileup -cs csneg -do2018
python makeGraph.py --fixinf --fixdes --constraint '0 0 1e4' --constraint '1 0 1e9' --constraint '2 0 1e9' -unc piledown -cs csneg -do2018
