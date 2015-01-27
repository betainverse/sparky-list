#!/usr/bin/env python
"""
changenumberssparkypeaklist.py reads a sparky peaklist and 
adds a specified value to the peak numbers, in order to number
a C-terminal domain peaks according to the numbering for the
full-length protein or for the domain only.
"""

import argparse,re
from os.path import exists
from sys import stdout

def main():
    # Parse inputs, complain about some problems.
    parser = argparse.ArgumentParser(
        description="Convert Sparky peak lists into csv files, and remove unusable lines.",
        epilog = "")
    parser.add_argument("-a", "--add",dest="addend",type=int,
                        nargs='?',default=None,metavar="resnum",
                        help='Number to add to residue numbers. Required.')
    parser.add_argument("-i", "--input", dest="infile",
                      help="Name of the input sparky.list file", metavar="inputfile")
    parser.add_argument("-o", "--output", action="store",dest="outfile",default=None,
                      help="Optional name of the output file. By default, any .list will be removed from the input file name and .csv will be added. Already existing files will be overwritten.",
                        metavar="outputfile")

    args = parser.parse_args()
    infile = args.infile
    outfile = args.outfile
    addend = args.addend

    if outfile and exists(outfile):
        parser.error("%s exists. Please specify a unique output file name."%outfile)
    if not infile:
        parser.error("Please indicate an input file")
    elif not outfile:
        outfile = stdout

    openfile = open(infile,'r')
    filelines = openfile.readlines()
    openfile.close()

    headerline = filelines[0]
    headerline = headerline.replace('Data Height','Data-Height')
    headerline = headerline.replace('w1 (Hz)','w1(Hz)')
    headerline = headerline.replace('w2 (Hz)','w2(Hz)')
    headerline = headerline.replace('w1 (hz)','w1(Hz)')
    headerline = headerline.replace('w2 (hz)','w2(Hz)')
    headers = ['AA','ResNum','Atoms'] + headerline.split()[1:]

    newlines = []
    newlines.append(','.join(headers))
    excluded = []
    unkept = []

    for line in filelines[1:]:
        splitline = line.split()
        if len(splitline) > 0:
            if '?' in splitline[0]:
                splitline = [' ',' '] + splitline
            else:
                assignment = re.sub(r"([A-Z])([0-9]+)([A-Z])","\\1 \\2 \\3",splitline[0])
                splitline = assignment.split() + splitline[1:]
            Res = splitline[1]
            Atoms = splitline[2]
            newRes = str(int(Res)+addend)
            newlines.append(splitline[0]+newRes+Atoms+'\t'+'\t'.join(splitline[3:]))
    if outfile == stdout:
        openfile = outfile
    else:
        openfile = open(outfile,'w')
    for line in newlines:
        openfile.write(line+'\n')
    openfile.write('\n')
    for line in unkept:
        openfile.write(line+'\n')
    openfile.write('\n')
    for line in excluded:
        openfile.write(line+'\n')
    openfile.close()

        
    

# Execute everything
main()   
