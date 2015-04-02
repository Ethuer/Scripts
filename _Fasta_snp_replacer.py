import csv
import re
from Bio import SeqIO
import Bio
from Bio.Seq import Seq
from Bio.SeqRecord import SeqRecord
import sys,argparse
import os.path
from Bio.Alphabet import generic_dna


def letter_replace(position,string):
    position = int(position)

    out_string = string[:position] + 'N' + string[(position+1):]
    return out_string


# function to replace the SNP positions with the alternative Nucleotide
def snpreplace(ident,sequence, snpdict):
    counter = 0
    anticounter = 0
    for element, values in snpdict.items():
        if element[0] == ident:
            if sequence[int(element[1])-2] == values[0][1]:
                hit = int(element[1])
##                ref = sequence
                # Seq to string
                sequence = str(sequence)  
                print values[0][1],values[1][1]
                # Python has static strings, so this nonsense is neccessary,  is that how you write neccessary ?
                sequence_snp = sequence[:((hit)-2)]+  values[1][1]  + sequence[((hit)-1):]
                # String to Seq
                sequence_snp = Seq(sequence_snp,generic_dna)

                # pass it to the loop
                sequence = sequence_snp

                counter +=1

##    print counter
    return sequence_snp





with open('Het_genes_significantly_changed.txt','r') as in_raw,open('genesnps.snp','r') as snp_raw, open('C_orthopsilosis_Co_90-125_features.sort.gtf', 'r') as ref_raw,open('C_orthopsilosis_Co_90-125_chromosomes.fasta','r') as fasta_raw, open('Het_genes_significant_parental_B.fasta','w') as out_raw:

    # Catch the open handles
    infile = csv.reader(in_raw, delimiter = ' ')
    reffile = csv.reader(ref_raw, delimiter = '\t')
    record_dict = SeqIO.to_dict(SeqIO.parse(fasta_raw, "fasta"))
    snpfile = csv.reader(snp_raw, delimiter = '\t')
    snpfile.next()

    # Create neccessary dictionaries

    genedict = {}
    sequences = []
    snpdict = {}

    # populate dictionaries
    for row in infile:
        genedict[row[0]] = 1


    #  pass a regex comprehension,   ADAPT THIS STATEMENT
    genes = re.compile('CORT_\d\D\d{5}')


    # populate dictionaries
    for row in reffile:
        try:
            gene = re.search(genes,row[8])
            if 'gene' in row[2]:
                if gene.group(0) in genedict:
                    genedict[gene.group(0)] = [row[0],row[3],row[4],row[6]]
        except:
            pass


    # populate dictionaries
    for row in snpfile:
        snpdict[row[0],row[5]] = [row[6],row[7]]


##    print len(snpdict)
######    
    out_dict = {}
    for elementn, valuesn in genedict.items():
        # extract dictionary
        gene = elementn
        chrom = valuesn[0]
        start = int(valuesn[1])
        stop = int(valuesn[2])
        orientation = valuesn[3]
        
        for element,values in record_dict.items():
            
            if element == valuesn[0]:
                
                sequence_raw = (values.seq[start:stop])

                # Push to function

                sequence = snpreplace(elementn,sequence_raw, snpdict)



                # change the orientation of the fasta sequence according to gtf annotation,   for the reading frame
                if orientation == '-':
                    print 'reversing sequence'
                    seq_oriented = sequence[::-1]
                    record=SeqRecord(seq_oriented,elementn,'','')
                    sequences.append(record)

                elif orientation == '+':
                    seq_oriented = sequence
                    record=SeqRecord(seq_oriented,elementn,'','')
                    sequences.append(record)

                else:
                    print ' SEQUENCE WITHOUT ORIENTATION %s' %(elementn)
                     
    # write to file     
    SeqIO.write(sequences, out_raw, "fasta")
