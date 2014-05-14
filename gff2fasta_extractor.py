import csv
from Bio import SeqIO
import re as re
import sys,argparse
import os.path
#########################################################################################################
# this script takes a gff and a fasta file to create the fasta sequences of genes / annotated sequences #
# an overhead ( upstream, downstream ) is also retained, the output is directed to a new fasta file     #
#                                                                                                       #
#gff features                                                                                           #
#1.  Feature name (mandatory); this is the primary systematic name, if available                        #
#2.  Gene name (locus name)                                                                             #
#3.  Feature type                                                                                       #
#4.  Chromosome                                                                                         #
#5.  Start Coordinate                                                                                   #
#6.  Stop Coordinate                                                                                    #
#7.  Strand                                                                                             #
################################################(c) Ernst Thuer 2014#####################################

# arguments for commandline input and help
####################################################
parser = argparse.ArgumentParser(description='This script takes two files, a gff and one fasta format. It returns a multiple fasta conaining the annotated sequences')
parser.add_argument('-gff',
                    dest='gff',
                    required = True,
                    help='Input a gff file containing the annotations (strand 5,6 should be positions)',
                    metavar = 'FILE',
                    #type=lambda x: is_valid_file(parser,x)
                    )

parser.add_argument('-fasta',
                    dest='fasta',
                    required = True,
                    help='input a fasta file',
                    metavar = 'FILE',
                    #type=lambda x: is_valid_file(parser,x)
                    )

parser.add_argument('-out',
                    dest='output',
                    required = False,
                    default='output.fasta',
                    help='Output a fasta file containing the annotated fasta sequences including the threshold',
                    metavar = 'FILE',
                    #type=argparse.FileType('w')
                    )

parser.add_argument('-overhead',
                    dest='overhead',
                    required = False,
                    default='1000',
                    help='overhead of upstream and downstream bp beyond open reading frame will be cut off. Default 1000',
                    metavar = 'integer',
                    #type=argparse.FileType('w')
                    )


args = parser.parse_args()



overhead = (args.overhead)

def seq_extract(row, seqment):
    
    if int(row[5]) < int(row[6]):
        start = int(row[5])
        stop = int(row[6])
    elif int(row[5]) > int(row[6]):
        start = int(row[6])
        stop = int(row[5])

    start = start - int(overhead)
    stop = stop + int(overhead)
    subset = seqment[start:stop]

    return subset

def extractor(inseq,ref):
    collectdict={}
    for row in inseq:
        if row[3]:
            seqment = ref[row[4]]
            collectdict[row[0]] = seq_extract(row,seqment)
    return collectdict

with open('%s' %(args.output),'w') as out_raw, open('%s'%(args.fasta),'r') as ref_raw, open('%s'%(args.gff),'r') as gtf_raw:
    ref = SeqIO.to_dict(SeqIO.parse(ref_raw,'fasta'))
    gtf = csv.reader(gtf_raw,delimiter='\t')

    # header size, will implement better solution when I have the time
    next(gtf,None)
    next(gtf,None)
    next(gtf,None)
    next(gtf,None)
    next(gtf,None)
    next(gtf,None)
    next(gtf,None)
    next(gtf,None)
    
    collection = extractor(gtf,ref)
    for row,seq in collection.items():
        seq.id = row
        SeqIO.write(seq, out_raw, "fasta")
    
    
