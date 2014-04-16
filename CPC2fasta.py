import csv
from Bio import SeqIO
import sys,argparse
import os.path

#################################################################################################
# This script parses the .tab result from CPC creating a fasta file of noncoding transcripts    #
#                       (c) Ernst Thuer 2014                                                    #
#################################################################################################

# arguments for commandline input and help
####################################################
parser = argparse.ArgumentParser(description='parse result from CPC creating a fasta file of noncoding transcripts')
parser.add_argument('-in',
                    dest='filename',
                    required = True,
                    help='Input a CPC output (.tab) file  of type  sequence  lenght  non/coding   probability file containing RNASeq data',
                    metavar = 'FILE',
                    #type=lambda x: is_valid_file(parser,x)
                    )

parser.add_argument('-fasta',
                    dest='fasta',
                    required = True,
                    help='Input the reference fasta file, used by CPC',
                    metavar = 'FILE',
                    #type=lambda x: is_valid_file(parser,x)
                    )

parser.add_argument('-out',
                    dest='output',
                    required = False,
                    default='CPC.fasta',
                    help='Output a fasta file containing non-coding transcripts and their fasta sequence as predicted by cpc',
                    metavar = 'FILE',
                    #type=argparse.FileType('w')
                    )

parser.add_argument('-cutoff',
                    dest='cutoff',
                    required = False,
                    default='0',
                    help='value 0 to -1.4, it Defines cutoff probability for coding potential the lower the more strict is the prediction',
                    metavar = 'float',
                    #type=argparse.FileType('w')
                    )

args = parser.parse_args()

#####################################################


counter = 0


with open ((args.filename),'r') as in_file_raw, open((args.fasta)) as fasta, open((args.output),'w') as output_handle :
    in_file = csv.DictReader(in_file_raw, fieldnames = ("name","length","coding","probability"), delimiter='\t')
    record_dict = SeqIO.index((args.fasta), "fasta")
    for row in in_file :
        if row['length'] >= 200 and float(row['probability']) < float(args.cutoff) and row['name'] in record_dict:
            counter += 1
            SeqIO.write(record_dict[row['name']],output_handle,"fasta")
            
print  '%i transcripts written to file' %(counter)
