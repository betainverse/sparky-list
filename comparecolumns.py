#!/nmr/programs/python/bin/python2.7
"""
comparecolumns.py reads two sparky peaklists, extracts the requested
columns from each, and aligns them according to residue number and atom.
Missing values are replaced by 0 or another user-specified symbol. 
"""

import argparse,re
from os.path import exists
from sys import stdout

def fixheadercolumns(headerline):
    headerline = headerline.replace('Data Height','Data-Height')
    headerline = headerline.replace('w1 (Hz)','w1(Hz)')
    headerline = headerline.replace('w2 (Hz)','w2(Hz)')
    headerline = headerline.replace('w1 (hz)','w1(Hz)')
    headerline = headerline.replace('w2 (hz)','w2(Hz)')
    return headerline

def main():
    # Parse inputs, complain about some problems.
    parser = argparse.ArgumentParser(
##         description="Convert Sparky peak lists into csv files, and remove unusable lines.",
             epilog = "")
##     parser.add_argument("-x", "--exclude",dest="exclude",type=int,
##                         nargs='*',default=None,metavar="resnum",
##                         help='Residue numbers to exclude. Optional.')
##     parser.add_argument("-k", "--keep",metavar="atomname",dest="keep",
##                         type=str, nargs='?',default=None,
##                         help='Atom description to keep, typically N-H.')
    parser.add_argument("-i", "--input", dest="infiles",
                      help="Name of the input sparky.list file", metavar="inputfile", nargs=2)
    parser.add_argument("-o", "--output", action="store",dest="outfile",default=None,
                      help="Optional name of the output file. By default, any .list will be removed from the input file name and .csv will be added. Already existing files will be overwritten.",
                        metavar="outputfile")
    parser.add_argument("-m","--missing",action="store",dest="missing",default=None,
                        help='Character or symbol to indicate a missing value, defaults to 0.')
    parser.add_argument("-c","--columns",dest="columns",
                        help="Desired column number to extract from each input file, in order. Start counting from 0.",
                        metavar="column",nargs=2,type=int)
    args = parser.parse_args()
    infiles = args.infiles
    outfile = args.outfile
    missing = args.missing
    columns = args.columns
    if not missing:
        missing = '0'
##     if args.exclude:
##         exclude = [str(x) for x in args.exclude]
##     keep = args.keep

    if outfile and exists(outfile):
        parser.error("%s exists. Please specify a unique output file name."%outfile)
    if not infiles:
        parser.error("Please indicate an input file.")
    if not columns:
        parser.error("Please indicate which columns to extract from each file.")
    elif not outfile:
        outfile = stdout
    
##     for infile in infiles:
##         print infile

##     for col in columns:
##         print col

    openfile = open(infiles[0],'r')
    firstlines = openfile.readlines()
    openfile.close()

    datadict = {}
    unassigned = []
    
    firstcol = columns[0]
    for line in firstlines[2:]:
        firstcolumns=line.split()
        assignment = firstcolumns[0]
        data = firstcolumns[firstcol]
        if '?' in assignment:
            unassigned.append([assignment,data,missing])
        elif datadict.has_key(assignment):
            if datadict[assignment][0] == missing:
                datadict[assignment][0] = data
            else:
                unassigned.append([assignment,data,missing])
        else:
            datadict[assignment] = [data,missing]

    openfile = open(infiles[1],'r')
    secondlines = openfile.readlines()
    openfile.close()

    secondcol = columns[1]
    for line in secondlines[2:]:
        secondcolumns = line.split()
        assignment = secondcolumns[0]
        data = secondcolumns[secondcol]
        if '?' in assignment:
            unassigned.append([assignment,missing,data])
        elif datadict.has_key(assignment):
            if datadict[assignment][1] == missing:
                datadict[assignment][1] = data
            else:
                unassigned.append([assignment,missing,data])
        else:
            datadict[assignment] = [missing,data]
        
        

    firstheaders = fixheadercolumns(firstlines[0]).split()
    secondheaders = fixheadercolumns(secondlines[0]).split()

    if outfile == stdout:
        openfile = outfile
    else:
        openfile = open(outfile,'w')

##     openfile.write('\t'.join([missing,infiles[0],infiles[1]])+'\n')
##     openfile.write('\t'.join([firstheaders[0],firstheaders[firstcol],secondheaders[secondcol]])+'\n')
    openfile.write('%s\t%s-%s\t%s-%s\n'%(firstheaders[0],infiles[0],firstheaders[firstcol],infiles[1],secondheaders[secondcol]))
    for key in datadict:
        openfile.write('\t'.join([key,datadict[key][0],datadict[key][1]])+'\n')
#        print key,datadict[key][0],datadict[key][1]
#    print "Unassigned or duplicate peaks:"
    for item in unassigned:
        openfile.write('\t'.join([item[0],item[1],item[2]])+'\n')
#        print item[0],item[1],item[2]

# Execute everything
main()   
    
