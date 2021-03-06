#!/usr/bin/env python
"""
Read in two sparky peaklist files, and output a bar graph showing
normalized peak movement distance.
Optionally, show change in peak height.
"""
import sys
import pylab
from math import sqrt

def main():
    if len(sys.argv) != 4:
        print "Usage:"
        print "sparkygraph.py spectrum1.list spectrum2.list chart.pdf"
        return

    infile1 = sys.argv[1]
    infile2 = sys.argv[2]
    outfile = sys.argv[3]
    openfile = open(infile1,'r')
    list1Dict = {}
    heights = True
    for line in openfile.readlines():
        if 'N-H' in line:
            columns = line.split()
            res = columns[0][1:-3]
            Nppm = float(columns[1])
            Hppm = float(columns[2])
            try:
                height = float(columns[3])
            except IndexError, e:
                heights = False
            if height:
                list1Dict[res]=(Nppm,Hppm,height)
            else:
                list1Dict[res]=(Nppm,Hppm)
    openfile.close()
    openfile = open(infile2,'r')
    list2Dict = {}
    for line in openfile.readlines():
        if 'N-H' in line:
            columns = line.split()
            res = columns[0][1:-3]
            Nppm = float(columns[1])
            Hppm = float(columns[2])
            try:
                height = float(columns[3])
            except IndexError, e:
                heights = False
            if height:
                list2Dict[res]=(Nppm,Hppm,height)
            else:
                list2Dict[res]=(Nppm,Hppm)
    openfile.close()
    if heights:
        heightratios = {}
    distances = {}
    if len(list1Dict.keys()) != len(list2Dict.keys()):
        print "Error: residues in list1 and list2 differ in length."
    for key in list1Dict.keys():
        res1 = list1Dict[key]
        try:
            res2 = list2Dict[key]
        except KeyError, e:
            print e
            return
        if heights:
            heightratios[key]=res2[2]/res1[2]
        distances[key]=sqrt(0.2*(res1[0]-res2[0])**2+(res1[1]-res2[1])**2)
#    for key in distances.keys():
#        print key, distances[key], heightratios[key]
    xlist = [int(key) for key in distances.keys()]
    xlist.sort()
    ylist = [distances[str(x)] for x in xlist]
    pylab.figure(figsize=(10,3))
    pylab.bar(xlist,ylist)
    pylab.axis(xmin=min(xlist),xmax=max(xlist))
    pylab.xlabel("Residue")
    pylab.ylabel("$\Delta\delta$(ppm)")
    gcf().subplots_adjust(bottom=0.15)
    pylab.savefig(outfile)
    

main()
