import csv
from Bio import SeqIO
from Bio.SeqRecord import SeqRecord
import sys,argparse
import os.path


# This script cuts fasta sequences into smaller subsequences,  infile can be single or multifasta,  outfile is multifasta.



parser = argparse.ArgumentParser(description=' This script cuts fasta sequences into smaller subsequences,  infile can be single or multifasta,  outfile is multifasta.')
parser.add_argument('-in',
                    dest='input',
                    required = True,
                    help='Input a (multi) fasta file',
                    metavar = 'FILE',
                    #type=lambda x: is_valid_file(parser,x)
                    )

parser.add_argument('-out',
                    dest='out',
                    required = False,
                    default='Output.fasta',
                    help='output file is multifasta, sequences of desired length',
                    metavar = 'FILE',
                    #type=lambda x: is_valid_file(parser,x)
                    )

parser.add_argument('-len',
                    dest='len',
                    required = False,
                    default='100',
                    help='Desired sequence length, default 100',
                    metavar = 'INT',
                    #type=lambda x: is_valid_file(parser,x)
                    )

args = parser.parse_args()


with open('%s'%(args.input),'r') as in_raw, open('%s'%(args.out),'w') as out_raw:
##    infile = csv.reader(in_raw, delimiter = '\t')
    record_dict = SeqIO.to_dict(SeqIO.parse(in_raw, "fasta"))

    count = 0
    count2 = 0

    short_sequences = []
    
    out_dict = {}
    for element,value in record_dict.items():
        count2 +=1
        for fraq in range(0,len(value.seq),int(args.len)):
##            print value.seq[(seq):(seq+100)]
            count +=1
            name = '%s_%s' %(element,fraq)
            value_out = value
            value_out.fraq = value.seq[fraq:fraq+int(args.len)]
##            print value_out.fraq
            value_out.id = name

            record=SeqRecord(value_out.fraq,value_out.id,'','')
            short_sequences.append(record)
##            out_dict[name] = value
    print '%s fragments created from %s original sequences' %(count, count2)

    SeqIO.write(short_sequences, out_raw, "fasta")
