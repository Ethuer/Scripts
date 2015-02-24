import csv
from Bio import SeqIO
import random
import sys,argparse
import os.path

# this file takes a fasta sequence and creates RNA-seq style reads from it with a given coverage.
# used to test heterozygosity

# creates fastq files  high quality reads  PHRED 34

## @SEQ_ID
## GATTTGGGGTTCAAAGCAGTATCGATCAAATAGTAAATCCATTTGTTCAACTCACAGTTT
## +
## !~}~}~}~}~}~}~}~}~}~}~}~}~}~}~}~}~}~}~}~}~}~}~}~}~


parser = argparse.ArgumentParser(description=' This script takes a fasta file and creates 50 bp fastq reads of fixed quality. It was developed to complement the heterozygosity benchmark')
parser.add_argument('-in',
                    dest='input',
                    required = True,
                    help='Input a fasta file containing a 2500 bp sequence to be mutated',
                    metavar = 'FILE',
                    #type=lambda x: is_valid_file(parser,x)
                    )

parser.add_argument('-out',
                    dest='out',
                    required = False,
                    default='Output.fasta',
                    help='output file fasta sequence, changed bases to random. leave the .fasta suffix',
                    metavar = 'FILE',
                    #type=lambda x: is_valid_file(parser,x)
                    )

parser.add_argument('-reads',
                    dest='read',
                    required = False,
                    default='4200',
                    help='AMount of reads to be generated,  default 4200',
                    metavar = 'FILE',
                    #type=lambda x: is_valid_file(parser,x)
                    )

args = parser.parse_args()


with open("%s" %(args.input),'r') as infile, open("%s.fastq" %(args.out),"w") as outfile:
    record = SeqIO.read(infile,"fasta")
##    print record.seq
    out = csv.writer(outfile, delimiter = '\n')
    reads = int(args.read)

    count = 0
    
    while count < reads:
        string = str(record.seq)
        a = random.randint(0, (len(record.seq)-50))
        count += 1
        out.writerow(['@SEQ%s%s' %(count,args.input),string[a:(a+50)],'+','9?????????????????????????????????????????????????'])
##        print '@SEQ%s' %(count)
##        print string[a:(a+50)]
##        print '+'
##        print '!~}~}~}~}~}~}~}~}~}~}~}~}~}~}~}~}~}~}~}~}~}~}~}~}~'

