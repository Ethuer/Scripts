import csv
from Bio import SeqIO
import re as re

#gff features
#1.  Feature name (mandatory); this is the primary systematic name, if available
#2.  Gene name (locus name)
#3.  Feature type
#4.  Chromosome
#5.  Start Coordinate
#6.  Stop Coordinate
#7.  Strand 

overhead = 1000

def seq_extract(row, seqment):
    if int(row[5]) < int(row[6]):
        start = int(row[5])
        stop = int(row[6])
    elif int(row[5]) > int(row[6]):
        start = int(row[6])
        stop = int(row[5])
    # boundaries
    start = start - overhead
    stop = stop + overhead
    subset = seqment[start:stop]
    print 'subset = %i ' %(len(subset))
    print 'seqment = %i ' %(len(seqment))


    

def extractor(inseq,ref):
    for row in inseq:
        if row[3]:
            seqment = ref[row[4]]
            print type(seqment)
##            print row[6]
            sequence = seq_extract(row,seqment)


with open('C_parapsilosis_CDC317_current_chromosomes.fasta','r') as ref_raw, open('C_parapsilosis_CDC317_current_chromosomal_feature.tab','r') as gtf_raw:
    ref = SeqIO.to_dict(SeqIO.parse(ref_raw,'fasta'))
    gtf = csv.reader(gtf_raw,delimiter='\t')

    next(gtf,None)
    next(gtf,None)
    next(gtf,None)
    next(gtf,None)
    next(gtf,None)
    next(gtf,None)
    next(gtf,None)
    next(gtf,None)
    
    extractor(gtf,ref)
        
    
