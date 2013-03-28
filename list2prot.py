#!/usr/bin/python
"""
list2prot.py reads a new, unassigned sparky peaklist and 
generates a CARA prot file. Atom names for the columns in
the peaklist must be given in order as command-line
arguments: 

list2prot.py input.list CA N H
"""

from sys import argv

atomnumber = 1
systemnumber = 1

def parseline(line,columnnames):
    shifts = line.split()[1:]
    return zip(shifts,columnnames)

def printSystem(line,columnnames):
    global atomnumber,systemnumber
    for atom in parseline(line,columnnames):
        printstring = ('%d'%atomnumber).rjust(4)
        printstring += atom[0].rjust(8)
        printstring += ' 0.000 '
        printstring += atom[1].ljust(4)
        printstring += (' %d'%systemnumber).rjust(5)
        print printstring
        atomnumber += 1
    systemnumber += 1

def getlines(filename):
    openfile = open(filename,'r')
    filelines = openfile.readlines()
    openfile.close()
    return filelines

def main():
    infile = argv[1]
    atomnames = argv[2:]
    for line in getlines(infile)[2:]:
        printSystem(line,atomnames)


# Execute everything
main()   
