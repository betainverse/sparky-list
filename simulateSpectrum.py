#!/usr/bin/env python
"""
Read in a sparky peaklist file, and output a scatterplot showing
peak positions, with the area of each marker proportional to the
height of the peak.
"""
import sys
import pylab
from math import sqrt

def main():
    if len(sys.argv) != 3:
        print "Usage:"
        print "simulateSpectrum.py spectrum.list chart.pdf"
        return

    infile = sys.argv[1]
    outfile = sys.argv[2]
    openfile = open(infile,'r')
    listDict = {}
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
                listDict[res]=(Nppm,Hppm,height)
            else:
                listDict[res]=(Nppm,Hppm)
    openfile.close()
    residues = [int(key) for key in listDict.keys()]
    residues.sort()
    resnames = [str(res) for res in residues]
    Nlist = [listDict[str(res)][0] for res in residues]
    Hlist = [listDict[str(res)][1] for res in residues]
    sizes = [listDict[str(res)][2] for res in residues]
    maxsize = max(sizes)
    scaledsizes = [100*x/maxsize for x in sizes]
    pylab.figure()
    pylab.scatter(Hlist,Nlist,marker='o',s=scaledsizes)
    pylab.xlabel("$\omega$ H (ppm)")
    pylab.ylabel("$\omega$ N (ppm)")
    axes = pylab.gca()
    axes.invert_xaxis()
    axes.invert_yaxis()
    for label, x, y in zip(resnames, Hlist, Nlist):
        pylab.annotate(
            label, 
            xy = (x, y), xytext = (-2, 3),
            textcoords = 'offset points', ha = 'right', va = 'bottom',
            size=5,
            arrowprops = dict(arrowstyle = '->', connectionstyle = 'arc3,rad=0'))

    pylab.savefig(outfile)
    

main()
