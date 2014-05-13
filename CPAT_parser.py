from Bio import SeqIO
import sys
import csv
import sys,argparse
import os.path

#####################################################################################################################################
# This script takes a multifasta file CPC output , compares it with CPAT and writes the files below threshold to a new fasta file   #
# CPAT recommends 0.3-0.4 cutoff,  0.3 should be best                                                                               #
#####################################################################################################################################

# arguments for commandline input and help
####################################################
parser = argparse.ArgumentParser(description='This script takes a multifasta file CPC output , compares it with CPAT and writes the files below threshold to a new fasta file')
parser.add_argument('-fasta',
                    dest='fasta',
                    required = True,
                    help='Input a multi fasta file containing the sequence queries',
                    metavar = 'FILE',
                    #type=lambda x: is_valid_file(parser,x)
                    )

parser.add_argument('-cpat',
                    dest='cpat',
                    required = True,
                    help='Input a CPAt prediction file',
                    metavar = 'FILE',
                    #type=lambda x: is_valid_file(parser,x)
                    )

parser.add_argument('-out',
                    dest='output',
                    required = False,
                    default='output.fasta',
                    help='Output a file containing the remaining sequences',
                    metavar = 'FILE',
                    #type=argparse.FileType('w')
                    )

parser.add_argument('-cutoff',
                    dest='cutoff',
                    required = False,
                    default='0.3',
                    help='cutoff score to be considered noncoding, defaults to 0.3, less is more strict',
                    metavar = 'float',
                    #type=argparse.FileType('w')
                    )


args = parser.parse_args()

##
##(args.orfs)
##(args.intergen)


with open('%s' %(args.fasta),'r') as fasta_raw, open('%s' %(args.cpat),'r') as cpat_raw, open('%s' %(args.output),'w') as out_raw :
    cpat = csv.reader(cpat_raw, delimiter = '\t')
    fasta = SeqIO.parse(fasta_raw,'fasta')
    
    count = 0
    counter = 0
    cpat = list(cpat)
    for sequence in fasta:
        for row in cpat:
            if row[0] == sequence.id:
                count +=1
                if float(row[5]) < float(args.cutoff):
                    counter +=1
                    SeqIO.write(sequence,out_raw,'fasta')
    print ' %i  sequences in CPC  %i sequences confirmed by CPAT' %(count, counter) 
    
