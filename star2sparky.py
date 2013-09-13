#!/usr/bin/python

"""
read an nmrstar 2.1 file and produce a sparky HSQC peaklist

star2sparky.py input.star > output.list
"""
from sys import argv

def isfloat(numstring):
    if '.' in numstring and numstring.replace('.','',1).isdigit():
        return True
    else:
        return False

AA = {}
AA["ALA"] = "A"
AA["ARG"] = "R"
AA["ASN"] = "N"
AA["ASP"] = "D"
AA["CYS"] = "C"
AA["GLN"] = "Q"
AA["GLU"] = "E"
AA["GLY"] = "G"
AA["HIS"] = "H"
AA["ILE"] = "I"
AA["LEU"] = "L"
AA["LYS"] = "K"
AA["MET"] = "M"
AA["PHE"] = "F"
AA["PRO"] = "P"
AA["SER"] = "S"
AA["THR"] = "T"
AA["TRP"] = "W"
AA["TYR"] = "Y"
AA["VAL"] = "V"

infile = argv[1]
openfile = open(infile,'r')
filelines = openfile.readlines()
openfile.close()

Nshifts = {}
Hshifts = {}
residues = {}

for line in filelines:
    columns = line.split()
    if len(columns) == 9:
        atno = columns[0]
        resno = columns[1]
        resname = columns[3]
        atname = columns[4]
        shift = columns[6]
        if atno.isdigit() and resno.isdigit() and isfloat(shift) and resname in AA.keys():
            if atname == "H" or atname == "N":
                if resno not in residues.keys():
                    residues[resno]=AA[resname]
                if atname == "N":
                    Nshifts[resno]=shift
                elif atname == "H":
                    Hshifts[resno]=shift

for res in residues.keys():
    if res in Nshifts.keys() and res in Hshifts.keys():
        print residues[res]+res+'N-H '+Nshifts[res]+' '+Hshifts[res]
