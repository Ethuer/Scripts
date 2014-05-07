import csv
from Bio import SeqIO
import re as re
from Bio.Blast.Applications import NcbiblastxCommandline

#####################################################################################
# this script will extract inergenic regions from two multifasta files,             #
# one containing orfs one containing orfs and intergenic regions                    #
# a cutoff or 1000bp upstream and downstream is recommended, and removed as well    #
# the remaining fragments will be blasted against the orf database,                 #
# to see if they do not match                                                       #
# output is for teaching purpouse in CPAT                                           #
#                                                                                   #
###############(c) Ernst Thuer 2014 #################################################

# arguments for commandline input and help
####################################################
parser = argparse.ArgumentParser(description='This script takes two files in fasta format, one containint orfs only another orfs +intergenic, it returns intergenic regions')
parser.add_argument('-orfs',
                    dest='orfs',
                    required = True,
                    help='Input a fasta file containing the orfs only',
                    metavar = 'FILE',
                    #type=lambda x: is_valid_file(parser,x)
                    )

parser.add_argument('-inter',
                    dest='intergen',
                    required = True,
                    help='input a fasta file containing the orfs and intergenic regions',
                    metavar = 'FILE',
                    #type=lambda x: is_valid_file(parser,x)
                    )

parser.add_argument('-out',
                    dest='output',
                    required = False,
                    default='output.fasta',
                    help='Output a fasta file containing the intergenic regions beyond the threshold',
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


#####################################################

def match_string(large,small,ident):
    """ REGEX via python re. looking for bp upstream downstream"""
    count_string = 0
    collectstring = {}
    string = ('\w{1,%i}%s\w{1,%i}') % (args.overhead, small, args.overhead)
    reg  = re.compile(string)
    large = str(large)
    reg_string = reg.sub('',large)
    return reg_string


def compare(infile,compare):
    """ compares two files according to their row[0] field"""
    counter = 0
    collect_seq={}
    for row,seq in infile.items():
        for rown,seqn in compare.items():
            if row == rown:
                lenght=(len(seqn.seq)-len(seq.seq))
                if lenght > 2000:
                    string = match_string(seqn.seq,seq.seq,row)
                    if len(string) < len(seqn.seq):
                        collect_seq[row] = string
                    
                    counter +=1
    print counter
    return collect_seq


with open('%s','r')%(args.orfs) as handle_orf, open('%s','r') % (args.intergen) as handle_inter, open('%s','w') % (args.output) as out_raw :

    orf = SeqIO.to_dict(SeqIO.parse(handle_orf,'fasta'))
    inter = SeqIO.to_dict(SeqIO.parse(handle_inter,'fasta'))
    out = csv.writer(out_raw,delimiter='\n')
    collection = compare(orf,inter)
    print len(collection)
    count = 0
    for key in collection:
        if len(collection[key]) > 100:
            out.writerow(['> surrounding region of gene %s after 1000bp overhead' %(key),collection[key]])
            count += len(collection[key])
    print 'average length = %i' %(count/len(collection))

