import csv
import random
from Bio import SeqIO
import operator
import sys,argparse
import os.path


parser = argparse.ArgumentParser(description=' This script takes a fasta file, with one singel sequence of 2500 bp and creates hybrid sequence of the middle 1500 bp. THe amount of divergence depends on the input value')
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

parser.add_argument('-het',
                    dest='het',
                    required = False,
                    default='1',
                    help='Percent difference of original and heterozygous region',
                    metavar = 'FILE',
                    #type=lambda x: is_valid_file(parser,x)
                    )

args = parser.parse_args()


handle = open("%s" %(args.input),'r')
counter = 0

record = SeqIO.read(handle, "fasta")

# give it the random letters
fasta = 'TGAC'

# take the sequence apart,  into upstream / downstream, which stay unchanged
# and the core string, which is permutated
upstream = str(record.seq[0:500])
string = str(record.seq[500:2000])
downstream = str(record.seq[2000:2500])

# the minus 5 is a correction factor, against letters being replaced by themselves
heterozygosity = (100 / float(args.het)) - (15 - (1.7* float(args.het)))
##print heterozygosity

# replace random letters,  until the percentage points of heterozygosity match the het input
checksum = 0
while (checksum - (100 - float(args.het)))*(checksum - (100 - float(args.het))) > 0.005  :
    x = ''.join(i if random.randint(0, int(heterozygosity)) else random.choice(fasta) for i in string)
    checksum = (float(map(operator.eq, x, string).count(True))/1500)*100
##    print ' %s  checksum' %(checksum)

    
##record.seq = ''.join(i if random.randint(0, 100) else random.choice(fasta) for i in string)

print '%s percent identity' %((float(map(operator.eq, x, string).count(True))/1500)*100)

with open("%s.fasta" %(args.out),'w') as outfile:
    fastawriter = csv.writer(outfile, delimiter='\n')
    fastawriter.writerow(['>%s'%(args.out),upstream,x,downstream])
