#!/usr/bin/python

"""
read an xpk peaklist from nmrview, output a sparky peaklist

xpk2sparky.py input.xpk > output.list
"""
from sys import argv

infile = argv[1]
openfile = open(infile,'r')
filelines = openfile.readlines()
openfile.close()


for line in filelines:
    columns = line.split()
    if len(columns) == 20:
        Hlabel = columns[1]
        Nlabel = columns[8]
        Hshift = columns[2]
        Nshift = columns[9]
        lenH = len(Hlabel)
        if lenH > 4 and '?' not in Hlabel:
            residue = Hlabel[1:lenH-1].split('.')[0]
            print residue+'N-H\t'+Nshift+'\t'+Hshift

