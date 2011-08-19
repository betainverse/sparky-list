#!/nmr/programs/python/bin/python2.7
"""
list2excel.py reads a sparky peaklist and reformats it from
a whitespace-delimted file to a CSV file. It also splits the
assignment column into 3 columns: amino acid letter, residue
number, and atoms.

list2excel.py also reads a list of residues to exclude and
a list of atoms to keep, and prints all lines corresponding
to excluded residues or unkept atoms at the bottom of the file.

For example,

list2excel.py -i HSQC.list -x 1252 1281 -k N-H

outputs HSQC.csv, with lines corresponding to residues 1252
and 1281 moved to the bottom, along with any sidechain peaks
"""

import argparse,re
from os.path import exists
from sys import stdout

def main():
    # Parse inputs, complain about some problems.
    parser = argparse.ArgumentParser(
        description="Convert Sparky peak lists into csv files, and remove unusable lines.",
        epilog = "")
    parser.add_argument("-x", "--exclude",dest="exclude",type=int,
                        nargs='*',default=None,metavar="resnum",
                        help='Residue numbers to exclude. Optional.')
    parser.add_argument("-k", "--keep",metavar="atomname",dest="keep",
                        type=str, nargs='?',default=None,
                        help='Max increment for each of the indirect dimensions, in the same order as the columns in the sampling schedule. Required.')
    parser.add_argument("-i", "--input", dest="infile",
                      help="Name of the input sparky.list file", metavar="inputfile")
    parser.add_argument("-o", "--output", action="store",dest="outfile",default=None,
                      help="Optional name of the output file. By default, any .list will be removed from the input file name and .csv will be added. Already existing files will be overwritten.",
                        metavar="outputfile")

    args = parser.parse_args()
    infile = args.infile
    outfile = args.outfile
    if args.exclude:
        exclude = [str(x) for x in args.exclude]
    keep = args.keep

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

            if keep and Atoms != keep:
                unkept.append(','.join(splitline))
            elif exclude and Res in exclude:
                excluded.append(','.join(splitline))
            else:
                newlines.append(','.join(splitline))
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
