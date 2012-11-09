#!/usr/bin/python
"""
splitpeaklists.py takes a sparky .list file and splits it into two files:
one file contains the peaks that are separated from others by a certain threshold
the other file contains the peaks that are clustered together
This script is specific to H-N HSQCs. Later versions may be more general.
"""

# Can get away with a tight threshold for situations like PREs,
# where the peaks shouldn't move much
#Hthresh=0.04 #ppm threshold for peaks being too close in H
#Nthresh=0.3

# Should use a looser threshold when peaks might shift a lot, 
# as when measuring chemical shift changes in a titration
Hthresh=0.08
Nthresh=0.4

from sys import argv

openfile = open(argv[1],'r')
lines = openfile.readlines()
openfile.close()

residues = []

for line in lines[2:]: #skip header, blank line
    columns = line.split()
    residue = (columns[0],columns[1],columns[2])
    residues.append(residue)

def tooclose(Nthresh,Hthresh,res1,res2):
    Ndist=abs(float(res1[1])-float(res2[1]))
    Hdist=abs(float(res1[2])-float(res2[2]))
    if Ndist<Nthresh and Hdist<Hthresh:
        #print res1[0], res2[0], Ndist, Hdist
        return True
    else:
        return False

closeList = []
farList = []

for i in range(len(residues)):
    thisRes = residues[i]
    closeness = False
    if i==0:
        otherRes = residues[1:]
    elif i==len(residues)-1:
        otherRes = residues[0:len(residues)-2]
    else:
        otherRes = residues[:i]+residues[i+1:]
    for res in otherRes:
        if tooclose(Nthresh,Hthresh,thisRes,res):
            closeness = True
    if closeness:
        closeList.append(thisRes)
    else:
        farList.append(thisRes)

closefilename = "close_"+argv[1]
farfilename = "far_"+argv[1]

openfile = open(closefilename,'w')
openfile.write(lines[0])
for residue in closeList:
    openfile.write(' '.join(residue)+'\n')
openfile.close()

openfile = open(farfilename,'w')
openfile.write(lines[0])
for residue in farList:
    openfile.write(' '.join(residue)+'\n')
openfile.close()
