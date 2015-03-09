from Bio import SeqIO
import sys
from Bio.Blast.Applications import NcbiblastnCommandline
##import subprocess
from Bio.Blast import NCBIXML
##import os
from StringIO import StringIO
import csv
import sys,argparse
import os.path

#################################################################################################################
# this script runs a blast of single fasta sequences in a multifasta against a reference multifasta database    #
# create database via makeblastdb.                                                                              #
# output consists of description and score                                                                      #
#                                                                                                               #
##for f in ../Predicted_fasta/*.fa; do                                                                          #
##	#echo $f                                                                                                #
##	s=${f#"../Predicted_fasta/"}                                                                            #
##	s=${s%".fa"}                                                                                            #
##	echo $s                                                                                                 #
##makeblastdb -in $f -dbtype nucl -input_type fasta -out blastdb/$s                                             #
##done                                                                                                          #
#################################### (c) Ernst Thuer 2014 #######################################################

# arguments for commandline input and help
####################################################
parser = argparse.ArgumentParser(description='This script takes a multifasta file, and queries against a blastdb, returning hits and score')
parser.add_argument('-fasta',
                    dest='fasta',
                    required = True,
                    help='Input a multi fasta file containing the sequence queries',
                    metavar = 'FILE',
                    #type=lambda x: is_valid_file(parser,x)
                    )

parser.add_argument('-db',
                    dest='db',
                    required = True,
                    help='name and location of the makeblastdb formated database',
                    metavar = 'FILE',
                    #type=lambda x: is_valid_file(parser,x)
                    )

parser.add_argument('-out',
                    dest='output',
                    required = False,
                    default='output.fasta',
                    help='Output a file containing the blast hits',
                    metavar = 'FILE',
                    #type=argparse.FileType('w')
                    )

parser.add_argument('-cutoff',
                    dest='cutoff',
                    required = False,
                    default='500',
                    help='cutoff score to be considered relevant, defaults to 500',
                    metavar = 'integer',
                    #type=argparse.FileType('w')
                    )


args = parser.parse_args()

##
##(args.orfs)
##(args.intergen)


def blastrun(infile):
    counter = 0
    collectdict = {}
    for f in infile:
        query = '%s' %(f.seq)  
        blastn_cline = NcbiblastnCommandline(db='%s' %(args.db), outfmt=5) #Blast command to commandline
        stdout, stderr = blastn_cline(stdin=query)  # execute, direct to stdout stderr
        blast_record = NCBIXML.read(StringIO(stdout))  # pipe to xmlparser,  use StringIO for conversion of str to xml
        for desc in blast_record.descriptions:
            if int(desc.score) > int(args.cutoff):
                counter +=1
##                print ' aligment %s has a score of %i  '  %(desc.title, desc.score)
                collectdict[f.id] = desc.score
    print ' %i blast hits encountered..' %(counter)  
    return collectdict


with open('%s' %(args.fasta),'r') as first_raw, open('%s' %(args.output), 'w') as out_raw:
    first = SeqIO.parse(first_raw,'fasta')
    out = csv.writer(out_raw,delimiter='\t')
   # print 'Processing ... '
   # print 'Commencing blastn ...'

    results = blastrun(first)

    for row, value in results.items():
        out.writerow( [row,value])
    
