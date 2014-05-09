# -*- coding: utf-8 -*-
import csv
from Bio import SeqIO
import sys,argparse
import os.path

#################################################################################################################################
#    This script takes an CPC output and the multi fasta file used for prediction to create a gtf file                          #
#                                                                                                                               #
#desired output format                                                                                                          #
#name    pipeline    exon    start    end    lenght    .    +-    .    gene_id “ID”;transcript_id ”ID”; gene_name”name”         #
#                                                                                                                               #
#                                                       (c) Ernst Thuer 2014                                                    #
#################################################################################################################################

counter = 0
start=0
end=0

# arguments for commandline input and help
####################################################
parser = argparse.ArgumentParser(description='This script takes an CPC output and the multi fasta file used for prediction to create a gtf file')
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
                    default='CPC.gtf',
                    help='Output a gtf file containing non-coding transcripts and their fasta sequence as predicted by cpc',
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

parser.add_argument('-name',
                    dest='chromosome',
                    required = False,
                    default='chromosome',
                    help='give an arbitrary name to the first column, default chromosome',
                    metavar = 'string',
                    #type=argparse.FileType('w')
                    )

args = parser.parse_args()

#####################################################

with open ((args.filename),'r') as in_file_raw, open((args.fasta)) as fasta, open((args.output),'w') as output_handle :
    in_file = csv.DictReader(in_file_raw, fieldnames = ("name","length","coding","probability"), delimiter='\t')
    output = csv.writer(output_handle, delimiter = '\t')
    record_dict = SeqIO.index((args.fasta), "fasta")
    for row in in_file :
        if row['length'] >= 200 and float(row['probability']) < 0 and row['name'] in record_dict:
            name =record_dict[row['name']].id
            length = len(record_dict[row['name']].seq)
            end = end+len(record_dict[row['name']].seq)
            counter += 1
            start = end
            name_parsed =  ' %s ' %(name)
            output.writerow(["%s" %(args.chromosome),"Pipeline","transcript",start,end,length,'.','+','.',"gene_id “%s”" %name,"gene_name “%s”" % (name_parsed)])
            
print counter

