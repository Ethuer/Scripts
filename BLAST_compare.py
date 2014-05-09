from Bio.Blast.Applications import NcbiblastnCommandline
from Bio.Blast import NCBIXML
import csv
from Bio import SeqIO
import re as re
import sys,argparse
import os.path

#########################################################################################################################
# This script takes a fasta file as input , performas blastn against a local database, and returns all the fasta files  #
# That have NO hit in the database.  Use this to get rid of falsely classified intergenic regions.                      #
#                                                                                                                       #
#####################################(c) Ernst Thuer ####################################################################

# run blast by commandline

# makeblastdb -in C_parapsilosis_CDC317_current_chromosomes.fasta -input_type fasta -dbtype nucl -out C_par_orf




# arguments for commandline input and help
####################################################
parser = argparse.ArgumentParser(description='This script takes two files, a gff and one fasta format. It returns a multiple fasta conaining the annotated sequences')
parser.add_argument('-xml',
                    dest='xml',
                    required = False,
                    default = 'intermediate.xml'
                    help='Input a name for an intermediate xml file containing blastresults ',
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

parser.add_argument('-re',
                    dest='regex',
                    required = False,
                    default='CPAR2_\d{6}',
                    help='overhead of upstream and downstream bp beyond open reading frame will be cut off. Default 1000',
                    metavar = 'string',
                    #type=argparse.FileType('w')
                    )

parser.add_argument('-db',
                    dest='database',
                    required = False,
                    default='C_par_orf',
                    help='input a mekeblastdb derived database  e.g makeblastdb -in C_parapsilosis_CDC317_current_chromosomes.fasta -input_type fasta -dbtype nucl -out C_par_orf',
                    metavar = 'FILE',
                    #type=lambda x: is_valid_file(parser,x)
                    )


args = parser.parse_args()

######################################################


cline = NcbiblastnCommandline(query='%s' %(args.fasta), evalue=0.001, strand="plus", db="%s" %(args.database),   out="%s" %(args.xml), outfmt=5) #strand="plus", evalue=0.001,



def getmatch(blast_records):
    collectdict = {}
    counter = 0
    for blast_record in blast_records:
        for alignment in blast_record.alignments:
            for hsp in alignment.hsps:
                gene = re.compile('%s') %(args.regex)  # 'CPAR2_\d{6}' change the regex for other organisms
                try:
                    match = gene.search(alignment.title)
                    collectdict[match.group(0)] = match.group(0)
                    counter += 1
                except:
                    print 'no match in description %s' %(alignment.title)
##                re.match alignment.title()
##                print 'found alignment in %s with a score : %s , e value of %s and %s identities' %(alignment.title,hsp.score,hsp.expect,hsp.identities)
                
    return collectdict
    print counter          

def kickout(fasta,matches):
    count_all=0
    count_match = 0
    count_mismatch = 0
    collection={}
    
    for row, value in fasta.items():
        count_all += 1

        if row not in matches:
            count_mismatch +=1
            collection[row] = value
        if row in matches:
            count_match += 1
            
    print 'total count %i, not found by blast %i , found by blast %i ' %(count_all,count_mismatch,count_match)
    return collection

            

    
with open('%s' %(args.fasta),'r') as in_raw, open('%s' %(args.xml), 'r') as intermediate_raw , open('%s'%(args.output),'w') as out_raw:
    infile = SeqIO.to_dict(SeqIO.parse(in_raw,'fasta'))
    blast_records = NCBIXML.parse(intermediate_raw)

    blast_match = getmatch(blast_records)

    result_list = kickout(infile,blast_match)

    for ident,seq in result_list.items():
##        seq.id = row
        SeqIO.write(seq, out_raw, "fasta")
    
